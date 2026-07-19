# middlewares/rate_limit.py — Rate Limiting Middleware
# Защита от DDoS и злоупотреблений API

import asyncio
import time
import logging
from typing import Optional
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseMiddleware):
    """Rate limiting middleware с Redis backend.

    Использует sliding window algorithm для точного подсчёта.

    Args:
        redis_url: URL Redis для хранения счётчиков
        config: RateLimitConfig из config.py
    """

    def __init__(self, redis_url: str, config):
        self.config = config
        self.redis_url = redis_url
        self._redis = None
        self._local_cache: dict = {}  # Fallback если Redis недоступен
        self._lock = asyncio.Lock()

    async def _get_redis(self):
        """Ленивая инициализация Redis."""
        if self._redis is None:
            try:
                import redis.asyncio as aioredis
                self._redis = await aioredis.from_url(self.redis_url)
            except Exception as e:
                logger.warning(f"⚠️ Redis недоступен для rate limit: {e}")
                self._redis = False  # Mark as failed
        return self._redis if self._redis else None

    async def _check_limit(
        self,
        key: str,
        limit: int,
        window: int = 60,
    ) -> tuple[bool, int, int]:
        """Проверяет rate limit по ключу.

        Returns:
            (allowed, remaining, reset_in)
        """
        redis = await self._get_redis()
        now = time.time()

        if redis:
            # Redis-based sliding window
            pipe = redis.pipeline()
            pipe.zremrangebyscore(key, 0, now - window)
            pipe.zcard(key)
            pipe.zadd(key, {str(now): now})
            pipe.expire(key, window)
            _, current_count, _, _ = await pipe.execute()

            allowed = current_count < limit
            remaining = max(0, limit - current_count - 1)
            reset_in = window
        else:
            # In-memory fallback (не подходит для production с несколькими инстансами)
            async with self._lock:
                if key not in self._local_cache:
                    self._local_cache[key] = []

                # Очищаем старые записи
                self._local_cache[key] = [
                    t for t in self._local_cache[key]
                    if now - t < window
                ]

                current_count = len(self._local_cache[key])
                allowed = current_count < limit

                if allowed:
                    self._local_cache[key].append(now)

                remaining = max(0, limit - current_count - 1)
                reset_in = window

        return allowed, remaining, reset_in

    async def __call__(self, handler, event, data):
        """Проверяет rate limit перед обработкой события."""
        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None

        if not user_id:
            return await handler(event, data)

        # Per-user limit
        user_key = f"rate_limit:user:{user_id}"
        allowed, remaining, reset_in = await self._check_limit(
            user_key,
            self.config.user_generations_per_minute,
            self.config.window_seconds,
        )

        if not allowed:
            logger.warning(
                f"⛔ Rate limit exceeded для user {user_id}",
                extra={"user_id": user_id, "type": "user_limit"}
            )
            if isinstance(event, Message):
                await event.answer(
                    f"⏳ Слишком много запросов. Попробуйте через {reset_in} сек.",
                    show_alert=True,
                )
            return None

        # Global limit
        global_key = "rate_limit:global"
        global_allowed, _, _ = await self._check_limit(
            global_key,
            self.config.global_generations_per_minute,
            self.config.window_seconds,
        )

        if not global_allowed:
            logger.warning(
                "⛔ Global rate limit exceeded",
                extra={"type": "global_limit"}
            )
            if isinstance(event, Message):
                await event.answer(
                    "⏳ Сервер перегружен. Попробуйте позже.",
                    show_alert=True,
                )
            return None

        # Добавляем remaining в data для handlers
        data["rate_limit_remaining"] = remaining

        return await handler(event, data)
