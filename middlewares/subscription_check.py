# middlewares/subscription_check.py — Middleware проверки подписки

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from database.models import get_user_subscription, check_daily_limit


class SubscriptionCheckMiddleware(BaseMiddleware):
    """
    Middleware для проверки статуса подписки
    Добавляет subscription и limit_info в data
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            # Получаем подписку
            try:
                sub = await get_user_subscription(user_id)
                data["subscription"] = sub

                # Получаем лимиты
                _, limit_info = await check_daily_limit(user_id)
                data["limit_info"] = limit_info

            except Exception as e:
                data["subscription"] = None
                data["limit_info"] = {"can_generate": True, "remaining": 3}
        else:
            data["subscription"] = None
            data["limit_info"] = {"can_generate": True, "remaining": 3}

        return await handler(event, data)