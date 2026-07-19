# content_engine/menu.py — Главный router бота TojikAI (v2.0)
# Полная интеграция всех SMM-инструментов, без глобальных словарей!
# Все состояния хранятся строго в FSMContext (state).

import random
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import (
    FREE_DAILY_LIMIT,
    OSON_DAILY_LIMIT,
    PRO_DAILY_LIMIT,
    WATERMARK_TEXT,
    ADMIN_IDS,
    REFERRAL_BONUS_GENERATIONS,
    TARIFFS,
    ADMIN_ID
)
from database.models import (
    get_or_create_user,
    get_user,
    get_user_stats,
    increment_generation,
    check_daily_limit,
    get_referral_count,
    add_referral_bonus,
    get_user_subscription,
    save_generation,
    get_generation_history,
)
from services.ai_generator import generate_ai_content
from content_engine.niche_manager import get_all_niches, get_niche_key_by_text, get_niche_name

# Проверка, является ли текст кнопкой ниши
def is_niche_button(text: str) -> bool:
    all_names = set()
    for country in ["uz", "tj"]:
        for lang in ["ru", "tg", "uz"]:
            for n in get_all_niches(lang, country):
                all_names.add(n.get(f"name_{lang}"))
                all_names.add(n.get("icon", "") + " " + n.get(f"name_{lang}", ""))
    return text in all_names


from keyboards.main_menu_content import get_main_menu
from keyboards.niche_menu import get_niche_menu
from keyboards.reels_count_menu import get_count_menu
from keyboards.topics_keyboard import get_topics_keyboard
from keyboards.language_menu import get_language_menu
from keyboards.subscription_menu import get_subscription_menu, get_payment_menu
from keyboards.share_keyboard import get_share_keyboard
from keyboards.referral_keyboard import get_referral_keyboard

router = Router()

# ============================================
# СТРУКТУРИРОВАННАЯ КАРТА SMM ИНСТРУМЕНТОВ
# ============================================

SMM_TOOLS = {
    "ideas": {
        "icon": "💡",
        "name_ru": "Идеи", "name_tg": "Идеяҳо", "name_uz": "G'oyalar",
        "options": {
            "ideas_5": ("5 идей", "5 идея", "5 ta g'oya"),
            "ideas_10": ("10 идей", "10 идея", "10 ta g'oya"),
            "ideas_20": ("20 идей", "20 идея", "20 ta g'oya"),
            "ideas_30": ("30 идей", "30 идея", "30 ta g'oya"),
            "ideas_viral": ("Вирусные идеи", "Идеяҳои вирусӣ", "Viral g'oyalar"),
            "ideas_trend": ("Трендовые идеи", "Идеяҳои трендӣ", "Trend g'oyalar"),
            "ideas_expert": ("Экспертные идеи", "Идеяҳои коршиносӣ", "Ekspert g'oyalari"),
            "ideas_sales": ("Продающие идеи", "Идеяҳои фурӯшанда", "Sotuvchi g'oyalar")
        }
    },
    "posts": {
        "icon": "📝",
        "name_ru": "Посты", "name_tg": "Постҳо", "name_uz": "Postlar",
        "options": {
            "posts_sales": ("Продающие", "Фурӯшанда", "Sotuvchi"),
            "posts_expert": ("Экспертные", "Коршиносӣ", "Ekspert"),
            "posts_edu": ("Образовательные", "Таълимӣ", "Ta'limiy"),
            "posts_cases": ("Кейсы", "Кейсҳо", "Keyslar"),
            "posts_reviews": ("Отзывы", "Фикру мулоҳизаҳо", "Sharhlar"),
            "posts_comp": ("Сравнения", "Муқоисаҳо", "Taqqoslamalar"),
            "posts_faq": ("FAQ", "Саволу ҷавоб", "FAQ"),
            "posts_check": ("Чек-листы", "Чек-листҳо", "Chek-listlar"),
            "posts_news": ("Новости", "Хабарҳо", "Yangiliklar")
        }
    },
    "stories": {
        "icon": "📸",
        "name_ru": "Stories", "name_tg": "Сторизҳо", "name_uz": "Stories",
        "options": {
            "stories_1": ("На 1 день", "Барои 1 рӯз", "1 kunlik"),
            "stories_3": ("На 3 дня", "Барои 3 рӯз", "3 kunlik"),
            "stories_7": ("На неделю", "Барои як ҳафта", "Bir haftalik"),
            "stories_warm": ("Прогрев", "Прогрев", "Progrev"),
            "stories_engage": ("Вовлечение", "Ҷалбкунӣ", "Jalb qilish"),
            "stories_sales": ("Продажи", "Фурӯш", "Sotuvlar"),
            "stories_reviews": ("Отзывы", "Мулоҳизаҳо", "Sharhlar"),
            "stories_polls": ("Опросы", "Пурсишҳо", "So'rovnomalar"),
            "stories_quizzes": ("Квизы", "Квизҳо", "Viktorinalar")
        }
    },
    "reels": {
        "icon": "🎬",
        "name_ru": "Reels", "name_tg": "Reels", "name_uz": "Reels",
        "options": {
            "reels_script": ("Сценарии", "Сценарияҳо", "Ssenariylar"),
            "reels_hooks": ("Хуки", "Хукҳо (Hooks)", "Hooklar"),
            "reels_cta": ("Призывы к действию", "Даъват ба амал", "CTA (Chaqiriqlar)"),
            "reels_tips": ("Монтажные подсказки", "Маслиҳатҳои монтаж", "Montaj bo'yicha maslahatlar")
        }
    },
    "shorts": {
        "icon": "🎥",
        "name_ru": "Shorts", "name_tg": "Shorts", "name_uz": "Shorts",
        "options": {
            "shorts_script": ("Сценарии", "Сценарияҳо", "Ssenariylar"),
            "shorts_ideas": ("Идеи", "Идеяҳо", "G'oyalar"),
            "shorts_struct": ("Структура ролика", "Сохтори ролик", "Rolik strukturasi")
        }
    },
    "plan": {
        "icon": "📅",
        "name_ru": "Контент-план", "name_tg": "Нақшаи контент", "name_uz": "Kontent-reja",
        "options": {
            "plan_1": ("На неделю", "Барои як ҳафта", "Bir haftalik"),
            "plan_2": ("На 2 недели", "Барои 2 ҳафта", "Ikki haftalik"),
            "plan_4": ("На месяц", "Барои як моҳ", "Bir oylik")
        }
    },
    "ads": {
        "icon": "📢",
        "name_ru": "Реклама", "name_tg": "Реклама", "name_uz": "Reklama",
        "options": {
            "ads_texts": ("Рекламные тексты", "Матнҳои рекламавӣ", "Reklama matnlari"),
            "ads_offers": ("Офферы", "Офферҳо", "Offerlar"),
            "ads_promos": ("Акции", "Аксияҳо", "Aksiyalar"),
            "ads_specials": ("Спецпредложения", "Пешниҳодҳои махсус", "Maxsus takliflar")
        }
    },
    "funnel": {
        "icon": "🎯",
        "name_ru": "Воронка продаж", "name_tg": "Воронкаи фурӯш", "name_uz": "Savdo voronkasi",
        "options": {
            "funnel_warm": ("Прогрев", "Прогрев", "Progrev"),
            "funnel_series": ("Серия сообщений", "Силсилаи паёмҳо", "Xabarlar seriyasi"),
            "funnel_close": ("Закрытие на продажу", "Пӯшидани фурӯш", "Sotuvni yopish")
        }
    },
    "tg_channel": {
        "icon": "📱",
        "name_ru": "Telegram", "name_tg": "Telegram", "name_uz": "Telegram",
        "options": {
            "tg_posts": ("Посты", "Постҳо", "Postlar"),
            "tg_rubrics": ("Рубрики", "Рубрикаҳо", "Rubrikalar"),
            "tg_plan": ("Контент-план", "Нақшаи контент", "Kontent-reja")
        }
    },
    "instagram": {
        "icon": "📷",
        "name_ru": "Instagram", "name_tg": "Instagram", "name_uz": "Instagram",
        "options": {
            "insta_posts": ("Посты", "Постҳо", "Postlar"),
            "insta_stories": ("Stories", "Stories", "Stories"),
            "insta_reels": ("Reels", "Reels", "Reels")
        }
    },
    "tiktok": {
        "icon": "🎵",
        "name_ru": "TikTok", "name_tg": "TikTok", "name_uz": "TikTok",
        "options": {
            "tiktok_ideas": ("Идеи", "Идеяҳо", "G'oyalar"),
            "tiktok_scripts": ("Сценарии", "Сценарияҳо", "Ssenariylar"),
            "tiktok_trends": ("Тренды", "Трендҳо", "Trendlar")
        }
    },
    "youtube": {
        "icon": "▶️",
        "name_ru": "YouTube", "name_tg": "YouTube", "name_uz": "YouTube",
        "options": {
            "yt_shorts": ("Shorts", "Shorts", "Shorts"),
            "yt_topics": ("Темы видео", "Мавзӯъҳои видео", "Video mavzulari"),
            "yt_scripts": ("Сценарии", "Сценарияҳо", "Ssenariylar")
        }
    }
}

