# app/services/billing_service.py
import uuid
import structlog
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Subscription, Payment, User, UsageEvent, Workspace
from app.core.errors import PaymentError, NotFoundError, ConflictError
from typing import Optional, Dict, Any

logger = structlog.get_logger(__name__)

class BillingService:
    """Управление подписками, платежами и квотами"""

    PLAN_LIMITS = {
        "free": {
            "monthly_generations": 5,
            "monthly_exports": 2,
            "max_batch_size": 1,
            "api_calls_per_hour": 10,
            "storage_gb": 1,
        },
        "starter": {
            "monthly_generations": 50,
            "monthly_exports": 20,
            "max_batch_size": 5,
            "api_calls_per_hour": 100,
            "storage_gb": 10,
        },
        "pro": {
            "monthly_generations": 200,
            "monthly_exports": 100,
            "max_batch_size": 20,
            "api_calls_per_hour": 500,
            "storage_gb": 100,
        },
        "team": {
            "monthly_generations": 1000,
            "monthly_exports": 500,
            "max_batch_size": 100,
            "api_calls_per_hour": 2000,
            "storage_gb": 500,
        },
        "enterprise": {
            "monthly_generations": 999999,
            "monthly_exports": 999999,
            "max_batch_size": 999999,
            "api_calls_per_hour": 999999,
            "storage_gb": 9999,
        }
    }

    PRICING = {
        "uz": {  # UZS - тийин (minor units)
            "starter": {
                "monthly": 29900,  # 299 UZS = ~0.02 USD
                "currency": "UZS",
                "duration_days": 30
            },
            "pro": {
                "monthly": 99900,  # 999 UZS
                "currency": "UZS",
                "duration_days": 30
            },
            "team": {
                "monthly": 299900,  # 2999 UZS
                "currency": "UZS",
                "duration_days": 30
            }
        },
        "tj": {  # TJS - дирам (minor units)
            "starter": {
                "monthly": 29900,  # 299 TJS
                "currency": "TJS",
                "duration_days": 30
            },
            "pro": {
                "monthly": 99900,  # 999 TJS
                "currency": "TJS",
                "duration_days": 30
            },
            "team": {
                "monthly": 299900,  # 2999 TJS
                "currency": "TJS",
                "duration_days": 30
            }
        },
        "ru": {  # RUB - копейки (minor units)
            "starter": {
                "monthly": 1999,  # 19.99 RUB
                "currency": "RUB",
                "duration_days": 30
            },
            "pro": {
                "monthly": 5999,  # 59.99 RUB
                "currency": "RUB",
                "duration_days": 30
            },
            "team": {
                "monthly": 19999,  # 199.99 RUB
                "currency": "RUB",
                "duration_days": 30
            }
        }
    }

    def __init__(self, db: AsyncSession):
        self.db = db

    async def apply_payment(
        self,
        reference: str,
        provider: str,
        amount_minor: int,
        provider_event_id: str,
        provider_payload: dict = None
    ) -> bool:
        """Применение платежа (идемпотентная операция)"""

        try:
            # Проверка на дубликат платежа (идемпотентность)
            existing_stmt = select(Payment).where(
                (Payment.reference == reference) |
                ((Payment.provider == provider) & (Payment.provider_event_id == provider_event_id))
            )
            existing_result = await self.db.execute(existing_stmt)
            existing_payment = existing_result.scalar_one_or_none()

            if existing_payment and existing_payment.status == "paid":
                logger.warning("payment_already_processed", reference=reference, provider=provider)
                return True  # Идемпотентный ответ

            # Получение подписки по reference
            sub_stmt = select(Subscription).where(Subscription.id == reference)
            sub_result = await self.db.execute(sub_stmt)
            subscription = sub_result.scalar_one_or_none()

            if not subscription:
                logger.error("subscription_not_found", reference=reference)
                raise NotFoundError("Subscription", reference)

            # Получить рабочее пространство
            ws_stmt = select(Workspace).where(Workspace.id == subscription.workspace_id)
            ws_result = await self.db.execute(ws_stmt)
            workspace = ws_result.scalar_one_or_none()
            country = workspace.country if workspace else "uz"

            # Создание или обновление платежа
            if existing_payment:
                existing_payment.status = "paid"
                existing_payment.paid_at = datetime.utcnow()
                existing_payment.provider_payload = provider_payload or {}
                payment = existing_payment
            else:
                payment = Payment(
                    id=uuid.uuid4(),
                    subscription_id=subscription.id,
                    provider=provider,
                    provider_event_id=provider_event_id,
                    reference=reference,
                    plan_code=subscription.plan_code,
                    status="paid",
                    amount_minor=amount_minor,
                    currency=self.PRICING.get(country, {}).get(subscription.plan_code, {}).get("currency", "UZS"),
                    paid_at=datetime.utcnow(),
                    provider_payload=provider_payload or {}
                )
                self.db.add(payment)

            # Активация подписки
            subscription.status = "active"
            subscription.current_period_start = datetime.utcnow()
            subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
            subscription.provider = provider
            subscription.auto_renew = True
            subscription.updated_at = datetime.utcnow()

            await self.db.commit()

            logger.info(
                "payment_applied_successfully",
                reference=reference,
                provider=provider,
                plan=subscription.plan_code,
                amount=amount_minor
            )

            return True

        except Exception as e:
            logger.exception("payment_apply_error", error=str(e), reference=reference)
            await self.db.rollback()
            return False

    async def get_subscription_limits(self, workspace_id: str) -> dict:
        """Получение лимитов текущего тарифа"""

        try:
            sub_stmt = select(Subscription).where(
                (Subscription.workspace_id == workspace_id) &
                (Subscription.status == "active")
            )
            result = await self.db.execute(sub_stmt)
            subscription = result.scalar_one_or_none()

            if not subscription:
                # Если нет активной подписки, возвращаем free лимиты
                return self.PLAN_LIMITS.get("free", {})

            return self.PLAN_LIMITS.get(subscription.plan_code, self.PLAN_LIMITS["free"])

        except Exception as e:
            logger.exception("get_limits_error", error=str(e))
            return self.PLAN_LIMITS["free"]

    async def check_usage(
        self,
        workspace_id: str,
        metric: str = "monthly_generations"
    ) -> dict:
        """Проверка использования лимитов"""

        try:
            limits = await self.get_subscription_limits(workspace_id)
            limit_value = limits.get(metric, 0)

            # Подсчет использования за месяц
            month_ago = datetime.utcnow() - timedelta(days=30)

            if metric == "monthly_generations":
                from app.db.models import Generation
                usage_stmt = select(func.count(Generation.id)).where(
                    (Generation.workspace_id == workspace_id) &
                    (Generation.created_at >= month_ago) &
                    (Generation.status.in_(["completed", "pending"]))
                )
            elif metric == "monthly_exports":
                usage_stmt = select(func.count(UsageEvent.id)).where(
                    (UsageEvent.workspace_id == workspace_id) &
                    (UsageEvent.metric == "export") &
                    (UsageEvent.created_at >= month_ago)
                )
            else:
                usage_stmt = select(func.count(UsageEvent.id)).where(
                    (UsageEvent.workspace_id == workspace_id) &
                    (UsageEvent.metric == metric) &
                    (UsageEvent.created_at >= month_ago)
                )

            result = await self.db.execute(usage_stmt)
            used_value = result.scalar() or 0

            return {
                "metric": metric,
                "limit": limit_value,
                "used": used_value,
                "remaining": max(0, limit_value - used_value),
                "percentage_used": round((used_value / limit_value * 100) if limit_value > 0 else 0, 2)
            }

        except Exception as e:
            logger.exception("check_usage_error", error=str(e))
            return {
                "metric": metric,
                "limit": 0,
                "used": 0,
                "remaining": 0,
                "percentage_used": 0
            }
