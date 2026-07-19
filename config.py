# config.py — Конфигурация бота Sozanda v2.0
# Enterprise-ready: Pydantic validation, circuit breaker config, structured logging
# Автор: Sozanda Team
# Цель: Масштабирование до 1M+ пользователей

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from functools import lru_cache
from dotenv import load_dotenv

from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# === ЗАГРУЗКА .ENV ===
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class ConfigError(Exception):
    """Кастомное исключение для ошибок конфигурации.

    Вместо sys.exit(1) — raise ConfigError, который ловится в main()
    и обрабатывается gracefully: логирование, уведомление админов,
    переход в safe mode или graceful shutdown.
    """
    pass


class PaymentConfig(BaseSettings):
    """Конфигурация платёжной системы с валидацией."""
    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    merchant_id: Optional[str] = None
    api_key: Optional[str] = None
    service_id: Optional[str] = None
    secret_key: Optional[str] = None

    @property
    def is_enabled(self) -> bool:
        """Проверяет, достаточно ли данных для активации платёжки."""
        base = bool(self.merchant_id and self.api_key)
        if self.service_id is not None:
            base = base and bool(self.service_id)
        return base

    @property
    def idempotency_key(self) -> str:
        """Генерирует уникальный ключ идемпотентности для каждой операции.

        Предотвращает дублирование транзакций при сетевых ошибках.
        """
        import uuid
        return str(uuid.uuid4())


class RateLimitConfig(BaseSettings):
    """Конфигурация rate limiting с Redis backend."""
    model_config = SettingsConfigDict(env_prefix="RATE_LIMIT_", extra="ignore")

    # Per-user limits (requests per window)
    user_generations_per_minute: int = Field(default=5, ge=1, le=100)
    user_generations_per_hour: int = Field(default=30, ge=1, le=1000)

    # Global limits (все пользователи вместе)
    global_generations_per_minute: int = Field(default=100, ge=10, le=10000)
    global_generations_per_hour: int = Field(default=2000, ge=100, le=100000)

    # Burst allowance (сколько запросов можно сделать мгновенно)
    burst_size: int = Field(default=3, ge=1, le=20)

    # Window size in seconds
    window_seconds: int = Field(default=60, ge=10, le=3600)


class CircuitBreakerConfig(BaseSettings):
    """Circuit Breaker для защиты от каскадных отказов.

    Pattern: CLOSED (норма) -> OPEN (отказ) -> HALF_OPEN (проверка)
    """
    model_config = SettingsConfigDict(env_prefix="CB_", extra="ignore")

    # Сколько ошибок подряд до открытия circuit
    failure_threshold: int = Field(default=5, ge=1, le=20)

    # Сколько секунд ждать перед попыткой восстановления (HALF_OPEN)
    recovery_timeout: int = Field(default=30, ge=5, le=300)

    # Сколько успешных запросов нужно для закрытия circuit
    success_threshold: int = Field(default=3, ge=1, le=10)

    # Fallback: что делать при OPEN state
    fallback_to_cache: bool = Field(default=True)
    fallback_to_local_model: bool = Field(default=False)


class Tariff(BaseSettings):
    """Модель тарифа — в будущем загружается из БД, сейчас — default values."""
    model_config = SettingsConfigDict(extra="ignore")

    name: str
    daily_limit: int = Field(ge=0)
    monthly_limit: int = Field(ge=0)
    price_monthly: int = Field(ge=0)
    price_yearly: int = Field(ge=0)
    features: List[str] = Field(default_factory=list)
    is_active: bool = Field(default=True)

    @property
    def price_per_generation(self) -> float:
        """Стоимость одной генерации для unit-экономики."""
        if self.monthly_limit == 0:
            return 0.0
        return self.price_monthly / self.monthly_limit


