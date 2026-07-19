# keyboards/niche_menu.py — Выбор ниши бизнеса, разделенный по странам

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from content_engine.niche_manager import get_all_niches


def get_niche_menu(language: str = "ru", country: str = "uz") -> ReplyKeyboardMarkup:
    """Динамическое меню выбора ниши бизнеса в зависимости от страны и языка.
    Показывает все доступные ниши (>50 на страну) с иконками.
    """
    niches = get_all_niches(language, country)

    buttons = []
    row = []
    for niche in niches:
        icon = niche.get("icon", "")
        name = niche.get(f"name_{language}", niche.get("name_ru"))
        btn_text = f"{icon} {name}".strip()
        row.append(KeyboardButton(text=btn_text))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Добавляем кнопку назад
    back_text = "⬅️ Ortga" if language == "uz" else ("⬅️ Бозгашт" if language == "tg" else "⬅️ Назад")
    buttons.append([KeyboardButton(text=back_text)])

    placeholder = "Sohani tanlang..." if language == "uz" else ("Нишаро интихоб кунед..." if language == "tg" else "Выберите нишу...")

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )
