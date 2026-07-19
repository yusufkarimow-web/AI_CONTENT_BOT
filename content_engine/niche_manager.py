# content_engine/niche_manager.py — Менеджер ниш TojikAI, разделенный по странам
# Более 100 специализированных бизнес-ниш, полностью адаптированных для Узбекистана и Таджикистана.

import json
import os
import random
from typing import Dict, List, Optional, Any
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts" / "niches"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# МАССИВ НИШ: БОЛЕЕ 100 СПЕЦИАЛИЗИРОВАННЫХ НИШ
# ============================================

DEFAULT_NICHES = {}

# --- УЗБЕКИСТАН (51 ниша) ---
UZ_NICHES = {
    "cafe_uz": ("🍔", "Миллий таомлар ва Чойхоналар", "Рестораны и Чайханы", ["Toshkentdagi eng mazali palov sirlari", "Milliy somsa tayyorlash an'analari"], ["Секрет самого вкусного плова в Ташкенте", "Традиции узбекской самсы"], "#palov #somsa", "#плов #самса"),
    "textile_uz": ("👗", "To'qimachilik va Kiyimlar", "Текстиль и Одежда", ["O'zbek paxtasi nega birinchi", "Ulgurji kiyim buyurtma qilish"], ["Почему узбекский хлопок лучший", "Как заказать трикотаж оптом"], "#toqimachilik", "#текстиль"),
    "realestate_uz": ("🏢", "Ko'chmas mulk va Ijara", "Недвижимость и Аренда", ["Toshkent yangi uylari sharhi", "Ijaraga arzon uy topish"], ["Обзор новостроек Ташкента", "Где арендовать квартиру выгодно"], "#toshkent #ijara", "#ташкент #аренда"),
    "auto_uz": ("🚗", "Sergeli avtosalon va Avtoservis", "Автосалоны и Автосервис", ["Sergeli avtobozori narxlari", "Chevrolet mashina parvarishi"], ["Обзор цен на авторынке Сергели", "Как ухаживать за Chevrolet"], "#sergeli #avto", "#сергели #авто"),
    "marketplace_uz": ("🛒", "Uzum Marketda Savdo", "Торговля на Uzum Market", ["Uzum Marketda savdo boshlash", "O'zbekistonda eng o'timli tovarlar"], ["Как выйти на Uzum Market", "Топ товаров для продаж в Узбекистане"], "#uzum", "#узум"),
    "logistics_uz": ("📦", "Xitoydan Kargo va Logistika", "Логистика и Карго Китай", ["Xitoydan Toshkentga yuk tashish", "Kargo yetkazish muddatlari"], ["Как возить товары из Гуанчжоу в Ташкент", "Сроки карго доставки"], "#kargo #xitoy", "#карго #китай"),
    "beauty_uz": ("💇‍♀️", "Go'zallik salonlari", "Салоны красоты", ["Toshkentda vizaj trendlari", "Yozda terini parvarishlash"], ["Тренды макияжа в Ташкенте", "Уход за кожей летом"], "#gozallik", "#красота"),
    "education_uz": ("🎓", "IT maktab va O'quv markazlari", "Учебные центры и IT школы", ["3 oyda IELTSga tayyorlanish", "Toshkentda eng istiqbolli IT sohalar"], ["Как подготовиться к IELTS за 3 месяца", "Перспективные IT направления в Ташкенте"], "#talim #it", "#образование"),
    "fastfood_uz": ("🍕", "Fast Fud Toshkent", "Фастфуд и Пиццерии", ["Toshkentdagi eng tez yetkazuvchi fastfud", "Laziz lavash tayyorlash siri"], ["Топ фастфудов Ташкента", "Секреты сочного лаваша"], "#fastfud", "#фастфуд"),
    "wedding_uz": ("💒", "To'ylar va Tadbirlar", "Свадьбы и Мероприятия", ["Kelin-salom marosimi tashkiloti", "Toshkent to'yxonalari sharhi"], ["Организация свадьбы в Узбекистане", "Традиции келин-салом"], "#toylar #tadbirlar", "#свадьба"),
    "tourism_uz": ("🏔️", "Samarqand va Buxoro Turizmi", "Туризм по Узбекистану", ["Samarqand tarixiy obidalari bo'yicha sayohat", "Buxoro choyxonalari va ziyorat"], ["Туры в Самарканд и Бухару", "Исторические гиды для иностранцев"], "#turizm #samarqand", "#туризм #самарканд"),
    "dentistry_uz": ("🦷", "Stomatologiya xizmatlari", "Стоматология и Лечение", ["Tishlarni og'riqsiz davolash", "Bredglar o'rnatish narxi"], ["Безболезненное лечение зубов в Ташкенте", "Установка брекетов"], "#stomatologiya", "#стоматология"),
    "mobile_uz": ("📱", "Telefon va Aksessuarlar", "Мобильные телефоны и Аксессуары", ["Eng so'nggi iPhone narxlari", "Malika bozoridan telefon tanlash"], ["Цены на новые смартфоны на рынке Малика", "Как выбрать аксессуары"], "#malika #telefon", "#малика #телефон"),
    "flowers_uz": ("💐", "Gullar yetkazib berish", "Доставка цветов", ["Toshkentda gullarni tez yetkazish", "Atirgullar guldastasi dizayni"], ["Быстрая доставка цветов в Ташкенте", "Красивые букеты роз"], "#gullar", "#цветы"),
    "drycleaning_uz": ("🧼", "Kimyoviy tozalash", "Химчистка одежды и ковров", ["Gilamlarni professional yuvish", "Kostyumlarni kimyoviy tozalash"], ["Профессиональная чистка ковров в Ташкенте", "Химчистка костюмов"], "#tozalash", "#химчистка"),
    "pharmacy_uz": ("💊", "Dorixona biznesi", "Аптечный бизнес", ["Dorixona ochish tartibi", "Eng ko'p sotiladigan dorilar"], ["Как открыть аптеку в Узбекистане", "Популярные лекарства"], "#dorixona", "#аптека"),
    "construction_uz": ("🧱", "Qurilish materiallari bozorlari", "Строительные материалы", ["Urikzor bozoridan arzon materiallar", "Sifatli gisht sotib olish"], ["Цены на стройматериалы на рынке Урикзор", "Как выбрать кирпич"], "#qurilish", "#стройматериалы"),
    "gym_uz": ("💪", "Sport zallari va Fitnes", "Спортивные залы и Фитнес", ["Toshkentdagi eng yaxshi fitnes klublar", "Ozish uchun mashqlar rejasi"], ["Топ фитнес-клубов Ташкента", "План тренировок для похудения"], "#fitnes #toshkent", "#фитнес #ташкент"),
    "cleaning_uz": ("🧹", "Tozalash xizmatlari", "Клининговые услуги", ["Xonadonlarni sifatli tozalash", "Ofis tozalash xizmati narxi"], ["Уборка квартир и офисов в Ташкенте", "Цены на клининг"], "#klining", "#клининг"),
    "confectionery_uz": ("🍰", "Qandolat mahsulotlari", "Кондитерские изделия", ["Mazali tortlar buyurtma qilish", "Milliy shirinliklar tayyorlash"], ["Заказ вкусных тортов в Ташкенте", "Узбекские сладости"], "#shirinliklar", "#сладости"),
    "carwash_uz": ("🚿", "Avtoyuvish shoxobchalari", "Автомойки", ["Avtomobilni to'g'ri yuvish sirlari", "Toshkentda kontaktsiz avtoyuvish"], ["Бесконтактная мойка в Ташкенте", "Химчистка салона авто"], "#avtoyuvish", "#автомойка"),
    "supermarket_uz": ("🛒", "Mini market va Do'konlar", "Мини-маркеты и Продукты", ["Mahallada do'kon ochish sirlari", "Ulgurji oziq-ovqat mahsulotlari"], ["Как открыть магазин у дома", "Оптовые закупки продуктов"], "#do'kon", "#магазин"),
    "solar_uz": ("☀️", "Quyosh panellari o'rnatish", "Солнечные панели", ["O'zbekistonda quyosh panellari foydasi", "Uyingizga quyosh paneli o'rnatish narxi"], ["Установка солнечных панелей в Узбекистане", "Экономия на электричестве"], "#quyosh #paneli", "#солнечныепанели"),
    "agrotech_uz": ("🚜", "Qishloq xo'jaligi texnikasi", "Сельхозтехника и Агро", ["Zamonaviy traktorlar narxlari", "Issiqxona jihozlari"], ["Цены на современные тракторы в Узбекистане", "Оборудование для теплиц"], "#agrotexnika", "#сельхозтехника"),
    "water_uz": ("💧", "Ichimlik suvi yetkazib berish", "Доставка питьевой воды", ["Toshkentda 19L suv buyurtma qilish", "Filtrlangan toza suv foydasi"], ["Заказ питьевой воды 19л в Ташкенте", "Польза чистой воды"], "#suv", "#доставкаводы"),
    "furniture_uz": ("🛋️", "Mebel salonlari va ishlab chiqarish", "Мебель под заказ", ["Toshkentda sifatli oshxona mebeli", "Yotoqxona mebellari dizayni"], ["Изготовление мебели под заказ в Ташкенте", "Дизайн кухонной мебели"], "#mebel", "#мебель"),
    "printing_uz": ("🖨️", "Bosmaxona va Poligrafiya", "Типография и Печать", ["Vizitkalar va flayerlar chop etish", "Brend logotipi tushirilgan qog'ozlar"], ["Печать визиток и буклетов в Ташкенте", "Брендирование упаковки"], "#bosmaxona", "#типография"),
    "legal_uz": ("⚖️", "Yuridik xizmatlar", "Юридические услуги", ["Toshkentda tadbirkorlar uchun yuridik maslahat", "Firma ochishni rasmiylashtirish"], ["Юридическая консультация для бизнеса", "Как зарегистрировать ООО"], "#yurist", "#юрист"),
    "audit_uz": ("📈", "Audit va Buxgalteriya", "Бухгалтерия и Аудит", ["Soliq hisobotlarini topshirish", "Autsorsing buxgalteriya xizmatlari"], ["Сдача налоговой отчетности в Ташкенте", "Бухгалтерский аутсорсинг"], "#buxgalteriya", "#бухгалтерия"),
    "kindergarten_uz": ("🧸", "Xususiy bog'chalar", "Частные детские сады", ["Toshkentdagi eng yaxshi xususiy bog'cha", "Bolalar uchun ingliz tili darslari"], ["Как выбрать частный детский сад", "Программа раннего развития"], "#bogcha", "#детскийсад"),
    "english_uz": ("🇬🇧", "Ingliz tili kurslari", "Курсы английского языка", ["Toshkentda intensiv ingliz tili", "IELTS imtihoniga tayyorgarlik"], ["Интенсивный английский в Ташкенте", "Подготовка к IELTS"], "#ingliztili", "#английский"),
    "security_uz": ("🛡", "Qo'riqlash agentliklari", "Охранные агентства", ["Ofis va do'konlarni qo'riqlash", "Xavfsizlik tizimlari o'rnatish"], ["Охрана офисов и коммерческих объектов", "Установка систем безопасности"], "#xavfsizlik", "#охрана"),
    "photo_uz": ("📸", "Fotosessiya va Video syomka", "Фото- и видеосъемка", ["Tashqi makonda professional fotosessiya", "Love story video olish"], ["Профессиональная фотосессия в Ташкенте", "Съемка рекламных видеороликов"], "#fotosessiya", "#фотосессия"),
    "pet_uz": ("🐱", "Zoodo'kon va Uy hayvonlari", "Зоомагазины", ["Mushuk va kuchuklar uchun sifatli ozuqalar", "Toshkent zoodo'konlari"], ["Качественные корма для кошек и собак", "Зоомагазины Ташкента"], "#zoodokon", "#зоомагазин"),
    "jewelry_uz": ("💎", "Zargarlik do'konlari", "Ювелирные изделия", ["Chorsu bozorida oltin narxlari", "Kumush taqinchoqlar dizayni"], ["Цены на золото на рынке Чорсу", "Серебряные украшения под заказ"], "#oltin", "#золото"),
    "coffee_uz": ("☕", "Qahvaxonalar (Coffee Shops)", "Кофейни", ["Toshkentdagi eng shinam kofeynalar", "Sifatli kofe donachalari"], ["Топ уютных кофеен Ташкента", "Где купить качественный зерновой кофе"], "#kofe", "#кофе"),
    "toy_uz": ("🧸", "Bolalar o'yinchoqlari do'koni", "Детские игрушки", ["Sifatli va xavfsiz bolalar o'yinchoqlari", "Yumshoq o'yinchoqlar yetkazish"], ["Безопасные развивающие игрушки", "Доставка мягких игрушек"], "#oyinchoqlar", "#игрушки"),
    "meat_uz": ("🥩", "Go'sht do'konlari (Halol Meat)", "Мясные лавки (Халяль)", ["Sifatli va yangi mol go'shti", "Toshkentda halol go'sht do'koni"], ["Свежее халяльное мясо в Ташкенте", "Оптовые поставки мяса"], "#gosht", "#мясо"),
    "cargodomestic_uz": ("🚛", "Ichki yuk tashish logistikasi", "Грузоперевозки по Узбекистану", ["Viloyatlararo yuk tashish xizmati", "Yengil va og'ir yuk mashinalari"], ["Грузоперевозки между вилоятами", "Доставка грузов по Ташкенту"], "#yuktashish", "#грузоперевозки"),
    "event_uz": ("🎉", "Tug'ilgan kunlar va Shou dasturlar", "Организация праздников", ["Bolalar uchun unutilmas shou dasturlar", "Tug'ilgan kunlarni bezatish"], ["Организация детских дней рождения", "Аниматоры в Ташкенте"], "#shou", "#праздник"),
    "solarwater_uz": ("🔥", "Quyosh suv isitgichlari", "Солнечные водонагреватели", ["Toshkentda quyosh kollektorlari o'rnatish", "Issiq suv tejamkorligi sirlari"], ["Установка солнечных водонагревателей", "Экономия на горячей воде"], "#quyoshsuv", "#водонагреватели"),
    "leather_uz": ("👞", "Charm va poyabzallar", "Кожаная обувь и производство", ["Charm poyabzallarni to'g'ri tanlash", "O'zbekistonda poyabzal ishlab chiqarish"], ["Производство кожаной обуви в Узбекистане", "Как ухаживать за туфлями"], "#charm", "#обувь"),
    "translation_uz": ("🌐", "Tarjimonlik markazlari", "Бюро переводов", ["Hujjatlarni rus va ingliz tillariga tarjima qilish", "Notarial tasdiqlangan tarjimalar"], ["Перевод документов на русский и английский", "Нотариальный перевод в Ташкенте"], "#tarjima", "#перевод"),
    "diagnostic_uz": ("🏥", "Tibbiy tahlil laboratoriyalari", "Медицинские лаборатории", ["Toshkentda tezkor tibbiy tahlillar", "Qon tahlili natijalari"], ["Быстрые медицинские анализы в Ташкенте", "Лабораторная диагностика"], "#tahlil", "#анализы"),
    "carpet_uz": ("🧺", "Gilam to'qish va sotish", "Продажа и стирка ковров", ["Marg'ilon gilamlari va ularning siri", "Gilamlarni tozalash usullari"], ["Маргиланские ковры ручной работы", "Как очистить дорогой ковер"], "#gilam", "#ковры"),
    "driedfruits_uz": ("🍇", "Quritilgan mevalar eksporti", "Экспорт сухофруктов", ["Urik va mayiz eksport qilish tartibi", "O'zbekiston milliy quruq mevalari"], ["Экспорт узбекского изюма и кураги", "Сухофрукты оптом"], "#quruqmeva", "#сухофрукты"),
    "drone_uz": ("🛸", "Dron orqali video va xizmatlar", "Аэросъемка и Дроны", ["Toshkentda dron orqali video suratga olish", "Dron xizmatlari narxlari"], ["Аэросъемка свадеб и объектов в Ташкенте", "Лицензирование дронов"], "#dron", "#аэросъемка"),
    "autotuning_uz": ("🏎️", "Avto tyuning va tuning xizmatlari", "Автотюнинг и стайлинг", ["Cobalt va Gentra avtomobillarini tyuning qilish", "Toshkentda sifatli tuning"], ["Тюнинг Cobalt и Gentra в Ташкенте", "Качественный автозвук и стайлинг"], "#tuning", "#тюнинг"),
    "handmade_uz": ("🎨", "Qo'l mehnati va Hunarmandchilik", "Ручная работа и сувениры", ["Milliy esdalik sovg'alari yasash", "Hunarmandchilik mahsulotlari sotuvi"], ["Узбекские национальные сувениры ручной работы", "Глиняная посуда Риштана"], "#hunarmand", "#сувениры"),
    "damolish_uz": ("🏞️", "Chorvoq va tog' dam olish zonalari", "Зоны отдыха (Чарвак/Амирсой)", ["Chorvoqda dacha ijaraga olish narxlari", "Amirsoy chang'i kurorti bo'yicha qo'llanma"], ["Аренда дачи на Чарваке", "Гид по горнолыжному курорту Amirsoy"], "#chorvoq", "#чарвак"),
    "franchise_uz": ("🤝", "Biznes franshiza va konsalting", "Франшизы и консалтинг", ["O'zbekistonda muvaffaqiyatli franshizalar", "Konsalting xizmati orqali biznesni oshirish"], ["Популярные франшизы в Узбекистане", "Консалтинг для малого бизнеса"], "#franshiza", "#франшиза")
}

