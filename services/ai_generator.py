# services/ai_generator.py — Умный AI-генератор контента TojikAI (v2.0)
# Полное жесткое разделение сценариев "Узбекистан" (uz) и "Таджикистан" (tj) на уровне системных и пользовательских промптов.
# Поддержка всех 12 категорий SMM-инструментов и субопций.

import json
import random
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

from config import OPENAI_API_KEY, OPENAI_MODEL

# ============================================
# БИБЛИОТЕКА ВИРУСНЫХ ХУКОВ (CTR-оптимизированные)
# ============================================

VIRAL_HOOKS_LIBRARY = {
    "uz": {
        "cafe_uz": [
            {"hook": "Nega Chorsu dagi palov markazida har doim odam turnaqator?", "ctr": 18.5},
            {"hook": "Tandir somsa qilishning ko'pchilik bilmaydigan 3 ta maxfiy siri", "ctr": 15.1},
            {"hook": "Ushbu choyxona mening milliy taomlar haqidagi tasavvurimni o'zgartirdi", "ctr": 13.4}
        ],
        "textile_uz": [
            {"hook": "Nega o'zbek trikotaji va paxtasi butun dunyoda peshqadam?", "ctr": 16.2},
            {"hook": "Kiyim ishlab chiqarishda millionlab pulni tejashning 3 ta yo'li", "ctr": 14.8},
            {"hook": "To'g'ridan-to'g'ri fabrikadan ulgurji kiyim sotib olish sirlari", "ctr": 17.5}
        ],
        "realestate_uz": [
            {"hook": "Toshkent yangi uylaridan (novostroyka) uy olishda aldanib qolmaslik choralari", "ctr": 19.3},
            {"hook": "Nega Toshkentda uy-joy narxlari to'xtovsiz oshib bormoqda?", "ctr": 15.2},
            {"hook": "Ijaraga uy olish va ijaraga berishda rieltorlar yashiradigan sirlar", "ctr": 18.1}
        ],
        "auto_uz": [
            {"hook": "Avtomobilingiz dvigatelini tezda yo'q qiladigan 3 ta jiddiy xato", "ctr": 22.4},
            {"hook": "Nega Cobalt va Gentra egalari doimo shu muammoga duch kelishadi?", "ctr": 19.1},
            {"hook": "Sergeli avtobozoridan aldovlarsiz yaxshi mashina olish siri", "ctr": 24.3}
        ],
        "marketplace_uz": [
            {"hook": "2026-yilda Uzum Marketda noldan savdo boshlash bo'yicha qo'llanma", "ctr": 25.1},
            {"hook": "Uzumda eng xaridorgir bo'lgan 5 ta tovar (sliv byudjetdan saqlaning)", "ctr": 21.3},
            {"hook": "Marketpleysda o'z do'koningizni TOPga olib chiqish strategiyasi", "ctr": 23.4}
        ]
    },
    "tj": {
        "wholesale_tj": [
            {"hook": "Чаро дар бозори Корвон савдои яклухт ҳамеша фоидаовар аст?", "ctr": 17.8},
            {"hook": "Чӣ тавр бо камтарин пул дар бозори Панҷшанбе тиҷорат сар кунем?", "ctr": 14.2},
            {"hook": "Раёси савдо ва ёфтани мизоҷони доимӣ дар Душанбе", "ctr": 16.5}
        ],
        "cargo_tj": [
            {"hook": "Интиқоли карго аз Чин ва Туркия ба Душанбе: кадомаш арзонтар меистад?", "ctr": 19.4},
            {"hook": "Чаро интихоби нодурусти карго метавонад бори шуморо кум кунад?", "ctr": 16.8},
            {"hook": "Мушкилоти гумрук ва интиқоли мол ба Хуҷанд бе дарди сар", "ctr": 21.7}
        ],
        "construction_tj": [
            {"hook": "Бозори сохтмон дар Душанбе: чӣ тавр хонаро бе хароҷоти зиёд таъмир кунем?", "ctr": 18.2},
            {"hook": "Нархи кони коғазӣ ва қитъаҳои замин дар атрофи Душанбе чӣ гуна аст?", "ctr": 15.6},
            {"hook": "5 хатои ҷиддӣ ҳангоми сохтани хонаи шахсӣ дар Тоҷикистон", "ctr": 19.8}
        ],
        "wedding_tj": [
            {"hook": "Зебоии либоси миллии чакан ва атлас дар тӯйҳои тоҷикӣ", "ctr": 21.3},
            {"hook": "Чӣ тавр як тӯи боҳашаматро дар Душанбе бе исрофкорӣ гузаронем?", "ctr": 17.6},
            {"hook": "Беҳтарин толори арӯсӣ ва салонҳои ороиш дар Душанбе", "ctr": 18.9}
        ],
        "tourism_tj": [
            {"hook": "Минтақаҳои истироҳатии Варзоб ва Ромит: куҷо рафтан беҳтар аст?", "ctr": 15.4},
            {"hook": "Саёҳати афсонавии Искандаркӯл ва Помир барои сайёҳони дохилӣ", "ctr": 18.7},
            {"hook": "Чаро табиати Тоҷикистон хориҷиёнро ба ҳайрат меорад?", "ctr": 14.5}
        ]
    }
}


