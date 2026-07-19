# services/payment/alif_pay.py — Интеграция с Alif Mobi (Таджикистан)

import aiohttp
import json
from typing import Optional, Dict, Any

from config import ALIF_MERCHANT_ID, ALIF_API_KEY


class AlifPay:
    """
    Платёжная система Alif Mobi для Таджикистана
    Документация: https://alif.tj/merchant-api
    """

    BASE_URL = "https://api.alif.tj/v1"
    TEST_MODE = True  # True = тестовый режим, без реальных списаний

    def __init__(self):
        self.merchant_id = ALIF_MERCHANT_ID
        self.api_key = ALIF_API_KEY

    async def create_payment(
        self,
        amount: float,
        order_id: str,
        description: str = "Sozanda Premium",
        callback_url: str = "https://sozanda.tj/callback/alif"
    ) -> Dict[str, Any]:
        """
        Создать платёж

        Args:
            amount: Сумма в сомони
            order_id: Уникальный ID заказа
            description: Описание платежа
            callback_url: URL для callback

        Returns:
            dict: {success: bool, payment_url: str, transaction_id: str, error: str}
        """

        if not self.merchant_id or not self.api_key:
            return {
                "success": False,
                "error": "Alif Mobi не настроен. Добавьте ALIF_MERCHANT_ID и ALIF_API_KEY в .env",
                "payment_url": None,
                "transaction_id": None,
            }

        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "currency": "TJS",
            "order_id": order_id,
            "description": description,
            "callback_url": callback_url,
            "test": self.TEST_MODE,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.BASE_URL}/payments",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "payment_url": data.get("payment_url"),
                            "transaction_id": data.get("transaction_id"),
                            "error": None,
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "payment_url": None,
                            "transaction_id": None,
                        }

        except aiohttp.ClientError as e:
            return {
                "success": False,
                "error": f"Ошибка соединения: {str(e)}",
                "payment_url": None,
                "transaction_id": None,
            }

    async def check_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        Проверить статус платежа

        Returns:
            dict: {success: bool, status: str, paid: bool, error: str}
        """

        if not self.merchant_id or not self.api_key:
            return {
                "success": False,
                "status": "unknown",
                "paid": False,
                "error": "Alif Mobi не настроен",
            }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.BASE_URL}/payments/{transaction_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        status = data.get("status", "unknown")
                        return {
                            "success": True,
                            "status": status,
                            "paid": status == "completed",
                            "error": None,
                        }
                    else:
                        return {
                            "success": False,
                            "status": "unknown",
                            "paid": False,
                            "error": f"HTTP {response.status}",
                        }

        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "paid": False,
                "error": str(e),
            }

    def get_payment_instructions(self, amount: float, order_id: str, lang: str = "ru") -> str:
        """Получить текст инструкций для ручной оплаты (fallback)"""

        if lang == "tg":
            return f"""💳 <b>Пардохт тавассути Alif Mobi</b>

Сумма: <b>{amount} сомонӣ</b>
Рақами ҳисоб: <code>+992 91 123 45 67</code>
Ном: <b>SOZANDA BOT</code>
Изоҳ: <code>{order_id}</code>

Пас аз пардохт тугмаи "Ман пардохт кардам"-ро зер кунед."""
        else:
            return f"""💳 <b>Оплата через Alif Mobi</b>

Сумма: <b>{amount} сомони</b>
Номер счёта: <code>+992 91 123 45 67</code>
Имя: <b>SOZANDA BOT</b>
Комментарий: <code>{order_id}</code>

После оплаты нажмите кнопку "Я оплатил"."""


# ============================================
# УПРОЩЁННАЯ ВЕРСИЯ (для старта без API)
# ============================================

class AlifPaySimple:
    """
    Упрощённая версия без API — ручная проверка админом
    """

    def __init__(self):
        self.merchant_id = ALIF_MERCHANT_ID

    def get_instructions(self, amount: float, order_id: str, lang: str = "ru") -> str:
        """Просто возвращает инструкции"""

        if lang == "tg":
            return f"""💳 <b>Пардохт тавассути Alif Mobi</b>

Сумма: <b>{amount} сомонӣ</b>
Рақам: <code>+992 91 123 45 67</code>
Ном: <b>SOZANDA</b>
Изоҳ: <code>{order_id}</code>

Пас аз пардохт тугмаи зерро зер кунед."""
        else:
            return f"""💳 <b>Оплата через Alif Mobi</b>

Сумма: <b>{amount} сомони</b>
Номер: <code>+992 91 123 45 67</code>
Имя: <b>SOZANDA</b>
Комментарий: <code>{order_id}</code>

После оплаты нажмите кнопку ниже."""