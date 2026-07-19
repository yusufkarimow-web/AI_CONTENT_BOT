# gamification/scenarios.py — Бизнес-кейсы и случайные события для игры "Бизнес Империя"

BUSINESS_EMPIRE_EVENTS = [
    {
        "text_ru": "Клиент оставил восторженный отзыв о вашем сервисе в соцсетях!",
        "text_tg": "Мизоҷ дар шабакаҳои иҷтимоӣ дар бораи хизматрасонии шумо фикру мулоҳизаҳои олӣ гузошт!",
        "text_uz": "Mijoz ijtimoiy tarmoqlarda xizmatingiz haqida ajoyib fikr qoldirdi!",
        "options": {
            "A": {
                "text_ru": "Репостнуть отзыв и поблагодарить (бонус клиентов)",
                "text_tg": "Фикри мизоҷро репост кунед ва ташаккур гӯед (бонуси мизоҷон)",
                "text_uz": "Fikrni ulashing va rahmat ayting (mijozlar bonusi)",
                "balance_diff": 0,
                "clients_diff": 20,
                "xp_diff": 15
            },
            "B": {
                "text_ru": "Предложить ему скидку на следующий заказ (небольшой расход, много клиентов)",
                "text_tg": "Ба ӯ барои фармоиши навбатӣ тахфиф пешниҳод кунед (хароҷоти кам, мизоҷони зиёд)",
                "text_uz": "Keyingi buyurtma uchun chegirma taklif qiling (kichik xarajat, ko'p mijozlar)",
                "balance_diff": -50,
                "clients_diff": 45,
                "xp_diff": 20
            },
            "C": {
                "text_ru": "Проигнорировать отзыв (нейтрально)",
                "text_tg": "Фикрро нодида гиред (нейтралӣ)",
                "text_uz": "Fikrga e'tibor bermaslik (neytral)",
                "balance_diff": 0,
                "clients_diff": 0,
                "xp_diff": 0
            }
        }
    },
    {
        "text_ru": "К вам пришёл крупный корпоративный заказ! Но требуется расширить штат.",
        "text_tg": "Ба назди шумо фармоиши калони корпоративӣ омад! Аммо васеъ кардани ҳайати коргарон лозим аст.",
        "text_uz": "Sizga katta korporativ buyurtma keldi! Ammo xodimlar sonini oshirish talab etiladi.",
        "options": {
            "A": {
                "text_ru": "Нанять дополнительных сотрудников (расход, прибыль, новые клиенты)",
                "text_tg": "Кормандони иловагӣ киро кунед (хароҷот, фоида, мизоҷони нав)",
                "text_uz": "Qo'shimcha xodimlarni ishga oling (xarajat, daromad, yangi mijozlar)",
                "balance_diff": -200,
                "clients_diff": 80,
                "xp_diff": 40,
                "employees_diff": 2
            },
            "B": {
                "text_ru": "Отказаться от заказа (нейтрально)",
                "text_tg": "Аз фармоиш даст кашед (нейтралӣ)",
                "text_uz": "Buyurtmani rad etish (neytral)",
                "balance_diff": 0,
                "clients_diff": -5,
                "xp_diff": 5
            },
            "C": {
                "text_ru": "Заставить текущих сотрудников работать сверхурочно (прибыль без затрат, но риск ухода сотрудников)",
                "text_tg": "Кормандони ҳозираро маҷбур кунед, ки изофакорӣ кунанд (фоида бе хароҷот, хавфи рафтани коргарон)",
                "text_uz": "Hozirgi xodimlarni vaqtinchalik ko'proq ishlashga majburlash (foyda, xodim ketish xavfi)",
                "balance_diff": 300,
                "clients_diff": 30,
                "xp_diff": 15,
                "employees_diff": -1
            }
        }
    },
    {
        "text_ru": "Появился инвестор, готовый вложить деньги в ваш бизнес за долю в прибыли в будущем.",
        "text_tg": "Сармоягузоре пайдо шуд, ки омода аст ба тиҷорати шумо маблағ гузорад.",
        "text_uz": "Sizning biznesingizga sarmoya kiritishga tayyor investor paydo bo'ldi.",
        "options": {
            "A": {
                "text_ru": "Принять инвестиции (большой бонус к балансу, новые клиенты)",
                "text_tg": "Сармояро қабул кунед (бонуси калон ба баланс, мизоҷони нав)",
                "text_uz": "Investitsiyalarni qabul qilish (balansga katta bonus, yangi mijozlar)",
                "balance_diff": 500,
                "clients_diff": 30,
                "xp_diff": 25
            },
            "B": {
                "text_ru": "Отказаться ради сохранения полной независимости (бонус к опыту)",
                "text_tg": "Барои нигоҳ доштани истиқлолияти комил рад кунед (бонуси таҷриба)",
                "text_uz": "Mustaqillikni saqlab qolish uchun rad etish (tajriba bonusi)",
                "balance_diff": 0,
                "clients_diff": 0,
                "xp_diff": 50
            },
            "C": {
                "text_ru": "Попросить больше денег (риск отказа инвестора 50/50)",
                "text_tg": "Маблағи бештар талаб кунед (хавфи рад шудани сармоягузор)",
                "text_uz": "Ko'proq pul so'rash (rad etilish xavfi)",
                "balance_diff": 250,
                "clients_diff": 15,
                "xp_diff": 15
            }
        }
    },
    {
        "text_ru": "Ваш ключевой сотрудник неожиданно решил уволиться из-за высокой нагрузки.",
        "text_tg": "Корманди калидии шумо ногаҳон қарор дод, ки аз сабаби сарбории зиёд аз кор равад.",
        "text_uz": "Sizning asosiy xodimingiz kutilmaganda og'ir ish sababli ketishga qaror qildi.",
        "options": {
            "A": {
                "text_ru": "Повысить ему зарплату и улучшить условия (расход бюджета)",
                "text_tg": "Маоши ӯро зиёд кунед ва шароитро беҳтар созед (хароҷоти буҷет)",
                "text_uz": "Uning maoshini oshirish va sharoitlarni yaxshilash (byudjet xarajati)",
                "balance_diff": -150,
                "clients_diff": 10,
                "xp_diff": 30
            },
            "B": {
                "text_ru": "Отпустить сотрудника (потеря сотрудника, снижение продуктивности)",
                "text_tg": "Ба ӯ иҷозати рафтан диҳед (талафи коргар, паст шудани маҳсулнокӣ)",
                "text_uz": "Javob berish (xodimni yo'qotish, samaradorlik pasayishi)",
                "balance_diff": 0,
                "clients_diff": -25,
                "xp_diff": 10,
                "employees_diff": -1
            },
            "C": {
                "text_ru": "Найти нового сотрудника на бирже труда (небольшой расход, обучение)",
                "text_tg": "Дар биржаи меҳнат корманди нав ёбед (хароҷоти кам, омӯзиш)",
                "text_uz": "Mehnat birjasidan yangi xodim topish (kichik xarajat, o'qitish)",
                "balance_diff": -50,
                "clients_diff": -5,
                "xp_diff": 20
            }
        }
    }
]