# ============================================
# ПРОМПТЫ ДЛЯ AI С ЖЕСТКИМ РАЗДЕЛЕНИЕМ СТРАН
# ============================================

def get_system_prompt(niche: str, language: str, content_type: str, country: str = "uz") -> str:
    """Системный промпт с жестким разделением по сценарию страны"""

    if country == "uz":
        prompt = f"""Ты — ведущий эксперт по SMM, копирайтингу и контент-маркетингу в Узбекистане.
Твоя цель — создавать взрывной, высококонверсионный и вирусный контент для бизнес-ниши: {niche}.
Язык генерации текста: {'узбекский (на латинице, uz)' if language == 'uz' else ('русский, ru' if language == 'ru' else 'таджикский, tg')}.

ЖЕСТКИЕ ПРАВИЛА И КУЛЬТУРНЫЙ КОНТЕКСТ УЗБЕКИСТАНА:
- Пиши с опорой на узбекский менталитет, семейные ценности, традиции уважения (ҳурмат-иззат) и гостеприимства (меҳмондўстлик).
- Интегрируй в сценарии Reels и посты упоминания городов Узбекистана: Ташкент (Toshkent), Самарканд (Samarqand), Бухара (Buxoro), Хива (Xiva), Андижан (Andijon).
- Упоминай локальные реалии и гастрономию: ароматный плов (palov), сочная тандыр-самса (tandir somsa), горячие лепешки (issiq non), чайхана (choyxona), чай на легендарном базаре Чорсу (Chorsu).
- Используй локальные экономические гиганты: маркетплейс Uzum Market (для торговли), автомобили Chevrolet Cobalt, Gentra, Tracker, авторынок Сергели и завод UzAuto (для автотемы).
- Тон контента: вовлекающий, искренний, эмоциональный, живой, мотивирующий совершить покупку или подписаться. Избегай скучной теории!
- ТЫ НЕ ДОЛЖЕН предлагать таджикский контекст (Душанбе, сомони, Корвон, чакан, Alif, Alif Mobi)! Только Узбекистан!
"""
    else:
        prompt = f"""Ты — ведущий эксперт по SMM, копирайтингу и контент-маркетингу в Таджикистане.
Твоя цель — создавать взрывной, высококонверсионный и вирусный контент для бизнес-ниши: {niche}.
Язык генерации текста: {'таджикский (кириллица, tg)' if language == 'tg' else ('русский, ru' if language == 'ru' else 'узбекский, uz')}.

ЖЕСТКИЕ ПРАВИЛА И КУЛЬТУРНЫЙ КОНТЕКСТ ТАДЖИКИСТАНА:
- Пиши с опорой на таджикские семейные ценности, уважение к родителям и родному краю.
- Интегрируй в сценарии Reels и посты упоминания городов и прекрасных регионов Таджикистана: Душанбе (Dushanbe), Худжанд (Khujand), Куляб (Kulob), Пенджикент (Panjakent), Памир (Pamir), ущелья Варзоб (Varzob) и Ромит (Romit).
- Упоминай локальные реалии бизнеса: легендарные вещевые и оптовые рынки Корвон (Korvon), Панжшанбе (Panjshanbe), карго-доставку товаров из Китая, Турции и Дубая в Душанбе.
- Ссылайся на платежные системы Таджикистана: перевод денег и оплата через Alif Mobi или Душанбе Сити. Валюта: Сомони (TJS).
- Упоминай культурные символы: красочный чакан, узоры атласа, роскошные традиционные свадьбы (тӯй), чайхану Рохат, курутоб (qurutob), таджикский плов и памирский чай.
- Тон контента: теплый, глубоко уважительный, вызывающий доверие у таджикской аудитории, с призывом заказать или подписаться.
- ТЫ НЕ ДОЛЖЕН предлагать узбекский контекст (Ташкент, Самарканд, Чорсу, Сергели, плов, самса, сум / UZS, Click/Payme)! Только Таджикистан!
"""

    return prompt


def get_content_prompt(topic: str, niche: str, language: str, content_type: str, hook: str, country: str = "uz", subtool: str = None) -> str:
    """Промпт для генерации конкретного типа контента в зависимости от категории и субопции"""

    country_name = "Узбекистана" if country == "uz" else "Таджикистана"
    currency_desc = "сумы UZS" if country == "uz" else "сомони TJS"
    realities_desc = "маркетплейс Uzum, авторынок Сергели, Чорсу" if country == "uz" else "рынок Корвон, Панжшанбе, карго доставка"

    # Умное автоматическое определение Tone of Voice (ToV) на основе ниши бизнеса
    niche_lower = niche.lower()
    if any(k in niche_lower for k in ["beauty", "shop", "fashion", "style", "salon", "cosmetology", "jewelry", "flowers"]):
        tov_desc = "💎 Эстетичный, премиальный, вдохновляющий и роскошный (Luxury & Aesthetic Tone of Voice)"
        audience_segment = "Любители стиля, премиум-клиенты, ценящие качество и индивидуальный подход"
    elif any(k in niche_lower for k in ["cafe", "food", "restaurant", "fastfood", "coffee", "meat", "confectionery"]):
        tov_desc = "🍕 Теплый, эмоциональный, дружелюбный, аппетитный (Friendly & Warm Tone of Voice)"
        audience_segment = "Семьи, дружеские компании, гурманы, ищущие уютную атмосферу и безупречный вкус"
    elif any(k in niche_lower for k in ["auto", "realestate", "construction", "legal", "audit", "security", "it", "solar"]):
        tov_desc = "💼 Экспертный, убедительный, авторитетный, надежный (Expert & Authoritative Tone of Voice)"
        audience_segment = "Предприниматели, прагматичные покупатели, ценящие безопасность, гарантии и точные цифры"
    else:
        tov_desc = "⚡️ Вирусный, вовлекающий, динамичный, креативный (Creative & Viral Tone of Voice)"
        audience_segment = "Активные пользователи соцсетей, молодежь, искатели трендов и новинок"

    prompt_intro = f"""
Создай профессиональный контент для бизнеса в сфере {niche} в реалиях {country_name}.
Категория инструмента: {content_type.upper()}
Суб-инструмент / Задача: {subtool if subtool else 'Общая'}
Пользовательская тема: "{topic}"
Вирусный хук: "{hook}"

Пожалуйста, выполни задачу со следующими требованиями (ЭКСПЕРТНЫЙ ИИ-КОУЧ РЕЖИМ):
1. **Культурный & Рыночный Кончет**: Строго соответствует рынку и культуре {country_name}. Валюта: {currency_desc}. Опирайся на {realities_desc}.
2. **Tone of Voice (Стиль общения)**: Используй стиль {tov_desc}.
3. **Целевой Сегмент Аудитории**: Адаптируй текст и триггеры под сегмент: [{audience_segment}].
4. **Преимущество перед конкурентами**: Интегрируй в контент явное УТП (Уникальное Торговое Предложение), показывающее, почему локальные конкуренты проигрывают (например, отсутствие сервиса, долгая доставка, сложные платежи), а данный бизнес выигрывает.
5. **Мульти-CTA Оптимизация**: Призыв к действию (CTA) должен предлагать удобные локальные варианты взаимодействия (например, быстрый переход в директ/чат-бот, быстрая оплата через Click/Payme или Alif Mobi/Душанбе Сити в зависимости от страны).
6. **Оформление**: Напиши структурированный, готовый к публикации текст с эмодзи, абзацами и четкими визуальными блоками.
"""

    # Динамическая кастомизация на основе 12 категорий SMM
    if content_type == "ideas":
        prompt_intro += """
- Напиши список креативных и вирусных идей для контента. Каждая идея должна содержать:
  1. Название идеи
  2. Визуальная подача
  3. Краткое описание сути
  4. Ожидаемый эффект (просмотры, заявки).
"""
    elif content_type == "posts":
        prompt_intro += f"""
- Напиши полноценный структурированный пост для публикации в социальной сети:
  1. Привлекающий внимание локальный заголовок с эмодзи.
  2. Введение: раскрытие боли клиента в контексте {country_name}.
  3. Основная часть: 3-4 практических совета или разбор ошибок с учетом местных особенностей бизнеса.
  4. Мощный призыв к действию (CTA), направленный на покупку, запись или консультацию.
"""
    elif content_type == "stories":
        prompt_intro += """
- Напиши готовую серию из 5 слайдов Stories для прогрева аудитории:
  Слайд 1: Крючок внимания (Хук).
  Слайд 2: Раскрытие боли/проблемы клиента.
  Слайд 3: Презентация решения.
  Слайд 4: Социальное доказательство/отзыв/кейс.
  Слайд 5: Призыв к действию с интерактивным элементом (опрос, стикер).
  Для каждого слайда опиши визуальное оформление и точный текст на экране.
"""
    elif content_type == "reels":
        prompt_intro += """
- Напиши подробный, динамичный сценарий для видео Reels:
  1. Хук (0-3 сек) — яркое визуальное и текстовое начало.
  2. Текст диктора (Voiceover) — простым, живым языком с интеграцией местного колорита.
  3. Описание видеоряда для кадра (B-rolls, действия спикера, титры).
  4. Монтажные подсказки (звуки, переходы, трендовая музыка).
"""
    elif content_type == "shorts":
        prompt_intro += """
- Создай структурированный сценарий YouTube Shorts / TikTok (до 60 секунд):
  1. Хук и интрига в первые секунды.
  2. Динамичный сторителлинг.
  3. Пошаговая структура ролика.
  4. Сильный призыв подписаться в конце.
"""
    elif content_type == "plan":
        prompt_intro += """
- Разработай еженедельный контент-план (7 дней):
  Каждый день должен содержать: Тему, Формат (Пост, Stories, Reels), Цель (Продажи, Экспертность, Юмор, Вовлечение) и Текст-план.
"""
    elif content_type == "ads":
        prompt_intro += """
- Сгенерируй 3 высокоэффективных рекламных объявления для таргета:
  Вариант 1: Сфокусирован на выгоде (скидка, акция, спецпредложение).
  Вариант 2: Сфокусирован на боли и решении проблемы.
  Вариант 3: Игровой/Креативный оффер.
"""
    elif content_type == "funnel":
        prompt_intro += """
- Опиши пошаговую автоворонку продаж в мессенджерах:
  Шаг 1: Лид-магнит (что дарим бесплатно).
  Шаг 2: Прогревающее сообщение 1 (знакомство, польза).
  Шаг 3: Прогревающее сообщение 2 (кейс, отзывы).
  Шаг 4: Продающее сообщение (оффер, закрытие сделки).
"""
    elif content_type == "tg_channel":
        prompt_intro += """
- Напиши пост, идеально подходящий для публикации в Telegram-канале:
  Используй форматирование, списки, выделение ключевых слов жирным и интерактивный опрос в конце. Тон: экспертный, без лишней воды.
"""
    elif content_type == "instagram":
        prompt_intro += """
- Напиши Instagram-пост, ориентированный на визуальную эстетику и высокие охваты. Опиши идеи для карусели фото/видео и добавь структурированный текст под фото.
"""
    elif content_type == "tiktok":
        prompt_intro += """
- Придумай концепцию и сценарий вирусного видео в TikTok. Укажи трендовые челленджи, музыку, звуковые эффекты и поведение в кадре.
"""
    elif content_type == "youtube":
        prompt_intro += """
- Создай подробную структуру сценария для полноценного длинного видео на YouTube. Включи таймкоды, введение, главы, перебивки и призыв к лайку/подписке.
"""

    prompt_intro += f"""
В конце контента обязательно добавь блок из 7-10 актуальных локальных хештегов.
"""

    return prompt_intro


# ============================================
# ОСНОВНАЯ ФУНКЦИЯ ГЕНЕРАЦИИ
# ============================================

async def generate_ai_content(
    topic: str,
    niche: str,
    language: str = "ru",
    content_type: str = "reels",
    use_best_hook: bool = True,
    country: str = "uz",
    subtool: str = None
) -> str:
    """
    Генерация AI-контента с вирусными хуками и жестким разделением по странам
    """

    # 1. Выбираем вирусный хук
    if use_best_hook:
        hook = select_viral_hook(niche, language, country)
    else:
        hook = topic

    # 2. Формируем промпты
    system_prompt = get_system_prompt(niche, language, content_type, country)
    content_prompt = get_content_prompt(topic, niche, language, content_type, hook, country, subtool)

    # 3. Генерируем через OpenAI
    try:
        if OPENAI_API_KEY and OPENAI_API_KEY != "mock-key":
            from services.openai_service import generate_content
            content = generate_content(
                system_prompt=system_prompt,
                user_prompt=content_prompt,
                model=OPENAI_MODEL
            )
        else:
            content = generate_template_content(topic, niche, language, content_type, hook, country, subtool)
    except Exception as e:
        content = generate_template_content(topic, niche, language, content_type, hook, country, subtool)

    content = content.strip()
    return content