class Settings(BaseSettings):
    """Главный класс конфигурации — единая точка правды.

    Все переменные окружения валидируются через Pydantic.
    При ошибке — raise ConfigError с понятным сообщением.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # === CORE ===
    bot_token: str = Field(..., description="Telegram Bot Token от @BotFather")
    bot_username: str = Field(default="sozanda_bot")
    env: str = Field(default="development", pattern=r"^(development|staging|production)$")

    # === ADMIN ===
    admin_ids: str = Field(default="", description="Comma-separated Telegram IDs")
    admin_id: Optional[str] = Field(default=None, description="Single Telegram ID")
    alif_card_number: str = Field(default="4444888811372899", description="Номер карты Alif")
    whatsapp_number: str = Field(default="+992918454323", description="Номер WhatsApp службы поддержки")

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Any) -> str:
        """Принимает сырое значение и возвращает валидированную строку.
        Реальный парсинг в список интов происходит в свойстве admin_ids_list.
        """
        if isinstance(v, list):
            return ",".join(str(x) for x in v)
        if v is None:
            return ""
        return str(v)

    # === DATABASE ===
    database_url: str = Field(default="sqlite:///sozanda.db")

    @field_validator("database_url", mode="after")
    @classmethod
    def validate_database_for_production(cls, v: str, info) -> str:
        """В production SQLite запрещён — raise ConfigError."""
        env = info.data.get("env", "development")
        if env == "production" and "sqlite" in v.lower():
            raise ConfigError(
                "❌ SQLite запрещён в production!\n"
                "   Используй PostgreSQL: DATABASE_URL=postgresql://user:pass@host/db"
            )
        return v

    # === REDIS ===
    redis_url: str = Field(default="redis://localhost:6379/0")

    # === AI ===
    openai_api_key: str = Field(..., description="OpenAI API Key")
    openai_model: str = Field(default="gpt-4o-mini")
    openai_fallback_model: str = Field(default="gpt-3.5-turbo")
    ai_timeout: int = Field(default=60, ge=5, le=300)
    ai_max_retries: int = Field(default=3, ge=0, le=10)

    # === PAYMENTS ===
    alif_merchant_id: Optional[str] = None
    alif_api_key: Optional[str] = None
    humo_merchant_id: Optional[str] = None
    humo_api_key: Optional[str] = None
    click_merchant_id: Optional[str] = None
    click_service_id: Optional[str] = None
    click_secret_key: Optional[str] = None
    payme_merchant_id: Optional[str] = None
    payme_key: Optional[str] = None
    crypto_pay_api_key: Optional[str] = None

    # === LIMITS ===
    free_daily_limit: int = Field(default=3, ge=0, le=100)
    free_monthly_limit: int = Field(default=15, ge=0, le=1000)
    oson_daily_limit: int = Field(default=20, ge=1, le=1000)

    # === REFERRAL ===
    referral_bonus_generations: int = Field(default=5, ge=0)
    referral_bonus_days: int = Field(default=3, ge=0)
    referral_bonus_pro_days: int = Field(default=30, ge=0)

    # === CONTENT ===
    watermark_text: Optional[str] = None
    content_of_the_day_hour: int = Field(default=9, ge=0, le=23)

    # === I18N ===
    default_language: str = Field(default="ru", pattern=r"^(ru|tg|uz)$")

    # === LOGGING ===
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    # === FEATURE FLAGS (для A/B тестов и постепенного rollout) ===
    feature_new_ui: bool = Field(default=False)
    feature_viral_score: bool = Field(default=False)
    feature_visual_gen: bool = Field(default=False)
    feature_competitor_spy: bool = Field(default=False)

    # === CIRCUIT BREAKER ===
    cb_failure_threshold: int = Field(default=5, ge=1, le=20)
    cb_recovery_timeout: int = Field(default=30, ge=5, le=300)
    cb_success_threshold: int = Field(default=3, ge=1, le=10)

    # === RATE LIMITING ===
    rate_limit_user_per_min: int = Field(default=5, ge=1, le=100)
    rate_limit_global_per_min: int = Field(default=100, ge=10, le=10000)

    # === PROPERTIES ===
    @property
    def bot_link(self) -> str:
        return f"https://t.me/{self.bot_username.lstrip('@')}"

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @property
    def is_development(self) -> bool:
        return self.env == "development"

    @property
    def admin_ids_list(self) -> List[int]:
        valid_ids = []
        if self.admin_ids:
            for item in self.admin_ids.split(","):
                item = item.strip()
                if item.isdigit():
                    valid_ids.append(int(item))
        if self.admin_id:
            item = self.admin_id.strip()
            if item.isdigit():
                valid_ids.append(int(item))
        return list(set(valid_ids))

    @property
    def active_payments(self) -> Dict[str, bool]:
        """Список активных платёжных систем."""
        return {
            "alif": bool(self.alif_merchant_id and self.alif_api_key),
            "humo": bool(self.humo_merchant_id and self.humo_api_key),
            "click": bool(self.click_merchant_id and self.click_service_id),
            "payme": bool(self.payme_merchant_id and self.payme_key),
            "crypto": bool(self.crypto_pay_api_key),
        }

    @property
    def tariffs(self) -> Dict[str, Tariff]:
        """Тарифы — в v2.1 будут загружаться из БД с кэшем Redis."""
        return {
            "free": Tariff(
                name="🆓 Free",
                daily_limit=self.free_daily_limit,
                monthly_limit=self.free_monthly_limit,
                price_monthly=0,
                price_yearly=0,
                features=["Базовые ниши", "Водяной знак"],
            ),
            "oson": Tariff(
                name="⚡ Oson",
                daily_limit=self.oson_daily_limit,
                monthly_limit=200,
                price_monthly=50000,
                price_yearly=450000,
                features=["Все ниши", "Без водяного знака", "Приоритетная генерация"],
            ),
            "pro": Tariff(
                name="👑 Pro",
                daily_limit=9999,
                monthly_limit=99999,
                price_monthly=150000,
                price_yearly=1350000,
                features=["Безлимит", "API доступ", "White-label", "Поддержка 24/7"],
            ),
            "business": Tariff(
                name="🏢 Business",
                daily_limit=99999,
                monthly_limit=999999,
                price_monthly=500000,
                price_yearly=4500000,
                features=["Команда до 10 человек", "Реселлерская модель", "Персональный менеджер"],
            ),
        }

    @property
    def watermark(self) -> str:
        if self.watermark_text:
            return self.watermark_text
        return f"💡 Создано ботом @{self.bot_username}\n🚀 AI-контент для бизнеса"

    @property
    def rate_limit_config(self) -> RateLimitConfig:
        return RateLimitConfig(
            user_generations_per_minute=self.rate_limit_user_per_min,
            global_generations_per_minute=self.rate_limit_global_per_min,
        )

    @property
    def circuit_breaker_config(self) -> CircuitBreakerConfig:
        return CircuitBreakerConfig(
            failure_threshold=self.cb_failure_threshold,
            recovery_timeout=self.cb_recovery_timeout,
            success_threshold=self.cb_success_threshold,
        )

    def get_payment_config(self, system: str) -> PaymentConfig:
        """Получает конфигурацию платёжной системы по имени."""
        configs = {
            "alif": PaymentConfig(
                merchant_id=self.alif_merchant_id,
                api_key=self.alif_api_key,
            ),
            "humo": PaymentConfig(
                merchant_id=self.humo_merchant_id,
                api_key=self.humo_api_key,
            ),
            "click": PaymentConfig(
                merchant_id=self.click_merchant_id,
                api_key=self.click_secret_key,
                service_id=self.click_service_id,
            ),
            "payme": PaymentConfig(
                merchant_id=self.payme_merchant_id,
                api_key=self.payme_key,
            ),
            "crypto": PaymentConfig(
                api_key=self.crypto_pay_api_key,
            ),
        }
        return configs.get(system, PaymentConfig())

    def is_feature_enabled(self, feature_name: str, user_id: Optional[int] = None) -> bool:
        """Проверяет, включена ли фича (feature flag).

        В будущем: процентный rollout, A/B тесты по user_id.
        """
        feature_map = {
            "new_ui": self.feature_new_ui,
            "viral_score": self.feature_viral_score,
            "visual_gen": self.feature_visual_gen,
            "competitor_spy": self.feature_competitor_spy,
        }
        return feature_map.get(feature_name, False)

    def get_bot_info(self) -> str:
        """Диагностика конфигурации при старте."""
        active = [k for k, v in self.active_payments.items() if v]
        db_type = "PostgreSQL ✅" if "postgresql" in self.database_url else "SQLite ⚠️"

        return f"""
