# content_engine/start.py — Стартовый handler бота TojikAI с выбором страны и языка

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.models import get_or_create_user, update_user_language, update_user_country, get_user
from keyboards.language_menu import get_language_menu
from keyboards.main_menu_content import get_main_menu

router = Router()

# ============================================
# ТЕКСТЫ
# ============================================

WELCOME_TEXT = """👋 Хуш омадед ба / Добро пожаловать в / Xush kelibsiz <b>TojikAI v2.2</b>!

🤖 Первая AI & SMM Платформа для вашего бизнеса в Таджикистане, Узбекистане и России.

<b>Выберите вашу страну / Интихоби кишвар / Mamlakatni tanlang:</b>"""


# ============================================
# /START
# ============================================

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Парсим реферальный код
    args = message.text.split()
    referrer_id = None
    if len(args) > 1 and args[1].startswith("ref"):
        try:
            referrer_id = int(args[1].replace("ref", ""))
        except ValueError:
            pass

    # Создаём/получаем пользователя
    await get_or_create_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        referrer_id=referrer_id
    )

    await state.clear()

    # Показываем выбор страны
    buttons = [
        [
            InlineKeyboardButton(text="Таджикистан 🇹🇯", callback_data="sel_country_tj"),
            InlineKeyboardButton(text="Узбекистан 🇺🇿", callback_data="sel_country_uz")
        ],
        [
            InlineKeyboardButton(text="Россия 🇷🇺", callback_data="sel_country_ru")
        ]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(
        WELCOME_TEXT,
        reply_markup=markup,
        parse_mode="HTML"
    )


# ============================================
# ОБРАБОТКА ВЫБОРА СТРАНЫ
# ============================================

@router.callback_query(F.data == "sel_country_tj")
async def select_language_tj(callback: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="Тоҷикӣ 🇹🇯", callback_data="set_cl_tj_tg"),
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="set_cl_tj_ru")
        ]
    ]
    await callback.message.edit_text(
        "🇹🇯 <b>Тоҷикистон</b>\n\nИнтихоби забон / Выберите язык:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "sel_country_uz")
async def select_language_uz(callback: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data="set_cl_uz_uz"),
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="set_cl_uz_ru")
        ]
    ]
    await callback.message.edit_text(
        "🇺🇿 <b>O'zbekiston</b>\n\nTilni tanlang / Выберите язык:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "sel_country_ru")
async def select_language_ru(callback: CallbackQuery):
    # Для России поддерживается только русский язык
    user_id = callback.from_user.id
    await update_user_language(user_id, "ru")
    await update_user_country(user_id, "ru")

    text = "✅ Включен сценарий <b>Россия 🇷🇺</b> (валюта RUB ₽, оплата Картой) на русском языке."
    await callback.message.edit_text(text, parse_mode="HTML")

    await callback.message.answer(
        "👋 Главное меню\n\n✨ Выберите, что создать:",
        reply_markup=get_main_menu("ru")
    )
    await callback.answer()


# ============================================
# ОБРАБОТКА СВЯЗКИ СТРАНА + ЯЗЫК
# ============================================

@router.callback_query(F.data.startswith("set_cl_"))
async def set_country_and_lang(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data.replace("set_cl_", "")  # "tj_tg", "tj_ru", "uz_uz", "uz_ru"
    country, lang = data.split("_")

    await update_user_language(user_id, lang)
    await update_user_country(user_id, country)

    if country == "tj":
        if lang == "tg":
            text = "✅ Забон танзим шуд: <b>Тоҷикӣ 🇹🇯</b>\n\nСенарияи <b>Тоҷикистон</b> (асъори Сомони TJS, пардохтҳои Alif/Душанбе Сити) фаъол гардид."
            main_text = "👋 Менюи асосӣ"
        else:
            text = "✅ Язык установлен: <b>Русский 🇷🇺</b>\n\nАктивирован сценарий <b>Таджикистан 🇹🇯</b> (валюта Сомони TJS, Alif/Душанбе Сити)."
            main_text = "👋 Главное меню"
    else:
        if lang == "uz":
            text = "✅ Til o'rnatildi: <b>O'zbek tili 🇺🇿</b>\n\n<b>O'zbekiston</b> ssenariysi (valyuta UZS, Click/Payme) faollashtirildi."
            main_text = "👋 Asosiy menyu"
        else:
            text = "✅ Язык установлен: <b>Русский 🇷🇺</b>\n\nАктивирован сценарий <b>Узбекистан 🇺🇿</b> (валюта UZS, Click/Payme)."
            main_text = "👋 Главное меню"

    await callback.message.edit_text(text, parse_mode="HTML")

    await callback.message.answer(
        main_text,
        reply_markup=get_main_menu(lang)
    )
    await callback.answer()


# ============================================
# ПОМОЩЬ
# ============================================

@router.message(Command("help"))
async def cmd_help(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    if lang == "uz":
        help_text = """📖 <b>TojikAI boti bo'yicha qo'llanma</b>

🎬 <b>AI Kontent</b> — Reels va mukammal kontent-rejalar yaratish
📈 <b>Postlar</b> — sotuvchi va ta'limiy postlar matnlari
🎬 <b>Stories</b> — stories g'oyalar va o'yinlar ketma-ketligi
💡 <b>G'oyalar</b> — TikTok, Instagram va Telegram uchun g'oyalar

⭐ <b>Premium</b> — tariflar va unga ulanish
👥 <b>Hamkorlik</b> — do'stlarni taklif qilib, bonuslar oling
📊 <b>Statistika</b> — hisobingiz holati va generatsiyalar soni
📋 <b>Tarix</b> — saqlab qolingan barcha AI matnlaringiz

Buyruqlar:
/start — botni ishga tushirish
/help — qo'llanma

Savollar bo'yicha: @tojikai_support"""
    elif lang == "tg":
        help_text = """📖 <b>Дастури TojikAI</b>

🎬 <b>AI Контент</b> — сохтани Reels, нақшаҳои контент
📈 <b>Постҳо</b> — матнҳои тайёр ва фурӯшанда барои Instagram
🎬 <b>Сторисҳо</b> — идеяҳо ва прогрев барои сторис
💡 <b>Идеяҳо</b> — идеяҳои креативӣ барои TikTok ва Telegram

⭐ <b>Premium</b> — обунаҳо ва тарифҳо
👥 <b>Даъват</b> — даъвати дӯстон, гирифтани бонусҳо
📊 <b>Омор</b> — омори истифодаи шумо
📋 <b>Таърих</b> — матнҳои ҳифзшудаи шумо

Командаҳо:
/start — оғоз
/help — кӯмак

Барои саволҳо: @tojikai_support"""
    else:
        help_text = """📖 <b>Помощь по боту TojikAI</b>

🎬 <b>AI Контент</b> — создайте Reels, контент-планы
📈 <b>Посты</b> — продающие и экспертные тексты
🎬 <b>Сторис</b> — идеи и сценарии прогревов
💡 <b>Идеи</b> — креативные концепции для TikTok/Telegram

⭐ <b>Premium</b> — подписки и тарифы
👥 <b>Рефералка</b> — приглашайте друзей, получайте бонусы
📊 <b>Статистика</b> — ваш progress
📋 <b>История</b> — сохранённые генерации

Команды:
/start — начать
/help — помощь

По вопросам: @tojikai_support"""

    await message.answer(help_text, parse_mode="HTML")
