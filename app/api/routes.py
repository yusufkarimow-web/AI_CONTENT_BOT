# app/api/routes.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import structlog
import os

from app.db.session import get_db_session
from app.db.models import Generation, Subscription, User, Workspace, UsageEvent
from app.services.generation_service import GenerationService
from app.services.billing_service import BillingService
from app.services.pdf_generator import PDFGenerator
from app.services.whatsapp_service import WhatsAppService
from app.core.config import get_settings
from app.core.errors import QuotaExceededError, AIGenerationError
from pydantic import BaseModel, Field
from typing import Optional, List

logger = structlog.get_logger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api", tags=["API"])

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class GenerationRequest(BaseModel):
    """Запрос на генерацию контента"""
    niche: str = Field(..., min_length=3, max_length=50)
    platform: str = Field(...)
    goal: str = Field(...)
    format_type: str = Field(...)
    brief: Optional[str] = Field(None, max_length=500)
    tone: Optional[str] = Field("professional")

    class Config:
        populate_by_name = True


class GenerationResponse(BaseModel):
    """Ответ при успешной генерации"""
    generation_id: str
    success: bool
    output_text: str
    pdf_url: str
    estimated_reach: int
    tags: List[str]
    cta_suggestions: List[str]


class WhatsAppSendRequest(BaseModel):
    """Запрос на отправку в WhatsApp"""
    generation_id: str
    phone: str = Field(...)


class UserProfileResponse(BaseModel):
    """Профиль пользователя"""
    user_id: str
    username: str
    plan: str
    remaining_generations: int
    remaining_exports: int
    workspace_name: str
    created_at: datetime


class SubscriptionUpgradeRequest(BaseModel):
    """Запрос на обновление подписки"""
    plan_code: str = Field(...)


# ============================================================================
# GENERATION ENDPOINTS
# ============================================================================