# ============================================
# ГЛОБАЛЬНЫЙ ПЕРЕХВАТЧИК МЕНЮ (ДЛЯ ЛЮБОГО FSM-СОСТОЯНИЯ)
# ============================================

@router.message(F.text.in_([
    "🏠 Главное меню", "🏠 Менюи асосӣ", "🏠 Asosiy menyu",
    "🎬 Контент AI", "🎬 AI Контент", "🎬 AI мундод", "🎬 AI Reels/Kreativ", "🎬 AI Reels", "🎬 Reels",
    "📝 Посты", "📝 Постҳо", "📝 Postlar",
    "📸 Stories", "📸 Сториз",
    "💡 Идеи", "💡 Идеяҳо", "💡 G'oyalar",
    "⭐ Premium", "⭐ Премиум", "⭐ Premium obuna", "⭐ Premium тарифҳо",
    "👥 Рефералка", "👥 Даъват", "👥 Давват", "👥 Hamkorlik (Do'stlar)",
    "📊 Статистика", "📊 Омор", "📊 Statistika",
    "📋 История", "📋 Таърих", "📋 Tarix",
    "🎮 Бизнес-Игра", "🎮 Бозии тиҷорат", "🎮 Biznes o'yini", "🎮 Бизнес Империя",
    "📞 Поддержка", "📞 Дастгирӣ", "📞 Yordam / Aloqa"
]))
async def global_menu_interceptor(message: Message, state: FSMContext):
    await state.clear()

    text = message.text
    if text in ["🏠 Главное меню", "🏠 Менюи асосӣ", "🏠 Asosiy menyu"]:
        await back_to_main_text(message, state)
    elif text in ["🎬 Контент AI", "🎬 AI Контент", "🎬 AI мундод", "🎬 AI Reels/Kreativ", "🎬 AI Reels", "🎬 Reels"]:
        await reels_menu(message, state)
    elif text in ["📝 Посты", "📝 Постҳо", "📝 Postlar"]:
        await posts_menu(message, state)
    elif text in ["📸 Stories", "📸 Сториз"]:
        await stories_menu(message, state)
    elif text in ["💡 Идеи", "💡 Идеяҳо", "💡 G'oyalar"]:
        await ideas_menu(message, state)
    elif text in ["⭐ Premium", "⭐ Премиум", "⭐ Premium obuna", "⭐ Premium тарифҳо"]:
        from content_engine.subscription import show_plans
        await show_plans(message)
    elif text in ["👥 Рефералка", "👥 Даъват", "👥 Давват", "👥 Hamkorlik (Do'stlar)"]:
        await referral_menu_text(message, state)
    elif text in ["📊 Статистика", "📊 Омор", "📊 Statistika"]:
        await stats_menu(message, state)
    elif text in ["📋 История", "📋 Таърих", "📋 Tarix"]:
        await history_menu(message, state)
    elif text in ["🎮 Бизнес-Игра", "🎮 Бозии тиҷорат", "🎮 Biznes o'yini", "🎮 Бизнес Империя"]:
        await start_business_game(message, state)
    elif text in ["📞 Поддержка", "📞 Дастгирӣ", "📞 Yordam / Aloqa"]:
        await support_menu(message, state)


# ============================================
# ЛОКАЛИЗАЦИОННЫЕ ТЕКСТЫ С БРЕНДОМ TojikAI
# ============================================

