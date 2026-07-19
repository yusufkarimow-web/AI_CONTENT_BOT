# services/ai_generator.py — Умный AI-генератор контента Sozanda
# Полное жесткое разделение сценариев "Узбекистан" (uz) и "Таджикистан" (tj) на уровне системных промптов

import json
import random
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

from config import OPENAI_API_KEY, OPENAI_MODEL
from services.openai_service import generate_content_legacy


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
        "textile": [
            {"hook": "Nega o'zbek trikotaji va paxtasi butun dunyoda peshqadam?", "ctr": 16.2},
            {"hook": "Kiyim ishlab chiqarishda millionlab pulni tejashning 3 ta yo'li", "ctr": 14.8},
            {"hook": "To'g'ridan-to'g'ri fabrikadan ulgurji kiyim sotib olish sirlari", "ctr": 17.5}
        ],
        "realestate": [
            {"hook": "Toshkent yangi uylaridan (novostroyka) uy olishda aldanib qolmaslik choralari", "ctr": 19.3},
            {"hook": "Nega Toshkentda uy-joy narxlari to'xtovsiz oshib bormoqda?", "ctr": 15.2},
            {"hook": "Ijaraga uy olish va ijaraga berishda rieltorlar yashiradigan sirlar", "ctr": 18.1}
        ],
        "auto_uz": [
            {"hook": "Avtomobilingiz dvigatelini tezda yo'q qiladigan 3 ta jiddiy xato", "ctr": 22.4},
            {"hook": "Nega Cobalt va Gentra egalari doimo shu muammoga duch kelishadi?", "ctr": 19.1},
            {"hook": "Sergeli avtobozoridan aldovlarsiz yaxshi mashina olish siri", "ctr": 24.3}
        ],
        "marketplace": [
            {"hook": "2026-yilda Uzum Marketda noldan savdo boshlash bo'yicha qo'llanma", "ctr": 25.1},
            {"hook": "Uzumda eng xaridorgir bo'lgan 5 ta tovar (sliv byudjetdan saqlaning)", "ctr": 21.3},
            {"hook": "Marketpleysda o'z do'koningizni TOPga olib chiqish strategiyasi", "ctr": 23.4}
        ]
    },
    "tj": {
        "wholesale": [
            {"hook": "Чаро дар бозори Корвон савдои яклухт ҳамеша фоидаовар аст?", "ctr": 17.8},
            {"hook": "Чӣ тавр бо камтарин пул дар бозори Панҷшанбе тиҷорат сар кунем?", "ctr": 14.2},
            {"hook": "Раёси савдо ва ёфтани мизоҷони доимӣ дар Душанбе", "ctr": 16.5}
        ],
        "cargo": [
            {"hook": "Интиқоли карго аз Чин ва Туркия ба Душанбе: кадомаш арзонтар меистад?", "ctr": 19.4},
            {"hook": "Чаро интихоби нодурусти карго метавонад бори шуморо кум кунад?", "ctr": 16.8},
            {"hook": "Мушкилоти гумрук ва интиқоли мол ба Хуҷанд бе дарди сар", "ctr": 21.7}
        ],
        "construction": [
            {"hook": "Бозори сохтмон дар Душанбе: чӣ тавр хонаро бе хароҷоти зиёд таъмир кунем?", "ctr": 18.2},
            {"hook": "Нархи кони коғазӣ ва қитъаҳои замин дар атрофи Душанбе чӣ гуна аст?", "ctr": 15.6},
            {"hook": "5 хатои ҷиддӣ ҳангоми сохтани хонаи шахсӣ дар Тоҷикистон", "ctr": 19.8}
        ],
        "wedding_tj": [
            {"hook": "Зебоии либоси миллии чакан ва атлас дар тӯйҳои тоҷикӣ", "ctr": 21.3},
            {"hook": "Чӣ тавр як тӯи боҳашаматро дар Душанбе бе исрофкорӣ гузаронем?", "ctr": 17.6},
            {"hook": "Беҳтарин толори арӯсӣ ва салонҳои ороиш дар Душанбе", "ctr": 18.9}
        ],
        "tourism": [
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
        # СЦЕНАРИЙ УЗБЕКИСТАН
        prompt = f"""Ты — ведущий эксперт по SMM, копирайтингу и контент-маркетингу в Узбекистане.
Твоя цель — создавать взрывной, высококонверсионный и вирусный контент для бизнес-ниши: {niche}.
Язык генерации текста: {'узбекский (на латинице, uz)' if language == 'uz' else 'русский (с интеграцией узбекского колорита, ru)'}.

ЖЕСТКИЕ ПРАВИЛА И КУЛЬТУРНЫЙ КОНТЕКСТ УЗБЕКИСТАНА:
- Пиши с опорой на узбекский менталитет, семейные ценности, традиции уважения (ҳурмат-иззат) и гостеприимства (меҳмондўстлик).
- Интегрируй в сценарии Reels и посты упоминания городов Узбекистана: Ташкент (Toshkent), Самарканд (Samarqand), Бухара (Buxoro), Хива (Xiva), Андижан (Andijon).
- Упоминай локальные реалии и гастрономию: ароматный плов (palov), сочная тандыр-самса (tandir somsa), горячие лепешки (issiq non), чайхана (choyxona), чай на легендарном базаре Чорсу (Chorsu).
- Используй локальные экономические гиганты: маркетплейс Uzum Market (для торговли), автомобили Chevrolet Cobalt, Gentra, Tracker, авторынок Сергели и завод UzAuto (для автотемы).
- Тон контента: вовлекающий, искренний, эмоциональный, живой, мотивирующий совершить покупку или подписаться. Избегай скучной теории!
"""
    else:
        # СЦЕНАРИЙ ТАДЖИКИСТАН
        prompt = f"""Ты — ведущий эксперт по SMM, копирайтингу и контент-маркетингу в Таджикистане.
Твоя цель — создавать взрывной, высококонверсионный и вирусный контент для бизнес-ниши: {niche}.
Язык генерации текста: {'таджикский (кириллица, tg)' if language == 'tg' else 'русский (с интеграцией таджикского колорита, ru)'}.

ЖЕСТКИЕ ПРАВИЛА И КУЛЬТУРНЫЙ КОНТЕКСТ ТАДЖИКИСТАНА:
- Пиши с опорой на таджикские семейные ценности, уважение к родителям и родному краю.
- Интегрируй в сценарии Reels и посты упоминания городов и прекрасных регионов Таджикистана: Душанбе (Dushanbe), Худжанд (Khujand), Куляб (Kulob), Пенджикент (Panjakent), Памир (Pamir), ущелья Варзоб (Varzob) и Ромит (Romit).
- Упоминай локальные реалии бизнеса: легендарные вещевые и оптовые рынки Корвон (Korvon), Садовод, Панжшанбе (Panjshanbe), карго-доставку товаров из Китая, Турции и Дубая в Душанбе.
- Ссылайся на платежные системы Таджикистана: перевод денег и оплата через Alif Mobi или Душанбе Сити.
- Упоминай культурные символы: красочный чакан, узоры атласа, роскошные традиционные свадьбы (тӯй), чайхану Рохат, курутоб (qurutob), таджикский плов и памирский чай.
- Тон контента: теплый, глубоко уважительный, вызывающий доверие у таджикской аудитории, с призывом заказать или подписаться.
"""

    return prompt


def get_content_prompt(topic: str, niche: str, language: str, content_type: str, hook: str, country: str = "uz") -> str:
    """Промпт для генерации конкретного типа контента"""

    country_name = "Узбекистана" if country == "uz" else "Таджикистана"

    prompts = {
        "reels": f"""Создай подробный сценарий для Reels/TikTok видео на тему: "{topic}"
Используй вирусный хук: "{hook}"

Структура сценария должна быть строго следующей:
1. ХУК (первые 3 секунды) — цепляющая фраза, которая заставит зрителя досмотреть до конца.
2. ИНТРИГА/МУЧЕНИЕ — описание боли целевой аудитории в контексте бизнес-ниши {niche} в реалиях {country_name}.
3. РЕШЕНИЕ — 2-3 практических шага, применимых в повседневной жизни или бизнесе.
4. ПРИЗЫВ К ДЕЙСТВИЮ (CTA) — предложение написать в комментариях, подписаться или сохранить видео.
5. ХЕШТЕГИ — 10 трендовых локальных хештегов.

Напиши подробно, разделив на реплики диктора и визуальные инструкции для кадра. Длина: 200-300 слов.""",

        "post": f"""Напиши вовлекающий пост для Instagram на тему: "{topic}"
Используй цепляющее начало: "{hook}"

Структура поста:
1. Яркий заголовок с эмодзи.
2. Жизненное вступление, описывающее ситуацию в {country_name}.
3. 3-4 полезных, конкретных совета или секрета успеха по теме "{topic}".
4. Разбор типичных ошибок, которые совершают клиенты.
5. Завершение с открытым вопросом к аудитории для поднятия активности в комментариях.
6. Локальные хештеги.

Стиль письма: легкий, дружелюбный, экспертный. Объем: 150-250 слов.""",

        "stories": f"""Разработай цепочку из 5-6 слайдов Stories для прогрева аудитории на тему: "{topic}"
Хук первого слайда: "{hook}"

Для каждого слайда опиши:
- Визуальный ряд (фото, видео, инфографика).
- Краткий текст на экране (3-5 емких слов).
- Дополнительный текст для озвучки или стикеров.
- Интерактивный элемент (опрос, тест, ползунок реакции, окно для вопросов).

Создай плавную воронку, которая приведет к целевому действию на последнем слайде.""",

        "ideas": f"""Придумай 5 взрывных и креативных идей для Reels и постов на тему: "{topic}"

Для каждой идеи напиши:
- Название и формат контента.
- Короткий сценарий или суть идеи.
- Почему это сработает на аудиторию {country_name} и зацепит локальный менталитет.""",

        "hook": f"""Придумай 10 убойных вирусных хуков (заголовков) для темы: "{topic}".
Сделай их интригующими, используй цифры, провокации и локальный контекст {country_name}. Каждая фраза должна вызывать желание кликнуть!""",

        "caption": f"""Напиши идеальную, короткую подпись (caption) под видео на тему: "{topic}" с хуком "{hook}", призывом подписаться и локальными хештегами."""
    }

    return prompts.get(content_type, prompts["reels"])


# ============================================
# ОСНОВНАЯ ФУНКЦИЯ ГЕНЕРАЦИИ
# ============================================

async def generate_ai_content(
    topic: str,
    niche: str,
    language: str = "ru",
    content_type: str = "reels",
    use_best_hook: bool = True,
    country: str = "uz"
) -> str:
    """
    Генерация AI-контента с вирусными хуками и жестким разделением по странам
    """

    # 1. Выбираем вирусный хук
    hook = ""
    if use_best_hook:
        hook = select_viral_hook(niche, language, country)
    else:
        hook = topic

    # 2. Формируем промпты
    system_prompt = get_system_prompt(niche, language, content_type, country)
    content_prompt = get_content_prompt(topic, niche, language, content_type, hook, country)

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
            # Fallback на шаблонный генератор, если ключ тестовый или отсутствует
            content = generate_template_content(topic, niche, language, content_type, hook, country)
    except Exception as e:
        content = generate_template_content(topic, niche, language, content_type, hook, country)

    # 4. Пост-обработка
    content = content.strip()
    return content


def select_viral_hook(niche: str, language: str, country: str = "uz") -> str:
    """Выбирает лучший вирусный хук из библиотеки на основе CTR"""
    hooks = VIRAL_HOOKS_LIBRARY.get(country, VIRAL_HOOKS_LIBRARY["uz"]).get(niche, [])
    if not hooks:
        # Берем первый доступный список хуков
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
    country: str = "uz"
) -> str:
    """Шаблонный генератор контента при отсутствии активного OpenAI API ключа"""

    if country == "uz":
        city = random.choice(["Toshkent", "Samarqand", "Buxoro", "Andijon"])
        food = "palov va tandir somsa"
        currency = "UZS"
        payment = "Click/Payme"
        realities = "Uzum Market va Cobalt mashinalari"
    else:
        city = random.choice(["Душанбе", "Худжанд", "Куляб", "Варзоб"])
        food = "курутоб ва оши палов"
        currency = "TJS"
        payment = "Alif Mobi ва Душанбе Сити"
        realities = "бозори Корвон ва карго интиқоли молҳо"

    try:
        from content_engine.niche_manager import get_hashtags
        hashtags = get_hashtags(niche, language)
    except:
        hashtags = "#tashkent #uzbekistan" if country == "uz" else "#dushanbe #tajikistan"

    if language == "uz":
        return f"""🎬 <b>Reels Ssenariy (Ssenariysi)</b>

🔥 <b>Sarlavha (Hook):</b> "{hook}"

📍 <b>Soha:</b> {niche} (O'zbekiston ssenariysi)
📍 <b>Shahar:</b> {city}

📱 <b>Video tuzilishi:</b>
1. <b>Kadr 1 (0-3 soniya):</b> Kameraga qarab ishonch bilan ayting: "{hook}"
2. <b>Kadr 2 (3-10 soniya):</b> Biznesda yo'l qo'yiladigan eng katta xatolarni ko'rsating. {realities} haqida eslatib o'ting.
3. <b>Kadr 3 (10-25 soniya):</b> Yechim bering! {city} sharoitida qanday qilib daromad olish yoki mijoz topish mumkinligini tushuntiring.
4. <b>Kadr 4 (25-30 soniya):</b> Harakatga chaqiriq: "Ushbu videoni saqlab oling va profilimizga obuna bo'ling!"

#️⃣ <b>Xeshteglar:</b>
{hashtags} #uzbekistan #toshkent #biznes"""

    elif language == "tg":
        return f"""🎬 <b>Сенарияи Reels</b>

🔥 <b>Сарлавҳа (Hook):</b> "{hook}"

📍 <b>Ниша:</b> {niche} (Сенарияи Тоҷикистон)
📍 <b>Шаҳр:</b> {city}

📱 <b>Таркиби видео:</b>
1. <b>Кадри 1 (0-3 сония):</b> Диққати тамошобинро бо ин ҷумла ҷалб кунед: "{hook}"
2. <b>Кадри 2 (3-10 сония):</b> Нишон диҳед, ки чӣ тавр дар {realities} мушкилиҳо ба вуҷуд меоянд.
3. <b>Кадри 3 (10-25 сония):</b> Ҳалли муамморо пешниҳод кунед! Нишон диҳед, ки дар {city} бо усули {payment} чӣ гуна осон кор кардан мумкин аст.
4. <b>Кадри 4 (25-30 сония):</b> Даъват ба амал: "Видеоро ҳифз кунед ва ба саҳифаи мо обуна шавед!"

#️⃣ <b>Хештегҳо:</b>
{hashtags} #тоҷикистон #душанбе #тиҷорат"""

    else:
        # Русский язык (подходит для обеих стран, но разделен по контексту)
        return f"""🎬 <b>Сценарий Reels (Локализованный под {'Узбекистан' if country == 'uz' else 'Таджикистан'})</b>

🔥 <b>Заголовок (Hook):</b> "{hook}"

📍 <b>Ниша:</b> {niche}
📍 <b>Локация:</b> {city}
📍 <b>Реалии:</b> {realities}

🎙 <b>Текст диктора:</b>
- "А вы знали, что большинство совершают ошибку при работе в этой нише? Да-да, именно в {city} многие забывают про {realities}!"
- "Чтобы исправить это, используйте {payment} и делайте ставку на качество."
- "Подпишитесь, чтобы получать больше лайфхаков для бизнеса!"

#️⃣ <b>Хештеги:</b>
{hashtags} #{'uzbekistan' if country == 'uz' else 'tajikistan'}"""
