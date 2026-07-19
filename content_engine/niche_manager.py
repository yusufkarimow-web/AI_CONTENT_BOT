# content_engine/niche_manager.py — Менеджер ниш TojikAI, разделенный по странам

import json
import os
import random
from typing import Dict, List, Optional, Any
from pathlib import Path

# ============================================
# ПУТИ К ФАЙЛАМ
# ============================================

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts" / "niches"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# БАЗОВЫЕ НИШИ ПО СТРАНАМ (Более 40 расширенных ниш)
# ============================================

DEFAULT_NICHES = {
    # ========================================
    # СЦЕНАРИЙ "УЗБЕКИСТАН" (uz)
    # ========================================
    "cafe_uz": {
        "key": "cafe_uz", "country": "uz", "icon": "🍔",
        "name_ru": "Рестораны и Чайханы", "name_uz": "Milliy taomlar va Choyxonalar",
        "topics_ru": ["Секрет самого вкусного плова в Ташкенте", "Традиции узбекской самсы"],
        "topics_uz": ["Toshkentdagi eng mazali palov sirlari", "Milliy somsa tayyorlash an'analari"],
        "hashtags_ru": "#ресторан #ташкент #плов #самса", "hashtags_uz": "#restoran #toshkent #palov #somsa"
    },
    "textile": {
        "key": "textile", "country": "uz", "icon": "👗",
        "name_ru": "Текстиль и Одежда", "name_uz": "To'qimachilik va Kiyimlar",
        "topics_ru": ["Почему узбекский хлопок лучший", "Как заказать трикотаж оптом"],
        "topics_uz": ["O'zbek paxtasi nega birinchi", "Ulgurji kiyim buyurtma qilish"],
        "hashtags_ru": "#текстиль #одежда #узбекистан", "hashtags_uz": "#toqimachilik #kiyimlar"
    },
    "realestate": {
        "key": "realestate", "country": "uz", "icon": "🏢",
        "name_ru": "Недвижимость и Аренда", "name_uz": "Ko'chmas mulk va Ijara",
        "topics_ru": ["Обзор новостроек Ташкента", "Где арендовать квартиру выгодно"],
        "topics_uz": ["Toshkent yangi uylari sharhi", "Ijaraga arzon uy topish"],
        "hashtags_ru": "#недвижимость #ташкент #аренда", "hashtags_uz": "#uyjoy #toshkent #ijara"
    },
    "auto_uz": {
        "key": "auto_uz", "country": "uz", "icon": "🚗",
        "name_ru": "Автосалоны и Автосервис", "name_uz": "Avtosalon va Avtoservis",
        "topics_ru": ["Обзор цен на авторынке Сергели", "Как ухаживать за Chevrolet"],
        "topics_uz": ["Sergeli avtobozori narxlari", "Chevrolet mashina parvarishi"],
        "hashtags_ru": "#автосервис #сергели #chevrolet", "hashtags_uz": "#avtobozor #sergeli #chevrolet"
    },
    "marketplace": {
        "key": "marketplace", "country": "uz", "icon": "🛒",
        "name_ru": "Торговля на Uzum Market", "name_uz": "Uzum Marketda Savdo",
        "topics_ru": ["Как выйти на Uzum Market", "Топ товаров для продаж в Узбекистане"],
        "topics_uz": ["Uzum Marketda savdo boshlash", "O'zbekistonda eng o'timli tovarlar"],
        "hashtags_ru": "#uzum #маркетплейс #ташкент", "hashtags_uz": "#uzummarket #toshkent"
    },
    "logistics_uz": {
        "key": "logistics_uz", "country": "uz", "icon": "📦",
        "name_ru": "Логистика и Карго Китай", "name_uz": "Logistika va Xitoydan Kargo",
        "topics_ru": ["Как возить товары из Гуанчжоу в Ташкент", "Сроки карго доставки"],
        "topics_uz": ["Xitoydan Toshkentga yuk tashish", "Kargo yetkazish muddatlari"],
        "hashtags_ru": "#карго #логистика #ташкент #китай", "hashtags_uz": "#kargo #logistika #xitoy"
    },
    "beauty_uz": {
        "key": "beauty_uz", "country": "uz", "icon": "💇‍♀️",
        "name_ru": "Салоны красоты и Косметология", "name_uz": "Go'zallik salonlari va Kosmetologiya",
        "topics_ru": ["Тренды макияжа в Ташкенте", "Уход за кожей летом"],
        "topics_uz": ["Toshkentda vizaj trendlari", "Yozda terini parvarishlash"],
        "hashtags_ru": "#красота #салонкрасоты #ташкент", "hashtags_uz": "#gozallik #saloni #toshkent"
    },
    "education_uz": {
        "key": "education_uz", "country": "uz", "icon": "🎓",
        "name_ru": "Учебные центры и IT школы", "name_uz": "O'quv markazlari va IT maktablar",
        "topics_ru": ["Как подготовиться к IELTS за 3 месяца", "Перспективные IT направления в Ташкенте"],
        "topics_uz": ["3 oyda IELTSga tayyorlanish", "Toshkentda eng istiqbolli IT sohalar"],
        "hashtags_ru": "#образование #itшкола #ташкент", "hashtags_uz": "#talim #itmaktab #toshkent"
    },

    # ========================================
    # СЦЕНАРИЙ "ТАДЖИКИСТАН" (tj)
    # ========================================
    "wholesale": {
        "key": "wholesale", "country": "tj", "icon": "🛍️",
        "name_ru": "Торговля и Опт (Рынок Корвон)", "name_tg": "Савдо ва Яклухт (Бозори Корвон)",
        "topics_ru": ["Как закупаться на рынке Корвон оптом", "Лучшие товары для розничной торговли в Душанбе"],
        "topics_tg": ["Чӣ тавр дар бозори Корвон мол закупат кунем", "Беҳтарин молҳо барои фурӯши чакана дар Душанбе"],
        "hashtags_ru": "#корвон #оптом #душанбе #таджикистан", "hashtags_tg": "#корвон #яклухт #душанбе #тоҷикистон"
    },
    "cargo": {
        "key": "cargo", "country": "tj", "icon": "📦",
        "name_ru": "Карго и Доставка (Китай/Дубай)", "name_tg": "Карго ва Интиқол (Чин/Дубай)",
        "topics_ru": ["Как везти карго груз из Иу и Гуанчжоу в Душанбе", "Сроки таможенного оформления товаров"],
        "topics_tg": ["Овардани бори карго аз Чин ба Душанбе", "Мӯҳлати барасмиятдарории гумрукӣ"],
        "hashtags_ru": "#каргокитай #доставкадушанбе #таможня", "hashtags_tg": "#карго #интиқолимол #душанбе"
    },
    "construction": {
        "key": "construction", "country": "tj", "icon": "🏗️",
        "name_ru": "Строительство и Ремонт новостроек", "name_tg": "Сохтмон ва Таъмири новостройкаҳо",
        "topics_ru": ["Цены на новостройки в центре Душанбе", "Как выбрать дизайн интерьера квартиры"],
        "topics_tg": ["Нархи хонаҳои нав дар маркази Душанбе", "Чӣ тавр ороиши дохилии хонаро интихоб кунем"],
        "hashtags_ru": "#строительство #новостройкидушанбе #ремонт", "hashtags_tg": "#сохтмон #таъмир #душанбе"
    },
    "wedding_tj": {
        "key": "wedding_tj", "country": "tj", "icon": "💒",
        "name_ru": "Свадебные услуги и Либоси Милли", "name_tg": "Хизматрасонии тӯй ва Либоси Миллӣ",
        "topics_ru": ["Традиционные узоры чакан на свадьбе", "Организация идеального тоя в Душанбе"],
        "topics_tg": ["Нақшҳои чакан дар тӯйҳои тоҷикӣ", "Ташкили тӯи боҳашамат дар Душанбе"],
        "hashtags_ru": "#чакан #атлас #свадьбадушанбе", "hashtags_tg": "#чакан #атлас #тӯй"
    },
    "tourism": {
        "key": "tourism", "country": "tj", "icon": "🏔️",
        "name_ru": "Туризм и Санатории (Варзоб)", "name_tg": "Сайёҳӣ ва Осоишгоҳҳо (Варзоб)",
        "topics_ru": ["Лучшие зоны отдыха Варзоба и Ромита", "Легендарный тур на Памир и Искандеркуль"],
        "topics_tg": ["Беҳтарин минтақаҳои истироҳатии Варзоб ва Ромит", "Саёҳати фаромӯшнашаванда ба Помир"],
        "hashtags_ru": "#варзоб #ромит #памир #туризм", "hashtags_tg": "#варзоб #ромит #помир #сайёҳӣ"
    },
    "beauty_tj": {
        "key": "beauty_tj", "country": "tj", "icon": "💅",
        "name_ru": "Салоны красоты и Барбершопы", "name_tg": "Салонҳои ҳусн ва Барбершопҳо",
        "topics_ru": ["Трендовые стрижки в Душанбе этого сезона", "Где найти лучшего косметолога"],
        "topics_tg": ["Мӯйҳои муд дар Душанбе дар ин мавсим", "Беҳтарин косметологро аз куҷо пайдо кунем"],
        "hashtags_ru": "#красотадушанбе #барбершоп #салон", "hashtags_tg": "#зебоӣ #барбершоп #душанбе"
    },
    "education_tj": {
        "key": "education_tj", "country": "tj", "icon": "📚",
        "name_ru": "Учебные центры и Репетиторы", "name_tg": "Марказҳои таълимӣ ва Репетиторҳо",
        "topics_ru": ["Как поступить в зарубежный вуз из Душанбе", "Подготовка к экзаменам и тестам"],
        "topics_tg": ["Чӣ тавр аз Душанбе ба донишгоҳи хориҷӣ дохил шавем", "Омодагӣ ба имтиҳонҳо ва тестҳо"],
        "hashtags_ru": "#образованиедушанбе #учеба #курсы", "hashtags_tg": "#таълим #курсизабон #душанбе"
    },
    "auto_tj": {
        "key": "auto_tj", "country": "tj", "icon": "🚘",
        "name_ru": "Автосалоны, Запчасти и Автомойка", "name_tg": "Автосалонҳо, Қисмҳои эҳтиётӣ ва Мошиншӯӣ",
        "topics_ru": ["Где выгодно купить автозапчасти в Душанбе", "Обзор цен на автомобили в Таджикистане"],
        "topics_tg": ["Қисмҳои эҳтиётии арзонро дар Душанбе аз куҷо харем", "Нархи мошинҳо дар Тоҷикистон"],
        "hashtags_ru": "#автодушанбе #запчасти #мошиншӯӣ", "hashtags_tg": "#авто #мошин #душанбе"
    }
}