TEXTS = {
    "ru": {
        "welcome": "👋 Добро пожаловать в <b>TojikAI</b>!\n\n🤖 Я — AI-платформа, которая создаёт вирусный контент для бизнеса.\n\n<b>Выберите язык / Забонро интихоб кунед:</b>",
        "main_menu": "👋 Главное меню\n\n✨ Выберите, что создать:",
        "choose_niche": "🏢 Для какого бизнеса нужен контент?",
        "choose_tool": "⚡ <b>SMM & Media Платформа TojikAI</b>\n\nНиша выбрана: <b>{niche}</b>\n\nВыберите инструмент продвижения бизнеса:",
        "choose_subtool": "👇 Выберите необходимый вариант для <b>{tool}</b>:",
        "generating": "⏳ Генерирую профессиональный контент через ИИ...\n\nЭто займёт несколько секунд...",
        "limit_reached": "❌ Лимит исчерпан!\n\n💡 У вас закончились бесплатные генерации на сегодня.\n\n🚀 Получите больше:\n• Пригласите друга — +{ref_bonus} генераций\n• Оформите подписку Oson — {oson_limit} генераций/день\n• Или Professional — безлимит!",
        "premium_info": "⭐ <b>Premium подписки TojikAI</b>\n\nAppropriate limits apply for normal users. Free is watermarked. Premium tiers bypass all locks.",
        "support": "📞 <b>Поддержка TojikAI</b>\n\nПишите: @tojikai_support",
        "history_empty": "📭 История пуста.",
        "history_title": "📋 <b>Ваша история генераций</b>\n\n",
        "stats": "📊 <b>Ваша статистика TojikAI</b>\n\n🆔 ID: {user_id}\n🌍 Язык: {lang}\n📅 Регистрация: {reg_date}\n\n📈 Генераций сегодня: {today}/{limit}\n📈 Всего генераций: {total}\n👥 Приглашено друзей: {refs}\n\n💳 Тариф: {plan}",
    },
    "tg": {
        "welcome": "👋 Хуш омадед ба <b>TojikAI</b>!\n\n🤖 Платформаи AI барои сохтани мундоди касбӣ.",
        "main_menu": "👋 Менюи асосӣ\n\n✨ Интихоб кунед, чи сохтан мехоҳед:",
        "choose_niche": "🏢 Барои кадом бизнес контент лозим аст?",
        "choose_tool": "⚡ <b>SMM & Media Платформаи TojikAI</b>\n\nНиша интихоб шуд: <b>{niche}</b>\n\nАсбоби пешбурди тиҷоратро интихоб кунед:",
        "choose_subtool": "👇 Варианти дилхоҳро барои <b>{tool}</b> интихоб кунед:",
        "generating": "⏳ AI мундоди касбиро месозад...\n\nЧанд сония вақт мегирад...",
        "limit_reached": "❌ Лимит ба охир расид!\n\n💡 Генерацияҳои ройгони шумо тамом шуданд.\n\n🚀 Бештар гиред:\n• Дӯстро даъват кунед — +{ref_bonus} генерация\n• Обунаи Oson — {oson_limit} генерация/рӯз",
        "premium_info": "⭐ <b>Обунаҳои Premium TojikAI</b>",
        "support": "📞 <b>Дастгирии TojikAI</b>\n\n@tojikai_support",
        "history_empty": "📭 Таърих холӣ аст.",
        "history_title": "📋 <b>Таърихи генерацияҳои шумо</b>\n\n",
        "stats": "📊 <b>Омори шумо дар TojikAI</b>\n\n🆔 ID: {user_id}\n🌍 Забон: {lang}\n📅 Санаи бақайдгирӣ: {reg_date}\n\n📈 Генерацияҳои имрӯз: {today}/{limit}\n📈 Ҳамаи генерацияҳо: {total}\n👥 Даъват шудаанд: {refs}\n\n💳 Тариф: {plan}",
    },
    "uz": {
        "welcome": "👋 <b>TojikAI</b> botiga xush belibsiz!\n\n🤖 Biznesingiz uchun professional SMM va AI platforma.",
        "main_menu": "👋 Asosiy menyu\n\n✨ Nimani yaratishni xohlaysiz?",
        "choose_niche": "🏢 Qaysi soha (nisha) uchun kontent kerak?",
        "choose_tool": "⚡ <b>TojikAI SMM & Media Platformasi</b>\n\nSoha tanlandi: <b>{niche}</b>\n\nSohani rivojlantirish vositasini tanlang:",
        "choose_subtool": "👇 <b>{tool}</b> bo'limi uchun kerakli variantni tanlang:",
        "generating": "⏳ AI orqali professional kontent yaratilmoqda...\n\nBu bir necha soniya vaqt oladi...",
        "limit_reached": "❌ Kunlik limit tugadi!\n\n💡 Bugungi bepul generatsiyalaringiz yakunlandi.\n\n🚀 Ko'proq imkoniyat oling:\n• Do'shingizni taklif qiling — +{ref_bonus} ta generatsiya\n• Oson — {oson_limit} ta/kun",
        "premium_info": "⭐ <b>TojikAI Premium obunalar</b>",
        "support": "📞 <b>Yordam va Aloqa TojikAI</b>\n\n@tojikai_support",
        "history_empty": "📭 Tarix bo'sh.",
        "history_title": "📋 <b>Sizning generatsiyalar tarixingiz</b>\n\n",
        "stats": "📊 <b>Sizning statistikangiz TojikAI</b>\n\n🆔 ID: {user_id}\n🌍 Til: {lang}\n📅 Ro'yxatdan o'tilgan sana: {reg_date}\n\n📈 Bugungi generatsiyalar: {today}/{limit}\n📈 Jami generatsiyalar: {total}\n👥 Taklif qilingan do'stlar: {refs}\n\n💳 Tarif: {plan}",
    }
}


async def get_text(user_id: int, key: str, state: FSMContext, **kwargs) -> str:
    state_data = await state.get_data()
    lang = state_data.get("language")
    if not lang:
        user = await get_user(user_id)
        lang = user.get("language", "ru") if user else "ru"
        await state.update_data(language=lang)
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def get_niche_display(key: str, lang: str = "ru") -> str:
    return get_niche_name(key, lang)


# ============================================
# STATES GROUP (SMM HUB)
# ============================================

class QuizStates(StatesGroup):
    answering = State()

class GameStates(StatesGroup):
    answering_event = State()

class SMMHubStates(StatesGroup):
    selecting_niche = State()
    selecting_tool = State()
    selecting_subtool = State()


# ============================================
# ГЛАВНОЕ МЕНЮ И НАВИГАЦИЯ
# ============================================

@router.callback_query(F.data == "main_menu")
async def show_main_menu_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)
    await callback.answer()
    await callback.message.edit_text(
        await get_text(user_id, "main_menu", state),
        reply_markup=get_main_menu(lang)
    )


@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)
    await callback.answer()
    await callback.message.answer(
        await get_text(user_id, "main_menu", state),
        reply_markup=get_main_menu(lang)
    )


@router.message(F.text.in_(["🏠 Главное меню", "🏠 Менюи асосӣ", "🏠 Asosiy menyu"]))
async def back_to_main_text(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)
    await message.answer(
        await get_text(user_id, "main_menu", state),
        reply_markup=get_main_menu(lang)
    )


# ============================================
# КОНТЕНТ AI (ВХОД В ВОРОНКУ ВЫБОРА НИШИ)
# ============================================

