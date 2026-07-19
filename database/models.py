# database/models.py — Модели и функции для работы с БД Sozanda

from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

from database.connection import fetch_one, fetch_all, execute_query

from sqlalchemy import Column, Integer, String, DateTime, Text, select, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserGamification(Base):
    __tablename__ = 'user_gamification'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    total_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    streak_days = Column(Integer, default=0)
    last_active = Column(DateTime, nullable=True)
    content_generated = Column(Integer, default=0)
    reels_generated = Column(Integer, default=0)
    posts_generated = Column(Integer, default=0)
    stories_generated = Column(Integer, default=0)
    referrals_made = Column(Integer, default=0)
    _unlocked_achievements = Column("unlocked_achievements", Text, default="[]")

    @property
    def unlocked_achievements(self) -> list:
        import json
        try:
            return json.loads(self._unlocked_achievements or "[]")
        except:
            return []

    @unlocked_achievements.setter
    def unlocked_achievements(self, value: list):
        import json
        self._unlocked_achievements = json.dumps(value)

class LeaderboardCache(Base):
    __tablename__ = 'leaderboard_cache'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Text)


# ============================================
# ПОЛЬЗОВАТЕЛИ
# ============================================

async def get_or_create_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    referrer_id: Optional[int] = None
) -> Dict[str, Any]:
    """Получить или создать пользователя"""

    user = await fetch_one(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    if user:
        await execute_query("""
            UPDATE users
            SET username = COALESCE(?, username),
                first_name = COALESCE(?, first_name),
                last_name = COALESCE(?, last_name),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (username, first_name, last_name, user_id))
        return await fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))

    await execute_query("""
        INSERT INTO users (user_id, username, first_name, last_name, referrer_id)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, first_name, last_name, referrer_id))

    if referrer_id:
        await execute_query("""
            UPDATE users
            SET referral_count = referral_count + 1
            WHERE user_id = ?
        """, (referrer_id,))

    return await fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Получить пользователя по ID"""
    return await fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))


async def update_user_language(user_id: int, language: str):
    """Обновить язык пользователя"""
    await execute_query("""
        UPDATE users SET language = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (language, user_id))