@router.post("/generations/create", response_model=GenerationResponse)
async def create_generation(
    request: GenerationRequest,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Создание нового контента через AI
    """
    try:
        # Получение пользователя
        user_uuid = uuid.UUID(user_id)
        user_stmt = select(User).where(User.id == user_uuid)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Проверка лимитов
        billing_service = BillingService(db)
        usage = await billing_service.check_usage(user.workspace_id, "monthly_generations")

        if usage["remaining"] <= 0:
            raise QuotaExceededError(
                "monthly_generations",
                details={"limit": usage["limit"], "remaining": usage["remaining"]}
            )

        # Получение рабочего пространства
        workspace_stmt = select(Workspace).where(Workspace.id == user.workspace_id)
        workspace_result = await db.execute(workspace_stmt)
        workspace = workspace_result.scalar_one_or_none()

        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")

        # Генерация контента через AI Service
        gen_service = GenerationService(db)
        result = await gen_service.generate_smm_package(
            user_id=str(user.id),
            workspace_id=str(workspace.id),
            niche=request.niche,
            platform=request.platform,
            goal=request.goal,
            format_type=request.format_type,
            brief=request.brief or f"Профессиональный {request.niche}",
            language=user.language or "ru",
            country=workspace.country or "uz"
        )

        if not result.success:
            raise HTTPException(status_code=502, detail=result.error_message or "AI Generation failed")

        return GenerationResponse(
            generation_id=result.generation_id,
            success=True,
            output_text=result.output_text,
            pdf_url=result.pdf_url,
            estimated_reach=result.estimated_reach,
            tags=result.tags,
            cta_suggestions=result.cta
        )

    except QuotaExceededError as e:
        logger.warning("generation_quota_exceeded", user_id=user_id)
        raise HTTPException(
            status_code=429,
            detail="Квота превышена"
        )

    except AIGenerationError as e:
        logger.exception("generation_ai_error", error=str(e))
        raise HTTPException(status_code=502, detail="AI generation failed")

    except Exception as e:
        logger.exception("generation_create_error", error=str(e), user_id=user_id)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Generation failed")


@router.get("/generations/{generation_id}/pdf")
async def get_generation_pdf(
    generation_id: str,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Получение PDF файла генерации"""
    try:
        user_uuid = uuid.UUID(user_id)
        gen_uuid = uuid.UUID(generation_id)

        # Проверка прав доступа
        gen_stmt = select(Generation).where(
            (Generation.id == gen_uuid) &
            (Generation.user_id == user_uuid)
        )
        gen_result = await db.execute(gen_stmt)
        generation = gen_result.scalar_one_or_none()

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        pdf_path = f"generated/{generation_id}/content.pdf"

        if not os.path.exists(pdf_path):
            # Regenerate if missing on disk but exists in database
            pdf_generator = PDFGenerator()
            user_stmt = select(User).where(User.id == user_uuid)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()

            await pdf_generator.generate_branded_pdf(
                output_path=pdf_path,
                user_name=user.username if (user and user.username) else "Пользователь",
                content_type=generation.format_type or "SMM",
                content_text=generation.output_text
            )

        logger.info("pdf_downloaded", generation_id=generation_id, user_id=user_id)

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"TojikAI_SMM_{generation_id[:8]}.pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("pdf_download_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to download PDF")


@router.get("/generations/{generation_id}")
async def get_generation(
    generation_id: str,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Получение деталей генерации"""
    try:
        user_uuid = uuid.UUID(user_id)
        gen_uuid = uuid.UUID(generation_id)

        gen_stmt = select(Generation).where(
            (Generation.id == gen_uuid) &
            (Generation.user_id == user_uuid)
        )
        gen_result = await db.execute(gen_stmt)
        generation = gen_result.scalar_one_or_none()

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        return {
            "generation_id": str(generation.id),
            "status": generation.status,
            "niche": generation.niche,
            "platform": generation.platform,
            "goal": generation.goal,
            "output_text": generation.output_text,
            "tags": generation.tags,
            "cta_suggestions": generation.cta_suggestions,
            "created_at": generation.created_at,
            "completed_at": generation.completed_at
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("get_generation_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch generation")


@router.get("/generations/history")
async def get_generation_history(
    user_id: str = Query(...),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db_session)
):
    """Получение истории генераций"""
    try:
        user_uuid = uuid.UUID(user_id)
        stmt = select(Generation).where(
            Generation.user_id == user_uuid
        ).order_by(
            Generation.created_at.desc()
        ).limit(limit).offset(offset)

        result = await db.execute(stmt)
        generations = result.scalars().all()

        return {
            "total": len(generations),
            "generations": [
                {
                    "id": str(g.id),
                    "niche": g.niche,
                    "platform": g.platform,
                    "goal": g.goal,
                    "status": g.status,
                    "created_at": g.created_at
                }
                for g in generations
            ]
        }

    except Exception as e:
        logger.exception("history_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch history")


# ============================================================================
# WHATSAPP ENDPOINTS
# ============================================================================

@router.post("/whatsapp/send")
async def send_to_whatsapp(
    request: WhatsAppSendRequest,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Отправка контента в WhatsApp"""
    try:
        user_uuid = uuid.UUID(user_id)
        gen_uuid = uuid.UUID(request.generation_id)

        # Получение генерации
        gen_stmt = select(Generation).where(
            (Generation.id == gen_uuid) &
            (Generation.user_id == user_uuid)
        )
        gen_result = await db.execute(gen_stmt)
        generation = gen_result.scalar_one_or_none()

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        # Получение пользователя для номера WhatsApp
        user_stmt = select(User).where(User.id == user_uuid)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Проверка лимитов экспорта
        billing_service = BillingService(db)
        usage = await billing_service.check_usage(user.workspace_id, "monthly_exports")

        if usage["remaining"] <= 0:
            raise HTTPException(status_code=429, detail="Export quota exceeded")

        # Инициализация WhatsApp сервиса
        whatsapp_service = WhatsAppService(
            api_url=settings.whatsapp_api_url,
            instance_id=settings.whatsapp_instance_id,
            api_token=settings.whatsapp_api_token
        )

        # Отправка
        success = await whatsapp_service.send_message_with_pdf(
            phone=request.phone,
            text=f"""
🎯 Ваш SMM-пакет готов!

📝 {generation.niche.upper()} | {generation.platform.upper()}
🎯 Цель: {generation.goal}
📐 Формат: {generation.format_type}

Создано через TojikAI v4.0 ✨
            """,
            pdf_url=f"{settings.public_base_url}/api/generations/{generation.id}/pdf?user_id={user_id}"
        )

        if success:
            logger.info(
                "whatsapp_message_sent",
                generation_id=str(generation.id),
                user_id=user_id,
                phone=request.phone[-4:]
            )

            # Логирование использования
            usage_event = UsageEvent(
                id=uuid.uuid4(),
                workspace_id=user.workspace_id,
                user_id=user.id,
                metric="export",
                value=1,
                status="committed",
                idempotency_key=f"export_{uuid.uuid4()}",
                description="WhatsApp pdf export usage event"
            )
            db.add(usage_event)
            await db.commit()

            return {"success": True, "message": "Message sent successfully"}
        else:
            logger.error("whatsapp_send_failed", generation_id=str(generation.id))
            raise HTTPException(status_code=502, detail="WhatsApp send failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("whatsapp_send_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")


# ============================================================================
# USER PROFILE ENDPOINTS
# ============================================================================

@router.get("/user/profile", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Получение профиля пользователя"""
    try:
        user_uuid = uuid.UUID(user_id)
        user_stmt = select(User).where(User.id == user_uuid)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Получение активной подписки
        sub_stmt = select(Subscription).where(
            (Subscription.workspace_id == user.workspace_id) &
            (Subscription.status == "active")
        )
        sub_result = await db.execute(sub_stmt)
        subscription = sub_result.scalar_one_or_none()

        # Получение лимитов
        billing_service = BillingService(db)
        gen_usage = await billing_service.check_usage(user.workspace_id, "monthly_generations")
        export_usage = await billing_service.check_usage(user.workspace_id, "monthly_exports")

        # Получение рабочего пространства
        workspace_stmt = select(Workspace).where(Workspace.id == user.workspace_id)
        workspace_result = await db.execute(workspace_stmt)
        workspace = workspace_result.scalar_one_or_none()

        return UserProfileResponse(
            user_id=str(user.id),
            username=user.username or "unknown",
            plan=subscription.plan_code if subscription else "free",
            remaining_generations=gen_usage["remaining"],
            remaining_exports=export_usage["remaining"],
            workspace_name=workspace.name if workspace else "Default",
            created_at=user.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("profile_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch profile")


@router.post("/user/upgrade-subscription")
async def upgrade_subscription(
    request: SubscriptionUpgradeRequest,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Обновление подписки"""
    try:
        user_uuid = uuid.UUID(user_id)
        user_stmt = select(User).where(User.id == user_uuid)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Создание новой подписки
        new_subscription = Subscription(
            id=uuid.uuid4(),
            workspace_id=user.workspace_id,
            plan_code=request.plan_code,
            status="pending",
            current_period_start=datetime.utcnow()
        )

        db.add(new_subscription)
        await db.commit()

        logger.info(
            "subscription_upgrade_initiated",
            user_id=user_id,
            plan=request.plan_code
        )

        return {
            "subscription_id": str(new_subscription.id),
            "plan": request.plan_code,
            "status": "pending",
            "next_step": "complete_payment"
        }

    except Exception as e:
        logger.exception("upgrade_error", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to upgrade subscription")


# ============================================================================
# INTERNAL PAYMENT LINK GENERATOR
# ============================================================================

@router.get("/payments/create-link")
async def create_payment_link(
    plan: str,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Создание ссылки на оплату"""
    try:
        user_uuid = uuid.UUID(user_id)
        user_stmt = select(User).where(User.id == user_uuid)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        billing_service = BillingService(db)

        # Получение рабочего пространства
        ws_stmt = select(Workspace).where(Workspace.id == user.workspace_id)
        ws_result = await db.execute(ws_stmt)
        workspace = ws_result.scalar_one_or_none()
        country = workspace.country if workspace else "uz"

        # Получение цены
        pricing = billing_service.PRICING.get(country, {})
        plan_pricing = pricing.get(plan)

        if not plan_pricing:
            raise HTTPException(status_code=400, detail="Invalid plan or country")

        # Создание подписки в статусе pending
        subscription = Subscription(
            id=uuid.uuid4(),
            workspace_id=user.workspace_id,
            plan_code=plan,
            status="pending",
            current_period_start=datetime.utcnow()
        )
        db.add(subscription)
        await db.flush()

        # Возврат ссылок оплаты для разных провайдеров
        return {
            "subscription_id": str(subscription.id),
            "amount": plan_pricing["monthly"],
            "currency": plan_pricing["currency"],
            "payment_links": {
                "click": f"https://checkout.click.uz/{settings.click_service_id}/{subscription.id}",
                "payme": f"https://checkout.payme.uz/merchant/{settings.payme_merchant_id}/{subscription.id}",
                "alif": f"https://payment.alif.tj/merchant/{settings.alif_merchant_id}/{subscription.id}"
            }
        }

    except Exception as e:
        logger.exception("create_payment_link_error", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