# --- ТАДЖИКИСТАН (51 ниша) ---
TJ_NICHES = {
    "wholesale_tj": ("🛍️", "Бозори Корвон - Савдо ва Яклухт", "Торговля и Опт (Рынок Корвон)", ["Чӣ тавр дар бозори Корвон мол закупат кунем", "Беҳтарин молҳо барои фурӯши чакана дар Душанбе"], ["Как закупаться на рынке Корвон оптом", "Лучшие товары для розничной торговли в Душанбе"], "#корвон #яклухт", "#корвон #оптом"),
    "cargo_tj": ("📦", "Карго Чин/Дубай ва Интиқол", "Карго и Доставка (Китай/Дубай)", ["Овардани бори карго аз Чин ба Душанбе", "Мӯҳлати барасмиятдарории гумрукӣ"], ["Как везти карго груз из Иу и Гуанчжоу в Душанбе", "Сроки таможенного оформления товаров"], "#карго #душанбе", "#каргокитай #доставкадушанбе"),
    "construction_tj": ("🏗️", "Сохтмон ва Таъмири новостройкаҳо", "Строительство и Ремонт новостроек", ["Нархи хонаҳои нав дар маркази Душанбе", "Чӣ тавр ороиши дохилии хонаро интихоб кунем"], ["Цены на новостройки в центре Душанбе", "Как выбрать дизайн интерьера квартиры"], "#сохтмон #душанбе", "#строительство #новостройкидушанбе"),
    "wedding_tj": ("💒", "Либоси Миллии Чакан ва Тӯйҳо", "Свадебные услуги и Либоси Милли", ["Нақшҳои чакан дар тӯйҳои тоҷикӣ", "Ташкили тӯи боҳашамат дар Душанбе"], ["Традиционные узоры чакан на свадьбе", "Организация идеального тоя в Душанбе"], "#чакан #тӯй", "#чакан #атлас #свадьбадушанбе"),
    "tourism_tj": ("🏔️", "Истироҳатгоҳҳои Варзоб ва Ромит", "Туризм и Санатории (Варзоб)", ["Беҳтарин минтақаҳои истироҳатии Варзоб ва Ромит", "Саёҳати фаромӯшнашаванда ба Помир"], ["Лучшие зоны отдыха Варзоба и Ромита", "Легендарный тур на Памир и Искандеркуль"], "#варзоб #сайёҳӣ", "#варзоб #ромит #памир #туризм"),
    "beauty_tj": ("💅", "Салонҳои ҳусн ва Барбершопҳо", "Салоны красоты и Барбершопы", ["Мӯйҳои муд дар Душанбе дар ин мавсим", "Беҳтарин косметологро аз куҷо пайдо кунем"], ["Трендовые стрижки в Душанбе этого сезона", "Где найти лучшего косметолога"], "#зебоӣ #душанбе", "#красотадушанбе #барбершоп"),
    "education_tj": ("📚", "Марказҳои таълимӣ ва Репетиторҳо", "Учебные центры и Репетиторы", ["Чӣ тавр аз Душанбе ба донишгоҳи хориҷӣ дохил шавем", "Омодагӣ ба имтиҳонҳо ва тестҳо"], ["Как поступить в зарубежный вуз из Душанбе", "Подготовка к экзаменам и тестам"], "#таълим #душанбе", "#образованиедушанбе #учеба"),
    "auto_tj": ("🚘", "Қисмҳои эҳтиётии мошинҳо", "Автосалоны, Запчасти и Автомойка", ["Қисмҳои эҳтиётии арзонро дар Душанбе аз куҷо харем", "Нархи мошинҳо дар Тоҷикистон"], ["Где выгодно купить автозапчасти в Душанбе", "Обзор цен на автомобили в Таджикистане"], "#авто #мошин #душанбе", "#автодушанбе #запчасти"),
    "food_tj": ("🍲", "Оши палови миллӣ ва Чойхонаҳо", "Рестораны и Национальная Кухня", ["Сирри пухтани оши палови лазизи Душанбе", "Беҳтарин чойхонаҳои миллӣ барои оила"], ["Секрет вкусного таджикского плова", "Традиционные чайханы Душанбе"], "#палов #чойхона", "#плов #чайханадушанбе"),
    "cargotrans_tj": ("🚛", "Боркашонии дохилӣ ва байналмилалӣ", "Грузоперевозки и Логистика", ["Хизматрасонии боркашонӣ ба вилоятҳои Тоҷикистон", "Интиқоли бехатари борҳо"], ["Грузоперевозки по всем регионам Таджикистана", "Быстрая доставка грузов"], "#боркашонӣ #тоҷикистон", "#грузоперевозки #душанбе"),
    "chinacargo_tj": ("🇨🇳", "Карго аз Чин ба Душанбе", "Китай Карго Душанбе", ["Тарзи фармоиш додани мол аз Чин бо карго", "Нархи як кило бор аз Чин ба Душанбе"], ["Как заказать товары напрямую из Китая", "Цены за килограмм карго из Китая"], "#чин #карго", "#каргокитай #душанбе"),
    "panjshanbe_tj": ("🛒", "Бозори Панҷшанбе (Хуҷанд)", "Рынок Панчшанбе (Худжанд)", ["Нархҳои бозори Панҷшанбе дар Хуҷанд", "Хариди яклухти маҳсулоти хӯрокворӣ дар Суғд"], ["Обзор цен на рынке Панчшанбе в Худжанде", "Оптовые закупки товаров в Согде"], "#панҷшанбе #хуҷанд", "#панжшанбе #худжанд"),
    "pamir_tj": ("⛰️", "Саёҳати Бадахшон ва Помир", "Туризм по Памиру и ГБАО", ["Роҳнамои сайёҳӣ ба Помир ва кӯҳҳои Бадахшон", "Иҷораи мошинҳои 4x4 барои сафари Помир"], ["Гид по Памирскому тракту", "Аренда внедорожников для поездки на Памир"], "#помир #бадахшон", "#памир #бадахшон #туризм"),
    "mobile_tj": ("📱", "Фурӯши телефон ва аксбардорӣ", "Мобильные телефоны и аксессуары", ["Нархи охирини телефонҳо дар Садбарг", "Беҳтарин аксессуарҳо барои смартфон"], ["Цены на новые смартфоны в ТЦ Садбарг", "Как выбрать аксессуары для телефона"], "#садбарг #телефон", "#садбарг #телефоны"),
    "dryfruits_tj": ("🍇", "Меваҳои хушки Исфара ва содирот", "Сухофрукты Исфары и экспорт", ["Содироти зардолуи Исфара ба Русия", "Сирри сифати баланди меваи хушк"], ["Экспорт исфаринской кураги в Россию", "Поставки сухофруктов оптом из Исфары"], "#исфара #мева", "#исфара #сухофрукты"),
    "dentistry_tj": ("🦷", "Тандурустӣ ва Дандонпизишкӣ", "Стоматология в Душанбе", ["Муолиҷаи бедарди дандон дар марказҳои муосир", "Нархи имплантатсияи дандон"], ["Качественное лечение зубов в Душанбе", "Цены на имплантацию зубов"], "#дандон #душанбе", "#стоматологиядушанбе"),
    "honey_tj": ("🐝", "Асали кӯҳии Тоҷикистон", "Горный мед Таджикистана", ["Манфиати асали табиии кӯҳҳои Рашт", "Чӣ тавр асали тозаро аз қалбакӣ фарқ кунем"], ["Польза натурального гармского меда", "Как отличить настоящий горный мед"], "#асал #тоҷикистон", "#мед #таджикистан"),
    "carpet_tj": ("🧺", "Фурӯши қолинҳо ва қолинбофӣ", "Ковры и Ковролин", ["Қолинҳои зебои истеҳсоли Кайроққум", "Тарзи тоза кардани қолинҳои гаронбаҳо"], ["Кайраккумские ковры ручной работы", "Чистка ковров в Душанбе"], "#қолин #қайроққум", "#ковры #кайраккум"),
    "cleaning_tj": ("🧹", "Хизматрасонии тозакунӣ (Клининг)", "Клининговые услуги Душанбе", ["Тозакунии касбии хонаҳо ва офисҳо", "Нархи хизматрасонии клининг дар Душанбе"], ["Профессиональная уборка квартир в Душанбе", "Услуги клининга цены"], "#тозакунӣ #клининг", "#уборкадушанбе #клининг"),
    "water_tj": ("💧", "Интиқоли оби нӯшокӣ (Оби Зулол)", "Доставка питьевой воды", ["Оби софи ошомиданӣ барои хона ва коргоҳ", "Фармоиши оби нӯшокӣ дар Душанбе"], ["Заказ чистой питьевой воды в Душанбе", "Польза артезианской воды"], "#об #обизулол", "#доставкаводы #душанбе"),
    "realestate_tj": ("🏢", "Агентии амволи ғайриманқул", "Агентства недвижимости", ["Хариду фурӯши хонаҳо дар Душанбе", "Иҷораи дафтари корӣ дар маркази пойтахт"], ["Покупка и продажа квартир в Душанбе", "Аренда коммерческой недвижимости"], "#хона #душанбе", "#недвижимостьдушанбе"),
    "autotuning_tj": ("🏎️", "Автотюнинг ва устохонаҳои мошин", "Автотюнинг и стайлинг", ["Тюнинги мошинҳои Opel ва Mercedes дар Душанбе", "Ороиши дарунии мошин"], ["Тюнинг автомобилей в Душанбе", "Шумоизоляция и перетяжка салона"], "#тюнинг #душанбе", "#автотюнинг #душанбе"),
    "printing_tj": ("🖨️", "Нашриёт ва матбааҳои муосир", "Типография и Полиграфия", ["Чопи кортҳои боздид ва флаерҳо дар Душанбе", "Брендиронии бастаҳо"], ["Качественная печать визиток в Душанбе", "Дизайн и печать рекламных буклетов"], "#матбаа #чоп", "#типографиядушанбе"),
    "confectionery_tj": ("🍰", "Қаннодӣ ва пирожниҳои лазиз", "Кондитерские изделия (Торты)", ["Фармоиши тортҳои ҷашнӣ ва зодрӯзӣ", "Маҳсулоти қаннодии болаззат"], ["Заказ красивых праздничных тортов", "Сладкая выпечка в Душанбе"], "#қаннодӣ #торт", "#кондитерскаядушанбе"),
    "security_tj": ("🛡", "Агентиҳои муҳофизатӣ (Амният)", "Охранные предприятия", ["Муҳофизати боэътимоди хонаҳо ва мағозаҳо", "Насби камераҳои назоратӣ"], ["Охрана объектов и частных домов в Таджикистане", "Установка камер видеонаблюдения"], "#амният #душанбе", "#охранадушанбе"),
    "english_tj": ("🇬🇧", "Курсҳои забони англисӣ (IELTS)", "Курсы английского языка", ["Курсҳои интенсивии забони англисӣ дар Душанбе", "Омодагии касбӣ ба IELTS"], ["Интенсивный английский язык в Душанбе", "Подготовка к экзамену IELTS"], "#англисӣ #душанбе", "#английскийдушанбе"),
    "it_tj": ("💻", "Академияҳои IT ва барномасозӣ", "IT академии и программирование", ["Омӯзиши барномасозӣ барои кӯдакон ва калонсолон", "Касбҳои сердаромад дар IT"], ["Обучение программированию в Душанбе", "Курсы веб-разработки и QA"], "#ит #барномасозӣ", "#itдушанбе #программирование"),
    "legal_tj": ("⚖️", "Хизматрасонии ҳуқуқӣ (Адвокатҳо)", "Юридические услуги и адвокаты", ["Машварати ҳуқуқӣ барои соҳибкорон", "Адвокат оид ба корҳои гражданӣ"], ["Консультация опытных адвокатов в Душанбе", "Регистрация бизнеса ООО и ИП"], "#ҳуқуқшинос #адвокат", "#юристудушанбе"),
    "gym_tj": ("💪", "Толорҳои варзишӣ ва фитнес", "Спортивные залы и фитнес", ["Толорҳои варзишии муосир барои занон ва мардон", "Машқҳо барои харобшавӣ"], ["Фитнес-центры Душанбе", "Индивидуальные тренировки с тренером"], "#фитнес #душанбе", "#фитнесдушанбе"),
    "pharmacy_tj": ("💊", "Дорухонаҳо ва маводи тиббӣ", "Аптечные сети и лекарства", ["Дарёфти доруҳои нодир дар дорухонаҳои шаҳр", "Маводи тиббии босифат"], ["Поиск редких лекарств в аптеках Душанбе", "Качественные медицинские препараты"], "#дорухона #душанбе", "#аптекидушанбе"),
    "flowers_tj": ("💐", "Фурӯши гулҳо ва ороиши чорабиниҳо", "Цветочные салоны", ["Фармоиши гулҳои тару тоза бо интиқол", "Ороиши толорҳо бо гулҳои табиӣ"], ["Доставка шикарных букетов роз в Душанбе", "Оформление свадеб цветами"], "#гулҳо #душанбе", "#цветыдушанбе"),
    "weddingdress_tj": ("👰", "Салонҳои либоси арӯсӣ ва ороиш", "Салоны свадебных платьев", ["Интихоби зеботарин либоси арӯсӣ", "Ороиши мӯй ва чеҳраи арӯсӣ"], ["Прокат свадебных платьев в Душанбе", "Профессиональный макияж невесты"], "#арӯсӣ #салон", "#невестадушанбе"),
    "furniture_tj": ("🛋️", "Истеҳсол ва фурӯши мебел", "Производство мебели под заказ", ["Мебели муосири ошхона ва меҳмонхона", "Истеҳсоли мебел бо тарҳи инфиродӣ"], ["Изготовление мебели на заказ в Душанбе", "Мягкая мебель и спальные гарнитуры"], "#мебел #душанбе", "#мебельдушанбе"),
    "agro_tj": ("🚜", "Рушди кишоварзӣ ва гармхонаҳо", "Сельское хозяйство и теплицы", ["Парвариши лиму дар гармхонаҳои Тоҷикистон", "Маслиҳатҳои фоиданок барои деҳқонон"], ["Выращивание лимонов в теплицах Таджикистана", "Современные агротехнологии"], "#деҳқон #тоҷикистон", "#агротаджикистан"),
    "privateschool_tj": ("🧸", "Мактабҳои хусусӣ ва кӯдакистонҳо", "Частные школы и детские сады", ["Беҳтарин кӯдакистонҳои хусусӣ дар пойтахт", "Таҳсилоти босифат дар мактабҳои хусусӣ"], ["Частные школы в Душанбе с английским уклоном", "Детские сады развивающие"], "#мактаб #кӯдакистон", "#детскийсаддушанбе"),
    "accounting_tj": ("📈", "Аудити молиявӣ ва ҳисобдорӣ", "Бухгалтерия и финансовый аудит", ["Хизматрасонии муҳосибӣ барои ширкатҳои хурд", "Ҳисоботи андоз"], ["Бухгалтерские услуги для бизнеса в Таджикистане", "Сдача налоговой отчетности"], "#муҳосиб #андоз", "#бухгалтердушанбе"),
    "photo_tj": ("📸", "Студияҳои аксбардорӣ ва видео", "Фото- и видеостудии", ["Аксбардории касбии тӯйҳо ва ҷашнҳо", "Наворбардории рекламӣ"], ["Профессиональные фотосессии в Душанбе", "Съемка рекламных роликов"], "#аксбардорӣ #душанбе", "#фотостудиядушанбе"),
    "pet_tj": ("🐱", "Дӯкони ҳайвоноти хонагӣ", "Зоомагазины в Душанбе", ["Хӯроки босифат барои гурба ва сагҳо", "Акссесуарҳои зебо барои ҳайвонот"], ["Корма премиум класса для питомцев", "Зоомагазины в Душанбе доставка"], "#ҳайвонот #душанбе", "#зоомагазиндушанбе"),
    "jewelry_tj": ("💎", "Фурӯши ҷавоҳирот ва тилловорӣ", "Ювелирные изделия и золото", ["Нархи тилло дар бозорҳои Душанбе", "Ҷавоҳироти нуқрагии дастӣ"], ["Цены на золото в ювелирных магазинах Душанбе", "Эксклюзивные серебряные украшения"], "#тилло #душанбе", "#золотодушанбе"),
    "coffee_tj": ("☕", "Қаҳвахонаҳои муосир (Coffee)", "Кофейни в Душанбе", ["Беҳтарин ҷойҳо барои хӯрдани қаҳва дар марказ", "Аромати қаҳваи табиӣ"], ["Где выпить лучший кофе в Душанбе", "Уютные кофейни для встреч"], "#қаҳва #душанбе", "#кофедушанбе"),
    "meat_tj": ("🥩", "Фурӯши гӯшти ҳалол ва қасобӣ", "Мясные лавки (Халяль)", ["Гӯшти тару тозаи гӯсфанд ва гов", "Дӯконҳои касбии гӯштӣ дар Душанбе"], ["Свежее халяльное мясо в Душанбе", "Оптовые поставки говядины"], "#гӯшт #ҳалол", "#мясодушанбе"),
    "cargouae_tj": ("✈️", "Карго Дубай-Душанбе бо тайёра", "Авиакарго Дубай-Душанбе", ["Интиқоли фаврии борҳо аз Аморати Муттаҳида", "Суръати болои интиқоли авиатсионӣ"], ["Быстрая авиадоставка грузов из Дубая в Душанбе", "Тарифы на грузоперевозки авиа"], "#каргодубай #душанбе", "#каргодубай #душанбе"),
    "foreignvacation_tj": ("🌍", "Саёҳати хориҷӣ барои шаҳрвандон", "Туристические агентства", ["Саёҳат ба Туркия ва Дубай бо нархҳои дастрас", "Визҳои сайёҳӣ ва чиптаҳо"], ["Горящие туры в Турцию и Египет из Душанбе", "Оформление виз и авиабилеты"], "#саёҳат #душанбе", "#турыиздушанбе"),
    "solarpower_tj": ("☀️", "Насби панелҳои офтобӣ дар хонаҳо", "Солнечные электростанции", ["Истифодаи энергияи офтоб дар шароити Тоҷикистон", "Нархи таҷҳизоти офтобӣ"], ["Установка солнечных панелей под ключ в Душанбе", "Альтернативная энергетика"], "#панелиофтобӣ", "#солнечныепанелитаджикистан"),
    "leather_tj": ("👞", "Истеҳсоли пойафзоли чармӣ", "Кожаная обувь ручной работы", ["Пойафзоли чармии мардона аз устоҳои маҳаллӣ", "Сифати баланди пойафзол"], ["Мужская кожаная обувь ручной работы в Душанбе", "Качественная кожаная галантерея"], "#пойафзол #чарм", "#обувьдушанбе"),
    "diagnostic_tj": ("🏥", "Марказҳои ташхиси тиббӣ", "Медицинская диагностика", ["Ташхиси пурраи бадан дар беҳтарин клиникаҳо", "Таҳлилҳои фаврӣ"], ["Комплексное обследование организма в Душанбе", "Современная УЗИ диагностика"], "#ташхис #тиб", "#диагностикадушанбе"),
    "event_tj": ("🎉", "Ташкили зодрӯз ва ҷашнвораҳо", "Организация праздников", ["Аниматорҳо ва барномаҳои шавқовар барои кӯдакон", "Ороиши ҷои зодрӯз"], ["Аниматоры и шоу программы для детей в Душанбе", "Оформление дней рождения"], "#зодрӯз #душанбе", "#праздникдушанбе"),
    "translation_tj": ("🌐", "Марказҳои тарҷумонии расмӣ", "Бюро переводов в Душанбе", ["Тарҷумаи расмии ҳуҷҷатҳо бо тасдиқи нотариус", "Тарҷумони забони англисӣ"], ["Официальный перевод документов с заверением", "Услуги переводчиков в Душанбе"], "#тарҷума #душанбе", "#бюропереводовдушанбе"),
    "handmade_tj": ("🎨", "Ҳунари дастӣ ва армуғонҳо", "Народные промыслы и сувениры", ["Армуғонҳои миллӣ аз устоҳои Хатлону Суғд", "Ҳунари дастӣ ва маҳсулот"], ["Таджикские национальные сувениры ручной работы", "Керамика и вышивка ручной работы"], "#ҳунаридастӣ", "#сувенирытаджикистан"),
    "gas_tj": ("⛽", "Нуқтаҳои сӯзишворӣ ва гази табиӣ", "Сети АЗС и Топливо", ["Сӯзишвории босифати Евро-5 дар шабакаҳои АЗС", "Нархи газ ва бензин имрӯз"], ["Качественное топливо Евро-5 на АЗС Душанбе", "Цены на бензин и газ сегодня"], "#сӯзишворӣ #азс", "#азстаджикистан"),
    "waterpark_tj": ("🏊‍♂️", "Боғҳои обӣ ва истироҳати тобистона", "Аквапарки и летний отдых", ["Истироҳати тобистона дар аквапаркҳои Душанбе", "Нархнома барои оилаҳо"], ["Летний отдых в аквапарках Душанбе", "Бассейны и водные аттракционы"], "#аквапарк #душанбе", "#аквапаркдушанбе")
}