@router.message(F.text.in_([
    "🎬 Контент AI", "🎬 AI Контент", "🎬 AI мундод",
    "🎬 AI Reels/Kreativ", "🎬 AI Reels", "🎬 Reels"
]))
async def reels_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    await state.update_data(language=lang, country=country)

    await state.set_state(SMMHubStates.selecting_niche)
    await message.answer(
        await get_text(user_id, "choose_niche", state),
        reply_markup=get_niche_menu(lang, country=country)
    )


@router.message(F.text.in_(["📝 Посты", "📝 Постҳо", "📝 Postlar"]))
async def posts_menu(message: Message, state: FSMContext):
    await reels_menu(message, state)


@router.message(F.text.in_(["📸 Stories", "📸 Сториз"]))
async def stories_menu(message: Message, state: FSMContext):
    await reels_menu(message, state)


@router.message(F.text.in_(["💡 Идеи", "💡 Идеяҳо", "💡 G'oyalar"]))
async def ideas_menu(message: Message, state: FSMContext):
    await reels_menu(message, state)


# ============================================
# ВЫБОР НИШИ И ПЕРЕХОД В SMM-ХАБ
# ============================================

@router.message(SMMHubStates.selecting_niche, lambda msg: is_niche_button(msg.text))
async def niche_selected_and_show_hub(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"

    niche_key = get_niche_key_by_text(message.text, country=country)
    await state.update_data(language=lang, country=country, niche=niche_key)

    await show_smm_hub_menu(message, state, user_id, lang, niche_key)


async def show_smm_hub_menu(message: Message, state: FSMContext, user_id: int, lang: str, niche_key: str):
    await state.set_state(SMMHubStates.selecting_tool)

    niche_name = get_niche_name(niche_key, lang)
    prompt = await get_text(user_id, "choose_tool", state, niche=niche_name)

    # Строим Reply-клавиатуру с 12 SMM инструментами
    buttons = []
    row = []
    for tool_id, tool_data in SMM_TOOLS.items():
        name = tool_data[f"name_{lang}"] if f"name_{lang}" in tool_data else tool_data["name_ru"]
        btn_text = f"{tool_data['icon']} {name}"
        row.append(KeyboardButton(text=btn_text))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Кнопка Назад
    back_text = "⬅️ Назад к нишам" if lang == "ru" else ("⬅️ Баргашт ба нишаҳо" if lang == "tg" else "⬅️ Nishalarga qaytish")
    buttons.append([KeyboardButton(text=back_text)])

    await message.answer(
        prompt,
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True),
        parse_mode="HTML"
    )


# ============================================
# ОБРАБОТКА ВЫБОРА SMM ИНСТРУМЕНТА (КАТЕГОРИИ)
# ============================================

def is_smm_tool_button(text: str) -> bool:
    cleaned = text.strip()
    for tool_id, tool_data in SMM_TOOLS.items():
        for l in ["ru", "tg", "uz"]:
            name = tool_data.get(f"name_{l}")
            if name:
                if cleaned == f"{tool_data['icon']} {name}".strip():
                    return True
                if cleaned == name:
                    return True
    return False


def get_tool_id_by_text(text: str, lang: str = "ru") -> str:
    cleaned = text.strip()
    for tool_id, tool_data in SMM_TOOLS.items():
        for l in ["ru", "tg", "uz"]:
            name = tool_data.get(f"name_{l}")
            if name and (cleaned == f"{tool_data['icon']} {name}".strip() or cleaned == name):
                return tool_id
    return "ideas"


@router.message(SMMHubStates.selecting_tool, lambda msg: is_smm_tool_button(msg.text))
async def smm_tool_selected(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    niche_key = data.get("niche", "cafe_uz")

    tool_id = get_tool_id_by_text(message.text, lang)
    await state.update_data(current_tool=tool_id)

    tool_data = SMM_TOOLS[tool_id]
    tool_name = tool_data[f"name_{lang}"] if f"name_{lang}" in tool_data else tool_data["name_ru"]

    await state.set_state(SMMHubStates.selecting_subtool)

    # Строим Reply-клавиатуру для субопций выбранной категории
    buttons = []
    row = []

    # Извлекаем все опции для выбранного инструмента
    options = tool_data["options"]
    idx = 0 if lang == "ru" else (1 if lang == "tg" else 2)

    for sub_id, names_tuple in options.items():
        # names_tuple: ("5 идей", "5 идея", "5 ta g'oya")
        btn_text = names_tuple[idx] if idx < len(names_tuple) else names_tuple[0]
        row.append(KeyboardButton(text=btn_text))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Кнопка Назад
    back_text = "⬅️ В меню инструментов" if lang == "ru" else ("⬅️ Ба менюи асбобҳо" if lang == "tg" else "⬅️ Asboblar menyusiga")
    buttons.append([KeyboardButton(text=back_text)])

    prompt = await get_text(user_id, "choose_subtool", state, tool=tool_name)

    await message.answer(
        prompt,
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True),
        parse_mode="HTML"
    )


