# keyboards/referral_keyboard.py — Клавиатура реферальной системы

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_referral_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура реферальной программы"""

    if language == "tg":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📤 Пайвандро фиристед",
                        switch_inline_query="🤖 AI-бот барои мундод! @SozandaBot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Омори даъватҳо",
                        callback_data="ref_stats"
                    ),
                    InlineKeyboardButton(
                        text="🎁 Бонусҳо",
                        callback_data="ref_bonuses"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🏆 Топ-10 рефоводон",
                        callback_data="ref_top"
                    ),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📤 Отправить ссылку",
                        switch_inline_query="🤖 AI-бот для контента! @SozandaBot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Статистика приглашений",
                        callback_data="ref_stats"
                    ),
                    InlineKeyboardButton(
                        text="🎁 Мои бонусы",
                        callback_data="ref_bonuses"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🏆 Топ-10 рефоводов",
                        callback_data="ref_top"
                    ),
                ],
            ]
        )

    return keyboard