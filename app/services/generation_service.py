# app/services/generation_service.py
import uuid
import structlog
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from app.db.models import Generation, User, Workspace, UsageEvent, Subscription
from app.services.ai_generator import AIGenerator
from app.services.pdf_generator import PDFGenerator
from app.core.errors import QuotaExceededError, AIGenerationError
from app.core.config import get_settings

logger = structlog.get_logger(__name__)

class GenerationServiceResult(BaseModel):
    success: bool
    generation_id: Optional[str] = None
    output_text: Optional[str] = None
    pdf_url: Optional[str] = None
    error_message: Optional[str] = None
    estimated_reach: int = 1500
    tags: List[str] = []
    cta: List[str] = []

class GenerationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_generator = AIGenerator()
        self.pdf_generator = PDFGenerator()
        self.settings = get_settings()

    async def generate_smm_package(
        self,
        user_id: str,
        workspace_id: str,
        niche: str,
        platform: str,
        goal: str,
        format_type: str,
        brief: str,
        language: str = "ru",
        country: str = "uz"
    ) -> GenerationServiceResult:
        """Основной метод генерации SMM-пакета с проверкой квот"""

        try:
            # Преобразуем UUID строки в uuid.UUID объекты для строгого соответствия asyncpg
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            workspace_uuid = uuid.UUID(workspace_id) if isinstance(workspace_id, str) else workspace_id

            # 1. Проверка квот
            has_quota = await self._check_and_reserve_quota(workspace_uuid)
            if not has_quota:
                raise QuotaExceededError("Вы исчерпали месячный лимит генераций")

            # 2. Создание записи генерации в БД
            generation = Generation(
                id=uuid.uuid4(),
                workspace_id=workspace_uuid,
                user_id=user_uuid,
                content_type="smm_package",
                language=language,
                country=country,
                brief=brief,
                niche=niche,
                platform=platform,
                goal=goal,
                format_type=format_type,
                status="pending"
            )
            self.db.add(generation)
            await self.db.flush()

            logger.info("generation_created", generation_id=str(generation.id))

            # 3. AI генерация
            ai_result = await self.ai_generator.generate_smm_package(
                niche=niche,
                platform=platform,
                goal=goal,
                format_type=format_type,
                brief=brief,
                language=language,
                country=country
            )

            if not ai_result.success:
                generation.status = "failed"
                generation.error_message = ai_result.error_message
                await self.db.commit()

                # Откат резервирования квоты
                await self._reverse_quota_reservation(generation.id)

                raise AIGenerationError(ai_result.error_message)

            # 4. Обновление генерации
            generation.output_text = ai_result.output_text
            generation.status = "completed"
            generation.estimated_reach = ai_result.estimated_reach
            generation.tags = ai_result.tags
            generation.cta_suggestions = ai_result.cta
            generation.completed_at = datetime.utcnow()

            # 5. Генерация PDF
            try:
                user_stmt = select(User).where(User.id == user_uuid)
                user_result = await self.db.execute(user_stmt)
                user = user_result.scalar_one_or_none()

                pdf_filename = f"content.pdf"
                pdf_dir = f"generated/{generation.id}"
                pdf_path = f"{pdf_dir}/{pdf_filename}"

                await self.pdf_generator.generate_branded_pdf(
                    output_path=pdf_path,
                    user_name=user.username if (user and user.username) else "Пользователь",
                    content_type=format_type,
                    content_text=ai_result.output_text
                )

                generation.pdf_url = f"/api/generations/{generation.id}/pdf"
                logger.info("pdf_generated", generation_id=str(generation.id), path=pdf_path)

            except Exception as e:
                logger.exception("pdf_generation_failed", error=str(e))
                generation.pdf_url = None

            await self.db.commit()

            logger.info(
                "generation_completed",
                generation_id=str(generation.id),
                tokens_estimated=len(ai_result.output_text) // 4
            )

            return GenerationServiceResult(
                success=True,
                generation_id=str(generation.id),
                output_text=ai_result.output_text,
                pdf_url=generation.pdf_url,
                estimated_reach=ai_result.estimated_reach,
                tags=ai_result.tags,
                cta=ai_result.cta
            )

        except Exception as e:
            logger.exception("generation_service_error", error=str(e))
            await self.db.rollback()
            return GenerationServiceResult(
                success=False,
                error_message=str(e)
            )

    async def _check_and_reserve_quota(self, workspace_uuid: uuid.UUID) -> bool:
        """Проверка и резервирование квоты на генерацию"""

        sub_stmt = (
            select(Subscription)
            .where(Subscription.workspace_id == workspace_uuid)
            .where(Subscription.status == "active")
        )
        sub_result = await self.db.execute(sub_stmt)
        subscription = sub_result.scalar_one_or_none()

        if not subscription:
            return False

        # Определение лимита
        limit_map = {
            "free": self.settings.free_plan_generations_per_month,
            "starter": 50,
            "pro": 200,
            "team": 1000,
            "enterprise": 999999
        }

        monthly_limit = limit_map.get(subscription.plan_code, 5)

        # Подсчет использованных генераций за месяц
        month_ago = datetime.utcnow() - timedelta(days=30)

        used_stmt = (
            select(func.count(Generation.id))
            .where(Generation.workspace_id == workspace_uuid)
            .where(Generation.created_at >= month_ago)
            .where(Generation.status == "completed")
        )
        used_result = await self.db.execute(used_stmt)
        used_count = used_result.scalar() or 0

        if used_count >= monthly_limit:
            return False

        # Резервирование квоты
        idempotency_key = f"quota_reserve_{uuid.uuid4()}"
        usage_event = UsageEvent(
            workspace_id=workspace_uuid,
            metric="generation",
            units=1,
            value=1,
            status="reserved",
            idempotency_key=idempotency_key,
            description="SMM package generation quota reserved"
        )
        self.db.add(usage_event)
        await self.db.flush()

        logger.info("quota_reserved", workspace_id=str(workspace_uuid), used=used_count, limit=monthly_limit)
        return True

    async def _reverse_quota_reservation(self, generation_id) -> None:
        """Отмена резервирования квоты при ошибке"""
        gen_uuid = uuid.UUID(generation_id) if isinstance(generation_id, str) else generation_id

        usage_stmt = (
            select(UsageEvent)
            .where(UsageEvent.generation_id == gen_uuid)
            .where(UsageEvent.status == "reserved")
        )
        result = await self.db.execute(usage_stmt)
        usage_event = result.scalar_one_or_none()

        if usage_event:
            usage_event.status = "reversed"
            await self.db.commit()
            logger.info("quota_reversed", generation_id=str(gen_uuid))
