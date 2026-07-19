# keyboards/reels_count_menu.py — Выбор количества идей

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_count_menu(language: str = "ru") -> ReplyKeyboardMarkup:
    """Меню выбора количества идей для генерации"""

    if language == "uz":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="5 ta g'oya"),
                    KeyboardButton(text="10 ta g'oya"),
                ],
                [
                    KeyboardButton(text="20 ta g'oya"),
                    KeyboardButton(text="30 ta g'oya"),
                ],
                [
                    KeyboardButton(text="⬅️ Ortga"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Soni tanlang..."
        )
    elif language == "tg":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="5 идея"),
                    KeyboardButton(text="10 идея"),
                ],
                [
                    KeyboardButton(text="20 идея"),
                    KeyboardButton(text="30 идея"),
                ],
                [
                    KeyboardButton(text="⬅️ Бозгашт"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Шумораро интихоб кунед..."
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="5 идей"),
                    KeyboardButton(text="10 идей"),
                ],
                [
                    KeyboardButton(text="20 идей"),
                    KeyboardButton(text="30 идей"),
                ],
                [
                    KeyboardButton(text="⬅️ Назад"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Выберите количество..."
        )

    return keyboard
