# content_engine/niche_manager.py — Менеджер ниш Sozanda, разделенный по странам

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
# БАЗОВЫЕ НИШИ ПО СТРАНАМ (Без дублирования)
# ============================================

DEFAULT_NICHES = {
    # ========================================
    # СЦЕНАРИЙ "УЗБЕКИСТАН" (uz)
    # ========================================
    "cafe_uz": {
        "key": "cafe_uz",
        "country": "uz",
        "name_ru": "🍔 Рестораны и Чайханы",
        "name_uz": "🍔 Milliy taomlar va Choyxonalar",
        "icon": "🍔",
        "topics_ru": [
            "Почему в нашей чайхане всегда свежий плов",
            "5 секретов идеальной самсы из тандыра",
            "Как мы выбираем лучшее мясо на базаре Чорсу",
            "Секретный рецепт маринада для узбекского шашлыка",
            "Традиции узбекского гостеприимства в нашем ресторане"
        ],
        "topics_uz": [
            "Nega bizning choyxonada palov har doim yangi va issiq",
            "Tandir somsa qilishning 5 ta oltin siri",
            "Chorsu bozoridan go'sht tanlashning o'zbekona usullari",
            "Haqiqiy o'zbekona kabob tayyorlash sirlari",
            "Restoranimizda o'zbekona mehmondo'stlik an'analari"
        ],
        "hashtags_ru": "#ресторан #чайхана #ташкент #плов #самса #еда #узбекистан",
        "hashtags_uz": "#restoran #choyxona #toshkent #palov #somsa #milliytaomlar #uzbekistan"
    },
    "textile": {
        "key": "textile",
        "country": "uz",
        "name_ru": "👗 Текстиль и Производство одежды",
        "name_uz": "👗 To'qimachilik va Kiyim ishlab chiqarish",
        "icon": "👗",
        "topics_ru": [
            "Почему узбекский хлопок ценится во всем мире",
            "Как работает наша текстильная фабрика изнутри",
            "5 причин покупать одежду оптом напрямую из Узбекистана",
            "Как мы контролируем качество пошива на производстве",
            "Тренды трикотажной одежды этого сезона"
        ],
        "topics_uz": [
            "Nega o'zbek paxtasi butun dunyoda mashhur va qadrli",
            "To'qimachilik fabrikamizning ichki ish jarayoni",
            "O'zbekistondan to'g'ridan-to'g'ri ulgurji kiyim sotib olishning 5 ta foydasi",
            "Ishlab chiqarishda kiyim tikish sifatini qanday nazorat qilamiz",
            "Ushbu mavsumning eng urfdagi trikotaj kiyimlari trendi"
        ],
        "hashtags_ru": "#текстиль #производство #одеждаоптом #хлопок #фабрика #узбекистан",
        "hashtags_uz": "#toqimachilik #ishlabchiqarish #kiyimlar #ulgurji #paxta #toshkent"
    },
    "realestate": {
        "key": "realestate",
        "country": "uz",
        "name_ru": "🏢 Недвижимость и Аренда в Ташкенте",
        "name_uz": "🏢 Toshkentda Ko'chmas mulk va Ijara",
        "icon": "🏢",
        "topics_ru": [
            "Обзор новостроек Ташкента: где выгоднее купить квартиру",
            "Как правильно арендовать жилье в Ташкенте и не переплатить",
            "5 ошибок при покупке недвижимости в Узбекистане",
            "Почему цены на недвижимость в Ташкенте продолжают расти",
            "Советы риелтора: как подготовить квартиру к быстрой продаже"
        ],
        "topics_uz": [
            "Toshkent yangi uylari (novostroyka) sharhi: qayerdan uy olgan afzal",
            "Toshkentda ijaraga uy olishda aldanib qolmaslik yo'llari",
            "O'zbekistonda ko'chmas mulk sotib olishda yo'l qo'yiladigan 5 ta xato",
            "Nega Toshkentda ko'chmas mulk narxlari tinimsiz oshib bormoqda",
            "Rieltor maslahati: uyni tez va qimmat sotish sirlari"
        ],
        "hashtags_ru": "#недвижимость #арендаташкент #новостройки #риелтор #квартираташкент #узбекистан",
        "hashtags_uz": "#uyjoy #ijara #toshkent #novostroyka #rieltor #kochmasmulk #uzbekistan"
    },
    "auto_uz": {
        "key": "auto_uz",
        "country": "uz",
        "name_ru": "🚗 Автосалоны и Автосервис",
        "name_uz": "🚗 Avtosalon va Avtoservis",
        "icon": "🚗",
        "topics_ru": [
            "Специфика авторынка Узбекистана: цены на Chevrolet и электромобили",
            "3 ошибки, которые совершают владельцы UzAuto при уходе за авто",
            "Как выгодно купить б/у машину на авторынке Сергели",
            "Почему качественное обслуживание в автосервисе экономит миллионы сумов",
            "Как подготовить вашу машину к климату Узбекистана"
        ],
        "topics_uz": [
            "O'zbekiston avtobozori: Chevrolet va elektromobillar narxlari tahlili",
            "UzAuto egalari mashina parvarishida yo'l qo'yadigan 3 ta xato",
            "Sergeli avtobozoridan qanday qilib yaxshi va arzon mashina olish mumkin",
            "Nega sifatli avtoservis xizmati millionlab so'm pulingizni tejaydi",
            "O'zbekiston iqlimida mashinani qanday to'g'ri parvarishlash kerak"
        ],
        "hashtags_ru": "#автосервис #авторынок #ташкент #сергели #chevrolet #uzauto #электромобили",
        "hashtags_uz": "#avtoservis #avtobozor #sergeli #toshkent #mashina #chevrolet #elektromobil"
    },
    "marketplace": {
        "key": "marketplace",
        "country": "uz",
        "name_ru": "🛒 Торговля на Uzum Market",
        "name_uz": "🛒 Uzum Marketda savdo qilish",
        "icon": "🛒",
        "topics_ru": [
            "Как начать продавать на Uzum Market с нуля в 2026 году",
            "5 ходовых товаров для маркетплейсов в Узбекистане",
            "Секреты вывода карточки товара в топ на Uzum",
            "Как правильно настроить рекламу своего магазина на Uzum",
            "Ошибки начинающих продавцов, которые ведут к сливу бюджета"
        ],
        "topics_uz": [
            "2026-yilda Uzum Marketda savdoni mutlaqo noldan boshlash",
            "O'zbekiston marketpleyslarida eng ko'p sotiladigan 5 ta xaridorgir tovar",
            "Uzumda mahsulot kartochkasini TOPga olib chiqish sirlari",
            "Uzum marketpleysida do'koningiz reklamalarini to'g'ri sozlash",
            "Yangi boshlovchi sotuvchilar yo'l qo'yadigan va zarar keltiradigan xatolar"
        ],
        "hashtags_ru": "#uzum #маркетплейс #бизнес #торговля #ташкент #узбекистан",
        "hashtags_uz": "#uzummarket #marketpleys #tadbirkor #savdo #toshkent #uzbekistan"
    },

    # ========================================
    # СЦЕНАРИЙ "ТАДЖИКИСТАН" (tj)
    # ========================================
    "wholesale": {
        "key": "wholesale",
        "country": "tj",
        "name_ru": "🛍️ Торговля и Опт",
        "name_tg": "🛍️ Савдо ва Яклухт",
        "icon": "🛍️",
        "topics_ru": [
            "Как устроена торговля на рынках Корвон и Панжшанбе",
            "Как возить товары оптом из Китая и Турции в Таджикистан",
            "5 советов для успешных продаж на рынках Душанбе",
            "Как находить надежных поставщиков для вашего бизнеса",
            "Почему оптовая торговля — самый прибыльный бизнес в Таджикистане"
        ],
        "topics_tg": [
            "Савдо дар бозорҳои Корвон ва Панҷшанбе чӣ гуна ба роҳ монда шудааст",
            "Чӣ тавр молҳоро бо яклухт аз Чин ва Туркия ба Тоҷикистон орем",
            "5 маслиҳат барои фурӯши бомуваффақият дар бозорҳои Душанбе",
            "Чӣ тавр таъминкунандагони боэътимодро барои тиҷорати худ пайдо кунем",
            "Чаро савдои яклухт — сердаромадтарин тиҷорат дар Тоҷикистон аст"
        ],
        "hashtags_ru": "#торговля #оптом #корвон #панжшанбе #душанбе #бизнес #таджикистан",
        "hashtags_tg": "#савдо #яклухт #корвон #панҷшанбе #душанбе #тиҷорат #тоҷикистон"
    },
    "cargo": {
        "key": "cargo",
        "country": "tj",
        "name_ru": "📦 Карго и Доставка в Душанбе",
        "name_tg": "📦 Карго ва Интиқоли мол ба Душанбе",
        "icon": "📦",
        "topics_ru": [
            "Как работает доставка карго из Китая, Турции и Дубая в Душанбе",
            "Почему важно выбрать правильную карго-компанию",
            "Сроки и цены: сколько стоит привезти товар в Худжанд",
            "Как отслеживать свои грузы без головной боли",
            "Секреты таможенного оформления товаров в Таджикистане"
        ],
        "topics_tg": [
            "Интиқоли карго аз Чин, Туркия ва Дубай ба Душанбе чӣ тавр кор мекунад",
            "Чаро интихоби дурусти ширкати карго хеле муҳим аст",
            "Мӯҳлат ва нархҳо: овардани мол ба Хуҷанд чанд пул меистад",
            "Чӣ тавр бори худро бе дарди сар назорат кунем",
            "Сиррҳои барасмиятдарории гумрукии молҳо дар Тоҷикистон"
        ],
        "hashtags_ru": "#карго #доставка #душанбе #худжанд #китай #турция #таджикистан",
        "hashtags_tg": "#карго #интиқолимол #душанбе #хуҷанд #чин #туркия #тоҷикистон"
    },
    "construction": {
        "key": "construction",
        "country": "tj",
        "name_ru": "🏗️ Строительство и Недвижимость",
        "name_tg": "🏗️ Сохтмон ва Кони Коғазӣ",
        "icon": "🏗️",
        "topics_ru": [
            "Рынок недвижимости Душанбе: как выгодно купить квартиру в новостройке",
            "Как выбрать качественные стройматериалы в Таджикистане",
            "5 этапов строительства дома вашей мечты в Душанбе",
            "Почему инвестировать в недвижимость Таджикистана выгодно именно сейчас",
            "Как сделать ремонт квартиры без лишних расходов"
        ],
        "topics_tg": [
            "Бозори амволи ғайриманқули Душанбе: чӣ тавр хонаи навро арзон харем",
            "Чӣ тавр масолеҳи сохтмонии босифатро дар Тоҷикистон интихоб кунем",
            "5 марҳилаи сохтмони хонаи орзуҳои шумо дар Душанбе",
            "Чаро сармоягузорӣ ба амволи Тоҷикистон маҳз ҳозир фоидаовар аст",
            "Чӣ тавр таъмири хонаро бе хароҷоти зиёдатӣ анҷом диҳем"
        ],
        "hashtags_ru": "#строительство #недвижимость #душанбе #квартира #стройматериалы #таджикистан",
        "hashtags_tg": "#сохтмон #хонаҳо #душанбе #манзил #масолеҳ #тоҷикистон"
    },
    "wedding_tj": {
        "key": "wedding_tj",
        "country": "tj",
        "name_ru": "💒 Национальная одежда и Свадебные услуги",
        "name_tg": "💒 Либоси миллӣ ва Хизматрасонии тӯй",
        "icon": "💒",
        "topics_ru": [
            "Красота национального платья: атлас и чакан в свадебной моде",
            "Как организовать традиционный таджикский той по всем правилам",
            "Оформление свадебного зала: лучшие тренды в Душанбе",
            "Почему свадебные платья ручной работы ценятся на вес золота",
            "Как выбрать лучшего ведущего и музыкантов для вашего торжества"
        ],
        "topics_tg": [
            "Зебоии либоси миллӣ: атлас ва чакан дар мӯди арӯсӣ",
            "Чӣ тавр тӯи анъанавии тоҷикиро мувофиқи тамоми қоидаҳо ташкил кунем",
            "Ороиши толори тӯёна: беҳтарин трендҳо дар Душанбе",
            "Чаро либосҳои арӯсии дастдӯз баҳои тилло доранд",
            "Чӣ тавр беҳтарин баранда ва навозандагонро барои тӯи худ интихоб кунем"
        ],
        "hashtags_ru": "#тӯй #чакан #атлас #свадьба #душанбе #одежда #таджикистан",
        "hashtags_tg": "#тӯй #чакан #атлас #арӯсӣ #душанбе #либосимиллӣ #тоҷикистон"
    },
    "tourism": {
        "key": "tourism",
        "country": "tj",
        "name_ru": "🏔️ Туризм и Зоны отдыха",
        "name_tg": "🏔️ Сайёҳӣ ва Минтақаҳои истироҳат",
        "icon": "🏔️",
        "topics_ru": [
            "Лучшие зоны отдыха Варзоба и Ромита для семейного отдыха",
            "Путеводитель по Искандеркулю: легенды и природа Таджикистана",
            "Как организовать незабываемый тур на Памир для иностранцев",
            "Почему внутренний туризм в Таджикистане переживает бум",
            "Популярные санатории Таджикистана для здоровья и отдыха"
        ],
        "topics_tg": [
            "Беҳтарин минтақаҳои истироҳатии Варзоб ва Ромит барои оилаҳо",
            "Роҳнамои Искандаркӯл: афсонаҳо ва табиати Тоҷикистон",
            "Чӣ тавр саёҳати фаромӯшнашаванда ба Помирро барои хориҷиён ташкил кунем",
            "Чаро сайёҳии дохилӣ дар Тоҷикистон рушд карда истодааст",
            "Омӯзиши беҳтарин осоишгоҳҳои Тоҷикистон барои саломатӣ ва истироҳат"
        ],
        "hashtags_ru": "#варзоб #ромит #памир #туризм #таджикистан #искандеркуль #душанбе",
        "hashtags_tg": "#варзоб #ромит #помир #сайёҳӣ #тоҷикистон #искандаркӯл #душанбе"
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
    # Пробуем загрузить из JSON
    niche = load_niche_from_json(key)
    if niche:
        return niche

    # Берём из встроенных
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
    генерирует дополнительные динамические темы на лету,
    чтобы гарантировать выдачу ровно count штук без повторений.
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
            # Создаем уникальные темы
            new_theme = templates[i % len(templates)]
            if needed > len(templates):
                new_theme += f" (часть {i // len(templates) + 1})"
            topics.append(new_theme)

    selected = random.sample(topics, count)
    return selected


async def get_topic_ideas(key: str, count: int, language: str = "ru") -> List[Dict[str, Any]]:
    """
    Асинхронно получить темы в формате списка словарей с ключом 'title'
    """
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


def add_custom_niche(
    key: str,
    name_ru: str,
    topics_ru: List[str],
    country: str = "uz",
    name_tg: str = "",
    topics_tg: List[str] = None,
    hashtags_ru: str = "",
    hashtags_tg: str = "",
    icon: str = "🏢",
    name_uz: str = "",
    topics_uz: List[str] = None,
    hashtags_uz: str = ""
):
    """
    Добавить новую нишу
    Сохраняется в JSON — переживёт перезапуск бота
    """
    niche_data = {
        "key": key,
        "country": country,
        "name_ru": name_ru,
        "name_tg": name_tg or name_ru,
        "name_uz": name_uz or name_ru,
        "icon": icon,
        "topics_ru": topics_ru,
        "topics_tg": topics_tg or topics_ru,
        "topics_uz": topics_uz or topics_ru,
        "hashtags_ru": hashtags_ru or ("#таджикистан #душанбе" if country == "tj" else "#uzbekistan #toshkent"),
        "hashtags_tg": hashtags_tg or "#тоҷикистон #душанбе",
        "hashtags_uz": hashtags_uz or "#uzbekistan #toshkent",
        "is_active": True,
    }

    save_niche_to_json(niche_data)
    return niche_data


def deactivate_niche(key: str):
    """Деактивировать нишу (не удалять)"""
    niche = load_niche_from_json(key)
    if niche:
        niche["is_active"] = False
        save_niche_to_json(niche)


def get_niche_key_by_text(text: str, country: str = "uz") -> str:
    """Определить ключ ниши по тексту кнопки"""
    # Сопоставляем по имени во всех локализациях
    for niche in get_all_niches(country=country):
        if text in [niche.get("name_ru"), niche.get("name_tg"), niche.get("name_uz"), niche.get("icon", "") + " " + niche.get("name_ru", "")]:
            return niche["key"]
        # Точное совпадение очищенного текста
        if text.strip() == niche.get("name_ru") or text.strip() == niche.get("name_tg") or text.strip() == niche.get("name_uz"):
            return niche["key"]

    # Fallback-маппинг
    text_lower = text.lower()
    if "ресторан" in text_lower or "чайхан" in text_lower or "choyxon" in text_lower or "kafe" in text_lower or "кафе" in text_lower:
        return "cafe_uz" if country == "uz" else "wholesale"
    if "текстиль" in text_lower or "производство" in text_lower or "to'qimachilik" in text_lower or "kiyim" in text_lower:
        return "textile"
    if "недвижимость" in text_lower or "аренда" in text_lower or "ko'chmas" in text_lower or "ijara" in text_lower or "сохтмон" in text_lower:
        return "realestate" if country == "uz" else "construction"
    if "авто" in text_lower or "avto" in text_lower:
        return "auto_uz"
    if "карго" in text_lower or "cargo" in text_lower:
        return "cargo"
    if "wedding" in text_lower or "тӯй" in text_lower or "to'y" in text_lower:
        return "wedding_tj"
    if "туризм" in text_lower or "сайёҳӣ" in text_lower or "tourism" in text_lower:
        return "tourism"
    return "cafe_uz" if country == "uz" else "wholesale"


def init_default_niches():
    """
    При первом запуске сохранить все встроенные ниши в JSON
    А также обновить существующие
    """
    # Удалим старые JSON-файлы, чтобы не было конфликтов старого и нового разделения
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