# Объединяем списки ниш
for k, v in UZ_NICHES.items():
    DEFAULT_NICHES[k] = {
        "key": k, "country": "uz", "icon": v[0],
        "name_uz": v[1], "name_ru": v[2],
        "topics_uz": v[3], "topics_ru": v[4],
        "hashtags_uz": v[5], "hashtags_ru": v[6]
    }

for k, v in TJ_NICHES.items():
    DEFAULT_NICHES[k] = {
        "key": k, "country": "tj", "icon": v[0],
        "name_tg": v[1], "name_ru": v[2],
        "topics_tg": v[3], "topics_ru": v[4],
        "hashtags_tg": v[5], "hashtags_ru": v[6]
    }


def _get_niche_file_path(key: str) -> Path:
    return PROMPTS_DIR / f"{key}.json"


def save_niche_to_json(niche_data: dict):
    file_path = _get_niche_file_path(niche_data["key"])
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(niche_data, f, ensure_ascii=False, indent=2)


def load_niche_from_json(key: str) -> Optional[dict]:
    file_path = _get_niche_file_path(key)
    if not file_path.exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_niche(key: str, language: str = "ru") -> Optional[dict]:
    niche = load_niche_from_json(key)
    if niche:
        return niche
    return DEFAULT_NICHES.get(key)


