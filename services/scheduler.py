# services/scheduler.py — Планировщик задач Sozanda
# Ежедневный контент, напоминания, челленджи, рассылки

import asyncio
import random
from datetime import datetime, timedelta, time as dt_time
from typing import Optional, List, Dict, Any

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CONTENT_OF_THE_DAY_HOUR, ADMIN_IDS
from database.models import (
    get_user, get_all_users_count, log_event,
    save_content_of_day, get_content_of_day, increment_content_sent,
    get_generation_history, check_daily_limit
)
#from services.ai_generator import generate_content_of_day as generate_daily_content
from content_engine.niche_manager import get_all_niches


# ============================================
# ГЛОБАЛЬНЫЕ ЗАДАЧИ (храним ссылки для отмены)
# ============================================

scheduled_tasks: List[asyncio.Task] = []


# ============================================
# ЗАПУСК ПЛАНИРОВЩИКА
# ============================================

async def start_scheduler(bot: Bot):
    """Запуск всех фоновых задач"""

    print("⏰ Запуск планировщика...")

    # Очищаем старые задачи
    for task in scheduled_tasks:
        if not task.done():
            task.cancel()
    scheduled_tasks.clear()

    # Задача 1: Контент дня (каждый день в 9:00)
    task1 = asyncio.create_task(_content_of_day_loop(bot))
    scheduled_tasks.append(task1)

    # Задача 2: Напоминания неактивным (каждые 3 дня в 18:00)
    task2 = asyncio.create_task(_inactive_reminder_loop(bot))
    scheduled_tasks.append(task2)

    # Задача 3: Челленджи (каждый понедельник в 8:00)
    task3 = asyncio.create_task(_weekly_challenge_loop(bot))
    scheduled_tasks.append(task3)

    # Задача 4: Топ рефоводов (каждое 1-е число в 10:00)
    task4 = asyncio.create_task(_monthly_top_referrers_loop(bot))
    scheduled_tasks.append(task4)

    # Задача 5: Очистка старых данных (каждое воскресенье в 3:00)
    task5 = asyncio.create_task(_cleanup_loop(bot))
    scheduled_tasks.append(task5)

    print(f"✅ Планировщик запущен. Активных задач: {len(scheduled_tasks)}")


# ============================================
# 1. КОНТЕНТ ДНЯ (ежедневно в 9:00)
# ============================================

async def _content_of_day_loop(bot: Bot):
    """Цикл отправки контента дня"""

    while True:
        now = datetime.now()
        target = datetime.combine(now.date(), dt_time(hour=CONTENT_OF_THE_DAY_HOUR))

        # Если время уже прошло — на завтра
        if now >= target:
            target += timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        print(f"⏳ Контент дня через {wait_seconds / 3600:.1f} часов")

        await asyncio.sleep(wait_seconds)

        # Генерируем и отправляем
        try:
            await send_content_of_day(bot)
        except Exception as e:
            print(f"❌ Ошибка отправки контента дня: {e}")

        # Ждём до следующего дня
        await asyncio.sleep(60)  # небольшая задержка, чтобы не зациклиться


async def send_content_of_day(bot: Bot, test_mode: bool = False):
    """
    Сгенерировать и отправить контент дня всем пользователям
    test_mode = True — отправить только админам для проверки
    """

    # Генерируем контент
    content = "Сегодня отличный день для того, чтобы запустить новую вирусную рекламу вашего бизнеса!"

    # Сохраняем в БД
    today = datetime.now().date().isoformat()
    await save_content_of_day(
        content=content,
        niche="daily",
        hook="Контент дня",
        language="ru"
    )

    # Получаем ID контента
    cod = await get_content_of_day(today)
    content_id = cod.get("id") if cod else None

    # Клавиатура
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 Создать контент",
                    url="https://t.me/sozanda_bot"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⭐ Получить Premium",
                    callback_data="cod_premium"
                ),
            ],
        ]
    )

    # Кому отправляем
    if test_mode:
        target_users = ADMIN_IDS
    else:
        # Все активные пользователи
        from database.connection import fetch_all
        users = await fetch_all(
            "SELECT user_id, language FROM users WHERE is_active = 1"
        )
        target_users = [u["user_id"] for u in users]

    # Отправляем
    sent_count = 0
    for user_id in target_users:
        try:
            user = await get_user(user_id)
            lang = user.get("language", "ru") if user else "ru"

            # Текст на языке пользователя
            if lang == "tg":
                header = f"🌅 <b>Контенти рӯз</b> | {today}\n\n"
                footer = (
                    "\n\n─────────────\n"
                    "💡 Мехоҳед ҳар рӯз чунин контент?\n"
                    "🤖 Ба @SozandaBot обуна шавед!"
                )
            else:
                header = f"🌅 <b>Контент дня</b> | {today}\n\n"
                footer = (
                    "\n\n─────────────\n"
                    "💡 Хотите такой контент каждый день?\n"
                    "🤖 Подпишитесь на @SozandaBot!"
                )

            await bot.send_message(
                chat_id=user_id,
                text=header + content + footer,
                reply_markup=keyboard,
                parse_mode="HTML"
            )

            sent_count += 1

            # Логируем
            await log_event(user_id, "content_of_day_received")

            # Небольшая задержка, чтобы не спамить API
            await asyncio.sleep(0.05)

        except Exception as e:
            print(f"❌ Не удалось отправить контент дня пользователю {user_id}: {e}")

    # Обновляем счётчик
    if content_id:
        for _ in range(sent_count):
            await increment_content_sent(content_id)

    print(f"✅ Контент дня отправлен {sent_count} пользователям")

    return sent_count