╔══════════════════════════════════════════╗
║     SOZANDA BOT v2.0 — ДИАГНОСТИКА       ║
╠══════════════════════════════════════════╣
║ Бот: @{self.bot_username}
║ Окружение: {self.env.upper()}
║ Админов: {len(self.admin_ids_list)}
║ БД: {db_type}
║ Redis: {'✅' if self.redis_url else '❌'}
║ AI: {self.openai_model}
║ Платежи: {', '.join(active) if active else '❌ НЕТ'}
║ Языки: ru, tg, uz
║ Тарифы: {len(self.tariffs)}
║ Rate Limit: {self.rate_limit_user_per_min}/min per user
║ Circuit Breaker: {self.cb_failure_threshold} failures / {self.cb_recovery_timeout}s recovery
╚══════════════════════════════════════════╝
"""


# === SINGLETON ===
# Используем lru_cache для singleton pattern — конфиг создаётся один раз
@lru_cache()
def get_settings() -> Settings:
    """Получает singleton-экземпляр настроек.

    При ошибке валидации — raise ConfigError с детальным сообщением.
    """
    try:
        return Settings()
    except ValidationError as e:
        errors = []
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            msg = err["msg"]
            errors.append(f"  • {field}: {msg}")

        raise ConfigError(
            "❌ ОШИБКА КОНФИГУРАЦИИ:\n"
            + "\n".join(errors)
            + "\n\n"
            + "📋 Проверь файл .env и убедись, что все required поля заполнены."
        )


# Глобальный доступ (для обратной совместимости)
settings = get_settings()

# Экспортируем основные переменные для обратной совместимости
TOKEN = settings.bot_token
ADMIN_IDS = settings.admin_ids_list
ADMIN_ID = settings.admin_id
DATABASE_URL = settings.database_url
REDIS_URL = settings.redis_url
OPENAI_API_KEY = settings.openai_api_key
OPENAI_MODEL = settings.openai_model
OPENAI_FALLBACK_MODEL = settings.openai_fallback_model
ALIF_MERCHANT_ID = settings.alif_merchant_id
ALIF_API_KEY = settings.alif_api_key
HUMO_MERCHANT_ID = settings.humo_merchant_id
HUMO_API_KEY = settings.humo_api_key
CLICK_MERCHANT_ID = settings.click_merchant_id
CLICK_SERVICE_ID = settings.click_service_id
CLICK_SECRET_KEY = settings.click_secret_key
PAYME_MERCHANT_ID = settings.payme_merchant_id
PAYME_KEY = settings.payme_key
CRYPTO_PAY_API_KEY = settings.crypto_pay_api_key
FREE_DAILY_LIMIT = settings.free_daily_limit
FREE_MONTHLY_LIMIT = settings.free_monthly_limit
OSON_DAILY_LIMIT = settings.oson_daily_limit
REFERRAL_BONUS_GENERATIONS = settings.referral_bonus_generations
REFERRAL_BONUS_DAYS = settings.referral_bonus_days
REFERRAL_BONUS_PRO_DAYS = settings.referral_bonus_pro_days
WATERMARK_TEXT = settings.watermark
CONTENT_OF_THE_DAY_HOUR = settings.content_of_the_day_hour
DEFAULT_LANGUAGE = settings.default_language
LOG_LEVEL = settings.log_level
AI_TIMEOUT = settings.ai_timeout
AI_MAX_RETRIES = settings.ai_max_retries
BOT_NAME = "Sozanda"
BOT_USERNAME = settings.bot_username
BOT_LINK = settings.bot_link
TARIFFS = settings.tariffs
ACTIVE_PAYMENTS = settings.active_payments

ALIF_ENABLED = settings.active_payments["alif"]
HUMO_ENABLED = settings.active_payments["humo"]
CRYPTO_PAY_ENABLED = settings.active_payments["crypto"]

ALIF_CARD_NUMBER = settings.alif_card_number
WHATSAPP_NUMBER = settings.whatsapp_number

# Константы
SUPPORTED_LANGUAGES = ["ru", "tg", "uz"]
AVAILABLE_NICHES = [
    "cafe", "beauty", "shop", "barber", "wedding",
    "education", "religious", "fitness", "auto", "other",
]
TRENDING_NICHES = ["cafe", "beauty", "wedding", "shop"]
CONTENT_TYPES = {
    "post": "📄 Пост для Instagram",
    "reels": "🎬 Reels / Видео",
    "stories": "📸 Stories",
    "ideas": "💡 Идеи для контента",
    "hook": "⚡ Вирусный хук",
    "caption": "📝 Подпись (caption)",
    "script": "📋 Сценарий для видео",
    "hashtags": "🏷️ Подбор хештегов",
}

# Реферальные уровни — формула вместо magic numbers
# days = base * (referrals ^ factor), где base=1, factor=0.6
# Это даёт: 1→1, 3→2, 5→3, 10→4, 25→6, 50→8 (approx)
# Но мы используем ступенчатую систему для ясности
REFERRAL_LEVELS = {
    1: {"bonus": 5, "type": "generations", "description": "1 друг = 5 бонусных генераций"},
    3: {"bonus": 3, "type": "days_oson", "description": "3 друга = 3 дня Oson"},
    5: {"bonus": 7, "type": "days_oson", "description": "5 друзей = 7 дней Oson"},
    10: {"bonus": 30, "type": "days_pro", "description": "10 друзей = 30 дней Pro"},
    25: {"bonus": 90, "type": "days_pro", "description": "25 друзей = 90 дней Pro"},
    50: {"bonus": 365, "type": "days_pro", "description": "50 друзей = 1 год Pro"},
}

# Обратная совместимость
OSON_DAILY_LIMIT = TARIFFS["oson"].daily_limit
PRO_DAILY_LIMIT = TARIFFS["pro"].daily_limit


if __name__ == "__main__":
    print(settings.get_bot_info())