async def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Получить статистику пользователя"""

    user = await get_user(user_id)
    if not user:
        return {}

    today_count = await fetch_one("""
        SELECT COUNT(*) as count FROM generations
        WHERE user_id = ? AND date(created_at) = date('now')
    """, (user_id,))

    total_count = await fetch_one("""
        SELECT COUNT(*) as count FROM generations WHERE user_id = ?
    """, (user_id,))

    sub = await get_user_subscription(user_id)

    daily_limit = 3
    if sub and sub.get("plan") == "oson":
        daily_limit = 20
    elif sub and sub.get("plan") in ("pro", "business"):
        daily_limit = 9999

    return {
        "user_id": user_id,
        "username": user.get("username"),
        "language": user.get("language", "ru"),
        "created_at": user.get("created_at"),
        "referral_count": user.get("referral_count", 0),
        "referral_bonus": user.get("referral_bonus_generations", 0),
        "today_count": today_count["count"] if today_count else 0,
        "total_count": total_count["count"] if total_count else 0,
        "daily_limit": daily_limit,
        "plan": sub.get("plan", "free") if sub else "free",
    }


# ============================================
# ЛИМИТЫ ГЕНЕРАЦИЙ
# ============================================

async def check_daily_limit(user_id: int) -> tuple:
    """Проверить лимит генераций. Возвращает (can_generate, info)"""
    from config import ADMIN_ID
    if str(user_id) == str(ADMIN_ID):
        return True, {
            "count": 0,
            "limit": 99999,
            "remaining": 99999,
            "can_generate": True
        }

    today = date.today().isoformat()

    limit_record = await fetch_one("""
        SELECT * FROM daily_limits WHERE user_id = ? AND date = ?
    """, (user_id, today))

    if not limit_record:
        sub = await get_user_subscription(user_id)
        limit_value = 3

        if sub:
            if sub.get("plan") == "oson":
                limit_value = 20
            elif sub.get("plan") in ("pro", "business"):
                limit_value = 9999

        user = await get_user(user_id)
        bonus = user.get("referral_bonus_generations", 0) if user else 0

        await execute_query("""
            INSERT INTO daily_limits (user_id, date, count, limit_value)
            VALUES (?, ?, 0, ?)
        """, (user_id, today, limit_value + bonus))

        limit_record = {"count": 0, "limit_value": limit_value + bonus}

    count = limit_record.get("count", 0)
    limit = limit_record.get("limit_value", 3)
    remaining = max(0, limit - count)

    return (remaining > 0), {
        "count": count,
        "limit": limit,
        "remaining": remaining,
        "can_generate": remaining > 0
    }


async def increment_generation(user_id: int):
    """Увеличить счётчик генераций за сегодня"""
    today = date.today().isoformat()
    await execute_query("""
        UPDATE daily_limits
        SET count = count + 1
        WHERE user_id = ? AND date = ?
    """, (user_id, today))


# ============================================
# БИЗНЕС ИМПЕРИЯ (БИЗНЕС-КВИЗ И СИМУЛЯТОР)
# ============================================

async def get_or_create_business_empire(user_id: int, username: Optional[str] = None) -> Dict[str, Any]:
    """Получить или создать профиль в Бизнес Империи"""
    row = await fetch_one("SELECT * FROM user_business_empire WHERE user_id = ?", (user_id,))
    if row:
        return row

    await execute_query("""
        INSERT INTO user_business_empire (user_id, username, balance, clients, employees, level, xp, businesses)
        VALUES (?, ?, 1000, 0, 0, 1, 0, '[]')
    """, (user_id, username))

    return {
        "user_id": user_id,
        "username": username,
        "balance": 1000,
        "clients": 0,
        "employees": 0,
        "level": 1,
        "xp": 0,
        "businesses": "[]"
    }


async def update_business_empire(
    user_id: int,
    balance: int,
    clients: int,
    employees: int,
    level: int,
    xp: int,
    businesses: str
):
    """Обновить состояние империи пользователя"""
    await execute_query("""
        UPDATE user_business_empire
        SET balance = ?, clients = ?, employees = ?, level = ?, xp = ?, businesses = ?
        WHERE user_id = ?
    """, (balance, clients, employees, level, xp, businesses, user_id))


async def get_business_empire_leaderboard(limit: int = 10) -> List[Dict[str, Any]]:
    """Получить топ игроков Бизнес Империи"""
    return await fetch_all("""
        SELECT * FROM user_business_empire
        ORDER BY level DESC, xp DESC, balance DESC
        LIMIT ?
    """, (limit,))


async def add_bonus_generation(user_id: int, bonus: int):
    """Добавить бонусные генерации"""
    today = date.today().isoformat()
    await execute_query("""
        UPDATE daily_limits
        SET limit_value = limit_value + ?
        WHERE user_id = ? AND date = ?
    """, (bonus, user_id, today))
    await execute_query("""
        UPDATE users
        SET referral_bonus_generations = referral_bonus_generations + ?
        WHERE user_id = ?
    """, (bonus, user_id))


# ============================================
# ГЕНЕРАЦИИ (ИСТОРИЯ)
# ============================================

async def save_generation(
    user_id: int,
    niche: str,
    topic: str,
    content: str,
    content_type: str = "reels",
    language: str = "ru",
    is_paid: bool = False
):
    """Сохранить генерацию в историю"""
    await execute_query("""
        INSERT INTO generations (user_id, niche, topic, content, content_type, language, is_paid)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, niche, topic, content, content_type, language, int(is_paid)))


async def get_generation_history(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Получить историю генераций"""
    return await fetch_all("""
        SELECT * FROM generations
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))


async def get_generation_by_id(generation_id: int) -> Optional[Dict[str, Any]]:
    """Получить конкретную генерацию"""
    return await fetch_one("SELECT * FROM generations WHERE id = ?", (generation_id,))


# ============================================
# ПОДПИСКИ
# ============================================

async def get_user_subscription(user_id: int) -> Optional[Dict[str, Any]]:
    """Получить активную подписку"""
    return await fetch_one("""
        SELECT * FROM subscriptions
        WHERE user_id = ? AND status = 'active' AND expires_at > datetime('now')
        ORDER BY expires_at DESC
        LIMIT 1
    """, (user_id,))