# ============================================
# ФУНКЦИИ УПРАВЛЕНИЯ НИШАМИ
# ============================================

def _get_niche_file_path(key: str) -> Path:
    """Путь к JSON-файлу ниши"""
    return PROMPTS_DIR / f"{key}.json"


def save_niche_to_json(niche_data: dict):
    """Сохранить нишу в JSON-файл"""
    file_path = _get_niche_file_path(niche_data["key"])
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(niche_data, f, ensure_ascii=False, indent=2)


def load_niche_from_json(key: str) -> Optional[dict]:
    """Загрузить нишу из JSON-файла"""
    file_path = _get_niche_file_path(key)
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_niche(key: str, language: str = "ru") -> Optional[dict]:
    """
    Получить данные ниши
    Сначала ищет JSON, потом берёт из встроенных
    """
    niche = load_niche_from_json(key)
    if niche:
        return niche
    return DEFAULT_NICHES.get(key)


def get_all_niches(language: str = "ru", country: str = "uz") -> List[dict]:
    """Получить список всех активных ниш для конкретной страны"""
    niches = []

    # Загружаем из JSON-файлов
    for file_path in PROMPTS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                niche = json.load(f)
                if niche.get("is_active", True) and niche.get("country", "uz") == country:
                    niches.append(niche)
        except:
            pass

    # Если JSON пуст — берём встроенные для этой страны
    if not niches:
        for key, niche in DEFAULT_NICHES.items():
            if niche.get("country", "uz") == country:
                niches.append(niche)

    # Сортируем по ключу
    return sorted(niches, key=lambda x: x.get("key", ""))


