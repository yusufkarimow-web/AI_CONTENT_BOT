# middlewares/database_middleware.py — Middleware для предоставления SQLAlchemy db_session

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import os
from config import DATABASE_URL

# Определение пути БД
DEFAULT_DB_PATH = "sozanda.db"
if DATABASE_URL and DATABASE_URL.startswith("sqlite:///"):
    DB_PATH = DATABASE_URL.replace("sqlite:///", "")
else:
    DB_PATH = DEFAULT_DB_PATH
DB_PATH = os.path.abspath(DB_PATH)

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
async_session = async_sessionmaker(engine, expire_on_commit=False)

class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware, который открывает сессию БД SQLAlchemy (async_session)
    и передает её в хэндлеры через параметр db_session.
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session() as session:
            data["db_session"] = session
            return await handler(event, data)