@router.message(SMMHubStates.selecting_tool, F.text.regexp(r"^⬅️"))
async def back_from_tool_to_niche(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    country = data.get("country", "uz")

    await state.set_state(SMMHubStates.selecting_niche)
    await message.answer(
        await get_text(user_id, "choose_niche", state),
        reply_markup=get_niche_menu(lang, country=country)
    )


# ============================================
# ОБРАБОТКА ВЫБОРА СУБ-ИНСТРУМЕНТА (ГЕНЕРАЦИЯ ИИ)
# ============================================

def is_smm_subtool_button(text: str, current_tool: str, lang: str = "ru") -> bool:
    if current_tool not in SMM_TOOLS:
        return False
    tool_data = SMM_TOOLS[current_tool]
    cleaned = text.strip()
    idx = 0 if lang == "ru" else (1 if lang == "tg" else 2)

    for sub_id, names_tuple in tool_data["options"].items():
        btn_text = names_tuple[idx] if idx < len(names_tuple) else names_tuple[0]
        if cleaned == btn_text or cleaned == names_tuple[0]:
            return True
    return False


def get_subtool_id_by_text(text: str, current_tool: str, lang: str = "ru") -> str:
    tool_data = SMM_TOOLS[current_tool]
    cleaned = text.strip()
    idx = 0 if lang == "ru" else (1 if lang == "tg" else 2)

    for sub_id, names_tuple in tool_data["options"].items():
        btn_text = names_tuple[idx] if idx < len(names_tuple) else names_tuple[0]
        if cleaned == btn_text or cleaned == names_tuple[0]:
            return sub_id
    # Default fallback
    return list(tool_data["options"].keys())[0]


@router.message(SMMHubStates.selecting_subtool, F.text.regexp(r"^⬅️"))
async def back_from_subtool_to_tool(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    niche_key = data.get("niche", "cafe_uz")

    await show_smm_hub_menu(message, state, user_id, lang, niche_key)


@router.message(SMMHubStates.selecting_subtool)
async def handle_smm_generation_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    country = data.get("country", "uz")
    niche_key = data.get("niche", "cafe_uz")
    current_tool = data.get("current_tool", "ideas")

    # Проверяем, действительно ли это кнопка субопции
    if not is_smm_subtool_button(message.text, current_tool, lang):
        # Если не кнопка, предлагаем меню заново
        back_text = "⬅️ В меню инструментов" if lang == "ru" else ("⬅️ Ба менюи асбобҳо" if lang == "tg" else "⬅️ Asboblar menyusiga")
        await message.answer("❌ Выберите один из вариантов ниже или вернитесь назад.", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=back_text)]], resize_keyboard=True))
        return

    subtool_id = get_subtool_id_by_text(message.text, current_tool, lang)

    # Проверка лимитов (для суперадмина безлимит)
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, limit_info = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                await get_text(user_id, "limit_reached", state,
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return

    processing_msg = await message.answer(await get_text(user_id, "generating", state), parse_mode="HTML")

    try:
        # Генерируем контент через умный ИИ-генератор с полной локализацией
        content = await generate_ai_content(
            topic=message.text,
            niche=niche_key,
            language=lang,
            content_type=current_tool,
            country=country,
            subtool=subtool_id
        )

        sub = await get_user_subscription(user_id)
        if not sub or sub.get("plan") == "free":
            content += f"\n\n─────────────\n{WATERMARK_TEXT}"

        await processing_msg.delete()

        await message.answer(
            content,
            reply_markup=get_share_keyboard(lang),
            parse_mode="HTML"
        )

        # Сохраняем генерацию в БД истории
        await save_generation(
            user_id=user_id,
            niche=get_niche_name(niche_key, lang),
            topic=f"{current_tool.upper()} - {message.text}",
            content=content
        )

        if not is_admin:
            await increment_generation(user_id)

    except Exception as e:
        err_msg = f"❌ Ошибка генерации ИИ: {str(e)[:150]}"
        await processing_msg.edit_text(err_msg)


# ============================================
# РЕФЕРАЛЬНАЯ СИСТЕМА
# ============================================

@router.message(F.text.in_(["👥 Рефералка", "👥 Даъват", "👥 Давват", "👥 Hamkorlik (Do'stlar)"]))
async def referral_menu_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)

    if lang == "uz":
        prompt = "💎 <b>TojikAI Hamkorlik dasturi</b>\n\nDo'stlaringizni taklif qiling va har bir faol foydalanuvchi uchun premium generatsiyalar va bonus ballarga ega bo'ling!"
    elif lang == "tg":
        prompt = "💎 <b>Барномаи ҳамкории TojikAI</b>\n\nДӯстони худро даъват кунед ва барои ҳар як корбари нав генерацияҳои бонусӣ гиред!"
    else:
        prompt = "💎 <b>Партнерская программа TojikAI</b>\n\nПриглашайте друзей по вашей ссылке и получайте бонусные генерации и повышение статуса партнера!"

    await message.answer(prompt, reply_markup=get_referral_keyboard(lang), parse_mode="HTML")


@router.callback_query(F.data == "referral_main")
async def referral_main_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)

    if lang == "uz":
        prompt = "💎 <b>TojikAI Hamkorlik dasturi</b>\n\nDo'stlaringizni taklif qiling va har bir faol foydalanuvchi uchun premium generatsiyalar va bonus ballarga ega bo'ling!"
    elif lang == "tg":
        prompt = "💎 <b>Барномаи ҳамкории TojikAI</b>\n\nДӯстони худро даъват кунед ва барои ҳар як корбари нав генерацияҳои бонусӣ гиред!"
    else:
        prompt = "💎 <b>Партнерская программа TojikAI</b>\n\nПриглашайте друзей по вашей ссылке и получайте бонусные генерации и повышение статуса партнера!"

    await callback.message.edit_text(prompt, reply_markup=get_referral_keyboard(lang), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "ref_stats")
async def referral_stats_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    stats = await get_user_stats(user_id)
    lang = stats.get("language", "ru")

    from database.models import get_referral_link
    ref_link = await get_referral_link(user_id)

    if lang == "uz":
        text = f"""📊 <b>Hamkorlik statistikasi:</b>

🏆 <b>Hamkorlik darajasi (Tier):</b> {stats.get('referral_tier', 'Bronze')}
👥 <b>Jami taklif etilganlar:</b> {stats.get('referral_count', 0)} ta
🎯 <b>Faol do'stlar:</b> {stats.get('referral_active_count', 0)} ta
💰 <b>Hamkorlik ballari:</b> {stats.get('referral_points', 0)} ball

🔗 <b>Sizning taklif havolangiz:</b>
<code>{ref_link}</code>"""
    elif lang == "tg":
        text = f"""📊 <b>Омори барномаи даъватӣ:</b>

🏆 <b>Сатҳи шарикӣ (Tier):</b> {stats.get('referral_tier', 'Bronze')}
👥 <b>Ҳамаи даъватшудагон:</b> {stats.get('referral_count', 0)} нафар
🎯 <b>Дӯстони фаъол:</b> {stats.get('referral_active_count', 0)} нафар
💰 <b>Баллҳои шарикӣ:</b> {stats.get('referral_points', 0)} балл

🔗 <b>Пайванди даъватии шумо:</b>
<code>{ref_link}</code>"""
    else:
        text = f"""📊 <b>Статистика вашей партнерской программы:</b>

🏆 <b>Ранг партнера (Tier):</b> {stats.get('referral_tier', 'Bronze')}
👥 <b>Всего приглашено:</b> {stats.get('referral_count', 0)} чел.
🎯 <b>Активные пользователи:</b> {stats.get('referral_active_count', 0)} чел.
💰 <b>Бонусные баллы:</b> {stats.get('referral_points', 0)} pts

🔗 <b>Ваша реферальная ссылка:</b>
<code>{ref_link}</code>"""

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад / Ortga", callback_data="referral_main"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "ref_bonuses")
async def referral_bonuses_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    stats = await get_user_stats(user_id)
    lang = stats.get("language", "ru")

    if lang == "uz":
        text = """🎁 <b>Hamkorlik mukofotlari tizimi:</b>

• <b>Bronze</b> (Boshlang'ich) — har bir do'stingiz uchun +3 ta bepul generatsiya!
• <b>Silver</b> (50 ball) — har bir do'stingiz uchun +5 ta generatsiya + TojikAI tajribasi (XP)!
• <b>Gold</b> (100 ball) — 1 kunlik Premium sinov muddati!
• <b>Platinum</b> (200 ball) — 3 kunlik to'liq Professional Premium obuna!"""
    elif lang == "tg":
        text = """🎁 <b>Тизми мукофотии шарикӣ:</b>

• <b>Bronze</b> (Ибтидоӣ) — барои ҳар як дӯст +3 генерацияи ройгон!
• <b>Silver</b> (50 балл) — барои ҳар як дӯст +5 генерация + холҳои таҷриба (XP)!
• <b>Gold</b> (100 балл) — 1 рӯз Premium-и ройгон!
• <b>Platinum</b> (200 балл) — 3 рӯз обунаи Professional Premium!"""
    else:
        text = """🎁 <b>Система партнерских наград TojikAI:</b>

• <b>Bronze</b> (Старт) — +3 генерации за каждого друга!
• <b>Silver</b> (50 pts) — +5 генераций за друга + XP для Бизнес Империи!
• <b>Gold</b> (100 pts) — 1 день бесплатного Premium-доступа!
• <b>Platinum</b> (200 pts) — 3 дня полной подписки Professional!"""

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад / Ortga", callback_data="referral_main"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "ref_top")
async def referral_top_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from database.models import get_top_referrers
    top_list = await get_top_referrers(limit=10)

    if lang == "uz":
        text = "🏆 <b>Eng yaxshi hamkorlar (Top-10):</b>\n\n"
    elif lang == "tg":
        text = "🏆 <b>Пешсафони барномаи даъватӣ (Top-10):</b>\n\n"
    else:
        text = "🏆 <b>Топ-10 лучших партнеров TojikAI:</b>\n\n"

    for i, r in enumerate(top_list, 1):
        text += f"{i}. <b>{r['name']}</b> — {r['ref_count']} takliflar/даъватҳо\n"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад / Ortga", callback_data="referral_main"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