def get_topics(key: str, count: int, language: str = "ru") -> List[str]:
    """
    Получить список тем для ниши.
    Если запрашиваемое количество больше, чем есть в базе,
    генерирует дополнительные динамические темы на лету.
    """
    niche = get_niche(key, language)
    if not niche:
        return []

    field = f"topics_{language}"
    topics = list(niche.get(field, niche.get("topics_ru", [])))

    if not topics:
        topics = ["Развитие и масштабирование вашего дела", "Секреты привлечения новых лояльных клиентов"]

    # Если тем меньше, чем просит пользователь (например, просит 10, 20 или 30, а в JSON только 5)
    if len(topics) < count:
        needed = count - len(topics)
        niche_name = get_niche_name(key, language)

        # Динамические шаблоны генерации тем
        if language == "uz":
            templates = [
                f"{niche_name} sohasida xatolar va ulardan qochish yo'llari",
                f"Muvaffaqiyatli {niche_name} biznesining 5 ta oltin qoidasi",
                f"Nega aynan bizning {niche_name} xizmatimizni tanlashadi?",
                f"Mijozlarni jalb qilishning yangi va samarali usullari",
                f"2026-yilda {niche_name} sohasidagi asosiy va muhim trendlar",
                f"Sifatli {niche_name} va uning sirlari",
                f"Qanday qilib {niche_name} orqali daromadni 2 barobar oshirish mumkin?",
                f"Tadbirkorlar uchun {niche_name} bo'yicha amaliy qo'llanma",
                f"Tez va xavfsiz {niche_name} xizmatlari",
                f"Mijozlarimiz tomonidan eng ko'p beriladigan savollarga javoblar"
            ]
        elif language == "tg":
            templates = [
                f"Хатогиҳои асосӣ дар соҳаи {niche_name} ва пешгирии онҳо",
                f"5 қоидаи тиллоӣ барои муваффақияти {niche_name}",
                f"Чаро мизоҷон маҳз хизматрасонии {niche_name}-и моро интихоб мекунанд",
                f"Роҳҳои муосири ҷалби мизоҷони нав ба {niche_name}",
                f"Трендҳои муҳими соҳаи {niche_name} дар соли 2026",
                f"Сирри сифати баланди {niche_name} дар чист?",
                f"Чӣ тавр даромади худро дар {niche_name} 2 баробар зиёд кунем",
                f"Дастури амалӣ оид ба {niche_name} барои соҳибкорон",
                f"Хизматрасониҳои зуд ва боэътимоди {niche_name}",
                f"Ҷавобҳо ба саволҳои бештар додашавандаи мизоҷон"
            ]
        else:
            templates = [
                f"Главные ошибки в сфере {niche_name} и как их избежать",
                f"5 золотых правил успешного бизнеса: {niche_name}",
                f"Почему клиенты выбирают именно наши услуги в {niche_name}",
                f"Современные методы привлечения клиентов в {niche_name}",
                f"Важные тренды в сфере {niche_name} на 2026 год",
                f"В чем секрет высокого качества услуг {niche_name}?",
                f"Как удвоить прибыль в бизнесе {niche_name}",
                f"Практическое руководство по {niche_name} для предпринимателей",
                f"Быстрые и надежные услуги {niche_name}",
                f"Ответы на самые часто задаваемые вопросы клиентов"
            ]

        random.shuffle(templates)
        for i in range(needed):
            new_theme = templates[i % len(templates)]
            if needed > len(templates):
                new_theme += f" (часть {i // len(templates) + 1})"
            topics.append(new_theme)

    selected = random.sample(topics, count)
    return selected


