# app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session_maker
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency для получения асинхронной сессии БД"""
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
