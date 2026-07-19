# services/payment/eskhata.py — Заглушка для EskhataPay

class EskhataPay:
    def __init__(self, merchant_id: str = None, api_key: str = None):
        self.merchant_id = merchant_id
        self.api_key = api_key

    async def create_payment(self, amount: float, description: str, user_id: int) -> dict:
        # В будущем здесь будет реальная интеграция
        return {
            "payment_id": "eskhata_mock_id",
            "payment_url": "https://eskhata.tj"
        }
