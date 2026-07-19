# keyboards/topics_keyboard.py — Клавиатура выбора конкретной темы

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_topics_keyboard(count: int, language: str = "ru") -> InlineKeyboardMarkup:
    """Inline-клавиатура для выбора темы по номеру"""

    buttons = []
    row = []

    for i in range(1, count + 1):
        row.append(
            InlineKeyboardButton(
                text=str(i),
                callback_data=f"topic_{i}"
            )
        )
        # 5 кнопок в ряд
        if len(row) == 5:
            buttons.append(row)
            row = []

    # Добавляем оставшиеся кнопки
    if row:
        buttons.append(row)

    # Кнопка "Сгенерировать все" / "Ҳамаи онҳоро созед"
    if language == "uz":
        generate_all_text = "✨ Barchasini yaratish"
    elif language == "tg":
        generate_all_text = "✨ Ҳамаи онҳоро созед"
    else:
        generate_all_text = "✨ Сгенерировать все"

    buttons.append([
        InlineKeyboardButton(
            text=generate_all_text,
            callback_data="topic_all"
        )
    ])

    # Кнопка назад
    if language == "uz":
        back_text = "⬅️ Ortga"
    elif language == "tg":
        back_text = "⬅️ Бозгашт"
    else:
        back_text = "⬅️ Назад"

    buttons.append([
        InlineKeyboardButton(
            text=back_text,
            callback_data="topic_back"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_topic_action_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура действий после выбора темы"""

    if language == "uz":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎬 Yaratish",
                        callback_data="action_generate"
                    ),
                    InlineKeyboardButton(
                        text="💾 Saqlab olish",
                        callback_data="action_save"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📤 Ulashish",
                        callback_data="action_share"
                    ),
                    InlineKeyboardButton(
                        text="🔁 Boshqa variant",
                        callback_data="action_regenerate"
                    ),
                ],
            ]
        )
    elif language == "tg":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎬 Созед",
                        callback_data="action_generate"
                    ),
                    InlineKeyboardButton(
                        text="💾 Нигоҳ доред",
                        callback_data="action_save"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📤 Мубодила кунед",
                        callback_data="action_share"
                    ),
                    InlineKeyboardButton(
                        text="🔁 Дигар",
                        callback_data="action_regenerate"
                    ),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎬 Сгенерировать",
                        callback_data="action_generate"
                    ),
                    InlineKeyboardButton(
                        text="💾 Сохранить",
                        callback_data="action_save"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📤 Поделиться",
                        callback_data="action_share"
                    ),
                    InlineKeyboardButton(
                        text="🔁 Другой вариант",
                        callback_data="action_regenerate"
                    ),
                ],
            ]
        )

    return keyboard
