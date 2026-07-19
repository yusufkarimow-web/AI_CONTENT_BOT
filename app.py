# app.py — Sozanda Bot (Strict content_engine imports only, no handlers folder)
import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем настройки, лимиты и токен
from config import TOKEN, settings

# Импортируем инициализацию базы данных
from database.connection import init_db

# Импортируем мидлвари
from middlewares import (
    I18nMiddleware,
    SubscriptionCheckMiddleware,
    AnalyticsMiddleware,
)

# Импортируем планировщик
from services.scheduler import start_scheduler, stop_scheduler

# Импортируем роутеры СТРОГО из content_engine
from content_engine.start import router as start_router
from content_engine.menu import router as menu_router
from content_engine.subscription import router as subscription_router

# ============ ЛОГИРОВАНИЕ ============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


# ============================================
# ИНИЦИАЛИЗАЦИЯ ДИСПЕТЧЕРА И БОТА
# ============================================
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ============ БОТ ============
async def main():
    logger.info("🚀 Запуск нового самодостаточного бота Sozanda...")

    # 1. Инициализация базы данных
    await init_db()

    # Запуск диагностики OpenAI API
    from services.openai_service import test_connection
    logger.info("🔍 Запуск диагностики OpenAI API...")
    test_connection()

    if not TOKEN:
        logger.error("❌ ОШИБКА: Не указан BOT_TOKEN!")
        return

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    try:
        bot_info = await bot.get_me()
        logger.info(f"🤖 Бот @{bot_info.username} подключен")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")
        return

    # Регистрация роутеров подписок, меню и старта из content_engine
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(subscription_router)

    # 2. Регистрация мидлварей
    dp.message.middleware(AnalyticsMiddleware())
    dp.callback_query.middleware(AnalyticsMiddleware())

    dp.message.middleware(I18nMiddleware())
    dp.callback_query.middleware(I18nMiddleware())

    dp.message.middleware(SubscriptionCheckMiddleware())
    dp.callback_query.middleware(SubscriptionCheckMiddleware())

    # 3. Запуск планировщика задач
    asyncio.create_task(start_scheduler(bot))

    logger.info("=" * 50)
    logger.info("✅ БОТ ГОТОВ К РАБОТЕ")
    logger.info("=" * 50)

    try:
        await dp.start_polling(bot)
    finally:
        await stop_scheduler()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен")
    except Exception as e:
        logger.critical(f"❌ ОШИБКА: {e}")
