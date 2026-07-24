# app/api/payments.py
import hashlib
import hmac
import time
from fastapi import APIRouter, Form, HTTPException, Depends, Header, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import structlog

from app.db.session import get_db_session
from app.services.billing_service import BillingService
from app.core.config import get_settings

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/payments", tags=["Payments"])

settings = get_settings()

# ============================================================================
# CLICK PAYMENT GATEWAY (Узбекистан)
# ============================================================================

@router.post("/callback/click")
async def click_payment_callback(
    click_trans_id: str = Form(...),
    service_id: str = Form(...),
    click_paydoc_id: str = Form(...),
    merchant_trans_id: str = Form(...),
    amount: float = Form(...),
    action: int = Form(...),
    error: int = Form(...),
    error_note: str = Form(...),
    sign_time: str = Form(...),
    sign_string: str = Form(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Click платежная система callback для Узбекистана"""

    logger.info(
        "click_callback_received",
        trans_id=click_trans_id,
        amount=amount,
        action=action
    )

    # Проверка подписи
    secret = settings.click_secret_key.get_secret_value()
    raw_sign = f"{click_trans_id}{service_id}{secret}{merchant_trans_id}{amount}{action}{sign_time}"
    expected_sign = hashlib.md5(raw_sign.encode("utf-8")).hexdigest()

    if sign_string != expected_sign:
        logger.warning("click_invalid_signature", trans_id=click_trans_id)
        return {
            "error": -1,
            "error_note": "Invalid signature"
        }

    if error != 0:
        logger.warning("click_payment_error", error=error, error_note=error_note)
        return {
            "error": error,
            "error_note": error_note
        }

    if action == 1:  # Выполнение платежа
        try:
            billing_service = BillingService(db)
            success = await billing_service.apply_payment(
                reference=merchant_trans_id,
                provider="click",
                amount_minor=int(amount * 100),
                provider_event_id=click_trans_id,
                provider_payload={
                    "click_trans_id": click_trans_id,
                    "click_paydoc_id": click_paydoc_id,
                    "service_id": service_id
                }
            )

            if success:
                logger.info("click_payment_processed", trans_id=click_trans_id)
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "error": 0,
                    "error_note": "Success"
                }
            else:
                logger.error("click_payment_apply_failed", trans_id=click_trans_id)
                return {
                    "error": -2,
                    "error_note": "Transaction activation failed"
                }
        except Exception as e:
            logger.exception("click_callback_exception", error=str(e))
            return {
                "error": -2,
                "error_note": "Internal server error"
            }

    elif action == 0:  # Проверка платежа
        return {
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "error": 0,
            "error_note": "Success"
        }


# ============================================================================
# PAYME PAYMENT GATEWAY (Узбекистан)
# ============================================================================

class PaymeCheckPerformRequest(BaseModel):
    id: str
    method: str
    params: dict

@router.post("/callback/payme")
async def payme_payment_callback(
    body: dict = Body(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Payme платежная система callback для Узбекистана"""

    logger.info("payme_callback_received", method=body.get("method"))

    method = body.get("method")
    params = body.get("params", {})
    merchant_id = params.get("merchant_id")

    # Проверка merchant_id
    if merchant_id != settings.payme_merchant_id:
        return {
            "error": {
                "code": -32504,
                "message": "Invalid merchant"
            }
        }

    try:
        if method == "CheckPerformance":
            # Проверка возможности выполнения платежа
            account = params.get("account", {})
            merchant_trans_id = account.get("order_id")

            # Проверить наличие заказа в БД
            from app.db.models import Subscription
            from sqlalchemy import select

            sub_stmt = select(Subscription).where(Subscription.id == merchant_trans_id)
            result = await db.execute(sub_stmt)
            subscription = result.scalar_one_or_none()

            if subscription:
                return {
                    "result": {
                        "allow": True
                    }
                }
            else:
                return {
                    "error": {
                        "code": -31050,
                        "message": "Order not found"
                    }
                }

        elif method == "CreateTransaction":
            # Создание транзакции
            account = params.get("account", {})
            amount = params.get("amount")
            merchant_trans_id = account.get("order_id")
            payme_trans_id = params.get("id")

            return {
                "result": {
                    "transaction": payme_trans_id,
                    "perform_time": 0,
                    "cancel_time": 0,
                    "state": 1  # Processing
                }
            }

        elif method == "PerformTransaction":
            # Выполнение транзакции
            account = params.get("account", {})
            amount = params.get("amount")
            merchant_trans_id = account.get("order_id")
            payme_trans_id = params.get("id")

            billing_service = BillingService(db)
            success = await billing_service.apply_payment(
                reference=merchant_trans_id,
                provider="payme",
                amount_minor=amount,
                provider_event_id=payme_trans_id,
                provider_payload={
                    "payme_trans_id": payme_trans_id,
                    "account": account
                }
            )

            if success:
                logger.info("payme_payment_processed", trans_id=payme_trans_id)
                return {
                    "result": {
                        "transaction": payme_trans_id,
                        "perform_time": int(time.time()),
                        "cancel_time": 0,
                        "state": 2  # Done
                    }
                }
            else:
                return {
                    "error": {
                        "code": -32400,
                        "message": "Payment processing failed"
                    }
                }

        elif method == "CancelTransaction":
            # Отмена транзакции
            payme_trans_id = params.get("id")

            logger.info("payme_transaction_cancelled", trans_id=payme_trans_id)
            return {
                "result": {
                    "transaction": payme_trans_id,
                    "perform_time": 0,
                    "cancel_time": int(time.time()),
                    "state": -2  # Cancelled
                }
            }

    except Exception as e:
        logger.exception("payme_callback_exception", error=str(e))
        return {
            "error": {
                "code": -32400,
                "message": "Internal server error"
            }
        }


# ============================================================================
# ALIF MOBI PAYMENT GATEWAY (Таджикистан)
# ============================================================================

class AlifCallbackPayload(BaseModel):
    transaction_id: str
    order_id: str
    amount: float
    currency: str
    status: str

@router.post("/callback/alif")
async def alif_payment_callback(
    payload: AlifCallbackPayload,
    x_alif_signature: str = Header(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Alif Mobi платежная система callback для Таджикистана"""

    logger.info("alif_callback_received", order_id=payload.order_id, status=payload.status)

    # Проверка HMAC-SHA256 подписи
    secret = settings.alif_secret_key.get_secret_value()
    raw_body = payload.model_dump_json(exclude_none=True).encode("utf-8")
    expected_signature = hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if x_alif_signature != expected_signature:
        logger.warning("alif_invalid_signature", order_id=payload.order_id)
        raise HTTPException(status_code=401, detail="UNAUTHORIZED_SIGNATURE")

    if payload.status == "success":
        try:
            billing_service = BillingService(db)
            success = await billing_service.apply_payment(
                reference=payload.order_id,
                provider="alif",
                amount_minor=int(payload.amount * 100),
                provider_event_id=payload.transaction_id,
                provider_payload={
                    "currency": payload.currency,
                    "status": payload.status
                }
            )

            if success:
                logger.info("alif_payment_processed", trans_id=payload.transaction_id)
                return {
                    "status": "ok",
                    "message": "Transaction verified and processed"
                }
            else:
                logger.error("alif_payment_apply_failed", order_id=payload.order_id)
                raise HTTPException(status_code=400, detail="PAYMENT_APPLY_FAILED")

        except Exception as e:
            logger.exception("alif_callback_exception", error=str(e))
            raise HTTPException(status_code=500, detail="Internal server error")

    elif payload.status == "failed":
        logger.warning("alif_payment_failed", order_id=payload.order_id)
        return {
            "status": "ok",
            "message": "Payment failure recorded"
        }

    else:
        logger.warning("alif_unknown_status", status=payload.status)
        return {
            "status": "ok",
            "message": "Status recorded"
        }
