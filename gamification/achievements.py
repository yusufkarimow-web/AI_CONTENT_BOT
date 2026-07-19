from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class AchievementRarity(Enum):
    COMMON = ("⭐", "Обычное", 0.5)
    RARE = ("🔷", "Редкое", 0.25)
    EPIC = ("💜", "Эпическое", 0.15)
    LEGENDARY = ("👑", "Легендарное", 0.1)

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    emoji: str
    rarity: AchievementRarity
    xp_reward: int
    condition_type: str  # 'count', 'streak', 'one_time'
    condition_value: int

    def render(self) -> str:
        rarity_emoji, rarity_name, _ = self.rarity.value
        return (
            f"{self.emoji} **{self.name}**\n"
            f"   {rarity_emoji} {rarity_name} | +{self.xp_reward} XP\n"
            f"   _{self.description}_"
        )


class AchievementEngine:
    """
    Достижения интегрированы с твоими хендлерами:
    - generate.py → достижения за контент
    - referral.py → достижения за рефералов
    - subscription.py → достижения за подписки
    """

    ACHIEVEMENTS = [
        # Контент (из generate.py + data/)
        Achievement("first_content", "Первые шаги", "Создай свой первый контент", "📝", AchievementRarity.COMMON, 50, "count", 1),
        Achievement("content_10", "Начинающий блогер", "Создай 10 постов", "📱", AchievementRarity.COMMON, 100, "count", 10),
        Achievement("content_50", "Контент-мейкер", "Создай 50 постов", "🎬", AchievementRarity.RARE, 300, "count", 50),
        Achievement("content_100", "Фабрика контента", "Создай 100 постов", "🏭", AchievementRarity.EPIC, 750, "count", 100),
        Achievement("reels_10", "Reels-звезда", "Создай 10 Reels", "🎵", AchievementRarity.RARE, 200, "count", 10),
        Achievement("stories_20", "Истори-мейкер", "Создай 20 Stories", "📸", AchievementRarity.RARE, 250, "count", 20),

        # Ниши (из content_engine/niche_manager.py)
        Achievement("niche_explorer", "Исследователь", "Попробуй 5 разных ниш", "🔍", AchievementRarity.COMMON, 75, "count", 5),
        Achievement("niche_master", "Мастер ниш", "Создай контент во всех нишах", "🎯", AchievementRarity.EPIC, 500, "count", 10),

        # Рефералы (из referral.py)
        Achievement("first_ref", "Пригласитель", "Приведи первого друга", "🤝", AchievementRarity.COMMON, 100, "count", 1),
        Achievement("ref_5", "Сетевик", "Приведи 5 друзей", "🕸️", AchievementRarity.RARE, 400, "count", 5),
        Achievement("ref_20", "Лидер мнений", "Приведи 20 друзей", "📢", AchievementRarity.EPIC, 1000, "count", 20),

        # Подписка (из subscription.py + payment/)
        Achievement("subscriber", "Подписчик", "Оформи подписку", "💎", AchievementRarity.RARE, 200, "one_time", 1),
        Achievement("loyal_30", "Лояльный", "Будь подписчиком 30 дней", "🏅", AchievementRarity.EPIC, 500, "streak", 30),
        Achievement("loyal_90", "Ветеран", "Будь подписчиком 90 дней", "🎖️", AchievementRarity.LEGENDARY, 1500, "streak", 90),

        # Сери (из middlewares + ежедневная активность)
        Achievement("streak_3", "На волне", "3 дня подряд", "🔥", AchievementRarity.COMMON, 50, "streak", 3),
        Achievement("streak_7", "Неделя огня", "7 дней подряд", "🔥🔥", AchievementRarity.RARE, 150, "streak", 7),
        Achievement("streak_30", "Месяц без остановки", "30 дней подряд", "🔥🔥🔥", AchievementRarity.LEGENDARY, 1000, "streak", 30),

        # Языки (из i18n/)
        Achievement("polyglot", "Полиглот", "Смени язык 3 раза", "🌍", AchievementRarity.COMMON, 25, "count", 3),
    ]

    def __init__(self):
        self.achievements_by_id = {a.id: a for a in self.ACHIEVEMENTS}

    def check_achievements(self, user_stats: Dict) -> List[Achievement]:
        """Проверяет, какие достижения можно выдать"""
        unlocked = []

        for ach in self.ACHIEVEMENTS:
            current_value = user_stats.get(ach.condition_type, 0)
            if current_value >= ach.condition_value:
                unlocked.append(ach)

        return unlocked

    def render_achievements_list(self, unlocked: List[str], total: int = None) -> str:
        """Красивый список достижений"""
        if total is None:
            total = len(self.ACHIEVEMENTS)

        lines = []
        lines.append(f"🏅 **ДОСТИЖЕНИЯ** ({len(unlocked)}/{total})")
        lines.append("━" * 30)

        for ach_id in unlocked:
            ach = self.achievements_by_id.get(ach_id)
            if ach:
                lines.append(ach.render())
                lines.append("")

        if not unlocked:
            lines.append("🌱 Пока нет достижений. Начни создавать контент!")

        # Прогресс коллекции
        percent = (len(unlocked) / total) * 100
        filled = int(percent / 5)
        bar = "█" * filled + "░" * (20 - filled)
        lines.append(f"\n📊 Коллекция: [{bar}] {percent:.0f}%")

        return "\n".join(lines)