def get_all_niches(language: str = "ru", country: str = "uz") -> List[dict]:
    niches = []
    # Сначала проверяем JSON файлы
    for file_path in PROMPTS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                niche = json.load(f)
                if niche.get("is_active", True) and niche.get("country", "uz") == country:
                    niches.append(niche)
        except:
            pass

    # Если файлов нет, подгружаем встроенные
    if not niches:
        for key, niche in DEFAULT_NICHES.items():
            if niche.get("country", "uz") == country:
                niches.append(niche)

    return sorted(niches, key=lambda x: x.get("key", ""))


def get_topics(key: str, count: int, language: str = "ru") -> List[str]:
    niche = get_niche(key, language)
    if not niche:
        return []

    field = f"topics_{language}"
    topics = list(niche.get(field, niche.get("topics_ru", [])))

    if not topics:
        topics = ["Развитие и масштабирование вашего дела", "Секреты привлечения новых лояльных клиентов"]

    if len(topics) < count:
        needed = count - len(topics)
        niche_name = get_niche_name(key, language)

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
    topics = get_topics(key, count, language)
    return [{"title": t} for t in topics]


def get_niche_name(key: str, language: str = "ru") -> str:
    niche = get_niche(key, language)
    if not niche:
        return key
    field = f"name_{language}"
    return niche.get(field, niche.get("name_ru", key))


