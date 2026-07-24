# app/bot/keyboards.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# Ниши для Узбекистана
NICHES_UZ = {
    "cafe": "☕ Кафе / Чайхана",
    "textile": "👕 Текстиль / Одежда",
    "real_estate": "🏢 Недвижимость",
    "auto": "🚗 Авто / Сервис",
    "marketplace": "📦 Узум Маркетплейс",
    "construction": "🏗 Строительство",
    "beauty": "💅 Салон Красоты",
    "cargo": "📮 Карго / Доставка",
}

# Ниши для Таджикистана
NICHES_TJ = {
    "wholesale": "📊 Саводои Яклухт (Опт)",
    "cargo": "📮 Карго (Китай/Турция)",
    "construction": "🏗 Сохтмон (Стройматериалы)",
    "cafe": "☕ Курутобхона / Чайхана",
    "beauty": "💅 Салони Зебоӣ (Свадебный)",
    "tourism": "🏔 Туризм (Варзоб/Памир)",
    "salon": "✂️ Салон Зебоӣ",
    "auto": "🚗 Автобозор / Сервис",
}

def build_niche_keyboard(country: str) -> InlineKeyboardMarkup:
    """Построение клавиатуры выбора ниши"""
    niches = NICHES_UZ if country == "uz" else NICHES_TJ
    buttons = []

    for niche_code, niche_label in niches.items():
        buttons.append(
            InlineKeyboardButton(text=niche_label, callback_data=f"niche_{niche_code}")
        )

    # Раскладываем по 2 кнопки в ряд
    keyboard = []
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            keyboard.append([buttons[i], buttons[i + 1]])
        else:
            keyboard.append([buttons[i]])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def build_platform_keyboard() -> InlineKeyboardMarkup:
    """Выбор платформы"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📸 Instagram", callback_data="platform_instagram"),
            InlineKeyboardButton(text="📱 Telegram", callback_data="platform_telegram"),
        ],
        [
            InlineKeyboardButton(text="🎵 TikTok", callback_data="platform_tiktok"),
            InlineKeyboardButton(text="▶️ YouTube", callback_data="platform_youtube"),
        ],
    ])

def build_goal_keyboard() -> InlineKeyboardMarkup:
    """Выбор цели продвижения"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Продажи & Заявки", callback_data="goal_sales")],
        [InlineKeyboardButton(text="📈 Охваты & Вирусность", callback_data="goal_reach")],
        [InlineKeyboardButton(text="💬 Вовлечение Аудитории", callback_data="goal_engagement")],
        [InlineKeyboardButton(text="🌟 Экспертный Личный Бренд", callback_data="goal_expertise")],
    ])

def build_format_keyboard() -> InlineKeyboardMarkup:
    """Выбор формата контента"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Взрывной Reels", callback_data="format_reels")],
        [InlineKeyboardButton(text="📄 Структурированный Пост", callback_data="format_post")],
        [InlineKeyboardButton(text="📖 Серия Stories (5 шт)", callback_data="format_stories")],
        [InlineKeyboardButton(text="📅 Еженедельный План", callback_data="format_weekly_plan")],
    ])

def build_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню"""
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🚀 Создать Контент")],
        [KeyboardButton(text="🎮 TojikAI Empire")],
        [KeyboardButton(text="🤖 AI Консультант")],
        [KeyboardButton(text="⚙️ Настройки")],
    ], resize_keyboard=True)

def build_smm_result_keyboard(generation_id: str) -> InlineKeyboardMarkup:
    """Кнопки под готовым результатом SMM-пакета"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 Скачать PDF", callback_data=f"download_pdf_{generation_id}"),
            InlineKeyboardButton(text="💬 Отправить в WhatsApp", callback_data=f"send_whatsapp_{generation_id}"),
        ],
        [
            InlineKeyboardButton(text="📝 Создать пост", callback_data=f"create_post_{generation_id}"),
            InlineKeyboardButton(text="🎬 Создать Reels", callback_data=f"create_reels_{generation_id}"),
        ],
        [InlineKeyboardButton(text="← Вернуться", callback_data="back_to_menu")],
    ])
