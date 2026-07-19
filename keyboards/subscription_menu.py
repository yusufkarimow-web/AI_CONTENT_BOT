# keyboards/subscription_menu.py — Меню подписок и оплаты (v2.0)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ALIF_ENABLED, HUMO_ENABLED, CRYPTO_PAY_ENABLED


def get_subscription_menu(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура выбора тарифа подписки"""

    if language == "uz":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💚 Oson — 32,000 UZS/oy",
                        callback_data="buy_oson"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💎 Professional — 85,000 UZS/oy",
                        callback_data="buy_pro"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🏢 Business — 215,000 UZS/oy",
                        callback_data="buy_business"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🎁 3 kunlik Oson bepul (3 do'stni taklif qilish)",
                        callback_data="buy_free_trial"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Asosiy menyu",
                        callback_data="back_to_main"
                    ),
                ],
            ]
        )
    elif language == "tg":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💚 Oson — 29 сомонӣ/моҳ",
                        callback_data="buy_oson"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💎 Professional — 79 сомонӣ/моҳ",
                        callback_data="buy_pro"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🏢 Business — 199 сомонӣ/моҳ",
                        callback_data="buy_business"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🎁 3 рӯзи Oson ройгон (даъват 3 дӯст)",
                        callback_data="buy_free_trial"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Менюи асосӣ",
                        callback_data="back_to_main"
                    ),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💚 Oson — 29 сомони/мес",
                        callback_data="buy_oson"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💎 Professional — 79 сомони/мес",
                        callback_data="buy_pro"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🏢 Business — 199 сомони/мес",
                        callback_data="buy_business"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🎁 3 дня Oson бесплатно (пригласи 3 друга)",
                        callback_data="buy_free_trial"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Главное меню",
                        callback_data="back_to_main"
                    ),
                ],
            ]
        )

    return keyboard


def get_payment_menu(language: str = "ru", plan: str = "oson") -> InlineKeyboardMarkup:
    """Клавиатура выбора способа оплаты — показывает только доступные"""

    buttons = []

    # Alif — всегда показываем (основной способ)
    buttons.append([
        InlineKeyboardButton(text="💳 Alif Mobi / Card ✅", callback_data=f"pay_alif_{plan}"),
    ])

    # Humo
    humo_text = "💳 Humo Online" + (" ✅" if HUMO_ENABLED else " ⏳")
    buttons.append([
        InlineKeyboardButton(text=humo_text, callback_data=f"pay_humo_{plan}"),
    ])

    # Click / Payme (for Uzbekistan)
    if language == "uz":
        buttons.append([
            InlineKeyboardButton(text="💳 Click / Payme ✅ (Manual)", callback_data=f"pay_uzcard_{plan}"),
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="💳 Eskhata ⏳", callback_data=f"pay_eskhata_{plan}"),
        ])

    # Crypto — скоро
    crypto_text = "₿ USDT (TRC-20)" + (" ✅" if CRYPTO_PAY_ENABLED else " ⏳")
    buttons.append([
        InlineKeyboardButton(text=crypto_text, callback_data=f"pay_crypto_{plan}"),
    ])

    # Telegram Stars — скоро
    buttons.append([
        InlineKeyboardButton(text="⭐ Telegram Stars ⏳", callback_data=f"pay_stars_{plan}"),
    ])

    # Назад
    if language == "uz":
        buttons.append([
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="pay_back"),
        ])
    elif language == "tg":
        buttons.append([
            InlineKeyboardButton(text="⬅️ Бозгашт", callback_data="pay_back"),
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="⬅️ Назад", callback_data="pay_back"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_payment_confirm_keyboard(language: str = "ru", payment_id: str = "") -> InlineKeyboardMarkup:
    """Клавиатура подтверждения оплаты"""

    if language == "uz":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ To'lov qildim",
                        callback_data=f"payment_done_{payment_id or 'manual'}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data="payment_cancel"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Ortga",
                        callback_data="pay_back"
                    ),
                ],
            ]
        )
    elif language == "tg":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Ман пардохт кардам",
                        callback_data=f"payment_done_{payment_id or 'manual'}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Бекор кардан",
                        callback_data="payment_cancel"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Бозгашт",
                        callback_data="pay_back"
                    ),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Я оплатил",
                        callback_data=f"payment_done_{payment_id or 'manual'}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Отмена",
                        callback_data="payment_cancel"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="pay_back"
                    ),
                ],
            ]
        )

    return keyboard


def get_alif_payment_keyboard(language: str = "ru", plan: str = "oson") -> InlineKeyboardMarkup:
    """Клавиатура для оплаты через Alif — с кнопкой 'Я оплатил' и 'Назад'"""

    if language == "uz":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ To'lov qildim",
                        callback_data=f"payment_done_alif_{plan}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💬 Adminga yozish",
                        url=f"https://t.me/sozanda_admin"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Ortga",
                        callback_data="pay_back"
                    ),
                ],
            ]
        )
    elif language == "tg":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Ман пардохт кардам",
                        callback_data=f"payment_done_alif_{plan}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💬 Нависед ба админ",
                        url=f"https://t.me/sozanda_admin"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Бозгашт",
                        callback_data="pay_back"
                    ),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Я оплатил",
                        callback_data=f"payment_done_alif_{plan}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💬 Написать админу",
                        url=f"https://t.me/sozanda_admin"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="pay_back"
                    ),
                ],
            ]
        )

    return keyboard
