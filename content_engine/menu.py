# content_engine/menu.py — Главный SMM-маркетолог бот TojikAI (v2.2)
# Полноценное интерактивное сопровождение пользователя: Страна -> Ниша -> Платформа -> Цель -> Формат -> Результат -> PDF Генерация -> AI Coach.

import random
import json
import io
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
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
from services.pdf_generator import generate_marketing_pdf
from content_engine.niche_manager import get_all_niches, get_niche_key_by_text, get_niche_name

# Вспомогательная функция для отправки длинных сообщений ИИ
async def send_long_message(message: Message, text: str, reply_markup=None):
    """Отправляет длинные тексты, аккуратно разбивая их по абзацам до 4000 символов"""
    if len(text) <= 4000:
        await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        return

    paragraphs = text.split("\n")
    current_chunk = []
    current_length = 0

    for p in paragraphs:
        if current_length + len(p) + 1 > 4000:
            chunk_text = "\n".join(current_chunk)
            await message.answer(chunk_text, parse_mode="HTML")
            current_chunk = [p]
            current_length = len(p)
        else:
            current_chunk.append(p)
            current_length += len(p) + 1

    if current_chunk:
        chunk_text = "\n".join(current_chunk)
        await message.answer(chunk_text, reply_markup=reply_markup, parse_mode="HTML")

