from typing import Union, List, Optional

class MessageFormatter:
    """
    Единый форматтер для ВСЕХ сообщений бота.
    Обеспечивает консистентный, красивый дизайн.
    """

    @staticmethod
    def header(text: str, emoji: str = "✨") -> str:
        return f"{emoji} **{text.upper()}** {emoji}\n{'━' * 32}\n"

    @staticmethod
    def section(title: str, content: str, emoji: str = "▸") -> str:
        return f"{emoji} **{title}**\n{content}\n"

    @staticmethod
    def stat_line(label: str, value: Union[int, str, float], emoji: str = "") -> str:
        return f"  {emoji} {label}: `{value}`\n"

    @staticmethod
    def divider(char: str = "━", length: int = 32) -> str:
        return f"\n{char * length}\n"

    @staticmethod
    def footer(text: str) -> str:
        return f"\n{'─' * 32}\n_{text}_"

    @classmethod
    def profile_card(
        cls,
        username: str,
        level: int,
        level_title: str,
        xp: int,
        xp_needed: int,
        progress_bar: str,
        rank: int,
        streak: int,
        achievements_count: int,
        total_achievements: int,
        content_count: int,
        referrals: int
    ) -> str:
        """Карточка профиля — визитная карточка бота"""
        msg = cls.header(f"Профиль {username}", "👤")
        msg += cls.stat_line("Звание", level_title, "🏆")
        msg += cls.stat_line("Уровень", level, "🎯")
        msg += cls.stat_line("Ранг", f"#{rank}", "🏅")
        msg += cls.stat_line("Серия", f"{streak} дней", "🔥")
        msg += cls.divider("─")
        msg += f"📊 Прогресс: {progress_bar}\n"
        msg += f"   `{xp} / {xp_needed} XP`\n"
        msg += cls.divider("─")
        msg += cls.stat_line("Контент создан", content_count, "📝")
        msg += cls.stat_line("Рефералов", referrals, "🤝")
        msg += cls.stat_line("Достижения", f"{achievements_count}/{total_achievements}", "🏅")
        msg += cls.footer("Продолжай создавать — расти быстрее!")
        return msg

    @classmethod
    def xp_gain_notification(
        cls,
        action: str,
        base_xp: int,
        total_xp: int,
        streak_bonus: int = 0,
        new_level: Optional[int] = None
    ) -> str:
        """Уведомление о получении XP — instant feedback"""
        lines = []
        lines.append(f"✨ **+{base_xp} XP** за {action}")

        if streak_bonus > 0:
            lines.append(f"🔥 Бонус серии: +{streak_bonus} XP")

        lines.append(f"📊 Всего XP: {total_xp}")

        if new_level:
            lines.append("")
            lines.append(f"🎉 **ПОВЫШЕНИЕ УРОВНЯ!**")
            lines.append(f"   Теперь ты {new_level} уровня!")

        return "\n".join(lines)