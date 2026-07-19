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
                FOREIGN KEY (referrer_id) REFERENCES users(user_id)
            )
        """)

        # === ТАБЛИЦА ПОДПИСОК ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT DEFAULT 'free',  -- free, oson, pro, business
                status TEXT DEFAULT 'active',  -- active, expired, cancelled
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
                is_paid INTEGER DEFAULT 0,  -- 0 = free, 1 = paid
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # === ТАБЛИЦА ЛИМИТОВ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS daily_limits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,  -- YYYY-MM-DD
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
                method TEXT,  -- alif, humo, eskhata, crypto, stars
                status TEXT DEFAULT 'pending',  -- pending, completed, failed, refunded
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
                event_type TEXT NOT NULL,  -- start, generate, share, subscribe, etc.
                event_data TEXT,  -- JSON с доп. данными
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # === ТАБЛИЦА КОНТЕНТА ДНЯ ===
        await db.execute("""
            CREATE TABLE IF NOT EXISTS content_of_day (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,  -- YYYY-MM-DD
                niche TEXT,
                hook TEXT,
                content TEXT,
                language TEXT DEFAULT 'ru',
                sent_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # === ТАБЛИЦА НИШ (для админ-панели