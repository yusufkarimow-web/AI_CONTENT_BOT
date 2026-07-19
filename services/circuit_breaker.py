# services/circuit_breaker.py — Circuit Breaker Pattern
# Защита от каскадных отказов при недоступности внешних API (OpenAI, платёжки)

import asyncio
import time
import logging
from enum import Enum
from typing import Optional, Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Состояния Circuit Breaker."""
    CLOSED = "closed"      # Норма — запросы проходят
    OPEN = "open"          # Отказ — запросы блокируются
    HALF_OPEN = "half_open"  # Проверка — пробный запрос


class CircuitBreaker:
    """Circuit Breaker для защиты от каскадных отказов.

    Pattern:
    - CLOSED: запросы проходят, считаем ошибки
    - После N ошибок подряд → OPEN
    - OPEN: запросы мгновенно отклоняются (fallback)
    - Через T секунд → HALF_OPEN (пробный запрос)
    - Если пробный успешен → CLOSED
    - Если пробный провален → OPEN

    Args:
        failure_threshold: Сколько ошибок подряд до OPEN
        recovery_timeout: Секунд до попытки восстановления
        success_threshold: Сколько успехов для закрытия
        name: Имя для логирования
        fallback: Функция-запасной вариант при OPEN
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        success_threshold: int = 3,
        name: str = "default",
        fallback: Optional[Callable] = None,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.name = name
        self.fallback = fallback

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._lock = asyncio.Lock()

    @property
    def state(self) -> CircuitState:
        return self._state

    @property
    def is_closed(self) -> bool:
        return self._state == CircuitState.CLOSED

    @property
    def is_open(self) -> bool:
        return self._state == CircuitState.OPEN

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Выполняет функцию с защитой Circuit Breaker.

        При OPEN state — возвращает fallback или raise CircuitBreakerOpen.
        """
        async with self._lock:
            await self._update_state()

            if self._state == CircuitState.OPEN:
                logger.warning(
                    f"⚡ Circuit [{self.name}] OPEN — запрос отклонён",
                    extra={"circuit": self.name, "state": "open"}
                )
                if self.fallback:
                    return await self.fallback(*args, **kwargs)
                raise CircuitBreakerOpen(f"Circuit {self.name} is OPEN")

            # Пробный запрос в HALF_OPEN
            is_trial = self._state == CircuitState.HALF_OPEN

        # Выполняем запрос (вне lock для параллелизма)
        try:
            result = await func(*args, **kwargs)
            await self._on_success(is_trial)
            return result
        except Exception as e:
            await self._on_failure(is_trial)
            raise

    async def _update_state(self):
        """Обновляет состояние при необходимости."""
        if self._state == CircuitState.OPEN:
            if self._last_failure_time and                (time.time() - self._last_failure_time) >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._success_count = 0
                logger.info(f"⚡ Circuit [{self.name}] → HALF_OPEN (пробуем восстановиться)")

    async def _on_success(self, is_trial: bool):
        """Обработка успешного запроса."""
        async with self._lock:
            if is_trial:
                self._success_count += 1
                if self._success_count >= self.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    logger.info(f"✅ Circuit [{self.name}] → CLOSED (восстановлен)")
            else:
                self._failure_count = 0

    async def _on_failure(self, is_trial: bool):
        """Обработка ошибки."""
        async with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if is_trial or self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.error(
                    f"🔴 Circuit [{self.name}] → OPEN ({self._failure_count} ошибок)",
                    extra={"circuit": self.name, "failures": self._failure_count}
                )

    def __call__(self, func: Callable) -> Callable:
        """Декоратор для обёртки функций."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        return wrapper


class CircuitBreakerOpen(Exception):
    """Исключение при открытом Circuit Breaker."""
    pass