# Проверка, является ли текст кнопкой ниши
def is_niche_button(text: str) -> bool:
    all_names = set()
    for country in ["uz", "tj", "ru"]:
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
    "instagram": {
        "icon": "📷",
        "name_ru": "Instagram", "name_tg": "Instagram", "name_uz": "Instagram",
        "formats": {
            "insta_post": ("📝 Пост", "📝 Постҳо", "📝 Post"),
            "insta_stories": ("📸 Stories", "📸 Сторизҳо", "📸 Stories"),
            "insta_reels": ("🎬 Reels", "🎬 Reels", "🎬 Reels"),
            "insta_plan": ("📅 Контент-план", "📅 Нақшаи контент", "📅 Kontent-reja")
        }
    },
    "tg_channel": {
        "icon": "📱",
        "name_ru": "Telegram", "name_tg": "Telegram", "name_uz": "Telegram",
        "formats": {
            "tg_posts": ("📄 Посты", "📄 Постҳо", "📄 Postlar"),
            "tg_rubrics": ("🗂️ Рубрики", "🗂️ Рубрикаҳо", "🗂️ Rubrikalar"),
            "tg_plan": ("📅 Контент-план", "📅 Нақшаи контент", "📅 Kontent-reja"),
            "tg_ads": ("🤝 Реклама канала", "🤝 Рекламаи канал", "🤝 Kanal reklamasi")
        }
    },
    "tiktok": {
        "icon": "🎵",
        "name_ru": "TikTok", "name_tg": "TikTok", "name_uz": "TikTok",
        "formats": {
            "tiktok_ideas": ("💡 Идеи", "💡 Идеяҳо", "💡 G'oyalar"),
            "tiktok_trends": ("🔥 Тренды", "🔥 Трендҳо", "🔥 Trendlar"),
            "tiktok_scripts": ("🎬 Сценарии", "🎬 Сценарияҳо", "🎬 Ssenariylar"),
            "tiktok_hooks": ("⚡ Хуки & CTA", "⚡ Хукҳо ва CTA", "⚡ Hooklar & CTA")
        }
    },
    "youtube": {
        "icon": "▶️",
        "name_ru": "YouTube", "name_tg": "YouTube", "name_uz": "YouTube",
        "formats": {
            "yt_topics": ("📹 Темы роликов", "📹 Мавзӯъҳои видео", "📹 Video mavzulari"),
            "yt_scripts": ("📋 Сценарии", "📋 Сценарияҳо", "📋 Ssenariylar"),
            "yt_shorts": ("🎥 Shorts", "🎥 Shorts", "🎥 Shorts"),
            "yt_seo": ("🏷️ SEO-заголовки & Описания", "🏷️ Сарлавҳаҳо ва Тавсифҳо", "🏷️ SEO va Tavsiflar")
        }
    },
    "funnel": {
        "icon": "🎯",
        "name_ru": "Воронка продаж", "name_tg": "Воронкаи фурӯш", "name_uz": "Savdo voronkasi",
        "formats": {
            "funnel_magnet": ("🧲 Привлечение (Лид-магнит)", "🧲 Лид-магнит", "🧲 Lead-magnit"),
            "funnel_warm": ("🔥 Прогрев и Доверие", "🔥 Прогрев ва Боварӣ", "🔥 Progrev va Ishonch"),
            "funnel_offer": ("💎 Оффер и Продажа", "💎 Оффер ва Фурӯш", "💎 Offer va Sotuv"),
            "funnel_retain": ("🔄 Удержание клиента", "🔄 Нигоҳдории мизоҷ", "🔄 Mijozni ushlab qolish")
        }
    },
    "ads": {
        "icon": "📢",
        "name_ru": "Реклама", "name_tg": "Реклама", "name_uz": "Reklama",
        "formats": {
            "ads_creative": ("📢 Рекламный креатив", "📢 Креативи рекламавӣ", "📢 Reklama kreativi"),
            "ads_offers": ("🎁 Акции и Офферы", "🎁 Аксия ва Офферҳо", "🎁 Aksiyalar va Offerlar"),
            "ads_strategy": ("🎯 Стратегия кампании", "🎯 Стратегияи реклама", "🎯 Reklama strategiyasi")
        }
    },
    "expert_presets": {
        "icon": "⚡",
        "name_ru": "Пресеты из памяти", "name_tg": "Пресетҳо аз хотира", "name_uz": "Xotira presetlari",
        "formats": {
            "preset_cafe": ("🍔 Кафе и Рестораны", "🍔 Кафе ва Ресторанҳо", "🍔 Kafe va Restoranlar"),
            "preset_beauty": ("💇‍♀️ Салоны красоты", "💇‍♀️ Салонҳои ҳусн", "💇‍♀️ Go'zallik salonlari"),
            "preset_shop": ("👗 Магазины одежды", "👗 Мағозаҳои либос", "👗 Kiyim do'konlari"),
            "preset_auto": ("🚗 Автосервисы", "🚗 Автосервисҳо", "🚗 Avtoservislar"),
            "preset_realestate": ("🏢 Недвижимость", "🏢 Хонаҳо/Иҷора", "🏢 Ko'chmas mulk")
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
    "🤖 Задать вопрос", "🤖 Саволи худ", "🤖 Savol berish",
    "💡 Советы AI", "💡 Тавсияҳо", "💡 AI tavsiyalar",
    "📚 Инструкция", "📚 Дастур", "📚 Qo'llanma",
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
    elif text in ["🤖 Задать вопрос", "🤖 Саволи худ", "🤖 Savol berish"]:
        await start_ai_assistant(message, state)
    elif text in ["💡 Советы AI", "💡 Тавсияҳо", "💡 AI tavsiyalar"]:
        await show_personal_recommendations(message, state)
    elif text in ["📚 Инструкция", "📚 Дастур", "📚 Qo'llanma"]:
        await show_onboarding_guide(message, state)
    elif text in ["📞 Поддержка", "📞 Дастгирӣ", "📞 Yordam / Aloqa"]:
        await support_menu(message, state)


# ============================================
# ЛОКАЛИЗАЦИОННЫЕ ТЕКСТЫ С БРЕНДОМ TojikAI
# ============================================

TEXTS = {
    "ru": {
        "welcome": "👋 Добро пожаловать в <b>TojikAI</b>!\n\n🤖 Я — AI-платформа, которая создаёт вирусный SMM-контент для бизнеса.\n\n<b>Выберите язык / Забонро интихоб кунед:</b>",
        "main_menu": "👋 Главное меню\n\n✨ Выберите, что создать:",
        "choose_niche": "🏢 Для какого бизнеса нужен контент?",
        "choose_tool": "⚡ <b>SMM & Media Платформа TojikAI</b>\n\nНиша выбрана: <b>{niche}</b>\n\nВыберите инструмент продвижения бизнеса:",
        "choose_goal": "🎯 <b>Шаг 1: Выберите цель продвижения</b>\n\nКакого результата вы хотите достичь?",
        "choose_format": "👇 <b>Шаг 2: Выберите желаемый формат контента</b> для платформы <b>{platform}</b>:",
        "generating": "⏳ Генерирую профессиональный маркетинговый пакет через ИИ...\n\nЭто займет несколько секунд...",
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
        "choose_goal": "🎯 <b>Қадами 1: Ҳадафи пешбурдро интихоб кунед</b>\n\nШумо мехоҳед ба кадом натиҷа бирасед?",
        "choose_format": "👇 <b>Қадами 2: Формати дилхоҳи контентро интихоб кунед</b> барои <b>{platform}</b>:",
        "generating": "⏳ AI пакети касбии маркетингиро месозад...\n\nЧанд сония вақт мегирад...",
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
        "choose_goal": "🎯 <b>1-qadam: Rivojlanish maqsadini tanlang</b>\n\nQanday natijaga erishmoqchisiz?",
        "choose_format": "👇 <b>2-qadam: Kerakli kontent formatini tanlang</b> <b>{platform}</b> uchun:",
        "generating": "⏳ AI orqali professional marketing paketi yaratilmoqda...\n\nBu bir necha soniya vaqt oladi...",
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
    selecting_tool = State()    # Выбор платформы/категории
    selecting_goal = State()    # Шаг 1: Цель продвижения
    selecting_format = State()  # Шаг 2: Формат контента
    asking_assistant = State()


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
    return "instagram"


@router.message(SMMHubStates.selecting_tool, lambda msg: is_smm_tool_button(msg.text))
async def smm_tool_selected(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # ПРЕДОТВРАЩЕНИЕ ПОТЕРИ КОНТЕКСТА: Загружаем из БД, если стерлось в FSM
    data = await state.get_data()
    lang = data.get("language")
    country = data.get("country")
    niche_key = data.get("niche")

    user = await get_user(user_id)
    if user:
        if not lang: lang = user.get("language", "ru")
        if not country: country = user.get("country", "uz")

    lang = lang or "ru"
    country = country or "uz"
    niche_key = niche_key or ("cafe_uz" if country == "uz" else "wholesale_tj")

    await state.update_data(language=lang, country=country, niche=niche_key)

    tool_id = get_tool_id_by_text(message.text, lang)
    await state.update_data(current_tool=tool_id)

    # ШАГ 1: ВЫБОР ЦЕЛИ ПРОДВИЖЕНИЯ
    await state.set_state(SMMHubStates.selecting_goal)

    # Локализованные кнопки целей
    if lang == "uz":
        btn_sales = "📈 Sotuvlar"
        btn_subs = "👥 Obunachilar"
        btn_brand = "📢 Taniqlilik (Brend)"
        btn_leads = "🎯 Leadlar (So'rovlar)"
        btn_personal = "💎 Shaxsiy brend"
        back_text = "⬅️ Asboblar menyusiga"
    elif lang == "tg":
        btn_sales = "📈 Фурӯш"
        btn_subs = "👥 Обуначиён"
        btn_brand = "📢 Шинохташавӣ (Бренд)"
        btn_leads = "🎯 Дархостҳо (Лидҳо)"
        btn_personal = "💎 Бренди шахсӣ"
        back_text = "⬅️ Ба менюи асбобҳо"
    else:
        btn_sales = "📈 Продажи"
        btn_subs = "👥 Подписчики"
        btn_brand = "📢 Узнаваемость (Бренд)"
        btn_leads = "🎯 Лиды (Заявки)"
        btn_personal = "💎 Личный бренд"
        back_text = "⬅️ В меню инструментов"

    buttons = [
        [KeyboardButton(text=btn_sales), KeyboardButton(text=btn_subs)],
        [KeyboardButton(text=btn_brand), KeyboardButton(text=btn_leads)],
        [KeyboardButton(text=btn_personal)],
        [KeyboardButton(text=back_text)]
    ]

    prompt = await get_text(user_id, "choose_goal", state)

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
# ШАГ 2: ОБРАБОТКА ВЫБОРА ЦЕЛИ И ПЕРЕХОД К ФОРМАТУ
# ============================================

def is_goal_button(text: str) -> bool:
    text_clean = text.lower()
    return any(x in text_clean for x in ["продажи", "подписчики", "узнаваемость", "лиды", "личный", "sotuv", "obunach", "taniql", "lead", "shaxsiy", "фурӯш", "обунач", "шинохт", "дархост", "бренд"])


@router.message(SMMHubStates.selecting_goal, lambda msg: is_goal_button(msg.text))
async def smm_goal_selected(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    tool_id = data.get("current_tool", "instagram")

    # Сохраняем цель в стейт
    await state.update_data(current_goal=message.text)

    # Переходим к выбору формата контента (Шаг 2)
    await state.set_state(SMMHubStates.selecting_format)

    tool_data = SMM_TOOLS[tool_id]
    tool_name = tool_data[f"name_{lang}"] if f"name_{lang}" in tool_data else tool_data["name_ru"]

    buttons = []
    row = []
    idx = 0 if lang == "ru" else (1 if lang == "tg" else 2)

    for format_id, names_tuple in tool_data["formats"].items():
        btn_text = names_tuple[idx] if idx < len(names_tuple) else names_tuple[0]
        row.append(KeyboardButton(text=btn_text))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    back_text = "⬅️ Изменить цель" if lang == "ru" else ("⬅️ Тағйири ҳадаф" if lang == "tg" else "⬅️ Maqsadni o'zgartirish")
    buttons.append([KeyboardButton(text=back_text)])

    prompt = await get_text(user_id, "choose_format", state, platform=tool_name)

    await message.answer(
        prompt,
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True),
        parse_mode="HTML"
    )


@router.message(SMMHubStates.selecting_goal, F.text.regexp(r"^⬅️"))
async def back_from_goal_to_tool(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    niche_key = data.get("niche", "cafe_uz")

    await show_smm_hub_menu(message, state, user_id, lang, niche_key)


# ============================================
# ШАГ 3: ОБРАБОТКА ФОРМАТА И ЗАПУСК AI-МАРКЕТОЛОГА (И ОТПРАВКА БРЕНДИРОВАННОГО PDF)
# ============================================

def is_smm_format_button(text: str, current_tool: str, lang: str = "ru") -> bool:
    if current_tool not in SMM_TOOLS:
        return False
    tool_data = SMM_TOOLS[current_tool]
    cleaned = text.strip()
    idx = 0 if lang == "ru" else (1 if lang == "tg" else 2)

    for format_id, names_tuple in tool_data["formats"].items():
        btn_text = names_tuple[idx] if idx < len(names_tuple) else names_tuple[0]
        if cleaned == btn_text or cleaned == names_tuple[0]:
            return True
    return False


def get_format_id_by_text(text: str, current_tool: str, lang: str = "ru") -> str:
    tool_data = SMM_TOOLS[current_tool]
    cleaned = text.strip()
    idx = 0 if lang == "ru" else (1 if lang == "tg" else 2)

    for format_id, names_tuple in tool_data["formats"].items():
        btn_text = names_tuple[idx] if idx < len(names_tuple) else names_tuple[0]
        if cleaned == btn_text or cleaned == names_tuple[0]:
            return format_id
    return list(tool_data["formats"].keys())[0]


@router.message(SMMHubStates.selecting_format, F.text.regexp(r"^⬅️"))
async def back_from_format_to_goal(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    tool_id = data.get("current_tool", "instagram")

    class FakeMessage:
        def __init__(self, text, from_user):
            self.text = text
            self.from_user = from_user
        async def answer(self, text, reply_markup=None, parse_mode=None):
            return await message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)

    fake = FakeMessage(text=f"{SMM_TOOLS[tool_id]['icon']} {SMM_TOOLS[tool_id][f'name_{lang}']}", from_user=message.from_user)
    await smm_tool_selected(fake, state)


@router.message(SMMHubStates.selecting_format)
async def handle_smm_generation_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    # 100% защита от потери контекста
    lang = data.get("language")
    country = data.get("country")
    niche_key = data.get("niche")
    current_tool = data.get("current_tool", "instagram")
    current_goal = data.get("current_goal", "Продажи")

    user = await get_user(user_id)
    if user:
        if not lang: lang = user.get("language", "ru")
        if not country: country = user.get("country", "uz")

    lang = lang or "ru"
    country = country or "uz"
    niche_key = niche_key or ("cafe_uz" if country == "uz" else "wholesale_tj")

    await state.update_data(language=lang, country=country, niche=niche_key)

    if not is_smm_format_button(message.text, current_tool, lang):
        await message.answer("❌ Выберите один из форматов в меню ниже.")
        return

    format_id = get_format_id_by_text(message.text, current_tool, lang)

    if current_tool == "expert_presets":
        preset_key = format_id.replace("preset_", "")  # "cafe", "beauty", etc.
        await state.update_data(current_preset_key=preset_key)

        # Present beautiful Inline Keyboard to choose the type of SMM content
        builder = InlineKeyboardBuilder()
        if lang == "uz":
            txt = "⚡️ <b>Ekspert SMM Presetlari</b>\n\nQuyidagi tayyor, professional va yuqori sifatli SMM andozalaridan birini tanlang:"
            builder.row(InlineKeyboardButton(text="📅 Haftalik kontent-reja", callback_data="preset_type_plan"))
            builder.row(InlineKeyboardButton(text="📝 Premium SMM Post", callback_data="preset_type_posts"))
            builder.row(InlineKeyboardButton(text="🎬 Viral Reels ssenariysi", callback_data="preset_type_reels"))
            builder.row(InlineKeyboardButton(text="📸 Stories progressiv zanjiri", callback_data="preset_type_stories"))
            builder.row(InlineKeyboardButton(text="📢 Target reklama nusxalari", callback_data="preset_type_ads"))
            builder.row(InlineKeyboardButton(text="🎯 Sotuv voronkasi", callback_data="preset_type_funnel"))
            builder.row(InlineKeyboardButton(text="💡 30 ta tayyor g'oya", callback_data="preset_type_ideas"))
            builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="go_to_smm_hub"))
        elif lang == "tg":
            txt = "⚡️ <b>Пресетҳои Эксперти SMM</b>\n\nYке аз қолабҳои тайёр ва босифати касбиро барои тиҷорати худ интихоб кунед:"
            builder.row(InlineKeyboardButton(text="📅 Нақшаи контенти 7-рӯза", callback_data="preset_type_plan"))
            builder.row(InlineKeyboardButton(text="📝 Пости касбии фурӯш", callback_data="preset_type_posts"))
            builder.row(InlineKeyboardButton(text="🎬 Сценарияи Reels-и вирусӣ", callback_data="preset_type_reels"))
            builder.row(InlineKeyboardButton(text="📸 Силсилаи Сторизҳои прогрев", callback_data="preset_type_stories"))
            builder.row(InlineKeyboardButton(text="📢 Намунаҳои Рекламаи target", callback_data="preset_type_ads"))
            builder.row(InlineKeyboardButton(text="🎯 Воронкаи фурӯши тайёр", callback_data="preset_type_funnel"))
            builder.row(InlineKeyboardButton(text="💡 30 идеяи ҷолиб", callback_data="preset_type_ideas"))
            builder.row(InlineKeyboardButton(text="⬅️ Бозгашт", callback_data="go_to_smm_hub"))
        else:
            txt = "⚡️ <b>Экспертные SMM Пресеты из памяти</b>\n\nВыберите один из готовых, высококонверсионных профессиональных шаблонов для вашего бизнеса:"
            builder.row(InlineKeyboardButton(text="📅 Еженедельный контент-план", callback_data="preset_type_plan"))
            builder.row(InlineKeyboardButton(text="📝 Премиальный продающий пост", callback_data="preset_type_posts"))
            builder.row(InlineKeyboardButton(text="🎬 Сценарий вирусного Reels", callback_data="preset_type_reels"))
            builder.row(InlineKeyboardButton(text="📸 Серия прогревающих Stories", callback_data="preset_type_stories"))
            builder.row(InlineKeyboardButton(text="📢 Варианты рекламы для таргета", callback_data="preset_type_ads"))
            builder.row(InlineKeyboardButton(text="🎯 Автоворонка продаж в директ", callback_data="preset_type_funnel"))
            builder.row(InlineKeyboardButton(text="💡 30 вирусных идей", callback_data="preset_type_ideas"))
            builder.row(InlineKeyboardButton(text="⬅️ Назад в меню SMM", callback_data="go_to_smm_hub"))

        await message.answer(txt, reply_markup=builder.as_markup(), parse_mode="HTML")
        return

    # Проверка лимитов
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
        # 1. Генерируем полный структурированный профессиональный пакет контента через OpenAI
        niche_name = get_niche_name(niche_key, lang)
        topic_prompt = (
            f"Создай полноценный TojikAI Marketing Package для ниши [{niche_name}]. "
            f"Пакет должен строго включать: "
            f"1. Анализ ниши (конкуренты, боли, потребности, преимущества). "
            f"2. Контент-план на 7-14 дней. "
            f"3. Готовый продающий SMM-Пост. "
            f"4. Сценарий Stories из 5 слайдов. "
            f"5. Полный сценарий Reels/Shorts (Хук, Реплики, Описание кадров). "
            f"6. Рекламные офферы и Чек-лист следующих действий SMM коуча."
        )

        content = await generate_ai_content(
            topic=topic_prompt,
            niche=niche_key,
            language=lang,
            content_type=current_tool,
            country=country,
            subtool=format_id
        )

        sub = await get_user_subscription(user_id)
        if not sub or sub.get("plan") == "free":
            content += f"\n\n─────────────\n{WATERMARK_TEXT}"

        await processing_msg.delete()

        # Выводим текстовый пакет в телеграм чат (безопасно разделяя по лимитам символов Telegram)
        await send_long_message(
            message,
            f"🚀 <b>TojikAI SMM Marketing Package</b>\n\n{content}"
        )

        # 2. АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ И ОТПРАВКА БРЕНДИРОВАННОГО PDF-ОТЧЕТА
        pdf_msg = await message.answer("⚙️ <b>Создаю брендированный PDF-отчет...</b>")
        try:
            pdf_buffer = generate_marketing_pdf(
                country=country,
                language=lang,
                niche=niche_name,
                platform=current_tool.upper(),
                goal=current_goal,
                content_text=content
            )
            pdf_file = BufferedInputFile(pdf_buffer.getvalue(), filename=f"TojikAI_Marketing_Package_{niche_key}.pdf")

            await message.answer_document(
                pdf_file,
                caption=f"📄 <b>TojikAI Marketing Package</b>\n\nВаш готовый, профессионально оформленный маркетинговый отчет для ниши <b>{niche_name}</b>!",
                parse_mode="HTML"
            )
            await pdf_msg.delete()
        except Exception as pdf_err:
            await pdf_msg.edit_text(f"⚠️ Ошибка создания PDF: {str(pdf_err)}")

        # 3. ИНТЕРАКТИВНЫЙ AI-КОУЧ ПОСЛЕ ГЕНЕРАЦИИ (Follow-up Actions)
        builder = InlineKeyboardBuilder()

        if lang == "uz":
            btn_story = "📸 30 ta yangi g'oyalar"
            btn_reels = "🎬 Reels ssenariylari"
            btn_plan = "📅 Kontent-reja tuzish"
            btn_ad = "📢 Reklama yaratish"
            btn_funnel = "🎯 Sotuv voronkasi"
            btn_assistant = "🤖 AI g'oyalar ko'chidan so'rash"
            btn_hub = "⬅️ SMM Menuga qaytish"
        elif lang == "tg":
            btn_story = "📸 Сохтани 30 идеяи нав"
            btn_reels = "🎬 Сценарияҳои Reels"
            btn_plan = "📅 Нақшаи контент"
            btn_ad = "📢 Навиштани Реклама"
            btn_funnel = "🎯 Воронкаи фурӯш"
            btn_assistant = "🤖 Савол додан ба AI-Коуч"
            btn_hub = "⬅️ Бозгашт ба менюи SMM"
        else:
            btn_story = "📸 Создать ещё 30 идей"
            btn_reels = "🎬 Создать сценарии Reels"
            btn_plan = "📅 Создать контент на месяц"
            btn_ad = "📢 Создать рекламу"
            btn_funnel = "🎯 Создать воронку продаж"
            btn_assistant = "🤖 Спросить AI-Коуча"
            btn_hub = "⬅️ Назад в меню SMM"

        builder.row(InlineKeyboardButton(text=btn_story, callback_data="qa_ideas"))
        builder.row(InlineKeyboardButton(text=btn_reels, callback_data="qa_reels"))
        builder.row(InlineKeyboardButton(text=btn_plan, callback_data="qa_plan"))
        builder.row(InlineKeyboardButton(text=btn_ad, callback_data="qa_ads"))
        builder.row(InlineKeyboardButton(text=btn_funnel, callback_data="qa_funnel"))
        builder.row(InlineKeyboardButton(text=btn_assistant, callback_data="qa_assistant"))
        builder.row(InlineKeyboardButton(text=btn_hub, callback_data="go_to_smm_hub"))

        await message.answer(
            "<b>🎯 Что вы хотите сделать дальше? AI-Коуч TojikAI готов продолжить работу:</b>",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

        # Сохраняем генерацию в историю БД
        await save_generation(
            user_id=user_id,
            niche=niche_name,
            topic=f"Платформа: {current_tool.upper()} | Цель: {current_goal} | Формат: {message.text}",
            content=content
        )

        if not is_admin:
            await increment_generation(user_id)

    except Exception as e:
        err_msg = f"❌ Ошибка генерации ИИ: {str(e)[:150]}"
        await processing_msg.edit_text(err_msg)


@router.callback_query(F.data == "go_to_smm_hub")
async def go_to_smm_hub_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    niche_key = data.get("niche", "cafe_uz")

    await callback.answer()
    await show_smm_hub_menu(callback.message, state, user_id, lang, niche_key)


@router.callback_query(F.data.startswith("preset_type_"))
async def handle_preset_type_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()

    lang = data.get("language", "ru")
    preset_key = data.get("current_preset_key", "cafe")
    preset_type = callback.data.replace("preset_type_", "")

    from data.smm_memory_db import SMM_EXPERT_PRESETS

    preset_data = SMM_EXPERT_PRESETS.get(preset_key, SMM_EXPERT_PRESETS["cafe"])
    lang_data = preset_data.get(lang, preset_data["ru"])
    content = lang_data.get(preset_type, "Шаблон временно недоступен.")

    niche_name = preset_data[f"name_{lang}"] if f"name_{lang}" in preset_data else preset_data["name_ru"]

    await callback.message.delete()

    processing_msg = await callback.message.answer("⚡️ <b>Извлекаю премиум пресет из памяти...</b>", parse_mode="HTML")
    await asyncio.sleep(0.5)
    await processing_msg.delete()

    header = f"⚡️ <b>TojikAI Expert Preset: {niche_name}</b>\n"
    header += f"📌 <b>Формат:</b> {preset_type.upper()}\n\n"

    await send_long_message(
        callback.message,
        f"{header}{content}"
    )

    # Автоматическое создание брендированного PDF
    pdf_msg = await callback.message.answer("⚙️ <b>Создаю брендированный PDF-отчет...</b>")
    try:
        from services.pdf_generator import generate_marketing_pdf
        pdf_buffer = generate_marketing_pdf(
            country=data.get("country", "uz"),
            language=lang,
            niche=niche_name,
            platform="PRESET_MEMORY",
            goal=preset_type.upper(),
            content_text=content
        )
        pdf_file = BufferedInputFile(pdf_buffer.getvalue(), filename=f"TojikAI_Expert_Preset_{preset_key}_{preset_type}.pdf")

        await callback.message.answer_document(
            pdf_file,
            caption=f"📄 <b>TojikAI Expert Preset Report</b>\n\nВаш готовый, профессионально оформленный маркетинговый отчет на основе премиум-пресета для ниши <b>{niche_name}</b>!",
            parse_mode="HTML"
        )
        await pdf_msg.delete()
    except Exception as pdf_err:
        await pdf_msg.edit_text(f"⚠️ Ошибка создания PDF: {str(pdf_err)}")

    builder = InlineKeyboardBuilder()
    back_lbl = "⬅️ Назад в меню SMM" if lang == "ru" else ("⬅️ Бозгашт ба меню" if lang == "tg" else "⬅️ SMM Menuga qaytish")
    builder.row(InlineKeyboardButton(text=back_lbl, callback_data="go_to_smm_hub"))
    await callback.message.answer(
        "<b>Премиум шаблон успешно доставлен! Хотите выбрать другой?</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


# ============================================
# 🤖 AI-АССИСТЕНТ (ЗАДАТЬ СВОЙ ВОПРОС)
# ============================================

async def start_ai_assistant(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)
    await state.set_state(SMMHubStates.asking_assistant)

    if lang == "uz":
        text = "🤖 <b>TojikAI Sun'iy Intellekt Assisenti</b>\n\nSizni qiziqtirgan istalgan savolni yozing (masalan, 'Qanday qilib kargo biznesini ochish mumkin?'). Assistent sizga darhol javob beradi va uni kontentga aylantirishga yordam beradi."
    elif lang == "tg":
        text = "🤖 <b>Ёвари интеллектуалӣ (AI) TojikAI</b>\n\nСаволи худро бинависед (масалан, 'Чӣ тавр маҳсулоти чаканро дар Душанбе реклама кунем?'). Ман ба шумо кумак мекунам ва онро ба контент табдил медиҳам."
    else:
        text = "🤖 <b>AI-Ассистент TojikAI</b>\n\nЗадайте абсолютно любой вопрос по маркетингу или бизнесу (например, 'Как увеличить продажи текстиля в Ташкенте?'). Бот ответит и предложит превратить этот вопрос в готовый контент!"

    await message.answer(text, parse_mode="HTML")


@router.message(SMMHubStates.asking_assistant)
async def handle_ai_assistant_query(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    country = data.get("country", "uz")
    niche_key = data.get("niche", "cafe_uz")

    processing_msg = await message.answer("⏳ Думаю над вашим вопросом / Дар бораи саволи шумо фикр мекунам...", parse_mode="HTML")

    try:
        from services.openai_service import generate_content
        system_prompt = f"You are TojikAI assistant. Answer the user question comprehensively under {country.upper()} market context. Keep the answer highly professional and encouraging."
        answer = generate_content(
            system_prompt=system_prompt,
            user_prompt=message.text,
            language=lang
        )

        await processing_msg.delete()

        await state.update_data(assistant_topic=message.text)

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="📄 Создать пост", callback_data="qa_post"))
        builder.row(InlineKeyboardButton(text="📸 Создать Stories", callback_data="qa_stories"))
        builder.row(InlineKeyboardButton(text="🎬 Создать Reels", callback_data="qa_reels"))
        builder.row(InlineKeyboardButton(text="📅 Создать контент-план", callback_data="qa_plan"))
        builder.row(InlineKeyboardButton(text="📢 Создать рекламу", callback_data="qa_ads"))

        await message.answer(
            f"🤖 <b>Ответ TojikAI:</b>\n\n{answer}\n\n👇 <b>Быстрые SMM действия на основе вашего вопроса:</b>",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

    except Exception as e:
        await processing_msg.edit_text(f"❌ Ошибка ИИ: {str(e)[:150]}")


@router.callback_query(F.data.startswith("qa_"))
async def handle_quick_action(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()

    lang = data.get("language")
    country = data.get("country")
    niche_key = data.get("niche")
    topic = data.get("assistant_topic", "Бизнес и SMM")

    user = await get_user(user_id)
    if user:
        if not lang: lang = user.get("language", "ru")
        if not country: country = user.get("country", "uz")

    lang = lang or "ru"
    country = country or "uz"
    niche_key = niche_key or ("cafe_uz" if country == "uz" else "wholesale_tj")

    action = callback.data.replace("qa_", "")
    await callback.answer("⏳ Создаю контент...")

    processing_msg = await callback.message.answer("⏳ Генерирую SMM материал...")
    try:
        content = await generate_ai_content(
            topic=topic,
            niche=niche_key,
            language=lang,
            content_type=action,
            country=country,
            subtool=f"qa_{action}"
        )

        sub = await get_user_subscription(user_id)
        if not sub or sub.get("plan") == "free":
            content += f"\n\n─────────────\n{WATERMARK_TEXT}"

        await processing_msg.delete()
        await send_long_message(callback.message, content, reply_markup=get_share_keyboard(lang))
    except Exception as e:
        await processing_msg.edit_text(f"❌ Ошибка: {str(e)[:100]}")


# ============================================
# 💡 УМНЫЕ ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ И СОВЕТЫ AI
# ============================================

async def show_personal_recommendations(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")
    country = data.get("country", "uz")
    niche_key = data.get("niche", "cafe_uz")

    user = await get_user(user_id)
    if user:
        if not country: country = user.get("country", "uz")
        if not lang: lang = user.get("language", "ru")

    niche_name = get_niche_name(niche_key, lang)
    processing_msg = await message.answer("⏳ Анализирую тренды рынка и ниши...")

    try:
        from services.openai_service import generate_content
        system_prompt = f"You are a marketing strategist. Provide 3 highly personalized, actionable SMM and sales tips for a business in niche: {niche_name} in {country.upper()} context. Do not mention other countries."
        tips = generate_content(
            system_prompt=system_prompt,
            user_prompt=f"Дай советы для ниши {niche_name} в {country.upper()}",
            language=lang
        )

        await processing_msg.delete()
        await message.answer(
            f"💡 <b>Персональные рекомендации для ниши [{niche_name}]:</b>\n\n{tips}",
            parse_mode="HTML"
        )
    except Exception as e:
        await processing_msg.edit_text(f"❌ Ошибка получения советов: {str(e)[:100]}")


# ============================================
# 📚 ИНТЕРАКТИВНОЕ ОБУЧЕНИЕ: КАК ПОЛЬЗОВАТЬСЯ TojikAI
# ============================================

async def show_onboarding_guide(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("language", "ru")

    if lang == "uz":
        guide = """<b>📚 TojikAI Platformasidan foydalanish bo'yicha qo'llanma</b>

1️⃣ <b>Soha (Nisha) va Davlatni tanlang:</b>
Bot sizga O'zbekiston yoki Tojikiston realiyalari va valyutasiga moslashtirilgan kontent taqdim etishi uchun boshida to'g'ri sozlamani kiriting.

2️⃣ <b>SMM & Media Hub:</b>
Sohani tanlaganingizdan so'ng, sizga 12 ta kuchli SMM vositalari ochiladi (Postlar, Stories, Reels, Kontent-reja, Savdo voronkasi va boshqalar).

3️⃣ <b>AI Assistent ("Savol berish"):</b>
Istalgan marketing muammongizni botga o'z tilingizda yozing va tayyor javobni bir zumda Reels yoki Postga aylantiring!

4️⃣ <b>TojikAI Empire O'yini:</b>
Biznes imperiyangizni rivojlantiring, xodimlar yollang, haftalik turnirlarda qatnashing va bepul bonus generatsiyalarni qo'lga kiriting!

5️⃣ <b>Hamkorlik (Referal):</b>
Do'stlaringizni taklif qiling, ular orqali ballar to'plang va status (Tier) tizimi orqali mutlaqo bepul Premium obunalarni faollashtiring!"""
    elif lang == "tg":
        guide = """<b>📚 Дастури истифодабарии платформаи TojikAI</b>

1️⃣ <b>Интихоби Ниша ва Шаҳр:</b>
Аввал кишвар ва нишаро интихоб намоед, то ИИ мундодро махсус барои бозори Тоҷикистон омода созад.

2️⃣ <b>SMM & Media Хаб:</b>
Пас аз интихоби ниша 12 асбоби пешбурди тиҷорат (Постҳо, Сториз, Сценарияи Reels, Воронкаи фурӯш, Реклама) бароятон дастрас мегардад.

3️⃣ <b>Ёвари AI (Савол додан):</b>
Саволи худро бинависед ва бо ёрии ChatGPT посухи касбӣ гирифта, онро ба паём табдил диҳед.

4️⃣ <b>Бозии TojikAI Empire:</b>
Империяи худро созед, даромади пассивӣ гиред, квестро иҷро намуда генерацияҳои ройгон ба даст оред!

5️⃣ <b>Барномаи даъватӣ (Рефералка):</b>
Дӯстонро даъват кунед ва соҳиби холҳо ва обунаи Premium-и ройгон шавед!"""
    else:
        guide = """<b>📚 Интерактивная инструкция по TojikAI</b>

1️⃣ <b>Выбор страны и ниши:</b>
Бот разделяет все сценарии. Если вы выбрали Таджикистан — контент будет сомонях, про Корвон и Alif. Если Узбекистан — в сумах, про Uzum и Сергели.

2️⃣ <b>SMM & Media Хаб:</b>
Вам доступны 12 видов профессиональных инструментов (Посты, Stories, Сценарии Reels/Shorts, Автоворонки, Готовые контент-планы и Креативы) в один клик.

3️⃣ <b>Умный AI-Ассистент:</b>
Нажмите кнопку "🤖 Задать вопрос", напишите ваш запрос (например: 'Как запустить карго?'), и бот моментально выдаст ответ с возможностью сразу переделать его в пост или Reels!

4️⃣ <b>Игра TojikAI Empire:</b>
Развивайте виртуальный бизнес, выполняйте задания, нанимайте персонал, забирайте пассивный доход и получайте бесплатные генерации в награду!

5️⃣ <b>Многоуровневая реферальная система:</b>
Приглашайте коллег, копите баллы и открывайте бесплатный Premium-доступ на срок до 1 года!"""

    await message.answer(guide, parse_mode="HTML")


# ============================================
# РЕФЕРАЛЬНАЯ СИСТЕМА
# ============================================

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


async def support_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(await get_text(user_id, "support", state), parse_mode="HTML")


# ============================================
# ГЕЙМИФИКАЦИЯ: TojikAI Empire
# ============================================

RANKS = ["Новичок", "Предприниматель", "Бизнесмен", "Инвестор", "Магнат", "Миллионер", "Миллиардер", "Легенда бизнеса"]
CITIES = ["Душанбе", "Худжанд", "Бохтар", "Куляб", "Ташкент", "Самарканд", "Бухара"]

async def start_business_game(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    await state.update_data(language=lang)

    from database.models import get_or_create_business_empire
    profile = await get_or_create_business_empire(user_id, message.from_user.username)

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
        text = f"""<b>🚀 TojikAI Empire — Biznes va Media Simulyatori (v2.1)</b>

🏆 <b>Unvoningiz:</b> {rank} ({level}-daraja)
📍 <b>Hozirgi shahar:</b> {profile.get('city', 'Dushanbe')}
💰 <b>Kassa:</b> {profile.get('balance', 1000)} somoni
👥 <b>Faol mijozlar:</b> {profile.get('clients', 0)} ta
👔 <b>Xodimlar jamoasi:</b> {profile.get('employees', 0)} ta
🏢 <b>Ochilgan filiallar:</b> {len(opened)} ta

📈 <b>Kunlik passiv daromad:</b> +{passive_income} somoni / kuniga"""
        btn_case = "🎲 Tasodifiy voqea (Keys)"
        btn_buy = "🏢 Yangi filial ochish"
        btn_staff = "👔 Jamoani kengaytirish"
        btn_achieve = "🎖️ Mening yutuqlarim"
        btn_top = "🏆 Turnir / Liderlar"
    elif lang == "tg":
        text = f"""<b>🚀 TojikAI Empire — Симулятори Тиҷорат ва Медиа (v2.1)</b>

🏆 <b>Рутбаи шумо:</b> {rank} (Сатҳи {level})
📍 <b>Шаҳри фаъол:</b> {profile.get('city', 'Душанбе')}
💰 <b>Хазина:</b> {profile.get('balance', 1000)} сомонӣ
👥 <b>Мизоҷони доимӣ:</b> {profile.get('clients', 0)} нафар
👔 <b>Ҳайати кормандон:</b> {profile.get('employees', 0)} нафар
🏢 <b>Филиалҳои кушода:</b> {len(opened)} адад

📈 <b>Даромади пассиви рӯзона:</b> +{passive_income} сомонӣ / рӯзона"""
        btn_case = "🎲 Ҳодисаи тасодуфӣ (Keys)"
        btn_buy = "🏢 Кушодани филиали нав"
        btn_staff = "👔 Кормандон ва Мутахассисон"
        btn_achieve = "🎖️ Дастовардҳои ман"
        btn_top = "🏆 Мусобиқа / Пешсафон"
    else:
        text = f"""<b>🚀 TojikAI Empire — Симулятор Бизнеса и Медиа (v2.1)</b>

🏆 <b>Ваш ранг:</b> {rank} (Уровень {level})
📍 <b>Текущий город:</b> {profile.get('city', 'Душанбе')}
💰 <b>Баланс Кассы:</b> {profile.get('balance', 1000)} сомони
👥 <b>Клиенты:</b> {profile.get('clients', 0)} чел.
👔 <b>Сотрудники в штате:</b> {profile.get('employees', 0)} чел.
🏢 <b>Открытые филиалы:</b> {len(opened)} шт.

📊 <b>Пассивный доход:</b> +{passive_income} сомони / день"""
        btn_case = "🎲 Случайное событие (Кейс)"
        btn_buy = "🏢 Открыть новый филиал"
        btn_staff = "👔 Нанять персонал"
        btn_achieve = "🎖️ Мои Достижения"
        btn_top = "🏆 Турниры / Лидеры"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=btn_case, callback_data="game_event"))
    builder.row(InlineKeyboardButton(text=btn_buy, callback_data="game_buy_list"))
    builder.row(InlineKeyboardButton(text=btn_staff, callback_data="game_staff_list"))
    builder.row(InlineKeyboardButton(text=btn_achieve, callback_data="game_achievements"))
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
        text = f"""<b>🚀 TojikAI Empire — Biznes va Media Simulyatori (v2.1)</b>

🏆 <b>Unvoningiz:</b> {rank} ({level}-daraja)
📍 <b>Hozirgi shahar:</b> {profile.get('city', 'Dushanbe')}
💰 <b>Kassa:</b> {profile.get('balance', 1000)} somoni
👥 <b>Faol mijozlar:</b> {profile.get('clients', 0)} ta
👔 <b>Xodimlar jamoasi:</b> {profile.get('employees', 0)} ta
🏢 <b>Ochilgan filiallar:</b> {len(opened)} ta

📈 <b>Kunlik passiv daromad:</b> +{passive_income} somoni / kuniga"""
    elif lang == "tg":
        text = f"""<b>🚀 TojikAI Empire — Симулятори Тиҷорат ва Медиа (v2.1)</b>

🏆 <b>Рутбаи шумо:</b> {rank} (Сатҳи {level})
📍 <b>Шаҳри фаъол:</b> {profile.get('city', 'Душанбе')}
💰 <b>Хазина:</b> {profile.get('balance', 1000)} сомонӣ
👥 <b>Мизоҷони доимӣ:</b> {profile.get('clients', 0)} нафар
👔 <b>Ҳайати кормандон:</b> {profile.get('employees', 0)} нафар
🏢 <b>Филиалҳои кушода:</b> {len(opened)} адад

📈 <b>Даромади пассиви рӯзона:</b> +{passive_income} сомонӣ / рӯзона"""
    else:
        text = f"""<b>🚀 TojikAI Empire — Симулятор Бизнеса и Медиа (v2.1)</b>

🏆 <b>Ваш ранг:</b> {rank} (Уровень {level})
📍 <b>Текущий город:</b> {profile.get('city', 'Душанбе')}
💰 <b>Баланс Кассы:</b> {profile.get('balance', 1000)} сомони
👥 <b>Клиенты:</b> {profile.get('clients', 0)} чел.
👔 <b>Сотрудники в штате:</b> {profile.get('employees', 0)} чел.
🏢 <b>Открытые филиалы:</b> {len(opened)} шт.

📊 <b>Пассивный доход:</b> +{passive_income} сомони / день"""

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎲 Tasodifiy voqea", callback_data="game_event"))
    builder.row(InlineKeyboardButton(text="🏢 Yangi filial", callback_data="game_buy_list"))
    builder.row(InlineKeyboardButton(text="👔 Jamoani kengaytirish", callback_data="game_staff_list"))
    builder.row(InlineKeyboardButton(text="🎖️ Mening yutuqlarim", callback_data="game_achievements"))
    builder.row(InlineKeyboardButton(text="🏆 Turnir / Liderlar", callback_data="game_leaders"))

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
        builder.row(InlineKeyboardButton(text=f"Выбрать {opt_key}", callback_data=f"ge_opt_{opt_key}"))

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
    level_up = (new_level != profile["level"])

    new_rank = RANKS[min(new_level - 1, len(RANKS) - 1)]
    new_city = profile.get("city", "Душанбе")
    if level_up:
        new_city = random.choice(CITIES)

    import json
    achievements = json.loads(profile.get("achievements", "[]") or "[]")
    if "first_step" not in achievements:
        achievements.append("first_step")

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
        achievements=json.dumps(achievements),
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
            res_msg += f"\n🎉 <b>Darajangiz ko'tarildi: {new_level}! Rangingiz: {new_rank}, yangi shahar: {new_city}!</b>"
    elif lang == "tg":
        res_msg = f"<b>Натиҷаи интихоби шумо:</b>\n\n{diff_text}"
        if level_up:
            res_msg += f"\n🎉 <b>Сатҳи шумо баланд шуд: {new_level}! Рутбаи нав: {new_rank}, шаҳри нав: {new_city}!</b>"
    else:
        res_msg = f"<b>Результаты вашего решения:</b>\n\n{diff_text}"
        if level_up:
            res_msg += f"\n🎉 <b>Поздравляем! Ваш уровень вырос до {new_level}! Новый ранг: {new_rank}, открыт новый город: {new_city}!</b>"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад в империю", callback_data="game_back"))

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
    text = "<b>🏢 Открытие нового филиала / Кушодани филиали нав</b>\n\n"

    builder = InlineKeyboardBuilder()
    for b_key, b_data in BUSINESS_TYPES.items():
        is_opened = b_key in opened
        name = b_data[f"name_{lang}"] if f"name_{lang}" in b_data else b_data["name_ru"]
        desc = b_data[f"desc_{lang}"] if f"desc_{lang}" in b_data else b_data["desc_ru"]

        status_symbol = "✅ Открыто" if is_opened else f"🛒 Купить за {b_data['cost']} сомони"
        text += f"• <b>{name}</b>\n   {desc}\n   Статус: <i>{status_symbol}</i>\n\n"

        if not is_opened:
            builder.row(InlineKeyboardButton(text=f"Купить {name}", callback_data=f"game_buy_{b_key}"))

    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="game_back"))
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
        await callback.answer("Ошибка", show_alert=True)
        return

    if b_key in opened:
        await callback.answer("Этот филиал уже открыт!", show_alert=True)
        return

    if profile["level"] < b_data["required_level"]:
        await callback.answer(f"❌ Требуется уровень {b_data['required_level']}.", show_alert=True)
        return

    if profile["balance"] < b_data["cost"]:
        await callback.answer(f"❌ Недостаточно средств! Нужна {b_data['cost']} сомони.", show_alert=True)
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


@router.callback_query(F.data == "game_staff_list")
async def handle_game_staff_list(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from database.models import get_or_create_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)

    hired = json.loads(profile.get("employees_hired", '{"managers": 0, "marketers": 0, "drivers": 0, "accountants": 0, "lawyers": 0}') or '{}')

    text = f"""<b>👔 Наем персонала / Кормандон ва Мутахассисон</b>

Нанимайте команду профессионалов, чтобы поднять пассивный доход бизнеса!

• <b>Менеджеры:</b> {hired.get('managers', 0)} чел. (Цена: 200 сомони | +10 клиентов/день)
• <b>Маркетологи:</b> {hired.get('marketers', 0)} чел. (Цена: 300 сомони | +25 клиентов/день)
• <b>Водители:</b> {hired.get('drivers', 0)} чел. (Цена: 150 сомони | +5 клиентов/день)
• <b>Бухгалтеры:</b> {hired.get('accountants', 0)} чел. (Цена: 400 сомони | +15 сомони пассивного дохода/день)
• <b>Юристы:</b> {hired.get('lawyers', 0)} чел. (Цена: 500 сомони | +30 сомони пассивного дохода/день)
"""

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💼 Нанять Менеджера", callback_data="staff_buy_managers"))
    builder.row(InlineKeyboardButton(text="📈 Нанять Маркетолога", callback_data="staff_buy_marketers"))
    builder.row(InlineKeyboardButton(text="🚛 Нанять Водителя", callback_data="staff_buy_drivers"))
    builder.row(InlineKeyboardButton(text="🧮 Нанять Бухгалтера", callback_data="staff_buy_accountants"))
    builder.row(InlineKeyboardButton(text="⚖️ Нанять Юриста", callback_data="staff_buy_lawyers"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="game_back"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("staff_buy_"))
async def handle_staff_buy(callback: CallbackQuery):
    user_id = callback.from_user.id
    staff_type = callback.data.replace("staff_buy_", "")

    from database.models import get_or_create_business_empire, update_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)

    hired = json.loads(profile.get("employees_hired", '{"managers": 0, "marketers": 0, "drivers": 0, "accountants": 0, "lawyers": 0}') or '{}')

    prices = {"managers": 200, "marketers": 300, "drivers": 150, "accountants": 400, "lawyers": 500}
    price = prices.get(staff_type, 200)

    if profile["balance"] < price:
        await callback.answer("❌ Недостаточно средств на балансе!", show_alert=True)
        return

    new_balance = profile["balance"] - price
    hired[staff_type] = hired.get(staff_type, 0) + 1
    new_employees = profile["employees"] + 1

    added_clients = 0
    if staff_type == "managers": added_clients = 10
    elif staff_type == "marketers": added_clients = 25
    elif staff_type == "drivers": added_clients = 5

    await update_business_empire(
        user_id=user_id,
        balance=new_balance,
        clients=profile["clients"] + added_clients,
        employees=new_employees,
        level=profile["level"],
        xp=profile["xp"] + 10,
        businesses=profile["businesses"],
        rank=profile.get("rank", "Новичок"),
        city=profile.get("city", "Душанбе"),
        unlocked_cities=profile.get("unlocked_cities", '["Душанбе"]'),
        employees_hired=json.dumps(hired),
        achievements=profile.get("achievements", '[]'),
        daily_tasks=profile.get("daily_tasks", '[]')
    )

    await callback.answer("🎉 Сотрудник успешно нанят!", show_alert=True)
    await handle_game_staff_list(callback)


@router.callback_query(F.data == "game_achievements")
async def handle_game_achievements(callback: CallbackQuery):
    user_id = callback.from_user.id
    from database.models import get_or_create_business_empire
    profile = await get_or_create_business_empire(user_id, callback.from_user.username)

    achievements = json.loads(profile.get("achievements", "[]") or "[]")

    text = "<b>🎖️ Ваши достижения в TojikAI Empire:</b>\n\n"

    all_achievements = {
        "first_step": ("🚀 Первый Шаг", "Пройдено первое случайное событие!"),
        "rich": ("💰 Богач", "Накоплено более 5,000 сомони на балансе!"),
        "big_boss": ("🏢 Корпорация", "Открыто более 3-х филиалов бизнеса!")
    }

    for key, (title, desc) in all_achievements.items():
        status = "✅ Выполнено" if key in achievements else "❌ Заблокировано"
        text += f"• <b>{title}</b> — {desc}\n  Статус: <i>{status}</i>\n\n"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="game_back"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "game_leaders")
async def handle_game_leaders(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    from database.models import get_business_empire_leaderboard
    leaders = await get_business_empire_leaderboard(limit=10)

    if lang == "tg":
        text = "<b>🏆 Ҷадвали пешсафони Бизнес Империя TojikAI</b>\n\n"
    else:
        text = "<b>🏆 Турнирная таблица TojikAI Empire</b>\n\n"

    for i, l in enumerate(leaders, 1):
        name = l["username"] or f"Игрок_{l['user_id']}"
        text += f"{i}. <b>{name}</b> — Уровень: {l['level']} | Баланс: {l['balance']} TJS\n"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="game_back"))

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