# ============================================
# 2. НАПОМИНАНИЯ НЕАКТИВНЫМ (каждые 3 дня)
# ============================================

async def _inactive_reminder_loop(bot: Bot):
    """Напоминания пользователям, которые давно не генерировали контент"""

    while True:
        now = datetime.now()
        target = datetime.combine(now.date(), dt_time(hour=18, minute=0))

        if now >= target:
            target += timedelta(days=3)

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        try:
            await send_inactive_reminders(bot)
        except Exception as e:
            print(f"❌ Ошибка отправки напоминаний: {e}")

        await asyncio.sleep(60)


async def send_inactive_reminders(bot: Bot, days_inactive: int = 3):
    """Отправить напоминания неактивным пользователям"""

    from database.connection import fetch_all

    # Находим пользователей без генераций N дней
    inactive_users = await fetch_all("""
        SELECT u.user_id, u.language, u.first_name
        FROM users u
        LEFT JOIN generations g ON u.user_id = g.user_id
        WHERE u.is_active = 1
        GROUP BY u.user_id
        HAVING MAX(g.created_at) IS NULL
           OR date(MAX(g.created_at)) <= date('now', '-{} days')
    """.format(days_inactive))

    sent = 0
    for user in inactive_users:
        user_id = user["user_id"]
        lang = user.get("language", "ru")

        # Персонализированное сообщение
        name = user.get("first_name", "друг") if lang == "ru" else user.get("first_name", "дӯст")

        if lang == "tg":
            text = (
                f"👋 Салом, {name}!\n\n"
                f"🤖 Шумо {days_inactive} рӯз аст, ки аз Sozanda истифода намебаред.\n\n"
                f"✨ Нав идеяҳо ва хук-ҳои вирусӣ интизори шумоанд!\n\n"
                f"🎁 Барои бозгашт: +3 генерацияи иловагӣ"
            )
        else:
            text = (
                f"👋 Привет, {name}!\n\n"
                f"🤖 Ты не пользовался Sozanda уже {days_inactive} дня.\n\n"
                f"✨ Новые идеи и вирусные хуки ждут тебя!\n\n"
                f"🎁 За возвращение: +3 бонусные генерации"
            )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎬 Создать контент" if lang == "ru" else "🎬 Мундод созед",
                        url="https://t.me/sozanda_bot"
                    ),
                ],
            ]
        )

        try:
            await bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=keyboard
            )

            # Начисляем бонус
            from database.models import add_bonus_generation
            await add_bonus_generation(user_id, 3)

            await log_event(user_id, "inactive_reminder_sent")
            sent += 1
            await asyncio.sleep(0.05)

        except Exception as e:
            print(f"❌ Не удалось отправить напоминание {user_id}: {e}")

    print(f"✅ Напоминания отправлены {sent} неактивным пользователям")
    return sent


# ============================================
# 3. ЕЖЕНЕДЕЛЬНЫЙ ЧЕЛЛЕНДЖ (понедельник 8:00)
# ============================================

