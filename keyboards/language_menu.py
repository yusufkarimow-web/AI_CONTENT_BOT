# keyboards/language_menu.py — Выбор языка (русский / таджикский / узбекский)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_language_menu() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка при первом входе"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇷🇺 Русский",
                    callback_data="lang_ru"
                ),
                InlineKeyboardButton(
                    text="🇹🇯 Тоҷикӣ",
                    callback_data="lang_tg"
                ),
                InlineKeyboardButton(
                    text="🇺🇿 O'zbekcha",
                    callback_data="lang_uz"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Все языки / Ҳама / Barchasi",
                    callback_data="lang_both"
                ),
            ],
        ]
    )

    return keyboard