BUSINESS_TYPES = {
    "cargo": {
        "name_ru": "📦 Карго компания",
        "name_tg": "📦 Ширкати Карго",
        "name_uz": "📦 Kargo kompaniyasi",
        "cost": 500,
        "income_per_client": 15,
        "required_level": 1,
        "desc_ru": "Доставка товаров из Китая и Турции.",
        "desc_tg": "Интиқоли молҳо аз Чин ва Туркия.",
        "desc_uz": "Xitoy va Turkiyadan tovarlarni yetkazish."
    },
    "logistics": {
        "name_ru": "🚛 Логистическая компания",
        "name_tg": "🚛 Ширкати Логистикӣ",
        "name_uz": "🚛 Logistika kompaniyasi",
        "cost": 1200,
        "income_per_client": 30,
        "required_level": 2,
        "desc_ru": "Внутренние и международные перевозки грузов.",
        "desc_tg": "Интиқоли дохилӣ ва байналмилалии борҳо.",
        "desc_uz": "Ichki va xalqaro yuk tashish xizmatlari."
    },
    "store": {
        "name_ru": "🌐 Интернет-магазин",
        "name_tg": "🌐 Дӯкони интернетӣ",
        "name_uz": "🌐 Internet-do'kon",
        "cost": 800,
        "income_per_client": 20,
        "required_level": 1,
        "desc_ru": "Продажа трендовых товаров через соцсети.",
        "desc_tg": "Фурӯши молҳои трендӣ тавассути шабакаҳои иҷтимоӣ.",
        "desc_uz": "Ijtimoiy tarmoqlar orqali tovarlar savdosi."
    },
    "cafe": {
        "name_ru": "🍔 Кафе / Чайхана",
        "name_tg": "🍔 Кафе / Чойхона",
        "name_uz": "🍔 Kafe / Choyxona",
        "cost": 1500,
        "income_per_client": 35,
        "required_level": 2,
        "desc_ru": "Вкусная национальная кухня и высокий сервис.",
        "desc_tg": "Таомҳои миллии болаззат ва хизматрасонии олӣ.",
        "desc_uz": "Mazali milliy taomlar va yuqori xizmat ko'rsatish."
    },
    "clothes": {
        "name_ru": "👗 Магазин одежды",
        "name_tg": "👗 Дӯкони либосворӣ",
        "name_uz": "👗 Kiyim-kechak do'koni",
        "cost": 2000,
        "income_per_client": 45,
        "required_level": 3,
        "desc_ru": "Бутик модной одежды и национальных нарядов.",
        "desc_tg": "Бутики либосҳои замонавӣ ва либосҳои миллӣ.",
        "desc_uz": "Zamonaviy va milliy liboslar do'koni."
    },
    "education": {
        "name_ru": "🎓 Учебный центр",
        "name_tg": "🎓 Маркази таълимӣ",
        "name_uz": "🎓 O'quv markazi",
        "cost": 3000,
        "income_per_client": 60,
        "required_level": 4,
        "desc_ru": "Обучение IT, языкам и маркетингу.",
        "desc_tg": "Омӯзиши IT, забонҳо ва маркетинг.",
        "desc_uz": "IT, tillar va marketing bo'yicha ta'lim berish."
    },
    "marketing": {
        "name_ru": "🚀 Маркетинговое агентство",
        "name_tg": "🚀 Агентии маркетингӣ",
        "name_uz": "🚀 Marketing agentligi",
        "cost": 5000,
        "income_per_client": 100,
        "required_level": 5,
        "desc_ru": "SMM, продвижение и создание вирусного контента.",
        "desc_tg": "SMM, таблиғ ва сохтани контенти вирусӣ.",
        "desc_uz": "SMM, reklamalar va virusli kontent yaratish xizmati."
    }
}
