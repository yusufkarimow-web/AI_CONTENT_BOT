# middlewares/i18n_middleware.py — Middleware для определения языка пользователя

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class I18nMiddleware(BaseMiddleware):
    """
    Middleware для автоматического определения языка пользователя
    Добавляет language в data для использования в handlers
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем user_id
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            # Пробуем получить язык из БД
            try:
                from database.models import get_user
                user = await get_user(user_id)
                if user and user.get("language"):
                    data["language"] = user["language"]
                else:
                    data["language"] = "ru"  # По умолчанию русский
            except:
                data["language"] = "ru"
        else:
            data["language"] = "ru"

        return await handler(event, data)