async def create_subscription(
    user_id: int,
    plan: str,
    duration_days: int,
    payment_method: str,
    amount: float,
    payment_id: Optional[str] = None
):
    """Создать подписку"""
    expires = datetime.now() + timedelta(days=duration_days)
    await execute_query("""
        UPDATE subscriptions SET status = 'expired'
        WHERE user_id = ? AND status = 'active'
    """, (user_id,))
    await execute_query("""
        INSERT INTO subscriptions (user_id, plan, expires_at, payment_method, amount, payment_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, plan, expires, payment_method, amount, payment_id))


async def cancel_subscription(user_id: int):
    """Отменить подписку"""
    await execute_query("""
        UPDATE subscriptions
        SET status = 'cancelled'
        WHERE user_id = ? AND status = 'active'
    """, (user_id,))


# ============================================
# РЕФЕРАЛЬНАЯ СИСТЕМА
# ============================================

async def get_referral_count(user_id: int) -> int:
    """Количество рефералов пользователя"""
    user = await get_user(user_id)
    if user:
        return user.get("referral_count", 0)
    return 0


async def add_referral_bonus(user_id: int, bonus_generations: int):
    """Начислить бонус за реферала"""
    await execute_query("""
        UPDATE users
        SET referral_bonus_generations = referral_bonus_generations + ?,
            referral_count = referral_count + 1
        WHERE user_id = ?
    """, (bonus_generations, user_id))


async def get_referral_link(user_id: int) -> str:
    """Реферальная ссылка"""
    from config import BOT_LINK
    return f"{BOT_LINK}?start=ref{user_id}"


async def get_top_referrers(limit: int = 5) -> list:
    """Топ рефоводов"""
    rows = await fetch_all("""
        SELECT user_id, username, first_name, referral_count
        FROM users
        WHERE referral_count > 0
        ORDER BY referral_count DESC
        LIMIT ?
    """, (limit,))

    result = []
    for row in rows:
        name = row.get("first_name") or row.get("username") or f"User_{row['user_id']}"
        result.append({
            "user_id": row["user_id"],
            "name": name,
            "ref_count": row.get("referral_count", 0)
        })
    return result


# ============================================
# ПЛАТЕЖИ
# ============================================

async def create_payment(
    user_id: int,
    plan: str,
    amount: float,
    method: str,
    currency: str = "TJS"
) -> int:
    """Создать запись о платеже"""
    await execute_query("""
        INSERT INTO payments (user_id, plan, amount, method, currency, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    """, (user_id, plan, amount, method, currency))
    result = await fetch_one("SELECT last_insert_rowid() as id")
    return result["id"] if result else 0


async def confirm_payment(payment_id: int, transaction_id: Optional[str] = None):
    """Подтвердить платёж"""
    await execute_query("""
        UPDATE payments
        SET status = 'completed', confirmed_at = CURRENT_TIMESTAMP, transaction_id = ?
        WHERE id = ?
    """, (transaction_id, payment_id))

    payment = await fetch_one("SELECT * FROM payments WHERE id = ?", (payment_id,))
    if payment:
        plan_durations = {"oson": 30, "pro": 30, "business": 30}
        duration = plan_durations.get(payment["plan"], 30)
        await create_subscription(
            user_id=payment["user_id"],
            plan=payment["plan"],
            duration_days=duration,
            payment_method=payment["method"],
            amount=payment["amount"],
            payment_id=str(payment_id)
        )


async def get_pending_payments() -> List[Dict[str, Any]]:
    """Ожидающие платежи"""
    return await fetch_all("""
        SELECT p.*, u.username, u.first_name
        FROM payments p
        JOIN users u ON p.user_id = u.user_id
        WHERE p.status = 'pending'
        ORDER BY p.created_at DESC
    """)


# ============================================
# АНАЛИТИКА
# ============================================

async def log_event(user_id: int, event_type: str, event_data: Optional[str] = None):
    """Записать событие"""
    await execute_query("""
        INSERT INTO analytics (user_id, event_type, event_data)
        VALUES (?, ?, ?)
    """, (user_id, event_type, event_data))


async def get_analytics_summary(days: int = 7) -> Dict[str, Any]:
    """Сводка аналитики"""
    events = await fetch_all("""
        SELECT event_type, COUNT(*) as count
        FROM analytics
        WHERE created_at >= datetime('now', '-{} days')
        GROUP BY event_type
    """.format(days))

    active_users = await fetch_one("""
        SELECT COUNT(DISTINCT user_id) as count
        FROM analytics
        WHERE created_at >= datetime('now', '-{} days')
    """.format(days))

    new_users = await fetch_one("""
        SELECT COUNT(*) as count FROM users
        WHERE created_at >= datetime('now', '-{} days')
    """.format(days))

    return {
        "events": {e["event_type"]: e["count"] for e in events},
        "active_users": active_users["count"] if active_users else 0,
        "new_users": new_users["count"] if new_users else 0,
    }


# ============================================
# КОНТЕНТ ДНЯ
# ============================================

async def save_content_of_day(
    content: str,
    niche: str,
    hook: str,
    language: str = "ru"
):
    """Сохранить контент дня"""
    today = date.today().isoformat()
    await execute_query("""
        INSERT OR REPLACE INTO content_of_day (date, niche, hook, content, language)
        VALUES (?, ?, ?, ?, ?)
    """, (today, niche, hook, content, language))


async def get_content_of_day(today_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Получить контент дня"""
    today = today_date or date.today().isoformat()
    return await fetch_one("SELECT * FROM content_of_day WHERE date = ?", (today,))


async def increment_content_sent(content_id: int):
    """Увеличить счётчик отправок"""
    await execute_query("""
        UPDATE content_of_day SET sent_count = sent_count + 1 WHERE id = ?
    """, (content_id,))


# ============================================
# НИШИ
# ============================================

async def get_all_niches() -> List[Dict[str, Any]]:
    """Все активные ниши"""
    return await fetch_all("""
        SELECT * FROM niches WHERE is_active = 1 ORDER BY key
    """)


async def add_niche(key: str, name_ru: str, name_tg: str, icon: str = ""):
    """Добавить нишу"""
    await execute_query("""
        INSERT OR REPLACE INTO niches (key, name_ru, name_tg, icon, is_active)
        VALUES (?, ?, ?, ?, 1)
    """, (key, name_ru, name_tg, icon))


async def deactivate_niche(key: str):
    """Деактивировать нишу"""
    await execute_query("UPDATE niches SET is_active = 0 WHERE key = ?", (key,))


# ============================================
# АДМИН ФУНКЦИИ
# ============================================

async def get_all_users_count() -> int:
    """Всего пользователей"""
    result = await fetch_one("SELECT COUNT(*) as count FROM users")
    return result["count"] if result else 0


async def get_today_generations_count() -> int:
    """Генераций сегодня"""
    result = await fetch_one("""
        SELECT COUNT(*) as count FROM generations
        WHERE date(created_at) = date('now')
    """)
    return result["count"] if result else 0


async def get_paid_users_count() -> int:
    """Платных подписчиков"""
    result = await fetch_one("""
        SELECT COUNT(DISTINCT user_id) as count FROM subscriptions
        WHERE status = 'active' AND expires_at > datetime('now')
    """)
    return result["count"] if result else 0


async def get_total_revenue() -> float:
    """Общая выручка"""
    result = await fetch_one("""
        SELECT COALESCE(SUM(amount), 0) as total FROM payments WHERE status = 'completed'
    """)
    return result["total"] if result else 0.0
async def update_user_country(user_id: int, country: str):
    """Обновляет страну пользователя в базе данных"""
    await execute_query("""
        UPDATE users SET country = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (country, user_id))


async def get_user_language(user_id: int) -> Optional[str]:
    """Возвращает язык пользователя"""
    user = await get_user(user_id)
    if user:
        return user.get("language", "ru")
    return "ru"


async def get_or_create_gamification(user_id: int, username: Optional[str] = None) -> Dict[str, Any]:
    row = await fetch_one("SELECT * FROM user_gamification WHERE user_id = ?", (user_id,))
    if row:
        return row
    await execute_query("""
        INSERT INTO user_gamification (user_id, username, total_xp, current_level)
        VALUES (?, ?, 0, 1)
    """, (user_id, username))
    return {"user_id": user_id, "username": username, "total_xp": 0, "current_level": 1}


async def update_user_xp(user_id: int, xp_amount: int):
    await get_or_create_gamification(user_id)
    await execute_query("""
        UPDATE user_gamification
        SET total_xp = total_xp + ?,
            current_level = (total_xp + ?) / 100 + 1
        WHERE user_id = ?
    """, (xp_amount, xp_amount, user_id))


async def freeze_or_decrement_limit(user_id: int):
    """Снизить лимит на 1 в качестве штрафа"""
    today = date.today().isoformat()
    await execute_query("""
        UPDATE daily_limits
        SET count = count + 1
        WHERE user_id = ? AND date = ?
    """, (user_id, today))