async def get_topic_ideas(key: str, count: int, language: str = "ru") -> List[Dict[str, Any]]:
    """Асинхронно получить темы в формате списка словарей с ключом 'title'"""
    topics = get_topics(key, count, language)
    return [{"title": t} for t in topics]


def get_niche_name(key: str, language: str = "ru") -> str:
    """Получить название ниши на нужном языке"""
    niche = get_niche(key, language)
    if not niche:
        return key

    field = f"name_{language}"
    return niche.get(field, niche.get("name_ru", key))


def get_niche_display(niche_id: str, lang: str = "ru") -> str:
    """Возвращает название ниши для отображения пользователю"""
    return get_niche_name(niche_id, lang)


def get_hashtags(key: str, language: str = "ru") -> str:
    """Получить хештеги для ниши"""
    niche = get_niche(key, language)
    if not niche:
        return "#uzbekistan" if language == "uz" else "#tajikistan"

    field = f"hashtags_{language}"
    return niche.get(field, niche.get("hashtags_ru", ""))


def get_niche_key_by_text(text: str, country: str = "uz") -> str:
    """Определить ключ ниши по тексту кнопки"""
    for niche in get_all_niches(country=country):
        if text in [niche.get("name_ru"), niche.get("name_tg"), niche.get("name_uz"), niche.get("icon", "") + " " + niche.get("name_ru", "")]:
            return niche["key"]
        if text.strip() == niche.get("name_ru") or text.strip() == niche.get("name_tg") or text.strip() == niche.get("name_uz"):
            return niche["key"]

    # Fallback
    text_lower = text.lower()
    if "ресторан" in text_lower or "чайхан" in text_lower or "choyxon" in text_lower or "kafe" in text_lower:
        return "cafe_uz" if country == "uz" else "wholesale"
    if "текстиль" in text_lower or "to'qimachilik" in text_lower:
        return "textile"
    if "недвижимость" in text_lower or "ko'chmas" in text_lower or "сохтмон" in text_lower:
        return "realestate" if country == "uz" else "construction"
    if "авто" in text_lower or "avto" in text_lower:
        return "auto_uz" if country == "uz" else "auto_tj"
    if "карго" in text_lower or "cargo" in text_lower:
        return "logistics_uz" if country == "uz" else "cargo"
    if "wedding" in text_lower or "тӯй" in text_lower or "to'y" in text_lower:
        return "wedding_tj"
    if "туризм" in text_lower or "сайёҳӣ" in text_lower:
        return "tourism"
    return "cafe_uz" if country == "uz" else "wholesale"


def init_default_niches():
    """При первом запуске сохранить все встроенные ниши в JSON"""
    # Удалим старые JSON-файлы, чтобы не было конфликтов
    for f in PROMPTS_DIR.glob("*.json"):
        try:
            f.unlink()
        except:
            pass

    for key, niche in DEFAULT_NICHES.items():
        save_niche_to_json(niche)
        print(f"✅ Ниша сохранена: {key} ({niche.get('country')})")


# ============================================
# ИНИЦИАЛИЗАЦИЯ ПРИ СТАРТЕ
# ============================================

init_default_niches()
