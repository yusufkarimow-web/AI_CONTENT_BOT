import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

class TriggerType(Enum):
    SCARCITY = "scarcity"           # Ограниченное время
    AUTHORITY = "authority"         # Экспертное мнение
    CONSENSUS = "consensus"         # Социальное доказательство
    COMMITMENT = "commitment"       # Последовательность
    RECIPROCITY = "reciprocity"     # Взаимность
    LOSS_AVERSION = "loss_aversion" # Страх потери
    NEAR_MISS = "near_miss"         # Почти получилось


class PsychologyEngine:
    """
    Движок психологических триггеров.
    НЕ манипуляция — усиление ценности действия.
    """

    def __init__(self):
        self.active_events = {}
        self.user_sessions = {}

    def create_limited_time_event(
        self,
        event_id: str,
        title: str,
        description: str,
        duration_hours: int,
        bonus_xp: int,
        participants: int = 0
    ) -> Dict:
        """Событие с ограниченным временем — scarcity trigger"""
        end_time = datetime.now() + timedelta(hours=duration_hours)

        return {
            "id": event_id,
            "type": TriggerType.SCARCITY,
            "title": title,
            "description": description,
            "ends_at": end_time,
            "bonus_xp": bonus_xp,
            "participants": participants,
        }

    def render_scarcity_event(self, event: Dict) -> str:
        time_left = event["ends_at"] - datetime.now()
        hours = max(0, int(time_left.total_seconds() // 3600))
        minutes = max(0, int((time_left.total_seconds() % 3600) // 60))

        return (
            f"⏰ **{event['title'].upper()}**\n"
            f"{'━' * 30}\n"
            f"🎁 {event['description']}\n"
            f"💰 Бонус: +{event['bonus_xp']} XP\n"
            f"⏳ Осталось: {hours}ч {minutes}м\n"
            f"👥 Уже участвуют: {event['participants']} человек\n"
            f"⚡ Успей — время ограничено!"
        )

    def generate_daily_challenge(self, user_level: int, content_stats: Dict) -> Dict:
        """Ежедневный вызов с привязкой к активности"""
        challenges = [
            {
                "id": "daily_content",
                "name": "Марафон контента",
                "task": "Создай 3 поста",
                "reward": 50 + user_level * 5,
                "check": lambda s: s.get('content_generated', 0) >= 3
            },
            {
                "id": "daily_reels",
                "name": "Reels-день",
                "task": "Создай 1 Reels",
                "reward": 75 + user_level * 8,
                "check": lambda s: s.get('reels_generated', 0) >= 1
            },
            {
                "id": "daily_referral",
                "name": "День друга",
                "task": "Пригласи 1 друга",
                "reward": 100 + user_level * 10,
                "check": lambda s: s.get('referrals_today', 0) >= 1
            },
            {
                "id": "daily_niche",
                "name": "Исследователь",
                "task": "Попробуй новую нишу",
                "reward": 40 + user_level * 4,
                "check": lambda s: s.get('new_niche_today', False)
            },
        ]

        # Выбираем челлендж, который пользователь ещё не выполнил
        # В реальности — проверять against БД
        return random.choice(challenges)

    def render_social_proof(self, action: str, count: int, trend: str = "up") -> str:
        """Социальное доказательство"""
        templates = {
            "up": [
                f"👥 {count} человек уже {action} сегодня",
                f"🔥 Присоединяйся к {count}+ участникам",
                f"⭐ {count} пользователей рекомендуют",
            ],
            "down": [
                f"📉 Только {count} человек {action} — будь первым!",
                f"💎 Редкая активность: {count} участников",
            ]
        }
        return random.choice(templates.get(trend, templates["up"]))

    def render_near_miss(self, current: int, target: int, reward: str) -> str:
        """Near-miss effect — мотивирует доделать"""
        remaining = target - current

        messages = [
            f"🎯 Ещё {remaining} и получишь {reward}!",
            f"💪 Осталось совсем чуть-чуть: {remaining}",
            f"🔥 Почти там! {remaining} до {reward}",
        ]

        return random.choice(messages)

    def render_loss_aversion(self, streak: int, hours_until_reset: int) -> str:
        """Страх потери серии"""
        if streak <= 1:
            return ""

        return (
            f"⚠️ **ВНИМАНИЕ!**\n"
            f"Твоя серия 🔥 x{streak} скоро сгорит!\n"
            f"⏰ Осталось {hours_until_reset}ч чтобы сохранить её.\n"
            f"🚀 Зайди и создай контент — не теряй прогресс!"
        )

    def render_reciprocity(self, free_content_count: int) -> str:
        """Взаимность — дали бесплатно, просим взамен"""
        if free_content_count >= 3:
            return (
                f"💝 Ты уже использовал {free_content_count} бесплатных генерации!\n"
                f"🌟 Подписка откроет безлимит + бонусы XP\n"
                f"👉 Поддержи проект — получи преимущества!"
            )
        return ""