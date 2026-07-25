# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field
from typing import Optional, List
import os

class Settings(BaseSettings):
    # ===== BOT & PLATFORM =====
    bot_token: SecretStr = Field(..., description="Telegram Bot Token")
    bot_username: str = Field("tojikai_bot", description="Bot Username")
    public_base_url: str = Field("https://platform.tojikai.app", description="Public Base URL")
    run_mode: str = Field("webhook", description="webhook or polling")
    telegram_webhook_path: str = Field("/webhook/telegram", description="Webhook path")
    telegram_webhook_secret: SecretStr = Field(..., description="Webhook secret token")
    telegram_allowed_updates: List[str] = Field(
        default=["message", "callback_query", "web_app_info"],
        description="Allowed update types"
    )

    # ===== DATABASE =====
    database_url: str = Field(
        "postgresql+asyncpg://tojikai:tojikai_pwd_secure@postgres:5432/tojikai_db",
        description="PostgreSQL async URL"
    )
    redis_url: Optional[str] = Field(
        "redis://redis:6379/0",
        description="Redis connection URL"
    )

    # ===== PAYMENT GATEWAYS =====
    # Click (Uzbekistan)
    click_service_id: str = Field(..., description="Click Service ID")
    click_secret_key: SecretStr = Field(..., description="Click Secret Key")
    click_merchant_id: str = Field(..., description="Click Merchant ID")

    # Payme (Uzbekistan)
    payme_merchant_id: str = Field(..., description="Payme Merchant ID")
    payme_api_key: SecretStr = Field(..., description="Payme API Key")

    # Alif Mobi (Tajikistan)
    alif_merchant_id: str = Field(..., description="Alif Mobi Merchant ID")
    alif_secret_key: SecretStr = Field(..., description="Alif Secret Key")
    alif_api_url: str = Field("https://api.alif.tj", description="Alif API URL")

    # ===== WHATSAPP INTEGRATION =====
    whatsapp_api_provider: str = Field("greenapi", description="greenapi, official, chat-api")
    whatsapp_api_url: str = Field("https://api.green-api.com", description="WhatsApp API URL")
    whatsapp_instance_id: str = Field(..., description="Green API Instance ID")
    whatsapp_api_token: SecretStr = Field(..., description="WhatsApp API Token")

    # ===== AI SERVICES =====
    openai_api_key: SecretStr = Field(..., description="OpenAI API Key for GPT-4o-mini")
    openai_organization: Optional[str] = Field(None, description="OpenAI Organization")
    model_main: str = Field("gpt-4o-mini", description="Main AI Model")
    model_fast: str = Field("gpt-3.5-turbo", description="Fast AI Model")

    # ===== SECURITY =====
    jwt_secret: SecretStr = Field(..., description="JWT Secret Key")
    jwt_algorithm: str = Field("HS256", description="JWT Algorithm")
    jwt_expiration_minutes: int = Field(1440, description="JWT Token Expiration (minutes)")
    refresh_token_expiration_days: int = Field(30, description="Refresh Token Expiration (days)")

    # ===== LOGGING =====
    log_level: str = Field("INFO", description="Logging level")

    # ===== FEATURE FLAGS =====
    enable_empire_game: bool = Field(True, description="Enable TojikAI Empire game")
    enable_marketplace: bool = Field(True, description="Enable Marketplace")
    enable_ai_consultant: bool = Field(True, description="Enable AI Business Consultant")
    enable_analytics: bool = Field(True, description="Enable Analytics Tracking")

    # ===== DEFAULT QUOTAS & PRICING =====
    free_plan_generations_per_month: int = Field(5, description="Free tier monthly generations")
    starter_plan_price_uzs: int = Field(29900, description="Starter plan price in minor units (tiyn)")
    starter_plan_price_tjs: int = Field(2990, description="Starter plan price TJS in minor units")
    pro_plan_price_uzs: int = Field(99900, description="Pro plan price UZS")
    pro_plan_price_tjs: int = Field(9990, description="Pro plan price TJS")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

_settings: Optional[Settings] = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        # For validation / fallback during development, populate some environment variables
        # if not present, to prevent immediate pydantic validation crashes.
        os.environ.setdefault("BOT_TOKEN", "123456:fake_bot_token")
        os.environ.setdefault("TELEGRAM_WEBHOOK_SECRET", "fake_webhook_secret")
        os.environ.setdefault("CLICK_SERVICE_ID", "fake_click_service")
        os.environ.setdefault("CLICK_SECRET_KEY", "fake_click_secret")
        os.environ.setdefault("CLICK_MERCHANT_ID", "fake_click_merchant")
        os.environ.setdefault("PAYME_MERCHANT_ID", "fake_payme_merchant")
        os.environ.setdefault("PAYME_API_KEY", "fake_payme_key")
        os.environ.setdefault("ALIF_MERCHANT_ID", "fake_alif_merchant")
        os.environ.setdefault("ALIF_SECRET_KEY", "fake_alif_secret")
        os.environ.setdefault("WHATSAPP_INSTANCE_ID", "fake_wa_instance")
        os.environ.setdefault("WHATSAPP_API_TOKEN", "fake_wa_token")
        os.environ.setdefault("OPENAI_API_KEY", "fake_openai_key")
        os.environ.setdefault("JWT_SECRET", "fake_jwt_secret_with_32_characters_minimum")
        _settings = Settings()
    return _settings
