# app/services/whatsapp_service.py
import httpx
import structlog
from pydantic import SecretStr
from typing import Optional

logger = structlog.get_logger(__name__)

class WhatsAppService:
    """Интеграция с WhatsApp API через Green-API"""

    def __init__(self, api_url: str, instance_id: str, api_token: SecretStr):
        self.api_url = api_url.rstrip("/")
        self.instance_id = instance_id
        self.api_token = api_token.get_secret_value()
        self.base_url = f"{self.api_url}/waInstance{self.instance_id}"

    async def send_text_message(self, phone: str, text: str) -> bool:
        """Отправка текстового сообщения в WhatsApp"""

        if not phone or not text:
            logger.error("whatsapp_missing_params", phone=bool(phone), text=bool(text))
            return False

        # Очистка номера телефона (оставляем только цифры)
        clean_phone = "".join(filter(str.isdigit, phone))
        if not clean_phone:
            logger.error("whatsapp_invalid_phone", phone=phone)
            return False

        # Формат для WhatsApp: 992123456789@c.us или 998901234567@c.us
        chat_id = f"{clean_phone}@c.us"

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chatId": chat_id,
            "message": text
        }
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        try:
            # Fallback for mock credentials
            if "fake" in self.api_token:
                logger.info("whatsapp_message_sent_simulated", phone=clean_phone)
                return True

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code in [200, 201]:
                    logger.info(
                        "whatsapp_message_sent",
                        phone=clean_phone,
                        message_length=len(text)
                    )
                    return True
                else:
                    logger.error(
                        "whatsapp_send_failed",
                        status_code=response.status_code,
                        response=response.text[:200]
                    )
                    return False

        except httpx.TimeoutException:
            logger.error("whatsapp_timeout", phone=clean_phone)
            return False
        except Exception as e:
            logger.exception("whatsapp_send_exception", error=str(e), phone=clean_phone)
            return False

    async def send_file(
        self,
        phone: str,
        file_url: str,
        filename: str = "document.pdf",
        caption: str = ""
    ) -> bool:
        """Отправка файла (PDF, изображения) через WhatsApp"""

        clean_phone = "".join(filter(str.isdigit, phone))
        if not clean_phone:
            logger.error("whatsapp_invalid_phone_file", phone=phone)
            return False

        chat_id = f"{clean_phone}@c.us"
        url = f"{self.base_url}/sendFileByUrl"

        payload = {
            "chatId": chat_id,
            "urlFile": file_url,
            "fileName": filename,
            "caption": caption
        }
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        try:
            if "fake" in self.api_token:
                logger.info("whatsapp_file_sent_simulated", phone=clean_phone, filename=filename)
                return True

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code in [200, 201]:
                    logger.info("whatsapp_file_sent", phone=clean_phone, filename=filename)
                    return True
                else:
                    logger.error(
                        "whatsapp_file_send_failed",
                        status_code=response.status_code,
                        response=response.text[:200]
                    )
                    return False

        except Exception as e:
            logger.exception("whatsapp_file_send_exception", error=str(e), phone=clean_phone)
            return False

    async def send_message_with_pdf(
        self,
        phone: str,
        text: str,
        pdf_url: Optional[str] = None
    ) -> bool:
        """Отправка сообщения с опциональным PDF-файлом"""

        # Отправка текста
        text_success = await self.send_text_message(phone, text)

        if not text_success:
            return False

        # Отправка PDF если передан
        if pdf_url:
            file_success = await self.send_file(
                phone=phone,
                file_url=pdf_url,
                filename="TojikAI_SMM_Package.pdf",
                caption="📊 Ваш готовый SMM Маркетинговый Пакет"
            )
            return file_success

        return True

    async def get_account_status(self) -> dict:
        """Получение статуса аккаунта в Green-API"""

        url = f"{self.base_url}/getMe"
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        try:
            if "fake" in self.api_token:
                return {"status": "ok", "mock": True}

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        "whatsapp_status_failed",
                        status_code=response.status_code
                    )
                    return {}

        except Exception as e:
            logger.exception("whatsapp_status_exception", error=str(e))
            return {}
