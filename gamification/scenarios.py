# gamification/scenarios.py — Сценарии бизнес-игры для Таджикистана и Узбекистана

QUIZ_SCENARIOS = {
    "uz": [
        {
            "scenario": {
                "ru": "У вас упали продажи текстиля на рынке Чорсу в Ташкенте из-за высокой конкуренции. Что предпримете?",
                "tg": "Фурӯши бофандагии шумо дар бозори Чорсуи Тошканд аз сабаби рақобати баланд кам шуд. Чӣ кор мекунед?",
                "uz": "Toshkentdagi Chorsu bozorida raqobat kuchliligi sababli to'qimachilik (tekstil) savdongiz tushib ketdi. Nima qilasiz?"
            },
            "options": {
                "ru": {
                    "A": "Снизить цены ниже себестоимости, чтобы вытеснить конкурентов.",
                    "B": "Запустить рекламу в Instagram/TikTok и предложить уникальный дизайн.",
                    "C": "Закрыть точку на Чорсу и переехать на Сергели."
                },
                "tg": {
                    "A": "Нархҳоро аз арзиши аслӣ паст кунед, то рақобатчиёнро берун кунед.",
                    "B": "Рекламаро дар Instagram/TikTok фаъол кунед ва тарҳи беназир пешниҳод намоед.",
                    "C": "Нуқтаро дар Чорсу баста, ба Сергели кӯчед."
                },
                "uz": {
                    "A": "Raqobatchilarni siqib chiqarish uchun narxlarni tannarxidan ham pastga tushirish.",
                    "B": "Instagram/TikTok-da reklama yo'lga qo'yib, o'zgacha dizayndagi mahsulotlar taklif qilish.",
                    "C": "Chorsudagi do'konni yopib, Sergeliga ko'chib o'tish."
                }
            },
            "correct": "B",
            "explanation": {
                "ru": "Правильно! Продвижение через соцсети и уникальный дизайн помогут выделиться среди однотипных конкурентов.",
                "tg": "Дуруст! Танзими реклама дар шабакаҳои иҷтимоӣ ва тарҳи беназир ба шумо кӯмак мекунанд, ки фарқ кунед.",
                "uz": "To'g'ri! Ijtimoiy tarmoqlar va noyob dizayn sizga raqobatchilardan ajralib turishga yordam beradi."
            }
        },
        {
            "scenario": {
                "ru": "Вы хотите открыть точку продажи плова в Ташкенте, но сомневаетесь в локации. Какое место выберете?",
                "tg": "Шумо мехоҳед дар Тошканд нуқтаи фурӯши палов кушоед, аммо дар интихоби макон дудила ҳастед. Кадом ҷойро интихоб мекунед?",
                "uz": "Toshkentda palov markazi ochmoqchisiz, ammo joy tanlashda ikkilanmoqdasiz. Qaysi joyni tanlaysiz?"
            },
            "options": {
                "ru": {
                    "A": "Возле авторынка Сергели, где всегда много голодных автолюбителей.",
                    "B": "В глухом спальном районе без вывески.",
                    "C": "В арендованном гараже на окраине города."
                },
                "tg": {
                    "A": "Назди бозори мошини Сергели, ки ҳамеша дӯстдорони мошини гурусна зиёданд.",
                    "B": "Дар маҳаллаи дурдасти истиқоматӣ бе ягон лавҳа.",
                    "C": "Дар гаражи иҷорагирифташуда дар канори шаҳр."
                },
                "uz": {
                    "A": "Sergeli avtobozori yaqinida, u yerda doim och qolgan haydovchilar ko'p.",
                    "B": "Sokin turar-joy dahasida, peshtaxtasiz.",
                    "C": "Shahar chetidagi ijaraga olingan garajda."
                }
            },
            "correct": "A",
            "explanation": {
                "ru": "Правильно! Высокий трафик целевой аудитории (водители, покупатели авто) обеспечит быстрый старт.",
                "tg": "Дуруст! Трафики баланди аудиторияи мақсаднок (ронандагон, харидорон) оғози тезро таъмин мекунад.",
                "uz": "To'g'ri! Maqsadli auditoriyaning (haydovchilar, xaridorlar) yuqori trafigi tezda savdoni yo'lga qo'yishga yordam beradi."
            }
        },
        {
            "scenario": {
                "ru": "Какая платежная система наиболее популярна для онлайн-оплаты в розничной торговле в Узбекистане?",
                "tg": "Кадом системаи пардохт барои пардохти онлайн дар тиҷорати чакана дар Ӯзбекистон маъмултар аст?",
                "uz": "O'zbekistonda chakana savdoda onlayn to'lovlar uchun qaysi to'lov tizimlari eng mashhur?"
            },
            "options": {
                "ru": {
                    "A": "Alif и Душанбе Сити.",
                    "B": "Click и Payme.",
                    "C": "Только наличные рубли."
                },
                "tg": {
                    "A": "Alif ва Душанбе Сити.",
                    "B": "Click ва Payme.",
                    "C": "Танҳо рубли нақд."
                },
                "uz": {
                    "A": "Alif va Dushanbe City.",
                    "B": "Click va Payme.",
                    "C": "Faqat naqd rubl."
                }
            },
            "correct": "B",
            "explanation": {
                "ru": "Правильно! Click и Payme — лидеры финтех-рынка Узбекистана.",
                "tg": "Дуруст! Click ва Payme пешвоёни бозори финтехи Ӯзбекистон мебошанд.",
                "uz": "To'g'ri! Click va Payme — O'zbekiston fintech bozorining yetakchilaridir."
            }
        }
    ],
    "tj": [
        {
            "scenario": {
                "ru": "Ваш карго-груз из Китая застрял на границе по пути в Душанбе. Клиенты требуют товары. Ваши действия?",
                "tg": "Боргоҳи каргои шумо аз Чин дар роҳ ба Душанбе дар сарҳад банд монд. Мизоҷон мол талаб доранд. Чӣ кор мекунед?",
                "uz": "Xitoydan kelayotgan kargo yukingiz Dushanbega yo'lda chegarada tiqilib qoldi. Mijozlar tovarlarni talab qilmoqda. Nima qilasiz?"
            },
            "options": {
                "ru": {
                    "A": "Игнорировать звонки клиентов и отключить телефон.",
                    "B": "Честно объяснить ситуацию, предложить скидку на следующий заказ или бесплатную доставку.",
                    "C": "Обвинить клиентов в нетерпеливости и аннулировать их заказы без возврата денег."
                },
                "tg": {
                    "A": "Зангҳои мизоҷонро нодида гиред ва телефонро хомӯш кунед.",
                    "B": "Вазъиятро ростқавлона фаҳмонед, барои фармоиши навбатӣ тахфиф ё интиқоли ройгон пешниҳод кунед.",
                    "C": "Мизоҷонро ба бесабрӣ айбдор кунед ва фармоишҳоро бе бозгашти пул бекор кунед."
                },
                "uz": {
                    "A": "Mijozlar qo'ng'iroqlariga javob bermaslik va telefonni o'chirib qo'yish.",
                    "B": "Vaziyatni ochiq-oydin tushuntirish, keyingi buyurtma uchun chegirma yoki bepul yetkazib berish taklif qilish.",
                    "C": "Mijozlarni sabrsizlikda ayblash va pullarini qaytarmasdan buyurtmalarni bekor qilish."
                }
            },
            "correct": "B",
            "explanation": {
                "ru": "Правильно! Честность и лояльность удерживают клиентов при форс-мажорах.",
                "tg": "Дуруст! Ростқавлӣ ва вафодорӣ мизоҷонро дар ҳолатҳои форс-мажор нигоҳ медоранд.",
                "uz": "To'g'ri! Samimiylik va sodiqlik kutilmagan vaziyatlarda mijozlarni ushlab qolishga yordam beradi."
            }
        },
        {
            "scenario": {
                "ru": "Вы хотите запустить продажи национальной одежды чакан на рынке Корвон в Душанбе. Как привлечь первых покупателей?",
                "tg": "Шумо мехоҳед фурӯши либоси миллии чаканро дар бозори Корвони Душанбе оғоз кунед. Чӣ тавр харидорони аввалинро ҷалб мекунед?",
                "uz": "Dushanbedagi Korvon bozorida milliy chakan kiyimlari savdosini yo'lga qo'ymoqchisiz. Birinchi xaridorlarni qanday jalb qilasiz?"
            },
            "options": {
                "ru": {
                    "A": "Организовать красивую витрину, делать фотосессии в чакане для Instagram и продвигаться среди невест.",
                    "B": "Продавать только ночью без освещения.",
                    "C": "Ждать, пока покупатели сами случайно найдут вашу палатку без вывески."
                },
                "tg": {
                    "A": "Витринаи зебо ташкил кунед, дар Instagram аксҳои либоси чаканро ҷойгир кунед ва байни арӯсон таблиғ намоед.",
                    "B": "Танҳо шабона бе рӯшноӣ фурӯшед.",
                    "C": "Мунтазир бошед, то харидорон худашон хаймаи бе лавҳаи шуморо пайдо кунанд."
                },
                "uz": {
                    "A": "Chiroyli vitrina tashkil qilish, Instagram uchun chakan libosida fotosessiyalar qilish va kelinlar orasida reklama qilish.",
                    "B": "Faqat tunda, chiroqsiz sotish.",
                    "C": "Xaridorlar o'zlari tasodifan peshtaxtasiz do'koningizni topishini kutish."
                }
            },
            "correct": "A",
            "explanation": {
                "ru": "Правильно! Визуальный контент и ориентация на целевую аудиторию (свадьбы, невесты) — ключ к успеху в продажах чакана.",
                "tg": "Дуруст! Контенти визуалӣ ва нигаронида ба аудиторияи мақсаднок (тӯйҳо, арӯсон) калиди муваффақият аст.",
                "uz": "To'g'ri! Vizual kontent va maqsadli auditoriyaga (to'ylar, kelinlar) yo'naltirilganlik — chakan sotishning muvaffaqiyat kalitidir."
            }
        },
        {
            "scenario": {
                "ru": "Вы планируете построить зону отдыха в Варзобе. Какая услуга привлечет больше всего местных туристов летом?",
                "tg": "Шумо нақша доред, ки дар Варзоб минтақаи истироҳатӣ созед. Кадом хидмат сайёҳони маҳаллиро дар тобистон бештар ҷалб мекунад?",
                "uz": "Varzobda dam olish maskani qurishni rejalashtiryapsiz. Yozda mahalliy sayyohlarni eng ko'p qaysi xizmat jalb qiladi?"
            },
            "options": {
                "ru": {
                    "A": "Прокат зимних лыж.",
                    "B": "Топчаны у прохладной горной реки, чистый бассейн и вкусный шашлык.",
                    "C": "Лекции по квантовой физике на открытом воздухе."
                },
                "tg": {
                    "A": "Иҷораи лижаҳои зимистона.",
                    "B": "Катҳо (тапчан) дар назди дарёи салқини кӯҳӣ, ҳавзи тоза ва кабоби болаззат.",
                    "C": "Маърузаҳо оид ба физикаи квантӣ дар ҳавои кушод."
                },
                "uz": {
                    "A": "Qishki chang'ilar ijarasi.",
                    "B": "Salqin tog' daryosi bo'yidagi so'rilar (topchan), toza basseyndar va mazali kabob.",
                    "C": "Ochiq osmon ostida kvant fizikasi bo'yicha ma'ruzalar."
                }
            },
            "correct": "B",
            "explanation": {
                "ru": "Правильно! Топчаны у воды и бассейн — идеальное спасение от летней жары для жителей Душанбе.",
                "tg": "Дуруст! Катҳо дар назди об ва ҳавз — наҷоти беҳтарин аз гармии тобистон барои сокинони Душанбе мебошад.",
                "uz": "To'g'ri! Suv bo'yidagi so'rilar va basseyn — yozgi issiqdan qochgan Dushanbe aholisi uchun eng yaxshi dam olish variantidir."
            }
        }
    ]
}