async def _weekly_challenge_loop(bot: Bot):
    """Еженедельный челлендж контента"""

    while True:
        now = datetime.now()

        # Следующий понедельник
        days_until_monday = (7 - now.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7

        target = datetime.combine(
            now.date() + timedelta(days=days_until_monday),
            dt_time(hour=8, minute=0)
        )

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        try:
            await send_weekly_challenge(bot)
        except Exception as e:
            print(f"❌ Ошибка отправки челленджа: {e}")

        await asyncio.sleep(60)


async def send_weekly_challenge(bot: Bot):
    """Отправить еженедельный челлендж"""

    niches = await get_all_niches("ru")
    niche = random.choice(niches) if niches else None
    niche_name = niche.get("name_ru", "бизнес") if niche else "бизнес"

    challenge_tasks = [
        "Создайте 3 Reels за неделю",
        "Напишите пост, который наберёт 100 лайков",
        "Сделайте Stories с опросом каждый день",
        "Придумайте свой вирусный хук",
        "Сделайте контент про 'почему мы лучшие'",
        "Покажите закулисье вашего бизнеса",
        "Создайте контент с клиентом/отзывом",
    ]

    task = random.choice(challenge_tasks)

    # Награда
    rewards = [
        "🏆 7 дней Premium бесплатно",
        "🏆 +20 бонусных генераций",
        "🏆 Публикация в нашем канале",
    ]
    reward = random.choice(rewards)

    text = f"""🎯 <b>Челлендж недели!</b>

📅 Неделя: {datetime.now().strftime("%d.%m")} — {(datetime.now() + timedelta(days=6)).strftime("%d.%m")}

📝 <b>Задание:</b>
{task}

🏢 <b>Ниша:</b> {niche_name}

🎁 <b>Награда:</b>
{reward}

👇 Участвуйте и присылайте результаты!
"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Начать челлендж",
                    url="https://t.me/sozanda_bot"
                ),
            ],
        ]
    )

    # Отправляем всем
    from database.connection import fetch_all
    users = await fetch_all("SELECT user_id FROM users WHERE is_active = 1")

    sent = 0
    for u in users:
        try:
            await bot.send_message(
                chat_id=u["user_id"],
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            sent += 1
            await asyncio.sleep(0.05)
        except:
            pass

    print(f"✅ Челлендж отправлен {sent} пользователям")
    return sent


# ============================================
# 4. ТОП РЕФОВОДОВ (1-е число каждого месяца)
# ============================================

async def _monthly_top_referrers_loop(bot: Bot):
    """Ежемесячная рассылка топ рефоводов"""

    while True:
        now = datetime.now()

        # Следующее 1-е число
        if now.day == 1:
            target = now + timedelta(days=32)
        else:
            target = (now.replace(day=1) + timedelta(days=32)).replace(day=1)

        target = datetime.combine(target.date(), dt_time(hour=10, minute=0))
        wait_seconds = (target - now).total_seconds()

        await asyncio.sleep(wait_seconds)

        try:
            await send_top_referrers(bot)
        except Exception as e:
            print(f"❌ Ошибка отправки топа: {e}")

        await asyncio.sleep(60)


async def send_top_referrers(bot: Bot):
    """Отправить топ рефоводов месяца"""

    from database.models import get_top_referrers

    top = await get_top_referrers(10)

    text = "🏆 <b>Топ рефоводов месяца</b>\n\n"

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, user in enumerate(top[:10], 1):
        name = user.get("first_name") or user.get("username") or f"User_{user['user_id']}"
        refs = user.get("referral_count", 0)
        text += f"{medals[i-1]} {name} — {refs} друзей\n"

    text += "\n🎁 Победители получают 30 дней Professional бесплатно!"

    # Отправляем всем
    from database.connection import fetch_all
    users = await fetch_all("SELECT user_id FROM users WHERE is_active = 1")

    sent = 0
    for u in users:
        try:
            await bot.send_message(
                chat_id=u["user_id"],
                text=text,
                parse_mode="HTML"
            )
            sent += 1
            await asyncio.sleep(0.05)
        except:
            pass

    print(f"✅ Топ рефоводов отправлен {sent} пользователям")
    return sent


# ============================================
# 5. ОЧИСТКА СТАРЫХ ДАННЫХ (каждое воскресенье 3:00)
# ============================================

async def _cleanup_loop(bot: Bot):
    """Очистка старых данных"""

    while True:
        now = datetime.now()

        # Следующее воскресенье
        days_until_sunday = (6 - now.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7

        target = datetime.combine(
            now.date() + timedelta(days=days_until_sunday),
            dt_time(hour=3, minute=0)
        )

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        try:
            from database.connection import cleanup_old_data
            await cleanup_old_data(days=90)
        except Exception as e:
            print(f"❌ Ошибка очистки: {e}")

        await asyncio.sleep(60)


# ============================================
# РУЧНОЕ УПРАВЛЕНИЕ (для админов)
# ============================================

async def force_content_of_day(bot: Bot):
    """Принудительно отправить контент дня (для админа)"""

    return await send_content_of_day(bot, test_mode=False)


async def test_content_of_day(bot: Bot):
    """Тестовая отправка контента дня только админам"""

    return await send_content_of_day(bot, test_mode=True)


async def force_reminder(bot: Bot, user_id: Optional[int] = None):
    """Принудительно отправить напоминание"""

    if user_id:
        # Конкретному пользователю
        try:
            await bot.send_message(
                chat_id=user_id,
                text="📢 Тестовое напоминание от админа"
            )
            return 1
        except:
            return 0
    else:
        return await send_inactive_reminders(bot)


# ============================================
# УТИЛИТЫ
# ============================================

def get_scheduler_status() -> Dict[str, Any]:
    """Получить статус планировщика (для админ-панели)"""

    return {
        "active_tasks": len([t for t in scheduled_tasks if not t.done()]),
        "total_tasks": len(scheduled_tasks),
        "tasks": [
            {
                "done": t.done(),
                "cancelled": t.cancelled(),
            }
            for t in scheduled_tasks
        ]
    }


async def stop_scheduler():
    """Остановить все задачи планировщика"""

    for task in scheduled_tasks:
        if not task.done():
            task.cancel()

    scheduled_tasks.clear()
    print("⏹ Планировщик остановлен")