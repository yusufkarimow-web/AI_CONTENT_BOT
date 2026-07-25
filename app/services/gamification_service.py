# app/services/gamification_service.py
import uuid
import structlog
from datetime import datetime
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import EmpireUserStats, EmpireBusiness, EmpireEvent, User
from app.core.errors import ValidationError, NotFoundError
import random

logger = structlog.get_logger(__name__)

class GamificationService:
    """Управление игрой TojikAI Empire (Бизнес Империя)"""

    CITIES = {
        "tj": ["Dushanbe", "Khujand", "Bokhtar", "Kulob", "Khorog"],
        "uz": ["Tashkent", "Samarkand", "Bukhara", "Andijan", "Fergana"]
    }

    BUSINESSES = {
        "tj": {
            "cafe": {
                "name": "Курутобхона",
                "base_income": 50000,  # per hour in TJS
                "emoji": "☕"
            },
            "salon": {
                "name": "Салони Зебоӣ",
                "base_income": 100000,
                "emoji": "💅"
            },
            "textile": {
                "name": "Корхонаи Парчаи",
                "base_income": 80000,
                "emoji": "👕"
            },
            "cargo": {
                "name": "Карго аз Чин",
                "base_income": 120000,
                "emoji": "📦"
            }
        },
        "uz": {
            "cafe": {
                "name": "Чайхона",
                "base_income": 50000,  # per hour in UZS
                "emoji": "☕"
            },
            "salon": {
                "name": "Салон красоты",
                "base_income": 100000,
                "emoji": "💅"
            },
            "textile": {
                "name": "Ткацкая фабрика",
                "base_income": 80000,
                "emoji": "👕"
            },
            "cargo": {
                "name": "Карго Узум",
                "base_income": 120000,
                "emoji": "📦"
            }
        }
    }

    EVENTS = {
        "tj": [
            {
                "title": "🌧 Сильный дождь в Варзобской долине",
                "description": "Многие магазины закрылись из-за наводнения",
                "options": {
                    "evacuate": {"label": "Эвакуировать товары", "impact": -30},
                    "wait": {"label": "Ждать и надеяться", "impact": -50}
                }
            },
            {
                "title": "🎉 Национальный праздник Наврузы",
                "description": "Продажи выросли на 200%!",
                "options": {
                    "expand": {"label": "Нанять еще рабочих", "impact": 50},
                    "save": {"label": "Сэкономить прибыль", "impact": 20}
                }
            }
        ],
        "uz": [
            {
                "title": "🎊 Праздник Навруза",
                "description": "Спрос на товары вырос в 3 раза!",
                "options": {
                    "expand": {"label": "Нанять дополнительный персонал", "impact": 40},
                    "invest": {"label": "Инвестировать в оборудование", "impact": 30}
                }
            },
            {
                "title": "📱 Новый конкурент в городе",
                "description": "Появился новый крупный магазин",
                "options": {
                    "compete": {"label": "Снизить цены", "impact": -20},
                    "improve": {"label": "Улучшить сервис", "impact": 10}
                }
            }
        ]
    }

    def __init__(self, db: AsyncSession, user_country: str = "uz"):
        self.db = db
        self.user_country = user_country

    async def initialize_user_game(self, user_id: str) -> bool:
        """Инициализация игры для нового пользователя"""

        try:
            # Проверка наличия статистики
            stats_stmt = select(EmpireUserStats).where(EmpireUserStats.user_id == user_id)
            result = await self.db.execute(stats_stmt)
            existing_stats = result.scalar_one_or_none()

            if existing_stats:
                return True

            # Создание начальной статистики
            country_cities = self.CITIES.get(self.user_country, self.CITIES["uz"])
            initial_stats = EmpireUserStats(
                user_id=user_id,
                balance=1000.00,
                xp=0,
                level=1,
                passive_income_per_hour=0.00,
                current_city=country_cities[0],
                unlocked_cities=[country_cities[0]]
            )
            self.db.add(initial_stats)
            await self.db.commit()

            logger.info("game_initialized", user_id=user_id, start_balance=1000.0)
            return True

        except Exception as e:
            logger.exception("game_init_error", error=str(e))
            await self.db.rollback()
            return False

    async def buy_business(
        self,
        user_id: str,
        city: str,
        business_type: str
    ) -> dict:
        """Покупка бизнеса"""

        try:
            # Проверка наличия города в разблокированных
            stats_stmt = select(EmpireUserStats).where(EmpireUserStats.user_id == user_id)
            stats_result = await self.db.execute(stats_stmt)
            stats = stats_result.scalar_one_or_none()

            if not stats:
                raise NotFoundError("EmpireUserStats", user_id)

            if city not in stats.unlocked_cities:
                raise ValidationError(f"Город {city} не разблокирован", {
                    "available_cities": stats.unlocked_cities
                })

            # Получение данных бизнеса
            business_data = self.BUSINESSES.get(self.user_country, self.BUSINESSES["uz"]).get(business_type)
            if not business_data:
                raise ValidationError(f"Неизвестный тип бизнеса: {business_type}")

            # Цена бизнеса = base_income * 10
            price = business_data["base_income"] * 10

            if stats.balance < price:
                return {
                    "success": False,
                    "error": "Недостаточно средств",
                    "required": price,
                    "available": float(stats.balance)
                }

            # Создание бизнеса
            business = EmpireBusiness(
                id=uuid.uuid4(),
                user_id=user_id,
                city=city,
                business_type=business_type,
                name=f"{business_data['name']} в {city}",
                level=1,
                base_income_per_hour=business_data["base_income"],
                current_income_per_hour=business_data["base_income"],
                total_earnings=0.0
            )

            # Снятие средств
            stats.balance -= price
            stats.passive_income_per_hour += Decimal(str(business_data["base_income"] / 3600))
            stats.updated_at = datetime.utcnow()

            self.db.add(business)
            await self.db.commit()

            logger.info(
                "business_purchased",
                user_id=user_id,
                business_type=business_type,
                city=city,
                price=price
            )

            return {
                "success": True,
                "business_id": str(business.id),
                "business_name": business.name,
                "remaining_balance": float(stats.balance)
            }

        except Exception as e:
            logger.exception("buy_business_error", error=str(e))
            await self.db.rollback()
            return {"success": False, "error": str(e)}

    async def hire_staff(
        self,
        user_id: str,
        business_id: str,
        staff_type: str
    ) -> dict:
        """Наем персонала (менеджер, маркетолог, водитель)"""

        try:
            # Получение бизнеса
            business_stmt = select(EmpireBusiness).where(
                (EmpireBusiness.id == business_id) &
                (EmpireBusiness.user_id == user_id)
            )
            business_result = await self.db.execute(business_stmt)
            business = business_result.scalar_one_or_none()

            if not business:
                raise NotFoundError("EmpireBusiness", business_id)

            # Получение статистики
            stats_stmt = select(EmpireUserStats).where(EmpireUserStats.user_id == user_id)
            stats_result = await self.db.execute(stats_stmt)
            stats = stats_result.scalar_one_or_none()

            # Цены и эффекты
            staff_config = {
                "manager": {"price": 50000, "income_boost": 1.15},
                "marketer": {"price": 40000, "income_boost": 1.20},
                "driver": {"price": 30000, "income_boost": 1.10}
            }

            config = staff_config.get(staff_type)
            if not config:
                raise ValidationError(f"Неизвестный тип персонала: {staff_type}")

            if stats.balance < config["price"]:
                return {"success": False, "error": "Недостаточно средств"}

            # Наем персонала
            stats.balance -= config["price"]
            business.team_size += 1
            business.current_income_per_hour = Decimal(str(
                float(business.base_income_per_hour) * config["income_boost"]
            ))

            if staff_type == "manager":
                business.manager_hired = True
            elif staff_type == "marketer":
                business.marketer_hired = True

            await self.db.commit()

            logger.info(
                "staff_hired",
                user_id=user_id,
                business_id=business_id,
                staff_type=staff_type
            )

            return {
                "success": True,
                "message": f"{staff_type.capitalize()} нанят успешно",
                "new_income": float(business.current_income_per_hour)
            }

        except Exception as e:
            logger.exception("hire_staff_error", error=str(e))
            await self.db.rollback()
            return {"success": False, "error": str(e)}

    async def collect_passive_income(self, user_id: str) -> dict:
        """Сбор пассивного дохода"""

        try:
            stats_stmt = select(EmpireUserStats).where(EmpireUserStats.user_id == user_id)
            stats_result = await self.db.execute(stats_stmt)
            stats = stats_result.scalar_one_or_none()

            if not stats:
                raise NotFoundError("EmpireUserStats", user_id)

            # Подсчет времени с последнего сбора
            now = datetime.utcnow()
            if stats.last_passive_income_at:
                hours_passed = (now - stats.last_passive_income_at).total_seconds() / 3600
            else:
                hours_passed = 0  # Первый раз

            # Максимум можно собрать за 24 часа
            hours_passed = min(hours_passed, 24)

            income = float(stats.passive_income_per_hour) * hours_passed

            stats.balance += Decimal(str(income))
            stats.last_passive_income_at = now
            stats.updated_at = now

            await self.db.commit()

            logger.info(
                "passive_income_collected",
                user_id=user_id,
                hours=hours_passed,
                income=income
            )

            return {
                "success": True,
                "income": income,
                "new_balance": float(stats.balance)
            }

        except Exception as e:
            logger.exception("collect_income_error", error=str(e))
            return {"success": False, "error": str(e)}

    async def trigger_random_event(self, user_id: str) -> dict:
        """Случайное игровое событие"""

        try:
            events = self.EVENTS.get(self.user_country, self.EVENTS["uz"])
            event_data = random.choice(events)

            event = EmpireEvent(
                id=uuid.uuid4(),
                user_id=user_id,
                title=event_data["title"],
                description=event_data["description"],
                city="Dushanbe",  # Random city
                impact_type="neutral",
                options=event_data["options"]
            )

            self.db.add(event)
            await self.db.commit()

            return {
                "success": True,
                "event_id": str(event.id),
                "title": event.title,
                "description": event.description,
                "options": event.options
            }

        except Exception as e:
            logger.exception("trigger_event_error", error=str(e))
            return {"success": False, "error": str(e)}
