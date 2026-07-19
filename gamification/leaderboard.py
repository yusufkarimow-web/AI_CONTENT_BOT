from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class LeaderboardEntry:
    user_id: int
    username: str
    level: int
    total_xp: int
    streak: int
    content_count: int
    rank: int
    is_current_user: bool = False
    is_near_user: bool = False


class LeaderboardEngine:
    """
    Лидерборд с психологическими триггерами:
    - Показываем ближайших конкурентов (competitive context)
    - "Ты обогнал X человек за неделю"
    - Процентили для мотивации
    """

    def __init__(self, db_connection):
        self.db = db_connection

    async def get_personalized_leaderboard(
        self,
        user_id: int,
        limit: int = 10
    ) -> Dict:
        """
        Возвращает персонализированный лидерборд:
        - Топ-3 (aspiration target)
        - Пользователь + ±2 соседа (competitive context)
        """
        # Получаем глобальный топ
        top_global = await self._get_top_players(3)

        # Получаем позицию пользователя
        user_rank = await self._get_user_rank(user_id)
        user_data = await self._get_user_data(user_id)

        # Получаем соседей
        neighbors = await self._get_neighbors(user_id, 2)

        # Общее количество пользователей
        total_users = await self._get_total_users()
        percentile = ((total_users - user_rank) / total_users) * 100 if total_users > 0 else 0

        # Рост за неделю
        weekly_growth = await self._get_weekly_growth(user_id)

        return {
            "top_global": top_global,
            "user_context": neighbors,
            "user_rank": user_rank,
            "user_data": user_data,
            "percentile": percentile,
            "total_users": total_users,
            "weekly_growth": weekly_growth,
            "motivation": self._generate_motivation(user_rank, percentile, weekly_growth)
        }

    def _generate_motivation(self, rank: int, percentile: float, growth: int) -> str:
        """Генерация мотивирующего сообщения"""
        parts = []

        if rank == 1:
            parts.append("👑 Ты на вершине! Защищай свой титул!")
        elif rank <= 3:
            parts.append(f"🥈 Ты в топ-3! Всего {rank-1} человек впереди!")
        elif rank <= 10:
            parts.append(f"🔥 Ты в элите! Целься в топ-3!")
        elif percentile >= 90:
            parts.append(f"⭐ Ты в топ-{100-percentile:.0f}%! Целься в топ-10!")
        elif percentile >= 50:
            parts.append(f"📈 Ты лучше {percentile:.0f}% пользователей!")
        else:
            parts.append("🌱 Отличное начало! Постоянство = результат!")

        if growth > 0:
            parts.append(f"📊 За неделю ты обогнал {growth} человек!")
        elif growth < 0:
            parts.append(f"⚠️ За неделю тебя обогнали {abs(growth)} человек. Вперёд!")

        return "\n".join(parts)

    def render_leaderboard(self, data: Dict) -> str:
        """Красивый рендер лидерборда"""
        lines = []
        lines.append("🏆 **ГЛОБАЛЬНЫЙ ЛИДЕРБОРД**")
        lines.append("━" * 30)

        # Топ-3
        for i, player in enumerate(data["top_global"], 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "•")
            lines.append(
                f"{medal} #{i} {player.username} | "
                f"Ур.{player.level} | {player.total_xp} XP"
            )

        lines.append("─" * 30)

        # Контекст пользователя
        if data["user_context"]:
            lines.append("👤 **Ты и твои соседи:**")
            for player in data["user_context"]:
                marker = "👉" if player.is_current_user else "  "
                lines.append(
                    f"{marker} #{player.rank} {player.username} | "
                    f"Ур.{player.level} | {player.total_xp} XP"
                )

        lines.append("━" * 30)
        lines.append(data["motivation"])

        return "\n".join(lines)

    # Stub-методы для интеграции с твоей БД
    async def _get_top_players(self, limit: int) -> List[LeaderboardEntry]:
        """Заглушка — заменить на реальный запрос к твоей БД"""
        return []

    async def _get_user_rank(self, user_id: int) -> int:
        return 1

    async def _get_user_data(self, user_id: int) -> Optional[LeaderboardEntry]:
        return None

    async def _get_neighbors(self, user_id: int, context: int) -> List[LeaderboardEntry]:
        return []

    async def _get_total_users(self) -> int:
        return 1

    async def _get_weekly_growth(self, user_id: int) -> int:
        return 0