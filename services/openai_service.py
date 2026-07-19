# services/openai_service.py — OpenAI сервис для Sozanda
# Поддержка: системные промпты, мультиязычность, retry, fallback

import os
import time
import random
from typing import Optional, List, Dict
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

from config import OPENAI_API_KEY, OPENAI_MODEL

load_dotenv()

# ============================================
# КОНФИГУРАЦИЯ
# ============================================

# Проверяем ключ
_api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
if not _api_key:
    print("⚠️ WARNING: OPENAI_API_KEY не найден! Будет использоваться fallback-генератор.")

client = OpenAI(api_key=_api_key) if _api_key else None

# Настройки retry
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # секунды
TIMEOUT_SECONDS = 30


# ============================================
# КЭШ ПРОМПТОВ (для повторного использования)
# ============================================

_prompt_cache: Dict[str, str] = {}


# ============================================
# ОСНОВНАЯ ФУНКЦИЯ ГЕНЕРАЦИИ
# ============================================

def generate_content(
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    topic: Optional[str] = None,
    niche: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.85,
    max_tokens: int = 1500,
    language: str = "ru"
) -> str:
    """
    Универсальная функция генерации контента через OpenAI

    Args:
        system_prompt: Системный промпт (инструкции для AI)
        user_prompt: Промпт пользователя (конкретная задача)
        topic: Тема (legacy, для обратной совместимости)
        niche: Ниша (legacy, для обратной совместимости)
        model: Модель OpenAI (по умолчанию из config)
        temperature: Креативность (0.0-2.0)
        max_tokens: Максимальная длина ответа
        language: "ru" или "tg"

    Returns:
        str: Сгенерированный контент или fallback
    """

    # Если вызвано в legacy-режиме (только topic + niche)
    if topic and niche and not user_prompt:
        return _generate_legacy(topic, niche, language)

    # Формируем сообщения
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    if user_prompt:
        messages.append({
            "role": "user",
            "content": user_prompt
        })

    # Если нет промптов — ошибка
    if not messages:
        return _fallback_no_prompt()

    # Выбираем модель
    _model = model or OPENAI_MODEL or "gpt-4o-mini"

    # Пытаемся сгенерировать с retry
    for attempt in range(MAX_RETRIES):
        try:
            if not client:
                raise Exception("OpenAI клиент не инициализирован")

            response = client.chat.completions.create(
                model=_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=TIMEOUT_SECONDS
            )

            content = response.choices[0].message.content

            # Пост-обработка
            content = _post_process(content, language)

            return content

        except RateLimitError:
            # Лимит API — ждём и пробуем снова
            wait_time = RETRY_DELAY_BASE * (2 ** attempt) + random.uniform(0, 1)
            print(f"⏳ Rate limit. Ждём {wait_time:.1f}с... (попытка {attempt + 1}/{MAX_RETRIES})")
            time.sleep(wait_time)

        except APITimeoutError:
            # Таймаут — пробуем снова
            wait_time = RETRY_DELAY_BASE * (2 ** attempt)
            print(f"⏳ Таймаут. Ждём {wait_time:.1f}с... (попытка {attempt + 1}/{MAX_RETRIES})")
            time.sleep(wait_time)

        except APIError as e:
            # Ошибка API — пробуем снова
            print(f"❌ Ошибка API: {e}. Попытка {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_BASE)

        except Exception as e:
            # Любая другая ошибка
            print(f"❌ Ошибка генерации: {e}")
            break

    # Все попытки исчерпаны — fallback
    print("⚠️ Все попытки исчерпаны. Используем fallback.")
    return _fallback_generate(topic, niche, language, user_prompt)


# ============================================
# LEGACY: Старая функция (для обратной совместимости)
# ============================================

def _generate_legacy(topic: str, niche: str, language: str = "ru") -> str:
    """
    Legacy-генератор для старых вызовов generate_content(topic, niche)
    Теперь использует умные промпты с системным контекстом
    """

    # Системный промпт для legacy
    system = _get_legacy_system_prompt(language)

    # Пользовательский промпт
    user = _get_legacy_user_prompt(topic, niche, language)

    return generate_content(
        system_prompt=system,
        user_prompt=user,
        language=language
    )


def _get_legacy_system_prompt(language: str) -> str:
    """Системный промпт для legacy-режима"""

    prompts = {
        "ru": """Ты — эксперт по SMM и контент-маркетингу в Таджикистане.
Твоя задача — создавать вирусный контент для бизнеса в социальных сетях.

Правила:
- Пиши простым, разговорным русским языком
- Добавляй локальные реалии Таджикистана (Душанбе, Хуҷанд, Кӯлоб, Памир)
- Используй таджикскую культуру, традиции, еду (плов, чай, мехмоннавози)
- Делай контент цепляющим — первые 3 секунды решают всё
- Добавь призыв к действию
- Используй эмодзи для визуального разделения""",

        "tg": """Ту — мутахассиси SMM ва маркетинги мундод дар Тоҷикистон.
Вазифаи ту — офтани мундоди вирусӣ барои бизнес дар шабакаҳои иҷтимоӣ.

Қоидаҳо:
- Ба забони оддӣ, гуфтории тоҷикӣ бинавис
- Реалияҳои маҳаллии Тоҷикистон илова кун (Душанбе, Хуҷанд, Кӯлоб, Помир)
- Фарҳанги тоҷикӣ, анъанаҳо, хӯрок (пулов, чой, меҳмоннавозӣ) истифода бар
- Мундодро ҷолиб кун — 3 сонияи аввал ҳамаро ҳал мекунад
- Даъват ба амал илова кун
- Эмодзи барои тақсими визуалӣ истифода бар""",
    }

    return prompts.get(language, prompts["ru"])


def _get_legacy_user_prompt(topic: str, niche: str, language: str) -> str:
    """Пользовательский промпт для legacy-режима"""

    if language == "tg":
        return f"""Мундод барои бизнес созед.

Ниша: {niche}
Мавзӯъ: {topic}

Ҳатман дар формати зерин баргардонед:

🎬 Сарлавҳа

🎥 Сенарияи Reels

🎙 Матни гӯянда

📱 Пости Instagram

📢 Пости Telegram

#️⃣ Хештегҳо

🖼 Идеяи рӯйи саҳифа

🤖 Промпт барои акс

Забони оддӣ, аммо ҷолиб истифода баред."""

    return f"""Создай контент для бизнеса.

Ниша: {niche}
Тема: {topic}

Верни ответ строго в формате:

🎬 Заголовок

🎥 Сценарий Reels

🎙 Текст диктора

📱 Instagram пост

📢 Telegram пост

#️⃣ Хештеги

🖼 Идея обложки

🤖 Промпт для картинки

Пиши простым, но цепляющим русским языком.
Добавь локальный колорит Таджикистана."""


# ============================================
# POST-PROCESSING
# ============================================

def _post_process(content: str, language: str) -> str:
    """Пост-обработка сгенерированного контента"""

    if not content:
        return ""

    # Убираем лишние пробелы
    content = content.strip()

    # Проверяем, что контент не пустой
    if len(content) < 50:
        return content + "\n\n⚠️ Контент слишком короткий. Попробуйте снова."

    # Проверяем наличие всех секций
    required_sections_ru = ["🎬", "🎥", "📱", "📢"]
    required_sections_tg = ["🎬", "🎥", "📱", "📢"]

    required = required_sections_ru if language == "ru" else required_sections_tg

    missing = [s for s in required if s not in content]
    if missing and language == "ru":
        content += "\n\n⚠️ Внимание: в контенте могут отсутствовать некоторые секции."

    return content


# ============================================
# FALLBACK ГЕНЕРАТОРЫ
# ============================================

def _fallback_generate(
    topic: Optional[str],
    niche: Optional[str],
    language: str,
    user_prompt: Optional[str]
) -> str:
    """
    Fallback-генератор, когда OpenAI недоступен
    Использует умные шаблоны
    """

    from services.ai_generator import generate_template_content, select_viral_hook

    # Определяем нишу
    _niche = niche or "other"

    # Выбираем хук
    hook = select_viral_hook(_niche, language) if _niche else topic or "Контент для бизнеса"

    # Генерируем через шаблон
    return generate_template_content(
        topic=topic or hook,
        niche=_niche,
        language=language,
        content_type="reels",
        hook=hook
    )


def _fallback_no_prompt() -> str:
    """Fallback, когда нет промптов"""

    return """❌ Ошибка: не указаны промпты для генерации.

Пожалуйста, укажите:
- system_prompt (инструкции для AI)
- user_prompt (конкретная задача)

Или используйте legacy-режим:
generate_content(topic="Ваша тема", niche="Ваша ниша")"""


# ============================================
# УТИЛИТЫ
# ============================================

def test_connection() -> bool:
    """Проверка подключения к OpenAI API"""

    if not client:
        print("❌ OpenAI клиент не инициализирован")
        return False

    try:
        # Пробуем простой запрос
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print("✅ Подключение к OpenAI API работает")
        return True

    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


def get_available_models() -> List[str]:
    """Получить список доступных моделей (для админа)"""

    if not client:
        return ["gpt-4o-mini (fallback — API недоступен)"]

    try:
        models = client.models.list()
        return [m.id for m in models.data if "gpt" in m.id]
    except Exception as e:
        print(f"❌ Ошибка получения моделей: {e}")
        return ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]


def estimate_tokens(text: str) -> int:
    """Примерная оценка количества токенов"""

    # Приблизительно: 1 токен ≈ 4 символа для английского, 1.5 для русского/таджикского
    return int(len(text) / 1.5)


# ============================================
# LEGACY: Старая функция (для обратной совместимости с твоим старым кодом)
# ============================================

def generate_content_legacy(topic: str, niche: str) -> str:
    """
    LEGACY: Полностью совместима с твоей старой функцией
    generate_content(topic="...", niche="...")
    """
    return _generate_legacy(topic, niche, language="ru")