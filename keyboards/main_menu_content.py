# keyboards/main_menu_content.py — Главное меню бота Sozanda

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu(language: str = "ru") -> ReplyKeyboardMarkup:
    """Главное меню бота"""

    if language == "uz":
        # Узбекская версия
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🎬 AI Reels/Kreativ"),
                    KeyboardButton(text="📝 Postlar"),
                ],
                [
                    KeyboardButton(text="📸 Stories"),
                    KeyboardButton(text="💡 G'oyalar"),
                ],
                [
                    KeyboardButton(text="⭐ Premium obuna"),
                    KeyboardButton(text="👥 Hamkorlik (Do'stlar)"),
                ],
                [
                    KeyboardButton(text="📋 Tarix"),
                    KeyboardButton(text="📊 Statistika"),
                ],
                [
                    KeyboardButton(text="🎮 Biznes o'yini"),
                    KeyboardButton(text="📞 Yordam / Aloqa"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Menudan tanlang..."
        )
    elif language == "tg":
        # Таджикская версия
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🎬 AI мундод"),
                    KeyboardButton(text="📝 Постҳо"),
                ],
                [
                    KeyboardButton(text="📸 Сториз"),
                    KeyboardButton(text="💡 Идеяҳо"),
                ],
                [
                    KeyboardButton(text="⭐ Премиум"),
                    KeyboardButton(text="👥 Даъват"),
                ],
                [
                    KeyboardButton(text="📋 Таърих"),
                    KeyboardButton(text="📊 Омор"),
                ],
                [
                    KeyboardButton(text="🎮 Бозии тиҷорат"),
                    KeyboardButton(text="📞 Дастгирӣ"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Менюро интихоб кунед..."
        )
    else:
        # Русская версия (по умолчанию)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🎬 Контент AI"),
                    KeyboardButton(text="📝 Посты"),
                ],
                [
                    KeyboardButton(text="📸 Stories"),
                    KeyboardButton(text="💡 Идеи"),
                ],
                [
                    KeyboardButton(text="⭐ Premium"),
                    KeyboardButton(text="👥 Рефералка"),
                ],
                [
                    KeyboardButton(text="📋 История"),
                    KeyboardButton(text="📊 Статистика"),
                ],
                [
                    KeyboardButton(text="🎮 Бизнес-Игра"),
                    KeyboardButton(text="📞 Поддержка"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Выберите из меню..."
        )

    return keyboard
