import math
from dataclasses import dataclass
from typing import Optional, Tuple
from datetime import datetime, timedelta

@dataclass
class UserProgress:
    """Модель прогресса пользователя — будет храниться в БД"""
    user_id: int
    username: str
    total_xp: int = 0
    current_level: int = 1
    streak_days: int = 0
    last_active: Optional[datetime] = None
    content_generated: int = 0
    referrals_made: int = 0
    days_subscribed: int = 0


class ProgressEngine:
    """
    Движок прогресса с психологическими триггерами.
    Интегрируется с твоими handlers: generate.py, referral.py, subscription.py
    """

    BASE_XP = 100
    LEVEL_MULTIPLIER = 1.5
    STREAK_BONUS = 1.2  # Множитель за серию

    # XP за действия (интеграция с твоими хендлерами)
    XP_REWARDS = {
        'generate_content': 25,      # Из generate.py
        'generate_reels': 35,        # Из data/reels_templates.py
        'generate_post': 20,         # Из data/posts_templates.py
        'referral_signup': 100,      # Из referral.py
        'subscription_purchase': 200, # Из subscription.py + payment/
        'daily_login': 10,           # Ежедневный вход
        'streak_3_days': 50,         # Серия 3 дня
        'streak_7_days': 150,        # Серия 7 дней
        'streak_30_days': 500,       # Серия 30 дней
        'first_content': 50,         # Первый контент
        'niche_explored': 15,        # Новая ниша из niches.py
        'language_changed': 5,       # Из i18n/
    }

    def __init__(self):
        self.level_thresholds = self._generate_thresholds(100)

    def _generate_thresholds(self, max_level: int) -> list:
        """Экспоненциальный рост — сложнее на высоких уровнях"""
        thresholds = []
        for level in range(1, max_level + 1):
            xp_needed = int(self.BASE_XP * (level ** self.LEVEL_MULTIPLIER))
            thresholds.append(xp_needed)
        return thresholds

    def calculate_level(self, total_xp: int) -> Tuple[int, int, int, float]:
        """
        Returns: (level, xp_in_current_level, xp_needed_for_level, progress_percent)
        """
        level = 1
        accumulated = 0

        for threshold in self.level_thresholds:
            if total_xp < accumulated + threshold:
                current = total_xp - accumulated
                progress = (current / threshold) * 100
                return level, current, threshold, progress
            accumulated += threshold
            level += 1

        # Максимальный уровень
        final_threshold = self.level_thresholds[-1]
        return level, total_xp - accumulated, final_threshold, 99.9

    def render_progress_bar(self, percent: float, length: int = 18) -> str:
        """Красивый прогресс-бар с эмодзи"""
        filled = int((percent / 100) * length)
        empty = length - filled

        # Градиент цветов через эмодзи
        if percent >= 75:
            bar = "🟩" * filled + "⬜" * empty
        elif percent >= 50:
            bar = "🟨" * filled + "⬜" * empty
        elif percent >= 25:
            bar = "🟧" * filled + "⬜" * empty
        else:
            bar = "🟥" * filled + "⬜" * empty

        return f"{bar} {percent:.1f}%"

    def get_level_title(self, level: int) -> str:
        """Звания по уровням — социальное доказательство"""
        titles = {
            1: "🌱 Новичок",
            5: "📝 Блогер",
            10: "📱 Контент-мейкер",
            15: "🎬 Режиссёр Reels",
            20: "⭐ Инфлюенсер",
            25: "👑 Топ-блогер",
            30: "🚀 Контент-гуру",
            40: "💎 Легенда",
            50: "🔥 Мега-звезда",
        }

        # Находим ближайшее звание
        available = [k for k in titles.keys() if k <= level]
        return titles[max(available)] if available else "🌱 Новичок"

    def calculate_xp_with_streak(self, base_xp: int, streak: int) -> int:
        """Бонус за серию — loss aversion триггер"""
        if streak >= 30:
            multiplier = 2.0
        elif streak >= 7:
            multiplier = 1.5
        elif streak >= 3:
            multiplier = self.STREAK_BONUS
        else:
            multiplier = 1.0

        return int(base_xp * multiplier)

    def get_motivational_message(self, percent: float, streak: int, level: int) -> str:
        """Психологические триггеры на основе прогресса"""
        messages = []

        if percent >= 90:
            messages.append("🔥 Почти новый уровень! Остался один рывок!")
        elif percent >= 75:
            messages.append("💪 Уже больше половины пути к следующему уровню!")
        elif percent >= 50:
            messages.append("⭐ Отличный темп, продолжай в том же духе!")

        if streak >= 30:
            messages.append(f"👑 Невероятная серия x{streak}! Ты машина!")
        elif streak >= 7:
            messages.append(f"⚡ Серия x{streak}! Не прерывай — бонус растёт!")
        elif streak >= 3:
            messages.append(f"🔥 Серия x{streak}! Ещё немного — и бонус увеличится!")
        elif streak == 0:
            messages.append("🌱 Вернись завтра — начни серию и получи бонус!")

        if level <= 3:
            messages.append("🎯 Совет: генерируй больше контента для быстрого роста!")

        return "\n".join(messages) if messages else "🚀 Продолжай создавать контент!"

    def check_level_up(self, old_xp: int, new_xp: int) -> Tuple[bool, int]:
        """Проверяет, произошло ли повышение уровня"""
        old_level, _, _, _ = self.calculate_level(old_xp)
        new_level, _, _, _ = self.calculate_level(new_xp)

        return new_level > old_level, new_level