# ============================================
# СТАТИСТИКА, ИСТОРИЯ И ПОДДЕРЖКА
# ============================================

@router.message(F.text.in_(["📊 Статистика", "📊 Омор", "📊 Statistika"]))
async def stats_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    stats = await get_user_stats(user_id)
    lang = stats.get("language", "ru")

    sub = await get_user_subscription(user_id)
    plan_name = "Free"
    if sub:
        if sub.get("plan") == "oson":
            plan_name = "Oson"
        elif sub.get("plan") == "pro":
            plan_name = "Professional"
        elif sub.get("plan") == "business":
            plan_name = "Business"

    await message.answer(
        await get_text(user_id, "stats", state,
                 user_id=user_id,
                 lang="O'zbek tili" if lang == "uz" else ("Тоҷикӣ" if lang == "tg" else "Русский"),
                 reg_date=stats.get("created_at", "N/A"),
                 today=stats.get("today_count", 0),
                 limit=stats.get("daily_limit", FREE_DAILY_LIMIT),
                 total=stats.get("total_count", 0),
                 refs=stats.get("referral_count", 0),
                 plan=plan_name),
        parse_mode="HTML"
    )


@router.message(F.text.in_(["📋 История", "📋 Таърих", "📋 Tarix"]))
async def history_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    history = await get_generation_history(user_id, limit=10)
    if not history:
        await message.answer(await get_text(user_id, "history_empty", state))
        return
    text = await get_text(user_id, "history_title", state)
    for i, item in enumerate(history, 1):
        text += f"{i}. <b>{item['niche']}</b> — {item['topic'][:50]}...\n"
        text += f"   📅 {item['created_at']}\n\n"
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["📞 Поддержка", "📞 Дастгирӣ", "📞 Yordam / Aloqa"]))
async def support_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(await get_text(user_id, "support", state), parse_mode="HTML")


# ============================================
# ГЕЙМИФИКАЦИЯ: БИЗНЕС ИМПЕРИЯ
# ============================================

RANKS = ["Новичок", "Предприниматель", "Бизнесмен", "Инвестор", "Магнат", "Миллионер", "Миллиардер", "Легенда бизнеса"]
CITIES = ["Душанбе", "Худжанд", "Бохтар", "Куляб", "Ташкент", "Самарканд", "Бухара"]

@router.message(F.text.in_(["🎮 Бизнес-Игра", "🎮 Бозии тиҷорат", "🎮 Biznes o'yini", "🎮 Бизнес Империя"]))
async def start_business_game(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)

    from database.models import get_or_create_business_empire
    profile = await get_or_create_business_empire(user_id, message.from_user.username)

    current_xp = profile.get("xp", 0)
    level = profile.get("level", 1)
    rank_index = min(level - 1, len(RANKS) - 1)
    rank = RANKS[rank_index]

    businesses_json = profile.get("businesses", "[]") or "[]"
    try:
        opened = json.loads(businesses_json)
    except:
        opened = []

    passive_income = (profile.get("clients", 0) * 2) + (profile.get("employees", 0) * 5) + (len(opened) * 50)

    if lang == "uz":
        text = f"""<b>🎮 TojikAI Biznes Imperiyasi (v2.0)</b>

🏆 <b>Sizning unvoningiz:</b> {rank} (Level {level})
📍 <b>Hozirgi shahar:</b> {profile.get('city', 'Dushanbe')}
💰 <b>Balans:</b> {profile.get('balance', 1000)} somoni
👥 <b>Mijozlar:</b> {profile.get('clients', 0)} ta
👔 <b>Xodimlar jamoasi:</b> {profile.get('employees', 0)} ta
🏢 <b>Ochilgan korxonalar:</b> {len(opened)} ta

📊 <b>Passiv kunlik daromad:</b> +{passive_income} somoni / kuniga"""
        btn_case = "🎲 Tasodifiy voqea (Keys)"
        btn_buy = "🏢 Yangi biznes ochish"
        btn_top = "🏆 Liderlar jadvali"
    elif lang == "tg":
        text = f"""<b>🎮 Империяи Тиҷоратии TojikAI (v2.0)</b>

🏆 <b>Рутбаи шумо:</b> {rank} (Level {level})
📍 <b>Шаҳри фаъол:</b> {profile.get('city', 'Душанбе')}
💰 <b>Тавозун (Баланс):</b> {profile.get('balance', 1000)} сомонӣ
👥 <b>Мизоҷони умумӣ:</b> {profile.get('clients', 0)} нафар
👔 <b>Ҳайати кормандон:</b> {profile.get('employees', 0)} нафар
🏢 <b>Тиҷоратҳои кушода:</b> {len(opened)} адад

📊 <b>Даромади пассиви рӯзона:</b> +{passive_income} сомонӣ / рӯзона"""
        btn_case = "🎲 Ҳодисаи тасодуфӣ (Keys)"
        btn_buy = "🏢 Кушодани тиҷорати нав"
        btn_top = "🏆 Ҷадвали пешсафон"
    else:
        text = f"""<b>🎮 Бизнес Империя TojikAI (v2.0)</b>

🏆 <b>Ваш ранг:</b> {rank} (Уровень {level})
📍 <b>Текущий город:</b> {profile.get('city', 'Душанбе')}
💰 <b>Баланс:</b> {profile.get('balance', 1000)} сомони
👥 <b>Клиенты:</b> {profile.get('clients', 0)} чел.
👔 <b>Сотрудники в штате:</b> {profile.get('employees', 0)} чел.
🏢 <b>Открытые филиалы:</b> {len(opened)} шт.

📊 <b>Пассивный доход:</b> +{passive_income} сомони / день"""
        btn_case = "🎲 Случайное событие (Кейс)"
        btn_buy = "🏢 Открыть новый бизнес"
        btn_top = "🏆 Таблица лидеров"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=btn_case, callback_data="game_event"))
    builder.row(InlineKeyboardButton(text=btn_buy, callback_data="game_buy_list"))
    builder.row(InlineKeyboardButton(text=btn_top, callback_data="game_leaders"))

    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(F.data == "game_back")
async def handle_game_back(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)

    from database.models import get_or_create_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)

    level = profile.get("level", 1)
    rank_index = min(level - 1, len(RANKS) - 1)
    rank = RANKS[rank_index]

    businesses_json = profile.get("businesses", "[]") or "[]"
    try:
        opened = json.loads(businesses_json)
    except:
        opened = []

    passive_income = (profile.get("clients", 0) * 2) + (profile.get("employees", 0) * 5) + (len(opened) * 50)

    if lang == "uz":
        text = f"""<b>🎮 TojikAI Biznes Imperiyasi (v2.0)</b>

🏆 <b>Sizning unvoningiz:</b> {rank} (Level {level})
📍 <b>Hozirgi shahar:</b> {profile.get('city', 'Dushanbe')}
💰 <b>Balans:</b> {profile.get('balance', 1000)} somoni
👥 <b>Mijozlar:</b> {profile.get('clients', 0)} ta
👔 <b>Xodimlar jamoasi:</b> {profile.get('employees', 0)} ta
🏢 <b>Ochilgan korxonalar:</b> {len(opened)} ta

📊 <b>Passiv kunlik daromad:</b> +{passive_income} somoni / kuniga"""
        btn_case = "🎲 Tasodifiy voqea (Keys)"
        btn_buy = "🏢 Yangi biznes ochish"
        btn_top = "🏆 Liderlar jadvali"
    elif lang == "tg":
        text = f"""<b>🎮 Империяи Тиҷоратии TojikAI (v2.0)</b>

🏆 <b>Рутбаи шумо:</b> {rank} (Level {level})
📍 <b>Шаҳри фаъол:</b> {profile.get('city', 'Душанбе')}
💰 <b>Тавозун (Баланс):</b> {profile.get('balance', 1000)} сомонӣ
👥 <b>Мизоҷони умумӣ:</b> {profile.get('clients', 0)} нафар
👔 <b>Ҳайати кормандон:</b> {profile.get('employees', 0)} нафар
🏢 <b>Тиҷоратҳои кушода:</b> {len(opened)} адад

📊 <b>Даромади пассиви рӯзона:</b> +{passive_income} сомонӣ / рӯзона"""
        btn_case = "🎲 Ҳодисаи тасодуфӣ (Keys)"
        btn_buy = "🏢 Кушодани тиҷорати нав"
        btn_top = "🏆 Ҷадвали пешсафон"
    else:
        text = f"""<b>🎮 Бизнес Империя TojikAI (v2.0)</b>

🏆 <b>Ваш ранг:</b> {rank} (Уровень {level})
📍 <b>Текущий город:</b> {profile.get('city', 'Душанбе')}
💰 <b>Баланс:</b> {profile.get('balance', 1000)} сомони
👥 <b>Клиенты:</b> {profile.get('clients', 0)} чел.
👔 <b>Сотрудники в штате:</b> {profile.get('employees', 0)} чел.
🏢 <b>Открытые филиалы:</b> {len(opened)} шт.

📊 <b>Пассивный доход:</b> +{passive_income} сомони / день"""
        btn_case = "🎲 Случайное событие (Кейс)"
        btn_buy = "🏢 Открыть новый бизнес"
        btn_top = "🏆 Таблица лидеров"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=btn_case, callback_data="game_event"))
    builder.row(InlineKeyboardButton(text=btn_buy, callback_data="game_buy_list"))
    builder.row(InlineKeyboardButton(text=btn_top, callback_data="game_leaders"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "game_event")
async def handle_game_event(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from gamification.scenarios import BUSINESS_EMPIRE_EVENTS
    event = random.choice(BUSINESS_EMPIRE_EVENTS)

    await state.set_state(GameStates.answering_event)
    await state.update_data(current_event=event, lang=lang)

    text_key = f"text_{lang}"
    event_desc = event.get(text_key, event["text_ru"])

    text = f"<b>🎲 Случайное событие / Ҳодисаи тасодуфӣ</b>\n\n{event_desc}\n\n"

    builder = InlineKeyboardBuilder()
    options = event["options"]
    for opt_key, opt_data in options.items():
        opt_text = opt_data.get(f"text_{lang}", opt_data["text_ru"])
        text += f"<b>{opt_key}.</b> {opt_text}\n"
        builder.row(InlineKeyboardButton(text=f"Выбрать {opt_key} / Интихоб {opt_key}", callback_data=f"ge_opt_{opt_key}"))

    builder.row(InlineKeyboardButton(text="⬅️ Назад / Бозгашт", callback_data="game_back"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(GameStates.answering_event, F.data.startswith("ge_opt_"))
async def handle_game_event_choice(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    event = data.get("current_event")
    lang = data.get("lang", "ru")

    choice = callback.data.replace("ge_opt_", "")
    opt_data = event["options"][choice]

    from database.models import get_or_create_business_empire, update_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)

    new_balance = max(0, profile["balance"] + opt_data.get("balance_diff", 0))
    new_clients = max(0, profile["clients"] + opt_data.get("clients_diff", 0))
    new_employees = max(0, profile["employees"] + opt_data.get("employees_diff", 0))
    new_xp = profile["xp"] + opt_data.get("xp_diff", 0)

    new_level = (new_xp // 100) + 1
    if new_level != profile["level"]:
        level_up = True
    else:
        level_up = False

    new_rank = RANKS[min(new_level - 1, len(RANKS) - 1)]
    new_city = profile.get("city", "Душанбе")
    if level_up:
        new_city = random.choice(CITIES)

    await update_business_empire(
        user_id=user_id,
        balance=new_balance,
        clients=new_clients,
        employees=new_employees,
        level=new_level,
        xp=new_xp,
        businesses=profile["businesses"],
        rank=new_rank,
        city=new_city,
        unlocked_cities=profile.get("unlocked_cities", '["Душанбе"]'),
        employees_hired=profile.get("employees_hired", '{}'),
        achievements=profile.get("achievements", '[]'),
        daily_tasks=profile.get("daily_tasks", '[]')
    )

    diff_text = ""
    if opt_data.get("balance_diff", 0) != 0:
        diff_text += f"💰 {'+' if opt_data['balance_diff'] > 0 else ''}{opt_data['balance_diff']} сомони\n"
    if opt_data.get("clients_diff", 0) != 0:
        diff_text += f"👥 {'+' if opt_data['clients_diff'] > 0 else ''}{opt_data['clients_diff']} клиентов\n"
    if opt_data.get("employees_diff", 0) != 0:
        diff_text += f"👔 {'+' if opt_data['employees_diff'] > 0 else ''}{opt_data['employees_diff']} сотрудников\n"
    if opt_data.get("xp_diff", 0) != 0:
        diff_text += f"🏆 +{opt_data['xp_diff']} XP\n"

    if lang == "uz":
        res_msg = f"<b>Siz tanlagan yechim natijasi:</b>\n\n{diff_text}"
        if level_up:
            res_msg += f"\n🎉 <b>Darajangiz ko'tarildi: {new_level}! Rangingiz: {new_rank}, yangi shahar ochildi: {new_city}!</b>"
    elif lang == "tg":
        res_msg = f"<b>Натиҷаи интихоби шумо:</b>\n\n{diff_text}"
        if level_up:
            res_msg += f"\n🎉 <b>Сатҳи шумо баланд шуд: {new_level}! Рутбаи нав: {new_rank}, шаҳри нав кушода шуд: {new_city}!</b>"
    else:
        res_msg = f"<b>Результаты вашего решения:</b>\n\n{diff_text}"
        if level_up:
            res_msg += f"\n🎉 <b>Поздравляем! Ваш уровень вырос до {new_level}! Новый ранг: {new_rank}, открыт новый город: {new_city}!</b>"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад в империю / Бозгашт", callback_data="game_back"))

    await callback.message.edit_text(res_msg, reply_markup=builder.as_markup(), parse_mode="HTML")
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "game_buy_list")
async def handle_game_buy_list(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from database.models import get_or_create_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)
    try:
        opened = json.loads(profile["businesses"] or "[]")
    except:
        opened = []

    from gamification.scenarios import BUSINESS_TYPES
    text = "<b>🏢 Открытие нового бизнеса / Кушодани тиҷорати нав</b>\n\n"

    builder = InlineKeyboardBuilder()
    for b_key, b_data in BUSINESS_TYPES.items():
        is_opened = b_key in opened
        name = b_data[f"name_{lang}"] if f"name_{lang}" in b_data else b_data["name_ru"]
        desc = b_data[f"desc_{lang}"] if f"desc_{lang}" in b_data else b_data["desc_ru"]

        status_symbol = "✅ Открыто" if is_opened else f"🛒 Купить за {b_data['cost']} сомони"
        text += f"• <b>{name}</b>\n   {desc}\n   Статус: <i>{status_symbol}</i>\n\n"

        if not is_opened:
            builder.row(InlineKeyboardButton(text=f"Купить {name}", callback_data=f"game_buy_{b_key}"))

    builder.row(InlineKeyboardButton(text="⬅️ Назад / Бозгашт", callback_data="game_back"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("game_buy_"))
async def handle_game_buy_action(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    b_key = callback.data.replace("game_buy_", "")

    from database.models import get_or_create_business_empire, update_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)
    try:
        opened = json.loads(profile["businesses"] or "[]")
    except:
        opened = []

    from gamification.scenarios import BUSINESS_TYPES
    b_data = BUSINESS_TYPES.get(b_key)

    if not b_data:
        await callback.answer("Ошибка данных", show_alert=True)
        return

    if b_key in opened:
        await callback.answer("Этот бизнес уже открыт!", show_alert=True)
        return

    if profile["level"] < b_data["required_level"]:
        msg = f"❌ Требуется уровень {b_data['required_level']}."
        await callback.answer(msg, show_alert=True)
        return

    if profile["balance"] < b_data["cost"]:
        msg = f"❌ Недостаточно средств! Требуется {b_data['cost']} сомони."
        await callback.answer(msg, show_alert=True)
        return

    new_balance = profile["balance"] - b_data["cost"]
    opened.append(b_key)

    new_clients = profile["clients"] + random.randint(15, 45)
    new_employees = profile["employees"] + 2

    await update_business_empire(
        user_id=user_id,
        balance=new_balance,
        clients=new_clients,
        employees=new_employees,
        level=profile["level"],
        xp=profile["xp"] + 80,
        businesses=json.dumps(opened),
        rank=profile.get("rank", "Новичок"),
        city=profile.get("city", "Душанбе"),
        unlocked_cities=profile.get("unlocked_cities", '["Душанбе"]'),
        employees_hired=profile.get("employees_hired", '{}'),
        achievements=profile.get("achievements", '[]'),
        daily_tasks=profile.get("daily_tasks", '[]')
    )

    await callback.answer(f"🎉 Вы открыли {b_data['name_ru']}!", show_alert=True)
    await handle_game_buy_list(callback)


@router.callback_query(F.data == "game_leaders")
async def handle_game_leaders(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from database.models import get_business_empire_leaderboard
    leaders = await get_business_empire_leaderboard(limit=10)

    if lang == "tg":
        text = "<b>🏆 Ҷадвали пешсафони Бизнес Империя</b>\n\n"
    else:
        text = "<b>🏆 Лидеры Бизнес Империи</b>\n\n"

    for i, l in enumerate(leaders, 1):
        name = l["username"] or f"Игрок_{l['user_id']}"
        text += f"{i}. <b>{name}</b> — Сатҳ/Уровень: {l['level']} | Баланс: {l['balance']} сомони\n"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад / Бозгашт", callback_data="game_back"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


# ============================================
# CALLBACK: ПОДЕЛИТЬСЯ И ОЦЕНИТЬ
# ============================================

@router.callback_query(F.data == "share_content")
async def share_content(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from database.models import add_bonus_generation
    await add_bonus_generation(user_id, 1)

    text = "✅ +1 генерация за мубодила/шеринг!"
    await callback.answer(text, show_alert=True)


# ============================================
# ОБРАБОТКА НЕИЗВЕСТНЫХ СООБЩЕНИЙ
# ============================================

@router.message()
async def unknown_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)

    if lang == "uz":
        text = "❓ Buyruqni tushunmadim. Pastdagi menudan foydalaning."
    elif lang == "tg":
        text = "❓ Ман фармонро нафаҳмидам. Аз менюи поён истифода баред."
    else:
        text = "❓ Я не понял команду. Используйте меню ниже."

    await message.answer(text, reply_markup=get_main_menu(lang))