def select_viral_hook(niche: str, language: str, country: str = "uz") -> str:
    """Выбирает лучший вирусный хук из библиотеки на основе CTR"""
    hooks = VIRAL_HOOKS_LIBRARY.get(country, VIRAL_HOOKS_LIBRARY["uz"]).get(niche, [])
    if not hooks:
        for k, v in VIRAL_HOOKS_LIBRARY.get(country, VIRAL_HOOKS_LIBRARY["uz"]).items():
            if v:
                hooks = v
                break

    if not hooks:
        return "Секрет успеха, о котором молчат все конкуренты"

    total_ctr = sum(h["ctr"] for h in hooks)
    weights = [h["ctr"] / total_ctr for h in hooks]
    selected = random.choices(hooks, weights=weights, k=1)[0]
    return selected["hook"]


def generate_template_content(
    topic: str,
    niche: str,
    language: str,
    content_type: str,
    hook: str,
    country: str = "uz",
    subtool: str = None
) -> str:
    """Шаблонный генератор контента при отсутствии активного OpenAI API ключа"""

    if country == "uz":
        city = random.choice(["Toshkent", "Samarqand", "Buxoro", "Andijon"])
        food = "palov va tandir somsa"
        currency = "UZS (сум)"
        payment = "Click/Payme"
        realities = "Uzum Market va Cobalt"
    else:
        city = random.choice(["Душанбе", "Худжанд", "Куляб", "Варзоб"])
        food = "курутоб ва оши палов"
        currency = "TJS (сомони)"
        payment = "Alif Mobi ва Душанбе Сити"
        realities = "бозори Корвон ва карго"

    try:
        from content_engine.niche_manager import get_hashtags
        hashtags = get_hashtags(niche, language)
    except:
        hashtags = "#tashkent #uzbekistan" if country == "uz" else "#dushanbe #tajikistan"

    sub_desc = subtool if subtool else "Общий формат"

    if language == "uz":
        return f"""🎬 <b>TojikAI SMM Platformasi</b>
📌 <b>Bo'lim:</b> {content_type.upper()} ({sub_desc})
📌 <b>Soha:</b> {niche} (O'zbekiston)

🔥 <b>Sarlavha (Hook):</b> "{hook}"

📍 <b>Tavsif:</b>
Siz uchun {city} sharoitida {niche} sohasida kontent tayyorlandi. Biznesingizni rivojlantirish uchun {realities} tizimidan foydanling, to'lovlarni {payment} orqali qabul qiling va foydani {currency}da hisoblang.

📝 <b>Kontent rejasi (Mavzu: {topic}):</b>
1. Diqqat jalb qilish: "{hook}"
2. {city} shahridagi asosiy muammolar va mijozlar ehtiyojlari.
3. Bizning taklifimiz va professional yechimimiz.
4. Murojaat va sotuvni yopish.

#️⃣ <b>Xeshteglar:</b>
{hashtags} #uzbekistan #toshkent #smm"""

    elif language == "tg":
        return f"""🎬 <b>Платформаи SMM TojikAI</b>
📌 <b>Бахш:</b> {content_type.upper()} ({sub_desc})
📌 <b>Ниша:</b> {niche} (Тоҷикистон)

🔥 <b>Сарлавҳа (Hook):</b> "{hook}"

📍 <b>Тавсифи контент:</b>
Маводи махсус барои пешбурди {niche} дар шаҳри {city}. Аз шароити {realities} ва имкониятҳои тиҷоратии маҳаллӣ истифода баред. Пардохтҳоро бо {payment} қабул карда, даромадро ба {currency} баланд бардоред!

📝 <b>Матни омодашуда (Мавзӯъ: {topic}):</b>
1. Оғози вирусӣ: "{hook}"
2. Таҳлили бозор дар {city} ва талаботи мизоҷон.
3. Қадамҳои амалӣ барои афзоиши фурӯш ва ҷалби бештари харидорон.
4. Даъват ба амал барои сабти ном ё харид.

#️⃣ <b>Хештегҳо:</b>
{hashtags} #тоҷикистон #душанбе #smm"""

    else:
        return f"""🎬 <b>SMM Платформа TojikAI</b>
📌 <b>Раздел:</b> {content_type.upper()} ({sub_desc})
📌 <b>Ниша:</b> {niche} ({'Узбекистан' if country == 'uz' else 'Таджикистан'})

🔥 <b>Заголовок (Hook):</b> "{hook}"

📍 <b>Описание:</b>
Специально подготовленный контент для города {city}. Опирайтесь на {realities}, используйте платежные шлюзы {payment} и ведите учет в {currency}.

📝 <b>Сгенерированный текст (Тема: {topic}):</b>
1. Хук: "{hook}"
2. Описание болей клиентов в {city}.
3. 3 пошаговых шага для успешного продвижения вашего предложения.
4. Сильный локальный призыв к действию.

#️⃣ <b>Хештеги:</b>
{hashtags} #{'uzbekistan' if country == 'uz' else 'tajikistan'} #smm"""
