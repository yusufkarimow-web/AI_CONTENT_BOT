# services/payment/humo.py — Интеграция с Humo Online (Таджикистан)

import aiohttp
from typing import Dict, Any

from config import HUMO_MERCHANT_ID, HUMO_API_KEY


class HumoPay:
    """
    Платёжная система Humo Online для Таджикистана
    """

    BASE_URL = "https://api.humo.tj/v1"
    TEST_MODE = True

    def __init__(self):
        self.merchant_id = HUMO_MERCHANT_ID
        self.api_key = HUMO_API_KEY

    async def create_payment(
        self,
        amount: float,
        order_id: str,
        description: str = "Sozanda Premium"
    ) -> Dict[str, Any]:
        """Создать платёж через Humo"""

        if not self.merchant_id:
            return {
                "success": False,
                "error": "Humo не настроен",
                "payment_url": None,
            }

        # Fallback: ручная оплата
        return {
            "success": True,
            "payment_url": None,  # Ручная оплата
            "transaction_id": order_id,
            "error": None,
            "manual": True,
        }

    def get_instructions(self, amount: float, order_id: str, lang: str = "ru") -> str:
        """Инструкции для ручной оплаты Humo"""

        if lang == "tg":
            return f"""💳 <b>Пардохт тавассути Humo Online</b>

Сумма: <b>{amount} сомонӣ</b>
Рақам: <code>+992 93 456 78 90</code>
Ном: <b>SOZANDA BOT</b>
Изоҳ: <code>{order_id}</code>"""
        else:
            return f"""💳 <b>Оплата через Humo Online</b>

Сумма: <b>{amount} сомони</b>
Номер: <code>+992 93 456 78 90</code>
Имя: <b>SOZANDA BOT</b>
Комментарий: <code>{order_id}</code>"""


class HumoPaySimple:
    """Упрощённая версия"""

    def get_instructions(self, amount: float, order_id: str, lang: str = "ru") -> str:
        return HumoPay().get_instructions(amount, order_id, lang)