# database/connection.py — Подключение к базе данных Sozanda
# SQLite для старта, легко мигрировать на PostgreSQL потом

import os
import aiosqlite
from pathlib import Path

from config import DATABASE_URL

# ============================================
# КОНФИГУРАЦИЯ БД
# ============================================

# Путь к файлу БД (по умолчанию в папке проекта)
DEFAULT_DB_PATH = "sozanda.db"

# Извлекаем путь из DATABASE_URL или используем дефолт
if DATABASE_URL and DATABASE_URL.startswith("sqlite:///"):
    DB_PATH = DATABASE_URL.replace("sqlite:///", "")
else:
    DB_PATH = DEFAULT_DB_PATH

# Абсолютный путь
DB_PATH = os.path.abspath(DB_PATH)


# ============================================
# ИНИЦИАЛИЗАЦИЯ БД
# ============================================

async def init_db():
    """Создание таблиц при первом запуске"""

    async with aiosqlite.connect(DB_PATH) as db:
        # Включаем foreign keys
        await db.execute("PRAGMA foreign_keys = ON")

        # === ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'ru',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                referrer_id INTEGER,
                referral_count INTEGER DEFAULT 0,
                referral_bonus_generations INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                is_admin INTEGER DEFAULT 0,
                country TEXT DEFAULT 'uz',
                FOREIGN KEY (referrer_id) REFERENCES users(user_id)
            )
        """)

        # === ТАБЛИЦА ПОДПИСОК ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT DEFAULT 'free',
                status TEXT DEFAULT 'active',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                payment_method TEXT,
                payment_id TEXT,
                amount REAL,
                currency TEXT DEFAULT 'TJS',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # === ТАБЛИЦА ГЕНЕРАЦИЙ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                niche TEXT,
                topic TEXT,
                content_type TEXT DEFAULT 'reels',
                content TEXT,
                language TEXT DEFAULT 'ru',
                is_paid INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # === ТАБЛИЦА ЛИМИТОВ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS daily_limits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                count INTEGER DEFAULT 0,
                limit_value INTEGER DEFAULT 3,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id, date)
            )
        """)

        # === ТАБЛИЦА ПЛАТЕЖЕЙ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'TJS',
                method TEXT,
                status TEXT DEFAULT 'pending',
                transaction_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                confirmed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # === ТАБЛИЦА АНАЛИТИКИ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT NOT NULL,
                event_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # === ТАБЛИЦА КОНТЕНТА ДНЯ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS content_of_day (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                niche TEXT,
                hook TEXT,
                content TEXT,
                language TEXT DEFAULT 'ru',
                sent_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # === ТАБЛИЦА НИШ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS niches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                name_ru TEXT,
                name_tg TEXT,
                icon TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # === ТАБЛИЦА ГЕЙМИФИКАЦИИ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_gamification (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                total_xp INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                streak_days INTEGER DEFAULT 0,
                last_active TIMESTAMP,
                content_generated INTEGER DEFAULT 0,
                reels_generated INTEGER DEFAULT 0,
                posts_generated INTEGER DEFAULT 0,
                stories_generated INTEGER DEFAULT 0,
                referrals_made INTEGER DEFAULT 0,
                unlocked_achievements TEXT DEFAULT '[]'
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT
            )
        """)

        # === ИНДЕКСЫ ===
        await db.execute("CREATE INDEX IF NOT EXISTS idx_generations_user ON generations(user_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_generations_date ON generations(created_at)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_limits_user_date ON daily_limits(user_id, date)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_payments_user ON payments(user_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_analytics_user ON analytics(user_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_analytics_event ON analytics(event_type)")

        await db.commit()

    print(f"✅ База данных инициализирована: {DB_PATH}")


# ============================================
# УТИЛИТЫ ДЛЯ РАБОТЫ С БД
# ============================================

async def get_db():
    """Получить соединение с БД"""

    return await aiosqlite.connect(DB_PATH)


async def execute_query(query: str, params: tuple = ()):
    """Выполнить запрос без возврата данных"""

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(query, params)
        await db.commit()


async def fetch_one(query: str, params: tuple = ()):
    """Получить одну запись"""

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def fetch_all(query: str, params: tuple = ()):
    """Получить все записи"""

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def execute_many(query: str, params_list: list):
    """Выполнить запрос с множественными параметрами"""

    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(query, params_list)
        await db.commit()


# ============================================
# МИГРАЦИИ / ОБНОВЛЕНИЯ
# ============================================

async def run_migrations():
    """Запуск миграций при обновлении бота"""

    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY
                )
            """)
            await db.commit()
        except:
            pass

    print("✅ Миграции выполнены")


# ============================================
# ОЧИСТКА / УТИЛИТЫ
# ============================================

async def cleanup_old_data(days: int = 90):
    """Очистка старых данных"""

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            DELETE FROM analytics
            WHERE created_at < datetime('now', '-{} days')
        """.format(days))

        await db.execute("""
            DELETE FROM daily_limits
            WHERE date < date('now', '-{} days')
        """.format(days))

        await db.commit()

    print(f"✅ Очищены данные старше {days} дней")


async def get_db_stats() -> dict:
    """Получить статистику БД (для админ-панели)"""

    stats = {}

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        stats["total_users"] = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COUNT(DISTINCT user_id) FROM generations
            WHERE date(created_at) = date('now')
        """)
        stats["active_today"] = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM generations")
        stats["total_generations"] = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COUNT(DISTINCT user_id) FROM subscriptions
            WHERE status = 'active' AND expires_at > datetime('now')
        """)
        stats["paid_users"] = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status = 'completed'
        """)
        stats["total_revenue"] = (await cursor.fetchone())[0]

        db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
        stats["db_size_mb"] = round(db_size / (1024 * 1024), 2)

    return stats