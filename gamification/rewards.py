from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Reward:
    action: str
    base_xp: int
    description: str
    cooldown_hours: float = 0  # 0 = без кулдауна


class RewardEngine:
    """
    Интеграция с твоими существующими хендлерами.
    Каждое действие пользователя = XP + прогресс.
    """

    REWARDS = {
        # Из generate.py
        'generate_post': Reward('generate_post', 20, "Создание поста", 0.5),
        'generate_reels': Reward('generate_reels', 35, "Создание Reels", 1.0),
        'generate_stories': Reward('generate_stories', 15, "Создание Stories", 0.5),

        # Из data/ — разные типы контента
        'generate_beauty': Reward('generate_beauty', 25, "Контент для beauty", 0),
        'generate_cafe': Reward('generate_cafe', 25, "Контент для кафе", 0),
        'generate_shop': Reward('generate_shop', 25, "Контент для магазина", 0),

        # Из referral.py
        'referral_signup': Reward('referral_signup', 100, "Регистрация реферала", 0),
        'referral_premium': Reward('referral_premium', 300, "Реферал купил подписку", 0),

        # Из subscription.py + payment/
        'subscribe_month': Reward('subscribe_month', 200, "Подписка на месяц", 0),
        'subscribe_year': Reward('subscribe_year', 500, "Подписка на год", 0),

        # Ежедневные
        'daily_login': Reward('daily_login', 10, "Ежедневный вход", 20),  # 20ч кулдаун
        'streak_bonus_3': Reward('streak_bonus_3', 50, "Серия 3 дня", 0),
        'streak_bonus_7': Reward('streak_bonus_7', 150, "Серия 7 дней", 0),
        'streak_bonus_30': Reward('streak_bonus_30', 500, "Серия 30 дней", 0),

        # Из content_engine/niche_manager.py
        'explore_new_niche': Reward('explore_new_niche', 15, "Новая ниша", 0),

        # Из i18n/
        'change_language': Reward('change_language', 5, "Смена языка", 0),

        # Из handlers/admin.py
        'report_bug': Reward('report_bug', 50, "Сообщение о баге", 0),
    }

    def get_reward(self, action: str) -> Reward:
        return self.REWARDS.get(action, Reward(action, 5, "Неизвестное действие"))

    def calculate_total_xp(self, actions: List[str], streak: int = 0) -> Dict:
        """Подсчёт XP за список действий с учётом серии"""
        total = 0
        breakdown = []

        for action in actions:
            reward = self.get_reward(action)
            total += reward.base_xp
            breakdown.append(f"{reward.description}: +{reward.base_xp}")

        # Бонус за серию
        if streak >= 30:
            multiplier = 2.0
            bonus_name = "x2 Серия 30+ дней"
        elif streak >= 7:
            multiplier = 1.5
            bonus_name = "x1.5 Серия 7+ дней"
        elif streak >= 3:
            multiplier = 1.2
            bonus_name = "x1.2 Серия 3+ дня"
        else:
            multiplier = 1.0
            bonus_name = None

        if multiplier > 1.0:
            bonus_xp = int(total * (multiplier - 1))
            total = int(total * multiplier)
            breakdown.append(f"🔥 {bonus_name}: +{bonus_xp}")

        return {
            'total_xp': total,
            'breakdown': breakdown,
            'multiplier': multiplier
        }