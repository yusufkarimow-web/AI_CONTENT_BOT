# -*- coding: utf-8 -*-
# data/smm_memory_db.py — База знаний и премиум пресеты SMM (40% востребованных данных для 80% пользователей)
# Локализована для Узбекистана (UZS, Click, Payme, Tashkent), Таджикистана (TJS, Alif, Dushanbe) и России (RUB, Sber, Moscow)

SMM_EXPERT_PRESETS = {
    "cafe": {
        "icon": "🍔",
        "name_ru": "Рестораны и Кафе",
        "name_uz": "Restoranlar va Kafelar",
        "name_tg": "Ресторанҳо ва Кафеҳо",
        "ru": {
            "plan": """📅 Контент-план на 7 дней для Кафе/Ресторана:
День 1: [Пост] История создания фирменного блюда. Фокус: вовлечение и доверие.
День 2: [Stories] Опрос: "Что вы выберете сегодня — сочный плов или сытный курутоб?"
День 3: [Reels] Вирусный хук: "Секретный ингредиент, который делает наш соус неповторимым".
День 4: [Пост] Знакомство с шеф-поваром и его философией вкуса.
День 5: [Stories] Процесс подготовки кухни к открытию (эстетика чистоты).
День 6: [Reels] Видео-отзыв довольного гостя крупным планом.
День 7: [Пост] Рекламный оффер: бесплатный десерт при заказе от 150 сомони / 150,000 сум.""",
            "reels": """🎬 Сценарий Reels: "Вкус, который заставляет вернуться"
- Хук (0-3 сек): Шеф-повар медленно наливает золотистый соус на сочное мясо на фоне улыбающихся гостей. Текст на экране: "Вы никогда не пробовали это..."
- Кадры (B-rolls): Крупный план пара от свежего блюда, хруст корочки самсы, уютная атмосфера зала.
- Диктор: "Секрет идеального вкуса не в специях, а в любви к традициям. Каждое утро мы отбираем свежие фермерские продукты, чтобы подарить вам незабываемые эмоции."
- CTA (Призыв): "Приходите сегодня в гости! Забронируйте столик через директ и получите приветственный чай бесплатно."
- Хэштеги: #ресторан #кафе #вкуснаяеда #ужин #обед""",
            "posts": """🍔 Пост: Как превратить обычный ужин в кулинарный праздник?
Вы когда-нибудь задумывались, почему домашняя еда отличается от ресторанной?
Всё дело в деталях и атмосфере. Наша команда ежедневно трудится над тем, чтобы каждый визит дарил вам тепло родного дома и изысканность высокой кухни.

Мы используем только свежие локальные ингредиенты и авторские специи. Приглашаем вас расслабиться после тяжелого дня в нашем уютном зале под мягкий свет и приятную музыку.

📍 Наш адрес: ул. Рудаки / проспект А. Темура
📞 Забронировать стол: звоните или пишите в директ!
#кафе #ресторан #уют #вкусныйужин""",
            "stories": """Серия Stories (Прогрев за 5 слайдов):
Слайд 1: Загадочный кадр из кухни с паром. Текст: "Что здесь происходит? Шеф готовит кое-что новое..."
Слайд 2: Показ ингредиентов крупным планом. Текст: "Только свежайшие локальные продукты премиум-качества."
Слайд 3: Готовое блюдо в разрезе. Текст: "Наш новый фирменный бургер/плов готов покорить ваши сердца."
Слайд 4: Отзыв первого дегустатора. Текст: "10 из 10! Такого нежного мяса я еще не пробовал!"
Слайд 5: Стикер опроса/ссылки. Текст: "Хотите попробовать первыми со скидкой 20%? Жмите на стикер!" """,
            "ads": """📢 Таргетированная реклама (3 варианты):
Вариант 1 (Скидка): "Обедайте выгодно! Полноценный сытный бизнес-ланч всего за 35 сомони / 35,000 сум в самом центре города! Успейте заказать!"
Вариант 2 (Боль): "Устали готовить после работы? Мы доставим горячий ароматный ужин прямо к вашей двери за 30 минут! Бесплатная доставка при оплате через Click/Alif!"
Вариант 3 (Креатив): "Устройте романтический вечер, который она запомнит надолго. Изысканная атмосфера, живая музыка и авторские десерты. Бронируйте столик прямо сейчас!" """,
            "funnel": """🎯 Воронка продаж в мессенджере:
Шаг 1 (Лид-магнит): Дарим купон на бесплатный фирменный напиток при первой подписке на чат-бот.
Шаг 2 (Польза): Отправляем секретный рецепт легкого соуса от нашего шеф-повара.
Шаг 3 (Доверие): Показываем видеоэкскурсию по нашей стерильной и современной кухне.
Шаг 4 (Оффер): Ограниченная по времени акция — закажите доставку на сумму от 100 единиц валюты и получите вторую пиццу/порцию в подарок!""",
            "ideas": """💡 30 вирусных идей для контента кафе:
1. Закулисье кухни: как шеф нарезает овощи на скорость.
2. Рубрика "Угадай блюдо по ингредиентам" в комментариях.
3. Видео-сравнение: обычный день гостя vs идеальный день в нашем кафе.
4. Пост-история о том, как зародилась идея открыть это заведение.
5. Интерактивная викторина на знание кулинарных традиций.
6. Челлендж среди подписчиков на самый красивый отзыв.
... и еще 24 уникальные идеи в нашей базе!"""
        },
        "uz": {
            "plan": """📅 Kafelar uchun 7 kunlik mukammal kontent-reja:
1-kun: [Post] Bizning eng mazali milliy taomimiz tarixi. Maqsad: ishonch yaratish.
2-kun: [Stories] So'rovnoma: "Bugun tushlikka nima tanlaysiz — qaynoq palov yoki mazali somsa?"
3-kun: [Reels] Ssenariy: "Toshkentda eng mazali go'sht tayyorlash siri".
4-kun: [Post] Bizning pazandalarimiz va ularning mahorati bilan tanishuv.
5-kun: [Stories] Oshxonaning tozaligi va sterilligi haqida video-tur.
6-kun: [Reels] Mamnun mijozimizning taassurotlari.
7-kun: [Post] Maxsus taklif: Click yoki Payme orqali to'lov qiling va bepul shirinlikka ega bo'ling!""",
            "reels": """🎬 Reels ssenariysi: "Haqiqiy o'zbekona mehmondorchilik"
- Hook (0-3 sek): Qaynoq va ustidan yog' oqib turgan palovni suzish lahzasi. Matn: "Buni ko'rib och qolishingiz aniq..."
- B-roll: Kulib turgan ofitsiant, chiroyli bezatilgan dasturxon, milliy choynakdan quyilayotgan ko'k choy.
- Ovoz: "Mehmondo'stlik bizning qonimizda bor. Har kuni eng yaxshi guruch va yangi go'shtdan foydalanib, sizlar uchun san'at asari yaratamiz."
- CTA: "Bugun oilangiz bilan keling! Direct orqali stol band qiling va bepul non hamda choyga ega bo'ling!"
- Hashtaglar: #palov #toshkent #milliytaomlar #choyxona #uzb""",
            "posts": """🍔 Post: Oilaviy kechki ovqatni unutilmas qiling!
Uyingizda ovqat pishirishga vaqt yo'qmi? Yoki shunchaki shinam muhitda hordiq chiqarmoqchimisiz?
Bizning kafemizda siz xuddi o'z uyingizdagidek issiqlikni va eng yuqori darajadagi xizmatni his qilasiz.

Biz faqat halol va sifatli masalliqlardan foydalanamiz. Bugun kechqurun keling va haqiqiy pazandachilik mo'jizasidan bahramand bo'ling!

📍 Manzilimiz: Toshkent shahri, A. Temur shoh ko'chasi.
📞 Buyurtma va stol band qilish uchun directga yozing!""",
            "stories": """Stories ketma-ketligi (5 ta slayd):
1-slayd: Oshxonadan qaynoq somsa rasmi. Matn: "Ertalabki qaynoq somsa hidini his qilyapsizmi?"
2-slayd: Go'sht to'g'ralishi jarayoni. Matn: "Faqat yangi va halol go'shtdan foydalanamiz."
3-slayd: Ofitsiantlar tayyorgarligi. Matn: "Sizga xizmat qilish biz uchun katta sharaf!"
4-slayd: Mijozlarimiz fikri. Matn: "Toshkentdag'i eng shinam va mazali joy!"
5-slayd: So'rovnoma tugmasi. Matn: "Siz ham bugun kelmoqchimisiz? 'Ha' tugmasini bosing va 10% chegirmaga ega bo'ling!" """,
            "ads": """📢 Target reklama matnlari:
1-variant: "Uydan chiqmasdan mazali taomlardan bahramand bo'ling! Click va Payme orqali oson to'lov va 30 daqiqada tezyurar yetkazib berish!"
2-variant: "Toshkent markazida eng mazali milliy taomlar va shinam choyxona. Do'stlar bilan uchrashuv uchun eng zo'r joy! Stol band qilishga shoshiling!"
3-variant: "Beshbarmak yoki Palov? Qaysi birini ko'proq yoqtirasiz? Bizda ikkalasi ham eng yuqori darajada tayyorlanadi! Kelib o'zingiz baho bering!" """,
            "funnel": """🎯 Sotuv voronkasi (Bot orqali):
1-qadam (Lead-magnet): Telegram botimizga a'zo bo'ling va birinchi buyurtmada bepul kola/choyga ega bo'ling.
2-qadam: Bizning eng ko'p sotiladigan TOP 5 taomimiz haqida qiziqarli ma'lumot.
3-qadam: Mijozlarimizning samimiy video-sharhlari va oshxonamiz videosi.
4-qadam: Maxsus taklif — Click orqali 100,000 so'mdan ko'p buyurtma qilsangiz bepul yetkazish va bonus quponi!""",
            "ideas": """💡 30 ta o'tishli g'oyalar:
1. Qandolatchimiz qanday qilib antiqa tort tayyorlashini ko'rsatish.
2. Kafedagi eng qiziqarli va kulgili holatlar (ofitsiantlar hayotidan).
3. "Nega bizning kabob eng yumshoq?" sirlarini ochish.
4. Mehmonlar bilan qisqa intervyular va kulgili savol-javoblar.
5. Milliy musiqalar ostida chiroyli taomlar taqdimoti.
6. Mijozlarimiz uchun maxsus yutuqli o'yinlar tashkil etish."""
        },
        "tg": {
            "plan": """📅 Нақшаи контенти 7-рӯза барои Кафе ва Ресторан:
Рӯзи 1: [Пост] Таърихи пайдоиши хӯроки асосии мо. Ҳадаф: пайдо кардани боварии мизоҷон.
Рӯзи 2: [Stories] Овоздиҳӣ: "Имрӯз чиро интихоб мекунед — оши палови тару тоза ё курутоби миллӣ?"
Рӯзи 3: [Reels] Видео: "Сирри омода кардани беҳтарин курутоб дар Душанбе".
Рӯзи 4: [Пост] Муаррифии ошпазҳои мо ва маҳорати олии онҳо.
Рӯзи 5: [Stories] Намоиши тозагии ошхона ва риояи тамоми қоидаҳои санитарӣ.
Рӯзи 6: [Reels] Фикри самимии мизоҷони доимии мо пас аз хӯрдани таом.
Рӯзи 7: [Пост] Пешниҳоди махсус: Бо Alif Mobi пардохт кунед ва 15% кэшбэк гиред!""",
            "reels": """🎬 Сценарияи Reels: "Лаззати курутоби ҳақиқии тоҷикӣ"
- Hook (0-3 сек): Рехтани равғани зард ба рӯи курутоби гарм ва бухоршаванда. Матн: "Инро дида бетараф буда наметавонете..."
- B-roll: Нонҳои танӯрии резашуда, чакаи тару тоза, пиёзу кабудиҳо ва чеҳраи хандони мизоҷон.
- Овоз: "Мо курутобро бо риояи тамоми анъанаҳои ниёгон омода мекунем. Ҳар як компонент аз кӯҳсори Тоҷикистон оварда шудааст."
- CTA: "Имрӯз бо оила ё дӯстонатон ба чойхонаи мо биёед! Тавассути Direct мизро банд кунед ва чойи кабуди бепул гиред!"
- Hashtags: #курутоб #палов #душанбе #тоҷикистон #чойхона""",
            "posts": """🍲 Пост: Шоми худро бо наздиконатон дар фазои ором ва лазиз гузаронед!
Оё мехоҳед пас аз як рӯзи кориву хастакунанда истироҳат кунед ва хӯроки бомазза хӯред?
Дар кафеи мо шумо лаззати ҳақиқии хӯрокҳои миллӣ ва аврупоиро дар фазои ниҳоят орому самимӣ ҳис хоҳед кард.

Мо танҳо аз гӯшти ҳалол ва сабзавоти тару тоза истиводе мебарем. Ошпазони соҳибтаҷрибаи мо омодаанд, ки ҳар як хоҳиши кулинарии шуморо иҷро кунанд!

📍 Суроғаи мо: шаҳри Душанбе, хиёбони Рӯдакӣ.
📞 Барои банд кардани миз ба мо занг занед ё дар Direct нависед!""",
            "stories": """Силсилаи Stories (5 слайди прогрев):
Слайд 1: Навори пухтани оши палов дар деги калон. Матн: "Оши палови гарм барои нисфирӯзӣ омода аст!"
Слайд 2: Гӯшти лазиз дар болои оташ. Матн: "Танҳо гӯшти тозаи гӯсфанд ва гов."
Слайд 3: Чорабиниҳо ва хизматрасонии олӣ. Матн: "Омодаем, ки тӯю ҷашнҳои шуморо дар сатҳи олӣ гузаронем."
Слайд 4: Фикри мизоҷон. Матн: "Беҳтарин курутоби шаҳр маҳз дар ҳамин ҷост!"
Слайд 5: Интихоби тугма. Матн: "Имрӯз бо мо мешавед? Бале-ро пахш кунед ва купони туҳфавӣ гиред!" """,
            "ads": """📢 Матнҳои таблиғотӣ (Target):
1-вариант: "Доставкаи фаврии хӯрокҳои гарм дар Душанбе! Пардохти осон бо Alif Mobi ва Душанбе Сити. Фармоиш диҳед ва дар 30 дақиқа қабул кунед!"
2-вариант: "Чойхонаи миллӣ дар маркази Душанбе. Оши палов ва курутоби беҳтарин барои умури оилавӣ ва вохӯрии дӯстон. Мизро пешакӣ банд кунед!"
3-вариант: "Гӯшти реза, шашлики бомазза ва нони танӯрии гарм. Ҳамаи ин дар кафеи мо бо нархҳои ниҳоят дастрас! Биёед ва худатон баҳо диҳед!" """,
            "funnel": """🎯 Воронкаи фурӯш дар бот:
Қадам 1 (Лид-магнит): Ба боти мо аъзо шавед ва дар фармоиши аввал лимонади фирминии бепул ба даст оред.
Қадам 2: Намоиши видео аз тарзи омода кардани хӯрокҳо ва тозагии ошхона.
Қадам 3: Пешниҳоди аксияи махсус барои рӯзҳои таваллуд ва ҷашнҳо бо 15% тахфиф.
Қадам 4: Оффери маҳдуд — Фармоиши болотар аз 150 сомонӣ тавассути бот = интиқоли комилан бепул ва туҳфаи махсус!""",
            "ideas": """💡 30 идеяи ҷолиб барои SMM кафе:
1. Тарзи омода кардани хамири нони миллӣ бо мусиқии зебо.
2. Пурсидани андешаи мизоҷон дар бораи хидматрасонии официантҳо.
3. Видео-шӯхӣ в бораи касоне, ки парҳез доранду боз кабоб мехӯранд.
4. Муқоисаи курутоби Душанбе ва Худҷанд.
5. Рубрикаи "Саволу ҷавоб бо шеф-повар".
6. Намоиши пушти пардаи ошхона ва шӯхиҳои ошпазҳо."""
        }
    },
    "beauty": {
        "icon": "💇‍♀️",
        "name_ru": "Салоны красоты",
        "name_uz": "Go'zallik salonlari",
        "name_tg": "Салонҳои ҳусн",
        "ru": {
            "plan": """📅 План для Салона красоты:
День 1: [Пост] Развенчание мифов о домашнем уходе за волосами.
День 2: [Stories] Опрос: "Как часто вы делаете маникюр?"
День 3: [Reels] До/После преображения клиентки (WOW-эффект).
День 4: [Пост] Знакомство с топ-стилистом салона и его работами.
День 5: [Stories] Процесс стерилизации инструментов (безопасность).
День 6: [Reels] Быстрый туториал по укладке дома за 5 минут.
День 7: [Пост] Оффер: Скидка 20% на первое посещение.""",
            "reels": """🎬 Сценарий Reels: "Преображение, которое меняет жизнь"
- Хук (0-3 сек): Уставшая девушка сидит в кресле без макияжа. Текст: "Она пришла к нам с грустными глазами, а ушла..."
- B-roll: Ускоренное видео работы мастера (макияж, стрижка, укладка), искренний смех, кофе в красивой чашке.
- Голос: "Мы верим, что красота спасает мир. В нашем салоне мы не просто делаем процедуры — мы возвращаем уверенность и любовь к себе."
- CTA: "Запишитесь на преображение сегодня через директ и получите уход для волос в подарок!"
- Хэштеги: #салонкрасоты #макияж #укладка #маникюр""",
            "posts": """💅 Пост: Здоровые волосы — это не генетика, а правильный уход!
Часто мы тратим огромные суммы на дорогие шампуни, но не видим результата. Почему?
Секрет кроется в профессиональной диагностике кожи головы и структуры волос. В нашем салоне стилисты подберут индивидуальную программу восстановления именно для вас.

Позвольте себе расслабиться в руках профессионалов, выпить чашечку ароматного кофе и выйти от нас королевой!

📍 Ждем вас по адресу: центр города.
📞 Онлайн запись в шапке профиля или директ.""",
            "stories": """Серия Stories:
Слайд 1: Крупный план тусклых волос. Текст: "Устали от секущихся кончиков и сухости?"
Слайд 2: Мастер наносит маску премиум-бренда. Текст: "Используем только люксовые швейцарские/корейские уходы."
Слайд 3: Невероятный блеск волос на солнце после процедуры. Текст: "Вот он — зеркальный блеск и сила!"
Слайд 4: Счастливая улыбка клиентки. Текст: "Эффект держится до 3 месяцев!"
Слайд 5: Окошко записи. Текст: "Осталось всего 3 свободных места на этой неделе. Успейте записаться!" """,
            "ads": """📢 Таргет реклама:
1: "Идеальный маникюр, который держится 4 недели без сколов! Запишитесь прямо сейчас и получите дизайн двух пальчиков бесплатно!"
2: "Время побаловать себя! Комплекс 'Стрижка + Окрашивание + Уход' со скидкой 25% только до конца недели. Ваша красота в надежных руках!"
3: "Хотите сиять на любом мероприятии? Профессиональный макияж и укладка в 4 руки всего за 60 минут! Успейте забронировать время!" """,
            "funnel": """🎯 Воронка продаж:
Шаг 1: Дарим гайд "Топ-10 ошибок в домашнем уходе" за подписку.
Шаг 2: Присылаем видео-тест для определения типа кожи/волос.
Шаг 3: Показываем отзывы и фото работ наших мастеров.
Шаг 4: Дарим персональный купон на скидку 15% на любую процедуру при записи в течение 24 часов.""",
            "ideas": """💡 30 идей для Салона красоты:
1. Video "Один день из жизни администратора салона".
2. Разбор составов дешевой и дорогой косметики.
3. Интерактив: "Угадайте, какая процедура была сделана на фото".
4. Рубрика "Вредные советы от мастера" (с юмором).
5. Пост о трендах маникюра и дизайна ногтей на сезон.
6. Челлендж по преображению мамы/подруги."""
        },
        "uz": {
            "plan": """📅 Go'zallik salonlari uchun 7 kunlik reja:
1-kun: [Post] Sochlarni uyda noto'g'ri parvarish qilish oqibatlari.
2-kun: [Stories] So'rovnoma: "Qanday soch turmagini afzal ko'rasiz?"
3-kun: [Reels] Mijozimizning o'zgarishi (WOW-effekt).
4-kun: [Post] Salonimiz yetakchi stilisti bilan suhbat.
5-kun: [Stories] Asboblarni sterilizatsiya qilish va gigiyena jarayoni.
6-kun: [Reels] Uyda tezkor makiyaj qilish sirlari.
7-kun: [Post] Taklif: Birinchi tashrif uchun 15% chegirma.""",
            "reels": """🎬 Reels ssenariysi: "O'zingizga ishonchni qaytaring!"
- Hook (0-3 sek): Qiz sochini ushlab xafa bo'lib o'tiribdi. Matn: "Sochlaringiz jonsiz bo'lib qoldimi?"
- B-roll: Stilistning sochni yuvishi, professional parvarish qo'llashi, chiroyli fen qilish jarayoni va qizning porlab turgan ko'zlari.
- Ovoz: "Har bir ayol go'zal va takrorlanmas. Biz sizning tabiiy go'zalligingizni ochib berishga yordam beramiz."
- CTA: "Bugun ro'yxatdan o'ting va bepul maslahat hamda sovg'aga ega bo'ling!"
- Hashtaglar: #salon #gozallik #toshkent #sochparvarishi""",
            "posts": """💇‍♀️ Post: Go'zallik va parvarish professional qo'llarda!
Sochlaringiz va teringiz eng yaxshi parvarishga loyiq. Noto'g'ri tanlangan kosmetika muammolarni battar chuqurlashtirishi mumkin.
Bizning go'zallik salonimizda har bir mijozga individual yondashuv kafolatlanadi.

Kelib dam oling va o'zingizni haqiqiy malikadek his qiling!

📍 Manzil: Toshkent markazi.
📞 Ro'yxatdan o'tish uchun directga yozing yoki profil havolasidan foydalaning.""",
            "stories": """Stories ketma-ketligi:
1-slayd: Noto'g'ri makiyaj rasmi. Matn: "Bu xatolarga yo'l qo'ymang!"
2-slayd: Bizning master ishi. Matn: "Professional vizajistimiz sizga eng mos obrazni tanlaydi."
3-slayd: Tayyor chiroyli obraz. Matn: "Tabiiy va jozibador ko'rinish!"
4-slayd: Sifat kafolati. Matn: "Faqat brend kosmetikalar (Dior, Estee Lauder)."
5-slayd: Chegirmali ro'yxatdan o'tish tugmasi. Matn: "10% chegirma bilan yozilish uchun 'SMM' deb yozing!" """,
            "ads": """📢 Target reklamalari:
1: "Toshkentda eng sifatli soch laminatsiyasi! Birinchi marta kelgan mijozlar uchun soch parvarishlovchi sprey sovg'a qilinadi!"
2: "Siz orzu qilgan tirnoq dizayni va mukammal manikyur. 3 hafta davomida buzilmasdan saqlanishiga kafolat beramiz!"
3: "Yuz teringizni yoshartirish va tozalash sirlari. Professional kosmetologlarimiz xizmanidan chegirma bilan foydalaning!" """,
            "funnel": """🎯 Sotuv voronkasi:
1-qadam: Uy sharoitida sochni parvarish qilish bo'yicha bepul darslik/qo'llanma taqdim etiladi.
2-qadam: Soch holatini aniqlash uchun bot orqali kichik test.
3-qadam: Masterlarimiz ishlari va mijozlar hursandchiligi aks etgan videolar.
4-qadam: Maxsus aksiya — Click/Payme orqali oldindan to'lov qilsangiz, bepul yuz massaji sovg'a!""",
            "ideas": """💡 30 ta SMM g'oya:
1. "Mening kosmetichkam" — masterlarning shaxsiy sevimli vositalari.
2. Sochni to'g'ri tarash bo'yicha master-klass.
3. Salon ichidagi eng quvnoq trend videolar.
4. "Mijozning eng g'alati iltimosi" (kulgi bilan).
5. Kosmetik vositalarning yaroqlilik muddatini tekshirish usuli.
6. Tirnoqlar salomatligi uchun muhim tavsiyalar."""
        },
        "tg": {
            "plan": """📅 Нақшаи 7-рӯза барои Салони ҳусн:
Рӯзи 1: [Пост] Хатогиҳои маъмул дар нигоҳубини мӯй дар хона.
Рӯзи 2: [Stories] Овоздиҳӣ: "Оё шумо маникюри оддиро дӯст медоред ё бо дизайн?"
Рӯзи 3: [Reels] Тағйирёбии аҷиби мӯи мизоҷ (WOW-эффект).
Рӯзи 4: [Пост] Муаррифии стилисти пешсафи салони мо.
Рӯзи 5: [Stories] Чӣ тавр мо асбобҳоро стерилизатсия ва безарар мегардонем.
Рӯзи 6: [Reels] Тарзи ороиши мӯй барои ҷашнҳо дар 10 дақиқа.
Рӯзи 7: [Пост] Оффер: Нависед ва 20% тахфиф ба процедураи аввалин гиред!""",
            "reels": """🎬 Сценарияи Reels: "Дурахши ҳақиқии мӯйҳои шумо"
- Hook (0-3 сек): Мӯйҳои хушку беҷон дар шамол. Матн: "Оё мӯйҳоятон зебоии худро гум кардаанд?"
- B-roll: Стилист ниқоби касбӣ мемолад, истифодаи таҷҳизоти муосир, мӯйҳои дурахшону абрешимӣ пас аз хушконидан.
- Овоз: "Мӯйҳои зебо — ин нишонаи муҳаббат ба худ аст. Дар салони мо мо ба ҳар як тори мӯи шумо ҳаёти нав мебахшем."
- CTA: "Барои барқарорсозии мӯйҳо тавассути Direct худи ҳозир сабти ном кунед ва кэшбэк гиред!"
- Hashtags: #салониҳусн #душанбе #мӯй #маникюр #ороиш""",
            "posts": """💅 Пост: Зебоии шумо — илҳоми мост!
Салони ҳусни мо шуморо ба олами зебоӣ ва нигоҳубини касбӣ даъват мекунад. Мо медонем, ки чӣ тавр зебоии табиии шуморо таъкид кунем ва ба шумо оромиву эътимод бахшем.

Устодони соҳибтаҷрибаи мо танҳо бо брендҳои машҳури ҷаҳонӣ кор мекунанд. Барои шумо тамоми шароитҳо муҳайёст: қаҳваи болаззат, мусиқии форам ва хидматрасонии дараҷаи олӣ.

📍 Суроға: маркази шаҳри Душанбе.
📞 Барои сабт шудан ба мо дар Direct нависед ё занг занед!""",
            "stories": """Силсилаи Stories:
Слайд 1: Намоиши мӯйҳои беҷон. Матн: "Оё мехоҳед мӯйҳоятон мисли ситораҳои синамо дурахшанд?"
Слайд 2: Раванди ботокс ва кератини мӯй. Матн: "Танҳо маводҳои босифати Олмон ва Бразилия."
Слайд 3: Натиҷаи дурахшони кор. Матн: "Мӯйҳои комилан солим ва ҳамвор!"
Слайд 4: Табассуми зебои мизоҷ. Матн: "Зебоӣ ва сифати кафолатдодашуда."
Слайд 5: Сабти ном. Матн: "Танҳо барои 5 нафари аввал, ки 'ҲУСН' менависанд, тахфифи 15% фаъол мешавад!" """,
            "ads": """📢 Таблиғоти ҳадафнок (Target):
1: "Беҳтарин маникюр ва педикюр дар Душанбе! Кафолати сифат то 4 ҳафта. Барои процедураи аввал ороиши нохун туҳфа дода мешавад!"
2: "Мӯйҳои худро бо усулҳои нави спа-нигоҳубин ҷонбахш кунед. Танҳо ин ҳафта бо тахфифи 20%! Худи ҳозир нависед!"
3: "Ороиши мӯй ва ороиши чеҳра (макияж) дар 4 даст дар як вақт! Вақти худро сарфа кунед ва беҳтарин бошед!" """,
            "funnel": """🎯 Воронкаи фурӯш дар бот:
Қадам 1: Пешниҳоди дастури ройгон (гайд) в бораи нигоҳубини дурусти пӯст дар фасли тобистон.
Қадам 2: Санҷиши хурд (тест) дар бот барои муайян кардани сохтори мӯй.
Қадам 3: Нишон додани видеоҳои "Пеш ва Пас" ва муваффақиятҳои устодони мо.
Қ'адам 4: Кӯпони махсус бо 15% тахфиф ҳангоми пардохт тавассути Alif Mobi!""",
            "ideas": """💡 30 идеяи олӣ:
1. Навори кӯтоҳи "Пеш ва Пас" барои маникюр.
2. Маслиҳатҳои дерматолог дар бораи шустани дурусти рӯй.
3. Шӯхиҳои занона дар бораи рафтан ба салон ба ҷои кор.
4. "Интихоби ранги мӯй мувофиқи ранги чашм".
5. Чӣ тавр дар хона мӯйро дуруст хушк кунем.
6. Челлендж бо устодони салон: кӣ зудтар ороиши мӯй мекунад."""
        }
    },
    "shop": {
        "icon": "👗",
        "name_ru": "Магазины одежды",
        "name_uz": "Kiyim do'konlari",
        "name_tg": "Мағозаҳои либос",
        "ru": {
            "plan": """📅 План для Магазина одежды:
День 1: [Пост] Тренды этого сезона: как сочетать базовые вещи.
День 2: [Stories] Игра-опрос: "Какой лук выберете вы — Casual или Classic?"
День 3: [Reels] Примерка 5 стильных образов для офиса и прогулок.
День 4: [Пост] Качество материалов: почему наш хлопок/шелк не скатывается.
День 5: [Stories] Распаковка новой коллекции (живые эмоции байера).
День 6: [Reels] Вирусный переход со сменой одежды под трендовую музыку.
День 7: [Пост] Оффер: Бесплатная доставка по всей стране.""",
            "reels": """🎬 Сценарий Reels: "Твой идеальный гардероб"
- Хук (0-3 сек): Девушка стоит перед полным шкафом и вздыхает: "Опять нечего надеть..." Текст на экране: "Знакомо?"
- B-roll: Динамичная смена 3 потрясающих образов с помощью переходов (щелчок пальцев, прыжок). Одежда сидит идеально, подчеркивая достоинства.
- Голос: "Забудьте о часах раздумий перед зеркалом. Мы создали коллекцию, где каждая вещь идеально сочетается друг с другом. Стиль — это просто."
- CTA: "Напишите 'ХОЧУ' в комментариях, и наш стилист бесплатно подберет для вас готовый образ со скидкой 10%!"
- Хэштеги: #стиль #мода #магазиходежды #гардероб #тренды""",
            "posts": """👗 Пост: Капсульный гардероб: минимум вещей — максимум стиля!
У вас полный шкаф одежды, но вы всё равно носите одно и то же?
Решение — капсульный гардероб. Это набор из 6-8 базовых вещей, которые легко сочетаются между собой, создавая более 20 уникальных образов.

В нашей новой коллекции представлены идеальные базовые футболки, оверсайз жакеты и брюки идеальной посадки. Все вещи выполнены из премиальных натуральных тканей.

📍 Приходите на примерку: ТЦ Плаза, 2 этаж.
📞 Заказ онлайн с доставкой до двери!""",
            "stories": """Серия Stories:
Слайд 1: Распаковка коробки с бантом. Текст: "Она наконец-то приехала! Наша долгожданная коллекция!"
Слайд 2: Детали ткани крупным планом. Текст: "Посмотрите на эти швы и невероятно мягкий итальянский лен."
Слайд 3: Модель примеряет костюм. Текст: "Идеально садится на любую фигуру благодаря лекалам премиум-класса."
Слайд 4: Таблица размеров и цветов. Текст: "Доступно в 5 пастельных оттенках. Размеры от XS до XXL."
Слайд 5: Форма заказа. Текст: "Количество ограничено! Напишите в директ прямо сейчас для заказа с бесплатной примеркой!" """,
            "ads": """📢 Таргет реклама:
1: "Соберите идеальный гардероб со скидкой 30%! Премиальное качество по доступным ценам. Переходите в каталог!"
2: "Надоело покупать вещи, которые лежат без дела? Наш стилист бесплатно подберет капсулу под ваши параметры. Пишите в директ!"
3: "Шикарные платья из натурального шелка, в которых вы будете неотразимы. Доставка за 1 день и примерка перед покупкой!" """,
            "funnel": """🎯 Воронка продаж:
Шаг 1: Дарим лукбук "Топ-20 стильных образов на этот сезон" за подписку на аккаунт.
Шаг 2: Отправляем интерактивный тест на определение вашего цветотипа.
Шаг 3: Показываем видео-отзывы реальных покупателей с демонстрацией посадки одежды.
Шаг 4: Дарим промокод на скидку 15% на первый заказ в течение 48 часов с бесплатной доставкой.""",
            "ideas": """💡 30 идей для Магазина одежды:
1. "Ожидание vs Реальность" при примерке одежды.
2. Лайфхаки: как красиво завязать пояс или заправить рубашку.
3. Видео "Один костюм — 3 разных стиля" (спорт, офис, вечер).
4. История бренда или как создавалась коллекция.
5. Разбор гардероба известной киногероини.
6. Опрос: "Какой цвет этой модели вам нравится больше?" """
        },
        "uz": {
            "plan": """📅 Kiyim do'konlari uchun 7 kunlik reja:
1-kun: [Post] Mavsum trendlari: kiyimlarni qanday to'g'ri moslashtirish kerak.
2-kun: [Stories] Interaktiv o'yin: "Qaysi obraz sizga ko'proq yoqadi?"
3-kun: [Reels] Ofis va kundalik hayot uchun 5 ta chiroyli obraz taqdimoti.
4-kun: [Post] Mato sifati: nega bizning trikotaj mahsulotlarimiz cho'zilmaydi.
5-kun: [Stories] Yangi kolleksiyani ochish jarayoni (Unboxing).
6-kun: [Reels] Musiqa ostida tezkor kiyim almashtirish videosi.
7-kun: [Post] Maxsus taklif: O'zbekiston bo'ylab bepul yetkazib berish!""",
            "reels": """🎬 Reels ssenariysi: "Mukammal kiyinish sirlari"
- Hook (0-3 sek): Qiz garderob oldida xafa bo'lib turibdi: "Kiyishga hech narsa yo'q..." Matn: "Sizda ham shunday bo'ladimi?"
- B-roll: Qizning 3 xil zamonaviy va yorqin kiyimlarni kiyib ko'rsatishi, ishonchli qadamlar, kiyimlarning chiroyli yarashi.
- Ovoz: "Endi soatlab kiyim tanlashga hojat yo'q. Biz bir-biriga mukammal mos tushadigan kapsula kolleksiyasini yaratdik."
- CTA: "Directga 'KIYIM' deb yozing va bepul stilist maslahati hamda 10% chegirmaga ega bo'ling!"
- Hashtaglar: #moda #kiyimlar #toshkent #do'kon #uzb""",
            "posts": """👗 Post: Minimalizm va uslub — kam kiyim, ko'p obraz!
Shkafingiz to'la kiyim, lekin kiyishga kelganda qiynalasizmi?
Sizga kapsula garderobi yordam beradi. Bu bir-biri bilan oson moslashadigan 6-8 ta sifatli kiyimlar to'plamidir.

Yangi kolleksiyamizda eng yuqori sifatli tabiiy matolardan tikilgan liboslar taqdim etilgan. Ular sizga nafaqat go'zallik, balki qulaylik ham baxsh etadi.

📍 Manzilimiz: Toshkent sh., "Mega Planet" Savdo Markazi.
📞 Buyurtma bering, uyingizda kiyib ko'rib keyin to'lov qiling!""",
            "stories": """Stories ketma-ketligi:
1-slayd: Premium quti ochilishi. Matn: "Nihoyat yangi kolleksiyamiz yetib keldi!"
2-slayd: Mato sifati yaqindan. Matn: "100% tabiiy paxta va i'pak, Turkiyada ishlab chiqarilgan."
3-slayd: Model kiyimda. Matn: "Har qanday qomatga mukammal o'tiradi."
4-slayd: Ranglar tanlovi. Matn: "Ushbu mavsumning eng urf bo'lgan ranglari."
5-slayd: Buyurtma berish havolasi. Matn: "Cheklangan miqdorda! Hoziroq directga yozing va bepul yetkazib berishga ega bo'ling!" """,
            "ads": """📢 Target reklamalari:
1: "Mavsumning eng zamonaviy kiyimlari 30% chegirma bilan! Premium sifat va hamyonbop narxlar. Katalogni ko'rish!"
2: "Sizga qaysi uslub mos keladi? Directga yozing, stilistimiz bepul kiyimlar jamlanmasini yig'ib beradi!"
3: "Turkiyaning eng sifatli matolaridan tikilgan liboslar do'koni. Click/Payme orqali to'lov qiling va sovg'aga ega bo'ling!" """,
            "funnel": """🎯 Sotuv voronkasi:
1-qadam: "Bu yilgi eng zamonaviy 10 ta obraz" nomli bepul elektron jurnal/giyb taqdim etiladi.
2-qadam: Foydalanuvchining bo'yi va vazniga qarab mos kiyimlarni tanlash testi.
3-qadam: Mijozlarimizning kiyimlardagi suratlari va samimiy fikrlari.
4-qadam: 48 soat ichida buyurtma bersa bepul yetkazish va keyingi xarid uchun 15% chegirma quponi.""",
            "ideas": """💡 30 ta o'tishli g'oyalar:
1. "Arzon vs Qimmat" kiyimlarning ko'rinishi va sifati.
2. Sharfni chiroyli bog'lashning 3 xil usuli.
3. Do'konimizda bir kunlik ish jarayoni va qiziqarli lahzalar.
4. "Garderobingizdagi eng keraksiz 3 ta narsa".
5. Kiyimlarni qanday yuvish va parvarish qilish bo'yicha tavsiyalar.
6. Obunachilar o'rtasida eng yaxshi obraz uchun ovoz berish o'yini."""
        },
        "tg": {
            "plan": """📅 Нақшаи контенти 7-рӯза барои Мағозаи либос:
Рӯзи 1: [Пост] Трендҳои ин фасл: чӣ тавр либосҳоро зебо ҳамоҳанг кунем.
Рӯзи 2: [Stories] Бозии "Кадом либосро интихоб мекунед?" барои фаъол кардани аудитория.
Рӯзи 3: [Reels] Намоиши 5 образи зебо барои идора ва гардиш.
Рӯзи 4: [Пост] Сифати матоъ: чаро либосҳои мо пас аз шустан сифати худро гум намекунанд.
Рӯзи 5: [Stories] Раванди қабули коллексияи нави ва кушодани қуттиҳо.
Рӯзи 6: [Reels] Навори кӯтоҳи иваз кардани либосҳо бо гузаришҳои ҷолиб.
Рӯзи 7: [Пост] Пешниҳод: Интиқоли ройгон дар тамоми қаламрави Тоҷикистон.""",
            "reels": """🎬 Сценарияи Reels: "Услуби беназири ту"
- Hook (0-3 сек): Духтар дар назорати гардероб истодааст ва бо нигаронӣ мегӯяд: "Боз либоси муносиб надорам..." Матн: "Шумо ҳам инро ҳис мекунед?"
- B-roll: Ивазшавии тези 3 образи замонавӣ бо гузариши зебо. Либосҳо ниҳоят шикам ва баданро зебо нишон медиҳанд.
- Овоз: "Вақти худро барои интихоби либос зоеъ накунед. Мо коллексияе омода кардем, ки ҳар як ҷузъи он бо ҳамдигар мувофиқ аст. Зебоӣ осон аст."
- CTA: "Дар Direct калимаи 'ЛИБОС'-ро нависед ва аз стилисти мо маслиҳати бепул ва 10% тахфиф гиред!"
- Hashtags: #мода #либос #душанбе #тоҷикистон #стил""",
            "posts": """👗 Пост: Гардероби капсулӣ: либоси камтар — услуби бештар!
Оё гардероби шумо пур аз либос аст, вале боз ҳам ҳамон як либосро мепӯшед?
Роҳи ҳал — гардероби капсулист. Ин маҷмӯи 6-8 либоси асосӣ аст, ки ба осонӣ бо ҳам пайваст шуда, зиёда аз 20 образи беназир месозанд.

Дар коллексияи нави мо либосҳо аз матоъҳои табиӣ ва босифат пешниҳод шудаанд, ки ба шумо роҳат ва услуби хос мебахшанд.

📍 Суроғаи мо: шаҳри Душанбе, Маркази Савдои "Садбарг", ошёнаи 2.
📞 Фармоиши онлайн бо интиқоли зуд то дари хона!""",
            "stories": """Силсилаи Stories:
Слайд 1: Кушодани қуттии брендӣ бо тасмаи сурх. Матн: "Инҷо коллексияи нави мост, ки ниҳоят расид!"
Слайд 2: Намоиши матоъ аз наздик. Матн: "Лин ва пахтаи 100% табиии истеҳсоли Туркия."
Слайд 3: Модел либосро мепӯшад. Матн: "Ба ҳар як қомат зебо ва мувофиқ меистад."
Слайд 4: Намудҳои ранг ва андозаҳо. Матн: "Аз андозаи XS то XXL мавҷуд аст."
Слайд 5: Сабти фармоиш. Матн: "Миқдор маҳдуд аст! Барои фармоиш бо интиқоли ройгон худи ҳозир ба Direct нависед!" """,
            "ads": """📢 Таблиғоти ҳадафнок:
1: "Коллексияи нави либосҳои брендии Туркия бо тахфифи 25%! Сифати олӣ бо нархҳои дастрас. Барои дидани каталог пахш кунед!"
2: "Кадом услуб ба шумо бештар мувофиқ аст? Дар Direct нависед, стилисти мо ба таври ройгон капсулаи либосро барои шумо омода мекунад!"
3: "Либосҳои шево ва шинам барои шоҳдухтарони тоҷик. Интиқоли зуд ва пардохт тавассути Alif Mobi/Душанбе Сити!" """,
            "funnel": """🎯 Воронкаи фурӯш дар бот:
Қадам 1: Пешниҳоди лукбуки ройгони "20 образи беҳтарини фасл" барои обуна шудан ба саҳифа.
Қадам 2: Санҷиши ҷолиб дар бот барои муайян кардани услуби либоспӯшии шумо.
Қадам 3: Нишон додани видеоҳои воқеии мизоҷон дар либосҳои мо ва изҳори миннатдории онҳо.
Қадам 4: Промокоди махсус бо 15% тахфиф ба фармоиши аввал бо шарти харид дар давоми 24 соат.""",
            "ideas": """💡 30 идеяи олӣ:
1. Муқоисаи либосҳо: "Барои кор ва барои вохӯрии шом".
2. Лайфхак: чӣ тавр остинҳои куртаро зебо бардорем.
3. Рӯзи кории фурӯшандаи мағозаи мо (бо юмор).
4. "Чӣ тавр либосро интихоб кунем, ки ҷавонтар намоем".
5. Муайян кардани сифати матоъ ҳангоми харид.
6. Пурсиш дар бораи ранги дӯстдоштаи либос дар байни обуначиён."""
        }
    },
    "auto": {
        "icon": "🚗",
        "name_ru": "Автосервисы и Автосалоны",
        "name_uz": "Avtoservis va Salonlar",
        "name_tg": "Автосервис ва Мошинҳо",
        "ru": {
            "plan": """📅 План для Автобизнеса на 7 дней:
День 1: [Пост] 5 признаков того, что пора проверить тормоза.
День 2: [Stories] Викторина: "Что означает этот значок на панели?"
День 3: [Reels] Процесс качественного развал-схождения на 3D стенде.
День 4: [Пост] Почему нельзя заливать дешевое моторное масло.
День 5: [Stories] Показываем жизнь мастеров в автосервисе (честный бэкстейдж).
День 6: [Reels] Видео-лайфхак: Как продлить срок службы кондиционера.
День 7: [Пост] Реклама: Пройдите полную диагностику подвески по супер-цене!""",
            "reels": """🎬 Сценарий Reels: "Тихий убийца твоего мотора"
- Хук (0-3 сек): Мастер держит в руках черный, полностью забитый масляный фильтр. Текст: "Если вы не делали это вовремя, готовьте деньги..."
- B-roll: Слив старого черного масла, заливка нового чистого золотистого масла, улыбающийся мастер закручивает детали.
- Голос: "Многие думают, что замена масла — это просто формальность. Но просрочка даже на 2000 км медленно убивает ваш двигатель изнутри. Экономия на фильтре сегодня оборачивается капитальным ремонтом завтра."
- CTA: "Запишитесь на замену масла прямо сейчас через директ и получите бесплатную диагностику ходовой части!"
- Хэштеги: #автосервис #ремонтмотора #заменамасла #ходовая #авто""",
            "posts": """🚗 Пост: Почему горит Check Engine и что делать?
Этот значок на приборной панели заставляет нервничать любого водителя. Означает ли это мгновенную поломку?
Не всегда. Причиной может быть как банальная негерметичность топливной системы, так и серьезный сбой в датчиках двигателя.

Главное — не игнорировать сигнал. Своевременное чтение ошибок на профессиональном сканере поможет избежать дорогостоящего ремонта.

📍 Наш автосервис оборудован самым современным диагностическим оборудованием.
📞 Напишите нам для записи на быструю диагностику!""",
            "stories": """Серия Stories:
Слайд 1: Фото датчика Check Engine. Текст: "Опять загорелся? Не паникуйте!"
Слайд 2: Наш диагност подключает сканер. Текст: "Наш мастер определит точную причину за 10 минут."
Слайд 3: Процесс исправления неполадки. Текст: "Быстро устраняем проблему и сбрасываем ошибку."
Слайд 4: Инструменты и сертифицированные запчасти. Текст: "Все необходимые детали в наличии на нашем складе."
Слайд 5: Окошко записи. Текст: "Запишитесь на диагностику сегодня со скидкой 50%!" """,
            "ads": """📢 Таргет реклама:
1: "Подготовьте свой автомобиль к сезону! Комплексная диагностика по 15 пунктам всего за 100 сомони / 100,000 сум! Звоните!"
2: "Стук в подвеске? Не откладывайте безопасность на потом. Запишитесь на ремонт сегодня и получите гарантию 6 месяцев!"
3: "Профессиональный детейлинг и полировка фар. Сделайте ваш автомобиль снова новым за 1 день! Пишите в директ!" """,
            "funnel": """🎯 Воронка продаж:
Шаг 1: Чек-лист "Что проверить в машине перед дальней поездкой" за подписку.
Шаг 2: Интерактивный калькулятор стоимости ТО в чат-боте.
Шаг 3: Видео-советы от шеф-механика о правильной эксплуатации автомобиля.
Шаг 4: Специальный купон на бесплатную замену тормозных колодок при их покупке у нас.""",
            "ideas": """💡 30 идей для автотемы:
1. Как правильно проверить уровень масла самому.
2. Топ-5 глупых ошибок водителей зимой/летом.
3. Обзор цен на авторынке (Сергели/Корвон).
4. История редкого и интересного автомобиля, который приехал на ремонт.
5. Мифы об экономии топлива: что работает, а что нет.
6. Интерактив: "Угадайте деталь автомобиля по звуку"."""
        },
        "uz": {
            "plan": """📅 Avtoservis uchun 7 kunlik reja:
1-kun: [Post] Tormoz tizimini tekshirish kerakligini ko'rsatuvchi 5 ta belgi.
2-kun: [Stories] Viktorina: "Ushbu belgi panelda nimani anglatadi?"
3-kun: [Reels] 3D stendda g'ildiraklarni sozlash jarayoni.
4-kun: [Post] Sifatsiz motor moyi ishlatish oqibatlari.
5-kun: [Stories] Avtoservisimiz ustalarining ish jarayoni (jonli video).
6-kun: [Reels] Avtomobil konditsionerini to'g'ri ishlatish qoidalari.
7-kun: [Post] Taklif: To'liq diagnostika va tormoz nazorati chegirma bilan!""",
            "reels": """🎬 Reels ssenariysi: "Dvigatelingiz dushmani"
- Hook (0-3 sek): Usta qora va butkul tiqilib qolgan moy filtrini ushlab turibdi. Matn: "Buni o'z vaqtida almashtirmasangiz, katta xarajatga tayyor turing..."
- B-roll: Eski qora moyning oqishi, oltindek toza yangi moy quyilishi, usta detallarni mahkamlayotgani.
- Ovoz: "Moy almashtirish shunchaki oddiy ish emas. Uni kechiktirish dvigatelingizni asta-sekin ich-ichidan yemiradi. Filtrdan tejalgan pul ertaga katta kapital remontga olib keladi."
- CTA: "Directga yozing, moy almashtirishga yoziling va xodovoy qismini bepul tekshirtiring!"
- Hashtaglar: #avto #avtoservis #toshkent #chevrolet #cobalt""",
            "posts": """🚗 Post: Nega Check Engine chirog'i yonadi va nima qilish kerak?
Panelda ushbu belgining paydo bo'lishi har qanday haydovchini xavotirga soladi. Bu mashina butkul buzilganini anglatadimi?
Yo'q, har doim ham emas. Sababi oddiy yoqilg'i qopqog'ining yaxshi yopilmaganidan tortib, datchiklardagi jiddiy muammolargacha bo'lishi mumkin.

Eng muhimi — bunga befarq bo'lmaslik. Professional kompyuter diagnostikasi muammoni tez aniqlaydi.

📍 Avtoservisimiz eng zamonaviy uskunalar bilan jihozlangan.
📞 Diagnostikaga yozilish uchun profil havolasiga o'ting yoki directga yozing!""",
            "stories": """Stories ketma-ketligi:
1-slayd: Check Engine belgisi rasmi. Matn: "Chiroq yondimi? Havotirga o'rin yo'q!"
2-slayd: Usta skanerni ulamoqda. Matn: "Professional diagnostikachimiz 10 daqiqada sababini aniqlaydi."
3-slayd: Muammoni bartaraf etish. Matn: "Xatoliklarni tezda tuzatamiz va o'chirib beramiz."
4-slayd: Sifatli ehtiyot qismlar. Matn: "Barcha kerakli detallar o'zimizda bor."
5-slayd: Yozilish tugmasi. Matn: "Bugun ro'yxatdan o'ting va 50% chegirmaga ega bo'ling!" """,
            "ads": """📢 Target reklamalari:
1: "Chevrolet Cobalt va Gentra uchun eng sifatli texnik xizmat ko'rsatish! Click/Payme orqali to'lov qiling va bonusga ega bo'ling!"
2: "Xodovoy qismida shovqin bormi? Xavfsizlikni kechiktirmang. Bugun keling va 6 oylik kafolatga ega bo'ling!"
3: "Avtomobilingizni porlatib beramiz! Professional polirovka va kimyoviy tozalash xizmatlari faqat bizda!" """,
            "funnel": """🎯 Sotuv voronkasi:
1-qadam: "Safar oldidan avtomobilni tekshirish qoidalari" bepul yo'riqnomasi.
2-qadam: Avtomobil rusumi va yurgan masofasiga qarab xizmat narxini hisoblovchi bot bo'limi.
3-qadam: Bosh ustamizdan foydali maslahat videolari.
4-qadam: Bizdan tormoz kolodkalarini sotib olgan mijozlarga uni bepul o'rnatib berish aksiyasi.""",
            "ideas": """💡 30 ta o'tishli g'oyalar:
1. Motor moyi darajasini qanday to'g'ri tekshirish kerak.
2. Haydovchilarning yoz/qish mavsumidagi eng katta 5 xatosi.
3. Sergeli avtobozoridagi narxlar sharhi.
4. Bizga kelgan qiziqarli va noyob mashina videosi.
5. Yoqilg'ini tejash bo'yicha haqiqat va afsonalar.
6. Tirnoq va shinalarni qachon almashtirish kerakligi haqida maslahat."""
        },
        "tg": {
            "plan": """📅 Нақшаи 7-рӯза барои Автосервис:
Рӯзи 1: [Пост] 5 аломате, ки нишон медиҳанд вақти тафтиши тормозҳо расидааст.
Рӯзи 2: [Stories] Викторина: "Ин нишона дар панели мошин чиро мефаҳмонад?"
Рӯзи 3: [Reels] Раванди танзими чархҳо (развал-схождение) дар таҷҳизоти 3D.
Рӯзи 4: [Пост] Чаро набояд равғани арзон ва бесифатро ба муҳаррик рехт.
Рӯзи 5: [Stories] Намоиши лаҳзаҳои кории устоҳо дар автосервиси мо.
Рӯзи 6: [Reels] Маслиҳати муфид: Чӣ тавр ҳаёти кондитсионери мошинро дароз кунем.
Рӯзи 7: [Пост] Аксия: Ташхиси пурраи қисмҳои ҳаракаткунандаи мошин бо нархи махсус!""",
            "reels": """🎬 Сценарияи Reels: "Қотилони хомӯши муҳаррики мошин"
- Hook (0-3 сек): Усто филтри равғани ниҳоят ифлос ва сиёҳро нишон медиҳад. Матн: "Агар инро сари вақт иваз накунед, пули калон омода кунед..."
- B-roll: Рехтани равғани сиёҳ, рехтани равғани нави тиллоӣ ва тоза, маҳкам кардани қисмҳо аз ҷониби усто.
- Овоз: "Бисёриҳо фикр мекунанд, ки ивази равған чизи оддист. Аммо дер кардан муҳаррикро аз дарун вайрон мекунад. Экономияи имрӯза фардо ба таъмири гаронбаҳо оварда мерасонад."
- CTA: "Дар Direct нависед ва барои ивази равған сабт шуда, қисми ходовой-ро бепул ташхис кунед!"
- Hashtags: #автосервис #мошин #душанбе #таъмиримошин #тоҷикистон""",
            "posts": """🚗 Пост: Чаро Check Engine фурӯзон мешавад ва чӣ бояд кард?
Ин нишона дар панели мошин дилхоҳ ронандаро ба ташвиш меорад. Оё ин маънои вайроншавии ҷиддиро дорад?
На ҳамеша. Сабаб метавонад аз сарпӯши сӯзишворӣ то вайроншавии датчикҳои муҳаррик башад.

Муҳим он аст, ки инро нодида нагиред. Ташхиси компютерии саривақтӣ мушкилотво дақиқ муайян мекунад.

📍 Автосервиси мо бо таҷҳизоти пешрафтаи муосир муҷаҳҳаз аст.
📞 Барои ташхиси компютерӣ ба мо нависед ё занг занед!""",
            "stories": """Силсилаи Stories:
Слайд 1: Нишонаи Check Engine дар панел. Матн: "Фурӯзон шуд? Натарсед!"
Слайд 2: Устои мо сканерро пайваст мекунад. Матн: "Дар 10 дақиқа сабаби дақиқро муайян мекунем."
Слайд 3: Раванди таъмир. Матн: "Мушкилотро зуд бартараф карда, хатогиро тоза мекунем."
Слайд 4: Қисмҳои эҳтиётии босифат. Матн: "Ҳамаи қисмҳои лозимӣ дар анбори мо мавҷуданд."
Sлайд 5: Тугмаи сабт. Матн: "Имрӯз худро сабт кунед ва 50% тахфиф ба ташхис гиред!" """,
            "ads": """📢 Таблиғот барои автосервис:
1: "Мошини худро ба фасли нав омода кунед! Ташхиси пурра бо Alif Mobi пардохт кунед ва кэшбэк гиред!"
2: "Овози нохуш дар қисми ходовой? Амнияти худро зери хатар нагузоред. Нависед ва кафолати 6-моҳа гиред!"
3: "Полировкаи касбии чароғҳо ва тозакунии химиявии салон дар Душанбе бо нархҳои ниҳоят хуб!" """,
            "funnel": """🎯 Воронкаи фурӯш дар бот:
Қадам 1: Пешниҳоди дастури бепули "Чӣ тавр мошинро пеш аз сафари дур омода кунем" барои обуна.
Қадам 2: Калкулятори пардохтҳои моҳона дар бот.
Қадам 3: Маслиҳатҳои устои калони мо дар шакли видео.
Қадам 4: Ивази ройгони колодкаҳои тормоз ҳангоми хариди онҳо аз маркази мо.""",
            "ideas": """💡 30 идеяи олӣ барои авто-SMM:
1. Тарзи тафтиши равғани муҳаррик бо дастони худ.
2. 5 хатогии калони ронандагон дар гармо/сармо.
3. Баррасии нархҳои бозори мошинҳо дар Тоҷикистон.
4. Навори мошини нодире, ки барои таъмир омадааст.
5. Чӣ тавр сӯзишвориро сарфа кунем: факт ва дурӯғ.
6. Ташхиси чархҳо: кай вақти иваз кардани онҳо расидааст."""
        }
    },
    "realestate": {
        "icon": "🏢",
        "name_ru": "Недвижимость и Аренда",
        "name_uz": "Ko'chmas mulk va Ijara",
        "name_tg": "Хонаҳо ва Иҷора",
        "ru": {
            "plan": """📅 План для Недвижимости на 7 дней:
День 1: [Пост] Как выгодно купить квартиру в новостройке без переплат.
День 2: [Stories] Опрос: "Что выберете — 1-комнатную в центре или 3-комнатную на окраине?"
День 3: [Reels] Видео-тур по роскошной современной квартире с дизайнерским ремонтом.
День 4: [Пост] Юридические тонкости при покупке или аренде жилья.
День 5: [Stories] Сравниваем условия ипотеки и рассрочки от застройщиков.
День 6: [Reels] ТОП-3 района города, которые вырастут в цене через год.
День 7: [Пост] Спецпредложение: Бесплатное юридическое сопровождение сделки!""",
            "reels": """🎬 Сценарий Reels: "Квартира твоей мечты всего за..."
- Хук (0-3 сек): Агент плавно открывает панорамное окно с шикарным видом на город. Текст: "Вы не поверите, сколько стоит эта квартира..."
- B-roll: Просторная светлая кухня, стильная ванная, большая гардеробная комната, уютный балкон.
- Голос: "Ищете идеальное место для жизни? Эта квартира сочетает в себе премиум-локацию, продуманную планировку и потрясающий вид. Лучшая инвестиция в ваше будущее."
- CTA: "Напишите 'ДОМ' в комментариях, и мы пришлем вам подробную планировку и условия беспроцентной рассрочки!"
- Хэштеги: #недвижимость #купитьквартиру #новостройка #аренда #квартира""",
            "posts": """🏢 Пост: Рассрочка или ипотека: что выгоднее в этом году?
Покупка собственного жилья — один из самых важных шагов в жизни. Но как поступить, если всей суммы сразу нет?
Давайте сравним два популярных инструмента. Ипотека дает возможность заехать сразу, но имеет переплаты по процентам. Беспроцентная рассрочка от застройщика — это отличный шанс сэкономить, но требует больших ежемесячных платежей на короткий срок.

Наше агентство поможет подобрать идеальные условия и договориться о персональной скидке с застройщиком.

📍 Наш офис: центр города.
📞 Напишите нам для бесплатной консультации!""",
            "stories": """Серия Stories:
Слайд 1: Фото красивого жилого комплекса. Текст: "Старт продаж нового ЖК премиум-класса!"
Слайд 2: Рендер двора без машин. Текст: "Закрытая охраняемая территория, детские площадки и фонтаны."
Слайд 3: Планировка евро-двушки. Текст: "Самая популярная планировка с просторной кухней-гостиной."
Слайд 4: График рассрочки. Текст: "Первоначальный взнос всего 30%, рассрочка без процентов до конца строительства."
Слайд 5: Окошко обратной связи. Текст: "Хотите получить каталог квартир и прайс-лист? Жмите на стикер!" """,
            "ads": """📢 Таргет реклама:
1: "Купите квартиру в новостройке без первоначального взноса! Квартиры от надежного застройщика в центре города. Пишите!"
2: "Инвестируйте в недвижимость правильно! Пассивный доход от аренды до 12% годовых в валюте. Бесплатный подбор объектов!"
3: "Шикарные квартиры с готовым ремонтом в рассрочку! Заезжайте и живите уже в этом году. Подробности в директ!" """,
            "funnel": """🎯 Воронка продаж:
Шаг 1: Инвестиционный каталог "Топ-10 перспективных новостроек для покупки" за подписку.
Шаг 2: Удобный калькулятор рассрочки в чат-боте.
Шаг 3: Видео-советы от ведущего брокера о проверке надежности застройщика.
Шаг 4: Приглашение на бесплатный индивидуальный тур по лучшим объектам города.""",
            "ideas": """💡 30 идей для недвижимости:
1. Видео-обзор квартиры "До ремонта" и "После".
2. Топ-5 ошибок при покупке квартиры на вторичном рынке.
3. Как проверить документы продавца самостоятельно.
4. Обзор инфраструктуры популярного района города.
5. Ответы на частые вопросы про рассрочку и кредиты.
6. Интерактив: "Угадайте стоимость этой квартиры в комментариях"."""
        },
        "uz": {
            "plan": """📅 Ko'chmas mulk uchun 7 kunlik reja:
1-kun: [Post] Yangi uylardan ortiqcha to'lovsiz kvartira sotib olish sirlari.
2-kun: [Stories] So'rovnoma: "Markazdagi 1 xonali uymi yoki chekkaroqdagi 3 xonali uy?"
3-kun: [Reels] Zamonaviy va dizaynerlik ta'mirlangan uy bo'ylab video-tur.
4-kun: [Post] Uy sotib olish yoki ijaraga olishdagi yuridik nozikliklar.
5-kun: [Stories] Bo'lib to'lash va ipoteka shartlarini solishtirish.
6-kun: [Reels] Toshkentda 1 yilda narxi eng ko'p oshadigan TOP 3 ta tuman.
7-kun: [Post] Maxsus taklif: Shartnomani bepul yuridik rasmiylashtirish xizmati!""",
            "reels": """🎬 Reels ssenariysi: "Siz orzu qilgan xonadon"
- Hook (0-3 sek): Rieltor chiroyli panoramali oynani ochadi va ajoyib manzara ko'rinadi. Matn: "Bu uyning narxi qancha deb o'ylaysiz? Ishonmaysiz..."
- B-roll: Keng va yorug' oshxona, shinam yotoqxona, chiroyli dizayndagi yuvinish xonasi, shinam balkon.
- Ovoz: "Yashash uchun mukammal joy qidiryapsizmi? Bu xonadon qulay joylashuv, zamonaviy reja va ajoyib ko'rinishni o'zida mujassam etgan."
- CTA: "Directga 'UY' deb yozing, biz sizga batafsil rejani va foizsiz bo'lib to'lash shartlarini yuboramiz!"
- Hashtaglar: #uy #toshkent #novostroyka #ijara #kvartira""",
            "posts": """🏢 Post: Bo'lib to'lash yoki ipoteka: qaysi biri foydali?
Shaxsiy uyga ega bo'lish — hayotdagi eng muhim qadamlardan biridir. Agar uyni birdaniga sotib olishga mablag' yetarli bo'lmasa nima qilish kerak?
Keling, ipoteka va foizsiz bo'lib to'lash shartlarini solishtiramiz. Ipoteka uyingizga tezda ko'chib o'tish imkonini beradi, lekin foiz to'lovlari bor. Quruvchidan foizsiz bo'lib to'lash esa pulni tejaydi, lekin qisqa muddatda katta to'lovlarni talab qiladi.

Bizning agentligimiz sizga eng maqbul shartlarni topishda va quruvchidan maxsus chegirma olishda yordam beradi.

📍 Ofisimiz: Toshkent shahri markazida.
📞 Bepul konsultatsiya olish uchun directga yozing!""",
            "stories": """Stories ketma-ketligi:
1-slayd: Yangi turar-joy majmuasi rasmi. Matn: "Yangi premium klassdagi uy sotuvga chiqdi!"
2-slayd: Hovli ko'rinishi. Matn: "Mashinalarsiz xavfsiz hovli, bolalar maydonchalari va favvoralar."
3-slayd: Uy loyihasi (Plani). Matn: "Eng ko'p sotilayotgan 2 xonali uy loyihasi."
4-slayd: To'lov grafigi. Matn: "Boshlang'ich to'lov bor-yo'g'i 30%, foizsiz bo'lib to'lash imkoniyati."
5-slayd: So'rovnoma. Matn: "Uylarning narxlari va katalogini olmoqchimisiz? Havolaga o'ting!" """,
            "ads": """📢 Target reklamalari:
1: "Boshlang'ich to'lovsiz yangi uylardan kvartira sotib oling! Toshkent markasidagi ishonchli quruvchidan uylar!"
2: "Ko'chmas mulkka to'g'ri investitsiya qiling! Ijaradan oyiga yaxshigina dollar daromad olish sirlari!"
3: "Tayyor ta'mirlangan shinam uylar bo'lib to'lashga! Ushbu yilda ko'chib o'ting. Batafsil ma'lumot directda!" """,
            "funnel": """🎯 Sotuv voronkasi:
1-qadam: "Sotib olish uchun eng istiqbolli 10 ta yangi uy" bepul investitsiya katalogi.
2-qadam: Bot ichida oylik to'lovlarni hisoblovchi kalkulyator.
3-qadam: Rieltorlarimizdan quruvchilarning ishonchliligini tekshirish bo'yicha maslahat videolari.
4-qadam: Eng yaxshi yangi uylar bo'ylab bepul sayohat (tur) tashkil etish.""",
            "ideas": """💡 30 ta SMM g'oya:
1. Uyni ta'mirdan oldingi va keyingi holati videosi.
2. Ikkilamchi bozordan uy sotib olishdagi 5 ta eng katta xato.
3. Uy hujjatlarini qanday mustaqil tekshirish mumkin.
4. Toshkentning eng rivojlangan tumanlari sharhi.
5. Bo'lib to'lash va kreditlar haqidagi savollarga javoblar.
6. Interaktiv o'yin: "Ushbu uyning narxini toping"."""
        },
        "tg": {
            "plan": """📅 Нақшаи 7-рӯза барои Амволи ғайриманқул (Хонаҳо):
Рӯзи 1: [Пост] Чӣ тавр хонаи навро бе пардохти зиёдатӣ харем.
Рӯзи 2: [Stories] Овоздиҳӣ: "Кадомаш хубтар — хонаи 1-ҳуҷрагӣ дар марказ ё 3-ҳуҷрагӣ дар канор?"
Рӯзи 3: [Reels] Видео-тур дар хонаи боҳашамати замонавӣ бо таъмири стилӣ.
Рӯзи 4: [Пост] Нозукиҳои ҳуқуқӣ ҳангоми харид ва иҷораи хона.
Рӯзи 5: [Stories] Муқоисаи шартҳои ипотека ва пардохти қисм-қисм аз созандагон.
Рӯзи 6: [Reels] ТОП-3 ноҳияи Душанбе, ки нархи хонаҳояшон тез месабзад.
Рӯзи 7: [Пост] Пешниҳоди махсус: Дастгирии ройгони ҳуқуқии муомила!""",
            "reels": """🎬 Сценарияи Reels: "Хонаи орзуҳои ту дар Душанбе"
- Hook (0-3 сек): Агент тирезаи калони панорамиро кушода, манзараи зебои шаҳрро нишон медиҳад. Матн: "Шумо бовар намекунед, ки ин хона чанд пул аст..."
- B-roll: Ошхонаи васеъ ва равшан, ҳаммоми стилӣ, гардероби калон ва балкони шинам.
- Овоз: "Ҷои беҳтарин барои зиндагӣ меҷӯед? Ин хона макони қулай, тарҳрезии муосир ва манзараи дилраборо муттаҳид мекунад."
- CTA: "Дар Direct калимаи 'ХОНА' нависед, мо ба шумо банақшагирӣ ва шартҳои пардохти дарозмуддатро мефиристем!"
- Hashtags: #недвижимость #хона #иҷора #душанбе #тоҷикистон #новостройки""",
            "posts": """🏢 Пост: Ипотека ё пардохти қисм-қисм (рассрочка): кадомаш беҳтар аст?
Харидани хонаи худ — яке аз қадамҳои муҳимтарин дар ҳаёти ҳар як инсон аст. Аммо агар маблағи пурра дар даст набошад, чӣ бояд кард?
Биёед ду усули машҳурро муқоиса кунем. Ипотека имкон медиҳад, ки зудтар соҳиби хона шавед, вале фоизҳои иловагӣ дорад. Пардохти қисм-қисм бефоиз аз сохтмончӣ пулро сарфа мекунад, вале маблағҳои калони моҳонаро ба муҳлати кӯтоҳ талаб мекунад.

Агентии мо ба шумо кӯмак мекунад, ки шартҳои беҳтарин ва тахфифҳои махсусро аз созандагон ба даст оред.

📍 Дафтари мо: маркази шаҳри Душанбе.
📞 Барои машварати ройгон ба мо нависед!""",
            "stories": """Силсилаи Stories:
Слайд 1: Сурати бинои нави боҳашамат. Матн: "Оғози фурӯши хонаҳо дар ЖК-и нави премиум!"
Слайд 2: Намоиши ҳавлии бино. Матн: "Ҳавлии пӯшида ва бехатар барои кӯдакон, фаввораҳо ва посбонон."
Слайд 3: Тарҳи хонаи 2-ҳуҷрагӣ. Матн: "Тарҳи беҳтарин ва васеъ бо ошхонаи калон."
Слайд 4: Графики пардохт. Матн: "Пардохти аввалия ҳамагӣ 30%, пардохти қисм-қисм бе фоиз то анҷоми сохтмон."
Слайд 5: Саволнома. Матн: "Мехоҳед каталоги нархҳоро гиред? Тугмаро пахш кунед!" """,
            "ads": """📢 Таблиғот барои амволи ғайриманқул:
1: "Соҳиби хонаи нав дар Душанбе шавед! Хонаҳо бе фоиз ба муҳлати дароз аз сохтмончии боэътимод. Пишите!"
2: "Сармоягузории дуруст ба хонаҳо дар Тоҷикистон! Даромади устувор аз иҷора то 12% солона. Машварати ройгон!"
3: "Хонаҳои таъмиршуда ва омодаи зиндагӣ бо шартҳои ниҳоят хуб! Ҳамин сол соҳиби хона шавед!" """,
            "funnel": """🎯 Воронкаи фурӯш дар бот:
Қадам 1: Пешниҳоди каталоги ройгони "10 бинои нави беҳтарин барои харид" барои обуна.
Қадам 2: Калкулятори пардохтҳои моҳона дар бот.
Қадам 3: Видеоҳо аз брокери ботаҷрибаи мо дар бораи тарзи тафтиши ҳуҷҷатҳои сохтмонӣ.
Қадам 4: Саёҳати ройгон (тур) бо мошини ширкат ба объектҳои сохташаванда.""",
            "ideas": """💡 30 идеяи олӣ:
1. Навори видеоии "Пеш ва Пас" аз таъмири хона.
2. 5 хатои калон ҳангоми харидории хонаи дуюмдараҷа (вторичка).
3. Чӣ тавр мустақилона ҳуҷҷатҳои хонаро тафтиш кунем.
4. Шарҳи инфрасохтори маҳаллаҳои беҳтарини пойтахт.
5. Ҷавоб ба саволҳои тез-тез додашаванда дар бораи ипотека.
6. Бозӣ бо обуначиён: "Нархи ин хонаро тахмин кунед"."""
        }
    }
}
