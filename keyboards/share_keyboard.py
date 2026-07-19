# keyboards/share_keyboard.py — Клавиатура для шеринга контента

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_share_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура после генерации контента (поделиться, сохранить, ещё)"""

    if language == "uz":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📤 Kanalga ulashish",
                        switch_inline_query="📤 @SozandaBot orqali ajoyib kontent yarating!"
                    ),
                    InlineKeyboardButton(
                        text="📤 Do'stga yuborish",
                        switch_inline_query="🤖 Ushbu sun'iy intellekt boti biznesingiz uchun kontent tayyorlaydi! @SozandaBot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💾 Saqlab olish",
                        callback_data="share_save"
                    ),
                    InlineKeyboardButton(
                        text="🔁 Boshqa variant",
                        callback_data="share_regenerate"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="✨ Ulashish uchun +1 generatsiya!",
                        callback_data="share_content"
                    ),
                ],
            ]
        )
    elif language == "tg":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📤 Дар канал",
                        switch_inline_query="📤 Мундоди ҷолиб аз @SozandaBot"
                    ),
                    InlineKeyboardButton(
                        text="📤 Бо дӯст",
                        switch_inline_query="🤖 Ин бот мундод месозад! @SozandaBot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💾 Нигоҳ доштан",
                        callback_data="share_save"
                    ),
                    InlineKeyboardButton(
                        text="🔁 Варианти дигар",
                        callback_data="share_regenerate"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="✨ +1 генерация барои шеринг!",
                        callback_data="share_content"
                    ),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📤 В канал",
                        switch_inline_query="📤 Крутой контент от @SozandaBot"
                    ),
                    InlineKeyboardButton(
                        text="📤 Другу",
                        switch_inline_query="🤖 Этот бот делает контент! @SozandaBot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="💾 Сохранить",
                        callback_data="share_save"
                    ),
                    InlineKeyboardButton(
                        text="🔁 Другой вариант",
                        callback_data="share_regenerate"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="✨ +1 генерация за шеринг!",
                        callback_data="share_content"
                    ),
                ],
            ]
        )

    return keyboard