def get_niche_display(niche_id: str, lang: str = "ru") -> str:
    return get_niche_name(niche_id, lang)


def get_hashtags(key: str, language: str = "ru") -> str:
    niche = get_niche(key, language)
    if not niche:
        return "#uzbekistan" if language == "uz" else "#tajikistan"
    field = f"hashtags_{language}"
    return niche.get(field, niche.get("hashtags_ru", ""))


def get_niche_key_by_text(text: str, country: str = "uz") -> str:
    # Очищаем текст от иконки в начале, если она есть
    cleaned_text = text.strip()
    if len(cleaned_text) > 2 and not cleaned_text[0].isalnum():
        parts = cleaned_text.split(maxsplit=1)
        if len(parts) > 1:
            cleaned_text = parts[1]

    for niche in get_all_niches(country=country):
        # Проверяем точное совпадение имени (с и без иконки)
        if text in [niche.get("name_ru"), niche.get("name_tg"), niche.get("name_uz")]:
            return niche["key"]
        n_icon = niche.get("icon", "")
        n_ru = niche.get("name_ru", "")
        n_tg = niche.get("name_tg", "")
        n_uz = niche.get("name_uz", "")
        if text in [f"{n_icon} {n_ru}".strip(), f"{n_icon} {n_tg}".strip(), f"{n_icon} {n_uz}".strip()]:
            return niche["key"]
        if cleaned_text in [n_ru, n_tg, n_uz]:
            return niche["key"]

    # Дополнительный фоллбек-поиск
    text_lower = text.lower()
    for key, niche in DEFAULT_NICHES.items():
        if niche.get("country") == country:
            n_ru = niche.get("name_ru", "").lower()
            n_tg = niche.get("name_tg", "").lower()
            n_uz = niche.get("name_uz", "").lower()
            if text_lower in n_ru or text_lower in n_tg or text_lower in n_uz:
                return key

    # Окончательный фоллбек по умолчанию
    return "cafe_uz" if country == "uz" else "wholesale_tj"


def init_default_niches():
    # Удаляем старые файлы для обновления
    for f in PROMPTS_DIR.glob("*.json"):
        try:
            f.unlink()
        except:
            pass

    for key, niche in DEFAULT_NICHES.items():
        save_niche_to_json(niche)


init_default_niches()
