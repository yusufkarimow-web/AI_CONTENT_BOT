# middlewares/analytics_middleware.py — Middleware сбора аналитики

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from database.models import log_event


class AnalyticsMiddleware(BaseMiddleware):
    """
    Middleware для сбора аналитики
    Логирует все сообщения и callback'и
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            # Определяем тип события
            event_type = "message"
            event_data = ""

            if isinstance(event, Message):
                if event.text:
                    event_data = event.text[:100]  # Первые 100 символов
                    # Определяем тип по тексту
                    if event.text.startswith("/"):
                        event_type = "command"
                    elif event.text in ["🎬 Контент AI", "🎬 AI мундод"]:
                        event_type = "menu_content"
                    elif event.text in ["⭐ Premium", "⭐ Премиум"]:
                        event_type = "menu_premium"
                    elif event.text in ["👥 Рефералка", "👥 Даъват"]:
                        event_type = "menu_referral"
                    else:
                        event_type = "text_message"
                elif event.photo:
                    event_type = "photo"
                elif event.video:
                    event_type = "video"

            elif isinstance(event, CallbackQuery):
                event_type = "callback"
                event_data = event.data[:100] if event.data else ""

            # Логируем асинхронно (не блокируем)
            try:
                import asyncio
                asyncio.create_task(
                    log_event(user_id, event_type, event_data)
                )
            except:
                pass

        return await handler(event, data)