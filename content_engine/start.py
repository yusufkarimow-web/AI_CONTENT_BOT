# content_engine/start.py — Стартовый handler бота Sozanda с выбором страны и сценария

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

WELCOME_TEXT_RU = """👋 Добро пожаловать в <b>Sozanda</b>!

🤖 Я — AI-бот, который создаёт вирусный контент для бизнеса.

✨ Что я умею:
• 🎬 Reels / Видео с вирусными хуками
• 📝 Посты для Instagram
• 📸 Stories
• 💡 Идеи для контента
• ⚡ Цепляющие подписи

<b>Выберите язык / Забонро интихоб кунед / Tilni tanlang:</b>"""


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

    # Очищаем состояние
    await state.clear()

    # Показываем выбор языка
    await message.answer(
        WELCOME_TEXT_RU,
        reply_markup=get_language_menu(),
        parse_mode="HTML"
    )


# ============================================
# ВЫБОР ЯЗЫКА И СТРАНЫ
# ============================================

@router.callback_query(F.data == "lang_ru")
async def show_country_selection(callback: CallbackQuery):
    # Показываем клавиатуру выбора страны для русского языка
    buttons = [
        [
            InlineKeyboardButton(text="Узбекистан 🇺🇿", callback_data="country_uz_ru"),
            InlineKeyboardButton(text="Таджикистан 🇹🇯", callback_data="country_tj_ru")
        ]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(
        "🇷🇺 Выберите вашу страну для персонализации бизнес-ниш, логики ИИ и платежей:\n\n"
        "🇺🇿 <b>Узбекистан</b> (валюта UZS, платежи Click/Payme)\n"
        "🇹🇯 <b>Таджикистан</b> (валюта Сомони TJS, платежи Alif/Душанбе Сити)",
        reply_markup=markup,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("country_"))
async def set_country_ru(callback: CallbackQuery):
    user_id = callback.from_user.id
    country_data = callback.data.replace("country_", "")  # "uz_ru" или "tj_ru"
    country, lang = country_data.split("_")

    await update_user_language(user_id, lang)
    await update_user_country(user_id, country)

    text = "✅ Включен сценарий <b>Узбекистан 🇺🇿</b> (валюта UZS, Click/Payme) на русском языке." if country == "uz" else "✅ Включен сценарий <b>Таджикистан 🇹🇯</b> (валюта Сомони TJS, Alif/Душанбе Сити) на русском языке."
    await callback.message.edit_text(text, parse_mode="HTML")

    await callback.message.answer(
        "👋 Главное меню\n\n✨ Выберите, что создать:",
        reply_markup=get_main_menu(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "lang_tg")
async def set_language_tg(callback: CallbackQuery):
    user_id = callback.from_user.id
    await update_user_language(user_id, "tg")
    await update_user_country(user_id, "tj")

    text = "✅ Забон танзим шуд: <b>Тоҷикӣ 🇹🇯</b>\n\nСенарияи <b>Тоҷикистон</b> (асъори Сомони TJS, пардохтҳои Alif/Душанбе Сити) фаъол гардид. Барои оғоз менюро истифода баред 👇"
    await callback.message.edit_text(text, parse_mode="HTML")

    await callback.message.answer(
        "👋 Менюи асосӣ",
        reply_markup=get_main_menu("tg")
    )
    await callback.answer()


@router.callback_query(F.data == "lang_uz")
async def set_language_uz(callback: CallbackQuery):
    user_id = callback.from_user.id
    await update_user_language(user_id, "uz")
    await update_user_country(user_id, "uz")

    text = "✅ Til o'rnatildi: <b>O'zbek tili 🇺🇿</b>\n\n<b>O'zbekiston</b> ssenariysi (valyuta UZS, Click/Payme to'lovlari) faollashtirildi. Boshlash uchun quyidagi menyudan foydalaning 👇"
    await callback.message.edit_text(text, parse_mode="HTML")

    await callback.message.answer(
        "👋 Asosiy menyu",
        reply_markup=get_main_menu("uz")
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
        help_text = """📖 <b>Sozanda boti bo'yicha qo'llanma</b>

🎬 <b>AI Reels/Kreativ</b> — Reels ssenariylari yaratish
📝 <b>Postlar</b> — Instagram uchun tayyor post matnlari
📸 <b>Stories</b> — stories g'oyalar ketma-ketligi
💡 <b>G'oyalar</b> — kreativ kontent-reja g'oyalari

⭐ <b>Premium obuna</b> — tariflar va unga ulanish
👥 <b>Hamkorlik (Do'stlar)</b> — do'stlarni taklif qilib, bonuslar oling
📊 <b>Statistika</b> — hisobingiz holati va generatsiyalar soni
📋 <b>Tarix</b> — saqlab qolingan barcha AI matnlaringiz

Buyruqlar:
/start — botni ishga tushirish
/help — qo'llanma

Savollar bo'yicha: @sozanda_support"""
    elif lang == "tg":
        help_text = """📖 <b>Помощь по боту Sozanda</b>

🎬 <b>AI мундод</b> — сохтани Reels, постҳо ва Stories
📝 <b>Постҳо</b> — матнҳои тайёр барои Instagram
📸 <b>Сториз</b> — идеяҳо барои сторис
💡 <b>Идеяҳо</b> — идеяҳои креативӣ барои контент

⭐ <b>Премиум</b> — обунаҳо ва тарифҳо
👥 <b>Даъват</b> — даъвати дӯстон, гирифтани бонусҳо
📊 <b>Омор</b> — омори истифодаи шумо
📋 <b>Таърих</b> — матнҳои ҳифзшудаи шумо

Командаҳо:
/start — оғоз
/help — кӯмак

Барои саволҳо: @sozanda_support"""
    else:
        help_text = """📖 <b>Помощь по боту Sozanda</b>

🎬 <b>Контент AI</b> — создайте Reels, посты, Stories
📝 <b>Посты</b> — готовые тексты для Instagram
📸 <b>Stories</b> — идеи для сторис
💡 <b>Идеи</b> — креативные концепции

⭐ <b>Premium</b> — подписки и тарифы
👥 <b>Рефералка</b> — приглашайте друзей, получайте бонусы
📊 <b>Статистика</b> — ваш progress
📋 <b>История</b> — сохранённые генерации

Команды:
/start — начать
/help — помощь

По вопросам: @sozanda_support"""

    await message.answer(help_text, parse_mode="HTML")
