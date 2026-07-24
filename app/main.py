# app/main.py
import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import AsyncSession
import time
import os

from app.core.config import get_settings
from app.db.connection import get_db_connection
from app.db.session import get_db_session
from app.bot.handlers import router as bot_router
from app.api.routes import router as api_router
from app.api.payments import router as payments_router

logger = structlog.get_logger(__name__)

settings = get_settings()

# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""

    # Startup
    logger.info("application_starting")

    db_connection = await get_db_connection()

    # Инициализация Telegram Bot
    bot = Bot(token=settings.bot_token.get_secret_value())
    storage = RedisStorage.from_url(settings.redis_url) if settings.redis_url else None
    dp = Dispatcher(storage=storage)
    dp.include_router(bot_router)

    app.state.bot = bot
    app.state.dp = dp
    app.state.storage = storage

    if settings.run_mode == "webhook":
        webhook_url = f"{settings.public_base_url}{settings.telegram_webhook_path}"
        await bot.set_webhook(
            url=webhook_url,
            secret_token=settings.telegram_webhook_secret.get_secret_value(),
            allowed_updates=settings.telegram_allowed_updates
        )
        logger.info("telegram_webhook_configured", url=webhook_url)

    logger.info(
        "application_started",
        version="4.0",
        run_mode=settings.run_mode,
        database="postgresql",
        cache="redis"
    )

    yield

    # Shutdown
    logger.info("application_shutting_down")
    await db_connection.dispose()
    await bot.session.close()
    if storage:
        await storage.close()
    logger.info("application_stopped")


# ============================================================================
# APPLICATION FACTORY
# ============================================================================

def create_app() -> FastAPI:
    """Создание FastAPI приложения"""

    app = FastAPI(
        title="TojikAI SMM Platform",
        description="Professional SMM Content Generation & Gamification Platform",
        version="4.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )

    # ===== MIDDLEWARE (Security First) =====

    # GZIP compression
    app.add_middleware(GZIPMiddleware, minimum_size=1000)

    # Trusted hosts (prevent host header attacks)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["platform.tojikai.app", "api.tojikai.app", "*.tojikai.app", "localhost", "127.0.0.1"]
    )

    # CORS (Allow only Telegram)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://web.telegram.org",
            "https://t.me",
            "http://localhost:3000"  # For development
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware for rate limiting and request logging
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        """Rate limiting и логирование запросов"""

        start_time = time.time()

        # Логирование входящего запроса
        logger.info(
            "http_request_received",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "unknown"
        )

        response = await call_next(request)

        # Логирование ответа
        process_time = time.time() - start_time
        logger.info(
            "http_response_sent",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time * 1000)
        )

        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Powered-By"] = "TojikAI v4.0"

        return response

    # ===== STATIC FILES =====
    app.mount(
        "/static",
        StaticFiles(directory="app/static", html=True),
        name="static"
    )

    # ===== API ROUTES =====
    app.include_router(api_router)
    app.include_router(payments_router)

    # ===== TELEGRAM WEBHOOK =====

    @app.post(settings.telegram_webhook_path)
    async def telegram_webhook(request: Request):
        """Telegram Bot API webhook handler"""

        # Verify webhook secret
        secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if not secret_header or secret_header != settings.telegram_webhook_secret.get_secret_value():
            logger.warning("invalid_webhook_secret")
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})

        try:
            update_data = await request.json()
            update = types.Update(**update_data)

            # Re-use global bot & dispatcher from application state
            bot = request.app.state.bot
            dp = request.app.state.dp

            await dp.feed_update(bot, update)

            logger.info("webhook_update_processed", update_id=update.update_id)

        except Exception as e:
            logger.exception("webhook_error", error=str(e))
            return JSONResponse(status_code=500, content={"error": "Internal server error"})

        return {"ok": True}

    # ===== HEALTH CHECKS =====

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "tojikai_smm_saas",
            "version": "4.0",
            "timestamp": time.time()
        }

    @app.get("/api/version")
    async def version_check():
        """API version endpoint"""
        return {
            "api_version": "4.0.0",
            "build": os.getenv("BUILD_ID", "development"),
            "features": {
                "smm_generation": True,
                "empire_game": settings.enable_empire_game,
                "ai_consultant": settings.enable_ai_consultant,
                "marketplace": settings.enable_marketplace,
                "analytics": settings.enable_analytics,
                "white_label": True
            }
        }

    # ===== ERROR HANDLERS =====

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler"""
        logger.exception("unhandled_exception", error=str(exc), path=request.url.path)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "Something went wrong. Please try again later."
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """HTTP exception handler"""
        logger.warning(
            "http_exception",
            status_code=exc.status_code,
            detail=exc.detail,
            path=request.url.path
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    return app


# ===== APPLICATION INSTANCE =====

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.run_mode == "development",
        log_level=settings.log_level.lower()
    )
