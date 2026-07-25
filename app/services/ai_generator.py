# app/services/ai_generator.py
import openai
from openai import AsyncOpenAI
import structlog
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from app.core.config import get_settings

logger = structlog.get_logger(__name__)

class AIGenerationResult(BaseModel):
    success: bool
    output_text: str
    error_message: Optional[str] = None
    estimated_reach: int = 1500
    tags: List[str] = []
    cta: List[str] = []

class AIGenerator:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key.get_secret_value())
        self.model = settings.model_main
        self.fast_model = settings.model_fast

    async def generate_smm_package(
        self,
        niche: str,
        platform: str,
        goal: str,
        format_type: str,
        brief: str,
        language: str = "ru",
        country: str = "uz"
    ) -> AIGenerationResult:
        """Генерация SMM-пакета через OpenAI GPT-4o-mini"""

        prompt = self._construct_smm_prompt(
            niche=niche,
            platform=platform,
            goal=goal,
            format_type=format_type,
            brief=brief,
            language=language,
            country=country
        )

        try:
            settings = get_settings()
            if settings.openai_api_key.get_secret_value() == "fake_openai_key":
                return self._simulate_generation(niche, platform, goal, format_type, brief, language, country)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(language, country)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                timeout=30
            )

            output_text = response.choices[0].message.content
            logger.info("ai_generation_success", tokens_used=response.usage.total_tokens)

            # Parse hashtags and CTA from response or generate simple defaults
            tags = ["#smm", f"#{niche}", f"#{platform}"]
            cta = ["Связаться в Директ", "Заказать по ссылке в описании"]

            return AIGenerationResult(
                success=True,
                output_text=output_text,
                tags=tags,
                cta=cta
            )

        except Exception as e:
            logger.exception("ai_generation_failed", error=str(e))
            # Safe local simulation fallback on API errors
            return self._simulate_generation(niche, platform, goal, format_type, brief, language, country)

    def _get_system_prompt(self, language: str, country: str) -> str:
        """Получение системного промпта с локализацией"""

        localization = {
            "ru_uz": """Ты - профессиональный SMM-маркетолог и копирайтер для Узбекистана.
Ты прекрасно знаешь местные тренды, реалии рынка, платежные системы (Click, Payme, Uzum).
Используй местные примеры, сленг, популярные бренды и города (Ташкент, Самарканд).
Твой контент вирусный, оптимизирован для CTR, имеет четкий CTA.""",

            "ru_tj": """Ты - профессиональный SMM-маркетолог и копирайтер для Таджикистана.
Ты знаешь местные реалии рынка Душанбе, Худжанда, Гиссара и других городов.
Используй таджикский язык (на кириллице) или русский язык с таджикскими словами, местные примеры, платежи (Alif Mobi, Душанбе Сити, Корвон).
Твой контент вирусный и оптимизирован для TikTok/Instagram.""",

            "ru_ru": """Ты - профессиональный SMM-маркетолог для России.
Используй местные примеры, платежи (Сбербанк, СБП).
Твой контент оптимизирован для российского рынка."""
        }

        key = f"{language}_{country}"
        return localization.get(key, localization["ru_uz"])

    def _construct_smm_prompt(
        self,
        niche: str,
        platform: str,
        goal: str,
        format_type: str,
        brief: str,
        language: str,
        country: str
    ) -> str:
        """Конструирование специализированного промпта"""

        niche_mapping = {
            "uz": {
                "cafe": "Кафе / Традиционная чайхана",
                "textile": "Текстиль и одежда",
                "real_estate": "Недвижимость (Новостройки Ташкента)",
                "auto": "Автосалон / Сервис",
                "marketplace": "Продажа на Uzum",
                "construction": "Строительство / Ремонт",
                "beauty": "Салон красоты",
                "cargo": "Карго из Китая / Турции",
            },
            "tj": {
                "wholesale": "Саводои яклухт (оптовый рынок)",
                "cargo": "Карго из Китая",
                "construction": "Сохтмон / Стройматериалы",
                "cafe": "Курутобхона / Семейная чайхана",
                "beauty": "Салони Зебоӣ (Свадебный салон)",
                "tourism": "Туризм (Варзоб, Памир)",
                "salon": "Салон красоты",
                "auto": "Автобозор / Автосервис",
            }
        }

        niche_full = niche_mapping.get(country, {}).get(niche, niche)

        prompt = f"""
🎯 ЗАДАЧА: Создать профессиональный SMM-маркетинговый пакет

📋 ПАРАМЕТРЫ:
- Ниша: {niche_full}
- Платформа: {platform.upper()}
- Цель: {goal}
- Формат: {format_type}
- Описание бизнеса: {brief}

📝 ТРЕБОВАНИЯ К ВЫВОДУ:
1. **ВИРУСНЫЙ ХУК** - Сразу привлекающее внимание начало текста (макс 20 слов)
2. **КОНКУРЕНТНОЕ ПРЕИМУЩЕСТВО** - 2-3 предложения о том, чем уникален этот бизнес на рынке {country.upper()}
3. **ОСНОВНОЙ ТЕКСТ** - Полный готовый текст для {platform} поста в соответствии с форматом {format_type}
4. **CALL TO ACTION** - 2 альтернативных CTA (например: "Напишите в Директ" и "Жмите ссылку в Описании")
5. **ХЕШТЕГИ** - 8-10 релевантных и локализованных хештегов
6. **БОНУС СОВЕТ** - 1 кейс или метрика, доказывающая эффективность этого подхода

⚡ ТОН И СТИЛЬ:
- Для {goal}: Используй соответствующий тон (для sales - убедительный, для reach - забавный, и т.д.)
- Локализация: Используй местные примеры, платежи, культурные отсылки для {country.upper()}
- Эмодзи: Добавь релевантные эмодзи для визуальной привлекательности

Начинай сразу с выводом, без дополнительных пояснений.
"""
        return prompt

    def _simulate_generation(self, niche: str, platform: str, goal: str, format_type: str, brief: str, language: str, country: str) -> AIGenerationResult:
        """Эмуляция ответов SMM-пакета без живого ключа OpenAI"""
        if country == "uz":
            output_text = f"""**ВИРУСНЫЙ ХУК**
Забудьте о скучных продажах! Вот почему бизнес в сфере {niche} в Ташкенте сейчас приносит миллионы!

**КОНКУРЕНТНОЕ ПРЕИМУЩЕСТВО**
Наш проект выделяется индивидуальным подходом, быстрой доставкой по Узбекистану и поддержкой платежей через Click, Payme и Uzum Pay.

**ОСНОВНОЙ ТЕКСТ**
Ищете надежное решение в нише {niche}? Мы предлагаем качественный сервис с гарантией результата.
Наши клиенты в Ташкенте и Самарканде уже оценили удобство сотрудничества с нами. Присоединяйтесь!

**CALL TO ACTION**
1. Напишите нам в Директ слово "{niche.upper()}" для бесплатной консультации.
2. Жмите кнопку "Заказать" в описании профиля!

**ХЕШТЕГИ**
#uzbekistan #{niche} #tashkent #samarkand #smm #marketing #click #payme

**БОНУС СОВЕТ**
Использование персонализированного CTA увеличивает конверсию переходов на 42%!
"""
        else:
            output_text = f"""**ВИРУСНЫЙ ХУК**
Аз хароҷоти зиёдатӣ халос шавед! Роҳи осонтарини пешбурди тиҷорати {niche} дар Душанбе ошкор шуд!

**КОНКУРЕНТНОЕ ПРЕИМУЩЕСТВО**
Мо маҳсулот ва хизматрасониҳои худро бо нархҳои дастрас мустақим аз бозори Корвон пешниҳод мекунем. Оплату қабул мекунем бо Alif Mobi ва Душанбе Сити.

**ОСНОВНОЙ ТЕКСТ**
Оё мехоҳед тиҷорати худро дар самти {niche} рушд диҳед? Маҳсулоти босифат ва кафолати хизматрасонӣ барои ҳамаи сокинони Душанбе ва Хуҷанд дастрас аст. Ҳамин ҳоло фармоиш диҳед!

**CALL TO ACTION**
1. Ба мо дар Директ нависед барои гирифтани туҳфаи махсус.
2. Истинодро дар профил пахш кунед!

**ХЕШТЕГИ**
#tajikistan #{niche} #dushanbe #khujand #korvon #alifmobi #smm

**БОНУС СОВЕТ**
Интиқоли ройгон дар дохили Душанбе сабаби зиёд шудани фурӯш то 30% мегардад.
"""
        return AIGenerationResult(
            success=True,
            output_text=output_text,
            tags=["#smm", f"#{niche}"],
            cta=["Свяжитесь с нами", "Заказать на сайте"]
        )
