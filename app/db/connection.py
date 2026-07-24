# app/db/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import get_settings
import structlog

logger = structlog.get_logger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.engine = None
        self.async_session_maker = None

    async def initialize(self):
        """Инициализация асинхронного движка и сессий"""
        settings = get_settings()

        self.engine = create_async_engine(
            settings.database_url,
            echo=False,  # Set to True for SQL debugging
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=40,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

        logger.info("database_initialized", pool_size=20, max_overflow=40)

    async def dispose(self):
        """Закрытие подключений к БД"""
        if self.engine:
            await self.engine.dispose()
            logger.info("database_disposed")

    async def create_tables(self):
        """Создание всех таблиц (для первого запуска)"""
        from app.db.models import Base

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("database_tables_created")

    def get_session_maker(self):
        """Получение фабрики сессий"""
        return self.async_session_maker

_db_connection: DatabaseConnection | None = None

async def get_db_connection() -> DatabaseConnection:
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
        await _db_connection.initialize()
    return _db_connection

def get_session_maker() -> async_sessionmaker:
    global _db_connection
    if _db_connection is None:
        # Fallback to sync instantiation during imports or bootstrap if needed
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If the loop is already running, we shouldn't block, but can schedule init
            _db_connection = DatabaseConnection()
            # Inline initialization block since loop is active
            _db_connection.engine = create_async_engine(
                get_settings().database_url,
                echo=False,
                poolclass=QueuePool,
                pool_size=20,
                max_overflow=40,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            _db_connection.async_session_maker = async_sessionmaker(
                _db_connection.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )
        else:
            loop.run_until_complete(get_db_connection())

    return _db_connection.get_session_maker()
