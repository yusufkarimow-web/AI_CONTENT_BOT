# services/payment/crypto.py — Криптовалютные платежи (USDT TRC-20)

import aiohttp
from typing import Dict, Any

from config import CRYPTO_PAY_API_KEY


class CryptoPay:
    """
    Криптовалютные платежи через CryptoPay или аналог
    USDT TRC-20 — для диаспоры и анонимных платежей
    """

    # Адрес кошелька для приёма USDT (замени на свой!)
    USDT_WALLET = "TXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # TRC-20 адрес

    def __init__(self):
        self.api_key = CRYPTO_PAY_API_KEY

    async def create_invoice(
        self,
        amount: float,  # в USDT
        order_id: str,
        description: str = "Sozanda Premium"
    ) -> Dict[str, Any]:
        """
        Создать инвойс для оплаты

        Returns:
            dict: {success, invoice_url, invoice_id, error}
        """

        if not self.api_key:
            # Fallback: просто показываем адрес кошелька
            return {
                "success": True,
                "invoice_url": None,
                "invoice_id": order_id,
                "error": None,
                "manual": True,
                "wallet": self.USDT_WALLET,
            }

        # Если API настроен — можно интегрировать CryptoBot API или аналог
        try:
            # Пример интеграции с CryptoBot
            async with aiohttp.ClientSession() as session:
                payload = {
                    "asset": "USDT",
                    "amount": amount,
                    "description": description,
                    "hidden_message": f"Order: {order_id}",
                    "paid_btn_name": "callback",
                    "paid_btn_url": f"https://t.me/sozanda_bot?start=payment_{order_id}",
                }

                headers = {"Crypto-Pay-API-Token": self.api_key}

                async with session.post(
                    "https://pay.crypt.bot/api/createInvoice",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        if data.get("ok"):
                            result = data.get("result", {})
                            return {
                                "success": True,
                                "invoice_url": result.get("pay_url"),
                                "invoice_id": result.get("invoice_id"),
                                "error": None,
                                "manual": False,
                            }

                    return {
                        "success": False,
                        "error": "Ошибка создания инвойса",
                        "invoice_url": None,
                        "invoice_id": None,
                    }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "invoice_url": None,
                "invoice_id": None,
            }

    def get_instructions(self, amount: float, order_id: str, lang: str = "ru") -> str:
        """Инструкции для ручной оплаты USDT"""

        if lang == "tg":
            return f"""₿ <b>Пардохт бо USDT (TRC-20)</b>

Сумма: <b>{amount} USDT</b>
Шабака: <b>TRC-20 (Tron)</b>
Адрес: <code>{self.USDT_WALLET}</code>

⚠️ <b>Муҳим:</b>
- Танҳо TRC-20!
- Пас аз пардохт скриншот фиристед @sozanda_support

ID фармоиш: <code>{order_id}</code>"""
        else:
            return f"""₿ <b>Оплата USDT (TRC-20)</b>

Сумма: <b>{amount} USDT</b>
Сеть: <b>TRC-20 (Tron)</b>
Адрес: <code>{self.USDT_WALLET}</code>

⚠️ <b>Важно:</b>
- Только TRC-20!
- После оплаты отправьте скриншот @sozanda_support

ID заказа: <code>{order_id}</code>"""

    async def check_payment(self, invoice_id: str) -> Dict[str, Any]:
        """Проверить статус инвойса"""

        if not self.api_key:
            return {"success": False, "paid": False, "error": "API не настроен"}

        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Crypto-Pay-API-Token": self.api_key}

                async with session.get(
                    f"https://pay.crypt.bot/api/getInvoices",
                    params={"invoice_ids": invoice_id},
                    headers=headers,
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        if data.get("ok"):
                            invoices = data.get("result", {}).get("items", [])
                            if invoices:
                                status = invoices[0].get("status")
                                return {
                                    "success": True,
                                    "paid": status == "paid",
                                    "status": status,
                                    "error": None,
                                }

                    return {
                        "success": False,
                        "paid": False,
                        "status": "unknown",
                        "error": "Не удалось проверить",
                    }

        except Exception as e:
            return {
                "success": False,
                "paid": False,
                "status": "error",
                "error": str(e),
            }