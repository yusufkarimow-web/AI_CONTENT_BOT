# services/metrics.py — Prometheus Metrics Collection
# Мониторинг производительности и бизнес-метрик

import time
import logging
from typing import Optional, Dict
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Сбор метрик для Prometheus/Grafana.

    Метрики:
    - generations_total (counter): Всего генераций
    - generation_duration_seconds (histogram): Время генерации
    - errors_total (counter): Всего ошибок
    - active_users (gauge): Активные пользователи
    - payments_total (counter): Всего платежей
    - revenue_total (counter): Общая выручка
    """

    def __init__(self):
        self._metrics: Dict[str, any] = {}
        self._initialize_metrics()

    def _initialize_metrics(self):
        """Инициализация метрик (в production — используем prometheus_client)."""
        try:
            from prometheus_client import Counter, Histogram, Gauge, start_http_server

            self._metrics["generations_total"] = Counter(
                "sozanda_generations_total",
                "Total content generations",
                ["type", "niche", "tariff"]
            )
            self._metrics["generation_duration"] = Histogram(
                "sozanda_generation_duration_seconds",
                "Content generation duration",
                ["type"]
            )
            self._metrics["errors_total"] = Counter(
                "sozanda_errors_total",
                "Total errors",
                ["type", "handler"]
            )
            self._metrics["active_users"] = Gauge(
                "sozanda_active_users",
                "Currently active users"
            )
            self._metrics["payments_total"] = Counter(
                "sozanda_payments_total",
                "Total payments",
                ["system", "tariff", "status"]
            )
            self._metrics["revenue_total"] = Counter(
                "sozanda_revenue_total",
                "Total revenue in somoni",
                ["system"]
            )

            # Запускаем HTTP сервер для Prometheus scraping
            start_http_server(9090)
            logger.info("✅ Prometheus metrics server запущен на :9090")

        except ImportError:
            logger.warning("⚠️ prometheus_client не установлен, используем in-memory metrics")
            self._metrics = {}

    def record_generation(self, content_type: str, niche: str, tariff: str, duration: float):
        """Записывает метрику генерации."""
        if "generations_total" in self._metrics:
            self._metrics["generations_total"].labels(
                type=content_type, niche=niche, tariff=tariff
            ).inc()
        if "generation_duration" in self._metrics:
            self._metrics["generation_duration"].labels(type=content_type).observe(duration)

        logger.info(
            f"📊 Generation: {content_type}/{niche}/{tariff} in {duration:.2f}s",
            extra={"metric": "generation", "duration": duration}
        )

    def record_error(self, error_type: str, handler: str):
        """Записывает метрику ошибки."""
        if "errors_total" in self._metrics:
            self._metrics["errors_total"].labels(type=error_type, handler=handler).inc()

        logger.error(
            f"📊 Error: {error_type} in {handler}",
            extra={"metric": "error", "error_type": error_type, "handler": handler}
        )

    def record_payment(self, system: str, tariff: str, amount: int, status: str = "success"):
        """Записывает метрику платежа."""
        if "payments_total" in self._metrics:
            self._metrics["payments_total"].labels(
                system=system, tariff=tariff, status=status
            ).inc()
        if "revenue_total" in self._metrics:
            self._metrics["revenue_total"].labels(system=system).inc(amount)

        logger.info(
            f"📊 Payment: {system}/{tariff}/{amount} somoni ({status})",
            extra={"metric": "payment", "amount": amount, "status": status}
        )

    def set_active_users(self, count: int):
        """Устанавливает количество активных пользователей."""
        if "active_users" in self._metrics:
            self._metrics["active_users"].set(count)

    @contextmanager
    def generation_timer(self, content_type: str):
        """Контекстный менеджер для измерения времени генерации."""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            if "generation_duration" in self._metrics:
                self._metrics["generation_duration"].labels(type=content_type).observe(duration)
