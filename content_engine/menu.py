# content_engine/menu.py — Главный router бота Sozanda

import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import (
    FREE_DAILY_LIMIT,
    OSON_DAILY_LIMIT,
    PRO_DAILY_LIMIT,
    WATERMARK_TEXT,
    ADMIN_IDS,
    REFERRAL_BONUS_GENERATIONS,
    TARIFFS,
    ADMIN_ID
)
from database.models import (
    get_or_create_user,
    get_user,
    get_user_stats,
    increment_generation,
    check_daily_limit,
    get_referral_count,
    add_referral_bonus,
    get_user_subscription,
    save_generation,
    get_generation_history,
)
from services.ai_generator import generate_ai_content
from content_engine.niche_manager import get_topic_ideas, get_niche_key_by_text, get_niche_name

def is_niche_button(text: str) -> bool:
    from content_engine.niche_manager import get_all_niches
    all_names = set()
    for country in ["uz", "tj"]:
        for lang in ["ru", "tg", "uz"]:
            for n in get_all_niches(lang, country):
                all_names.add(n.get(f"name_{lang}"))
                all_names.add(n.get("icon", "") + " " + n.get(f"name_{lang}", ""))
    return text in all_names

from keyboards.main_menu_content import get_main_menu
from keyboards.niche_menu import get_niche_menu
from keyboards.reels_count_menu import get_count_menu
from keyboards.topics_keyboard import get_topics_keyboard
from keyboards.language_menu import get_language_menu
from keyboards.subscription_menu import get_subscription_menu, get_payment_menu
from keyboards.share_keyboard import get_share_keyboard

router = Router()

user_counts = {}
user_niches = {}
user_languages = {}
user_topics = {}

TEXTS = {
    "ru": {
        "welcome": "👋 Добро пожаловать в <b>Sozanda</b>!\n\n🤖 Я — AI-бот, который создаёт вирусный контент для бизнеса.\n\n✨ Что я умею:\n• 🎬 Reels / Видео с вирусными хуками\n• 📝 Посты для Instagram\n• 📸 Stories\n• 💡 Идеи для контента\n• ⚡ Цепляющие подписи\n\n<b>Выберите язык / Забонро интихоб кунед / Tilni tanlang:</b>",
        "main_menu": "👋 Главное меню\n\n✨ Выберите, что создать:",
        "choose_niche": "🏢 Для какого бизнеса нужен контент?",
        "choose_count": "🔢 Сколько идей подготовить?",
        "choose_topic": "👇 Выберите номер темы кнопкой ниже",
        "generating": "⏳ Генерирую контент через AI...\n\nЭто займёт несколько секунд...",
        "no_topic": "❌ Такой темы нет. Выберите из списка выше.",
        "limit_reached": "❌ Лимит исчерпан!\n\n💡 У вас закончились бесплатные генерации на сегодня.\n\n🚀 Получите больше:\n• Пригласите друга — +{ref_bonus} генераций\n• Оформите подписку Oson — {oson_limit} генераций/день\n• Или Professional — безлимит!",
        "premium_info": "⭐ <b>Premium подписки</b>\n\n🆓 <b>Free</b> — {free_limit} генераций/день\n   Водяной знак на контенте\n\n💚 <b>Oson</b> — {oson_price} сомони/мес\n   • {oson_limit} генераций/день\n   • Без водяного знака\n   • Все ниши\n\n💎 <b>Professional</b> — {pro_price} сомони/мес\n   • Безлимит генераций\n   • Без водяного знака\n   • Все ниши + приоритетная генерация\n\n🏢 <b>Business</b> — {biz_price} сомони/мес\n   • Всё из Professional\n   • White-label + API доступ",
        "support": "📞 <b>Поддержка</b>\n\nЕсть вопросы или предложения?\nПишите: @sozanda_support\n\n🤝 Для партнёрств и рекламы:\n@sozanda_admin",
        "history_empty": "📭 История пуста. Создайте свой первый контент!",
        "history_title": "📋 <b>Ваша история генераций</b>\n\n",
        "language_set": "✅ Язык установлен: {lang}",
        "stats": "📊 <b>Ваша статистика</b>\n\n🆔 ID: {user_id}\n🌍 Язык: {lang}\n📅 Регистрация: {reg_date}\n\n📈 Генераций сегодня: {today}/{limit}\n📈 Всего генераций: {total}\n👥 Приглашено друзей: {refs}\n\n💳 Тариф: {plan}",
    },
    "tg": {
        "welcome": "👋 Хуш омадед ба <b>Sozanda</b>!\n\n🤖 Ман — боти AI ҳастам, ки мундод барои бизнес месозам.\n\n✨ Чи корҳо мекунам:\n• 🎬 Reels / Видео бо hook-ҳои вирусӣ\n• 📝 Постҳо барои Instagram\n• 📸 Stories\n• 💡 Идеяҳо барои контент\n• ⚡ Сарлавҳаҳои ҷолиб\n\n<b>Забонро интихоб кунед / Выберите язык:</b>",
        "main_menu": "👋 Менюи асосӣ\n\n✨ Интихоб кунед, чи сохтан мехоҳед:",
        "choose_niche": "🏢 Барои кадом бизнес контент лозим аст?",
        "choose_count": "🔢 Чанд идея тайёр кунам?",
        "choose_topic": "👇 Рақами мавзӯъро аз менюи поён интихоб кунед",
        "generating": "⏳ AI контентро месозам...\n\nЧанд сония вақт мегирад...",
        "no_topic": "❌ Чунин мавзӯъ нест. Аз рӯйхати боло интихоб кунед.",
        "limit_reached": "❌ Лимит ба охир расид!\n\n💡 Генерацияҳои ройгони шумо барои имрӯз тамом шуданд.\n\n🚀 Бештар гиред:\n• Дӯстро даъват кунед — +{ref_bonus} генерация\n• Обунаи Oson — {oson_limit} генерация/рӯз\n• Ё Professional — беҳад!",
        "premium_info": "⭐ <b>Обунаҳои Premium</b>\n\n🆓 <b>Free</b> — {free_limit} генерация/рӯз\n   Нишони обуна (watermark)\n\n💚 <b>Oson</b> — {oson_price} сомонӣ/моҳ\n   • {oson_limit} генерация/рӯз\n   • Бе watermark\n   • Ҳама нишаҳо\n\n💎 <b>Professional</b> — {pro_price} сомонӣ/моҳ\n   • Беҳад генерация\n   • Бе watermark\n   • Ҳама нишаҳо + аввалият\n\n🏢 <b>Business</b> — {biz_price} сомонӣ/моҳ\n   • Ҳама аз Professional\n   • White-label + API дастрасӣ",
        "support": "📞 <b>Дастгирӣ</b>\n\nСавол ё пешниҳод доред?\nБинависед: @sozanda_support\n\n🤝 Барои ҳамкорӣ ва реклама:\n@sozanda_admin",
        "history_empty": "📭 Таърих холӣ аст. Аввалин контенти худро бисозед!",
        "history_title": "📋 <b>Таърихи генерацияҳои шумо</b>\n\n",
        "language_set": "✅ Забон танзим шуд: {lang}",
        "stats": "📊 <b>Омори шумо</b>\n\n🆔 ID: {user_id}\n🌍 Забон: {lang}\n📅 Санаи бақайдгирӣ: {reg_date}\n\n📈 Генерацияҳои имрӯз: {today}/{limit}\n📈 Ҳамаи генерацияҳо: {total}\n👥 Даъват шудаанд: {refs}\n\n💳 Тариф: {plan}",
    },
    "uz": {
        "welcome": "👋 <b>Sozanda</b> botiga xush kelibsiz!\n\n🤖 Men — biznesingiz uchun ommabop va virusli kontentlar yaratuvchi sun'iy intellekt (AI) botiman.\n\n✨ Nimalar qila olaman:\n• 🎬 Reels / Video ssenariylar va virusli hooklar\n• 📝 Instagram uchun mukammal postlar\n• 📸 Stories g'oyalari\n• 💡 Kreativ kontent g'oyalari\n• ⚡ Jalb qiluvchi sarlavhalar\n\n<b>Tilni tanlang / Забонро интихоб кунед / Выберите язык:</b>",
        "main_menu": "👋 Asosiy menyu\n\n✨ Nimani yaratishni xohlaysiz?",
        "choose_niche": "🏢 Qaysi soha (nisha) uchun kontent kerak?",
        "choose_count": "🔢 Nechta g'oya tayyorlash kerak?",
        "choose_topic": "👇 Pastdagi tugmalar yordamida mavzu raqamini tanlang",
        "generating": "⏳ AI orqali kontent yaratilmoqda...\n\nBu bir necha soniya vaqt oladi...",
        "no_topic": "❌ Bunday mavzu yo'q. Yuqoridagi ro'yxatdan tanlang.",
        "limit_reached": "❌ Kunlik limit tugadi!\n\n💡 Bugungi bepul generatsiyalaringiz yakunlandi.\n\n🚀 Ko'proq imkoniyat oling:\n• Do'shingizni taklif qiling — +{ref_bonus} ta generatsiya\n• Oson tarifiga ulaning — kuniga {oson_limit} ta generatsiya\n• Yoki Professional — cheksiz!",
        "premium_info": "⭐ <b>Premium obunalar</b>\n\n🆓 <b>Free</b> — kuniga {free_limit} ta generatsiya\n   Kontentda suv belgisi bo'ladi\n\n💚 <b>Oson</b> — {oson_price} so'm/oy (yoki 29 somoni)\n   • Kuniga {oson_limit} ta generatsiya\n   • Suv belgisiz (no watermark)\n   • Barcha sohalar\n\n💎 <b>Professional</b> — {pro_price} so'm/oy (yoki 79 somoni)\n   • Cheksiz generatsiyalar\n   • Suv belgisiz (no watermark)\n   • Barcha sohalar + Premium tezlik\n\n🏢 <b>Business</b> — {biz_price} so'm/oy\n   • Professional barcha imkoniyatlari\n   • White-label va API kirish",
        "support": "📞 <b>Yordam va Aloqa</b>\n\nSavollaringiz yoki takliflaringiz bormi?\nBizga yozing: @sozanda_support\n\n🤝 Hamkorlik va reklama masalalari bo'yicha:\n@sozanda_admin",
        "history_empty": "📭 Tarix bo'sh. Birinchi kontentingizni yarating!",
        "history_title": "📋 <b>Sizning generatsiyalar tarixingiz</b>\n\n",
        "language_set": "✅ Til o'rnatildi: {lang}",
        "stats": "📊 <b>Sizning statistikangiz</b>\n\n🆔 ID: {user_id}\n🌍 Til: {lang}\n📅 Ro'yxatdan o'tilgan sana: {reg_date}\n\n📈 Bugungi generatsiyalar: {today}/{limit}\n📈 Jami generatsiyalar: {total}\n👥 Taklif qilingan do'stlar: {refs}\n\n💳 Tarif: {plan}",
    }
}


def get_text(user_id: int, key: str, **kwargs) -> str:
    lang = user_languages.get(user_id, "ru")
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def get_niche_display(key: str, lang: str = "ru") -> str:
    from content_engine.niche_manager import get_niche_name
    return get_niche_name(key, lang)


from aiogram.fsm.state import State, StatesGroup

class QuizStates(StatesGroup):
    answering = State()

# ============================================
# ГЛАВНОЕ МЕНЮ — Callback
# ============================================

@router.callback_query(F.data == "main_menu")
async def show_main_menu_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    await callback.answer()
    await callback.message.edit_text(
        get_text(user_id, "main_menu"),
        reply_markup=get_main_menu(lang)
    )


# ============================================
# ГЛАВНОЕ МЕНЮ — Текстовые кнопки
# ============================================

@router.message(F.text.in_([
    "🎬 Контент AI", "🎬 AI Контент", "🎬 AI мундод",
    "🎬 AI Reels/Kreativ", "🎬 AI Reels", "🎬 Reels"
]))
async def reels_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    await message.answer(
        get_text(user_id, "choose_niche"),
        reply_markup=get_niche_menu(lang, country=country)
    )


@router.message(F.text.in_(["📝 Посты", "📝 Постҳо", "📝 Postlar"]))
async def posts_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    # Проверка на суперадмина
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, limit_info = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                get_text(user_id, "limit_reached",
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return
    await message.answer(
        get_text(user_id, "choose_niche"),
        reply_markup=get_niche_menu(lang, country=country)
    )


@router.message(F.text.in_(["📸 Stories", "📸 Сториз"]))
async def stories_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    # Проверка на суперадмина
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, _ = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                get_text(user_id, "limit_reached",
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return
    await message.answer(
        get_text(user_id, "choose_niche"),
        reply_markup=get_niche_menu(lang, country=country)
    )


@router.message(F.text.in_(["💡 Идеи", "💡 Идеяҳо", "💡 G'oyalar"]))
async def ideas_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    # Проверка на суперадмина
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, _ = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                get_text(user_id, "limit_reached",
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return
    await message.answer(
        get_text(user_id, "choose_niche"),
        reply_markup=get_niche_menu(lang, country=country)
    )


@router.message(F.text.in_(["⭐ Premium", "⭐ Премиум", "⭐ Premium obuna", "⭐ Premium тарифҳо"]))
async def premium_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    prices_somoni = {"oson": "29", "pro": "79", "biz": "199"}
    prices_uzs = {
        "oson": f"{TARIFFS['oson'].price_monthly:,}",
        "pro": f"{TARIFFS['pro'].price_monthly:,}",
        "biz": f"{TARIFFS['business'].price_monthly:,}"
    }

    if lang == "uz":
        text = get_text(user_id, "premium_info",
                 free_limit=FREE_DAILY_LIMIT,
                 oson_price=prices_uzs["oson"],
                 oson_limit=OSON_DAILY_LIMIT,
                 pro_price=prices_uzs["pro"],
                 biz_price=prices_uzs["biz"])
    else:
        text = get_text(user_id, "premium_info",
                 free_limit=FREE_DAILY_LIMIT,
                 oson_price=prices_somoni["oson"],
                 oson_limit=OSON_DAILY_LIMIT,
                 pro_price=prices_somoni["pro"],
                 biz_price=prices_somoni["biz"])

    await message.answer(
        text,
        reply_markup=get_subscription_menu(lang),
        parse_mode="HTML"
    )


# ============================================
# РЕФЕРАЛКА — Текстовая кнопка → callback кнопка
# ============================================

@router.message(F.text.in_(["👥 Рефералка", "👥 Даъват", "👥 Давват", "👥 Hamkorlik (Do'stlar)"]))
async def referral_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    builder = InlineKeyboardBuilder()

    if lang == "uz":
        btn_text = "🚀 Taklif dasturiga o'tish"
        prompt = "👇 Takliflar bo'limini ochish uchun quyidagi tugmani bosing:"
    elif lang == "tg":
        btn_text = "🚀 Ба бахши даъват гузаред"
        prompt = "👇 Барои кушодани барномаи даъват тугмаро пахш кунед:"
    else:
        btn_text = "🚀 Перейти к рефералке"
        prompt = "👇 Нажмите кнопку ниже, чтобы открыть реферальную программу:"

    builder.row(InlineKeyboardButton(text=btn_text, callback_data="referral_main"))
    await message.answer(prompt, reply_markup=builder.as_markup())


@router.message(F.text.in_(["📊 Статистика", "📊 Омор", "📊 Statistika"]))
async def stats_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    stats = await get_user_stats(user_id)
    sub = await get_user_subscription(user_id)
    plan_name = "Free"
    if sub:
        if sub.get("plan") == "oson":
            plan_name = "Oson"
        elif sub.get("plan") == "pro":
            plan_name = "Professional"
        elif sub.get("plan") == "business":
            plan_name = "Business"

    await message.answer(
        get_text(user_id, "stats",
                 user_id=user_id,
                 lang="O'zbek tili" if lang == "uz" else ("Тоҷикӣ" if lang == "tg" else "Русский"),
                 reg_date=stats.get("created_at", "N/A"),
                 today=stats.get("today_count", 0),
                 limit=stats.get("daily_limit", FREE_DAILY_LIMIT),
                 total=stats.get("total_count", 0),
                 refs=stats.get("referral_count", 0),
                 plan=plan_name),
        parse_mode="HTML"
    )


@router.message(F.text.in_(["📋 История", "📋 Таърих", "📋 Tarix"]))
async def history_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    history = await get_generation_history(user_id, limit=10)
    if not history:
        await message.answer(get_text(user_id, "history_empty"))
        return
    text = get_text(user_id, "history_title")
    for i, item in enumerate(history, 1):
        text += f"{i}. <b>{item['niche']}</b> — {item['topic'][:50]}...\n"
        text += f"   📅 {item['created_at']}\n\n"
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["🎮 Бизнес-Игра", "🎮 Бозии тиҷорат", "🎮 Biznes o'yini"]))
async def start_business_game(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    from gamification.scenarios import QUIZ_SCENARIOS
    country_scenarios = QUIZ_SCENARIOS.get(country, QUIZ_SCENARIOS["uz"])
    scenario_data = random.choice(country_scenarios)

    # Сохраняем правильный ответ и пояснение в FSM
    await state.set_state(QuizStates.answering)
    await state.update_data(
        correct_option=scenario_data["correct"],
        explanation=scenario_data["explanation"].get(lang, scenario_data["explanation"]["ru"]),
        lang=lang
    )

    # Получаем локализованные тексты
    scenario_text = scenario_data["scenario"].get(lang, scenario_data["scenario"]["ru"])
    options = scenario_data["options"].get(lang, scenario_data["options"]["ru"])

    text = f"<b>🎮 {message.text}</b>\n\n"
    text += f"{scenario_text}\n\n"
    for opt_key, opt_text in options.items():
        text += f"<b>{opt_key}.</b> {opt_text}\n"

    # Клавиатура с вариантами ответа А, Б, В
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="А", callback_data="quiz_ans_A"),
        InlineKeyboardButton(text="Б", callback_data="quiz_ans_B"),
        InlineKeyboardButton(text="В", callback_data="quiz_ans_C")
    )

    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(QuizStates.answering, F.data.startswith("quiz_ans_"))
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    correct_option = data.get("correct_option")
    explanation = data.get("explanation")
    lang = data.get("lang", "ru")

    user_ans = callback.data.replace("quiz_ans_", "")

    if user_ans == correct_option:
        # Начисляем баллы
        from database.models import update_user_xp
        await update_user_xp(user_id, 20)
        if lang == "uz":
            result_msg = "🎉 <b>To'g'ri javob!</b>\n\nSizga 20 XP ball taqdim etildi."
        elif lang == "tg":
            result_msg = "🎉 <b>Ҷавоби дуруст!</b>\n\nШумо 20 XP хол ба даст овардед."
        else:
            result_msg = "🎉 <b>Правильный ответ!</b>\n\nВам начислено 20 баллов опыта (XP)."
    else:
        # Замораживаем/уменьшаем лимиты генерации в качестве штрафа
        from database.models import freeze_or_decrement_limit
        await freeze_or_decrement_limit(user_id)
        if lang == "uz":
            result_msg = f"❌ <b>Noto'g'ri javob!</b> (To'g'ri javob: {correct_option})\n\nJarima sifatida kunlik limitlaringiz kamaytirildi/muzlatildi."
        elif lang == "tg":
            result_msg = f"❌ <b>Ҷавоби нодуруст!</b> (Ҷавоби дуруст: {correct_option})\n\nҲамчун ҷарима лимити генерацияи имрӯзаи шумо кам/ях карда шуд."
        else:
            result_msg = f"❌ <b>Неправильный ответ!</b> (Правильный ответ: {correct_option})\n\nВ качестве штрафа ваши лимиты генераций на сегодня были уменьшены/заморожены."

    if explanation:
        result_msg += f"\n\n💡 {explanation}"

    await callback.message.edit_text(result_msg, parse_mode="HTML")
    await state.clear()
    await callback.answer()


@router.message(F.text.in_(["📞 Поддержка", "📞 Дастгирӣ", "📞 Yordam / Aloqa"]))
async def support_menu(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    await message.answer(get_text(user_id, "support"), parse_mode="HTML")


@router.message(F.text.in_(["⬅️ Назад", "⬅️ Бозгашт", "⬅️ Ortga"]))
async def back_button(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    await message.answer(
        get_text(user_id, "main_menu"),
        reply_markup=get_main_menu(lang)
    )


# ============================================
# ВЫБОР НИШИ
# ============================================

@router.message(lambda msg: is_niche_button(msg.text))
async def niche_selected(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    # Проверка на суперадмина
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, limit_info = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                get_text(user_id, "limit_reached",
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return
    niche_key = get_niche_key_by_text(message.text, country=country)
    user_niches[user_id] = niche_key
    await state.update_data(niche=niche_key)
    await message.answer(
        get_text(user_id, "choose_count"),
        reply_markup=get_count_menu(lang)
    )


# ============================================
# ВЫБОР КОЛИЧЕСТВА ИДЕЙ
# ============================================

@router.message(F.text.regexp(r"^(\d+)\s+(иде(й|я)|идея|идеяҳо|g'oya|ta g'oya)$"))
async def show_topics(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    count = int(message.text.split()[0])

    # Проверка на суперадмина
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, limit_info = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                get_text(user_id, "limit_reached",
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return
        available = limit_info.get("remaining", FREE_DAILY_LIMIT)
        if count > available:
            count = available
            if lang == "uz":
                await message.answer(f"⚠️ Bugun uchun faqat {count} ta generatsiya qoldi.")
            elif lang == "tg":
                await message.answer(f"⚠️ Танҳо {count} генерация барои имрӯз дастрас аст.")
            else:
                await message.answer(f"⚠️ Доступно только {count} генераций на сегодня.")

    user_counts[user_id] = count
    data = await state.get_data()
    niche_key = data.get("niche", user_niches.get(user_id, "other"))
    from content_engine.niche_manager import get_topic_ideas
    topics = await get_topic_ideas(niche_key, count, lang)
    user_topics[user_id] = topics

    if lang == "uz":
        title_text = "📋 Mavzular ro'yxati"
    elif lang == "tg":
        title_text = "📋 Рӯйхати мавзӯъҳо"
    else:
        title_text = "📋 Список тем"

    text = f"{title_text}:\n\n"
    for index, topic in enumerate(topics, start=1):
        text += f"{index}. {topic['title']}\n"
    text += f"\n\n{get_text(user_id, 'choose_topic')}"
    await message.answer(
        text,
        reply_markup=get_topics_keyboard(len(topics), lang)
    )


# ============================================
# ВЫБОР КОНКРЕТНОЙ ТЕМЫ
# ============================================

@router.message(F.text.regexp(r"^\d+$"))
async def open_topic(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"
    user_languages[user_id] = lang

    # Проверка на суперадмина
    is_admin = (str(user_id) == str(ADMIN_ID))
    if not is_admin:
        can_generate, _ = await check_daily_limit(user_id)
        if not can_generate:
            await message.answer(
                get_text(user_id, "limit_reached",
                         ref_bonus=REFERRAL_BONUS_GENERATIONS,
                         oson_limit=OSON_DAILY_LIMIT)
            )
            return
    number = int(message.text)
    topics = user_topics.get(user_id, [])
    if not topics:
        if lang == "uz":
            await message.answer("❌ Avval soha va g'oyalar sonini tanlang.")
        elif lang == "tg":
            await message.answer("❌ Аввал ниша ва шумораи идеяро интихоб кунед.")
        else:
            await message.answer("❌ Сначала выберите нишу и количество идей.")
        return
    if number < 1 or number > len(topics):
        await message.answer(get_text(user_id, "no_topic"))
        return
    topic = topics[number - 1]
    processing_msg = await message.answer(get_text(user_id, "generating"))
    data = await state.get_data()
    niche_key = data.get("niche", user_niches.get(user_id, "other"))
    try:
        content = await generate_ai_content(
            topic=topic["title"],
            niche=niche_key,
            language=lang,
            content_type="reels",
            country=country
        )
        sub = await get_user_subscription(user_id)
        if not sub or sub.get("plan") == "free":
            content += f"\n\n─────────────\n{WATERMARK_TEXT}"
        await processing_msg.delete()
        await message.answer(
            content,
            reply_markup=get_share_keyboard(lang),
            parse_mode="HTML"
        )
        await save_generation(
            user_id=user_id,
            niche=get_niche_display(niche_key, lang),
            topic=topic["title"],
            content=content
        )
        if not is_admin:
            await increment_generation(user_id)
    except Exception as e:
        if lang == "uz":
            err_msg = f"❌ Kontent yaratishda xatolik yuz berdi. Keyinroq urinib ko'ring.\n\n{str(e)[:100]}"
        elif lang == "tg":
            err_msg = f"❌ Хатои генерация. Баъдтар кӯшиш кунед.\n\n{str(e)[:100]}"
        else:
            err_msg = f"❌ Ошибка генерации. Попробуйте позже.\n\n{str(e)[:100]}"
        await processing_msg.edit_text(err_msg)


# ============================================
# CALLBACK: ПОДЕЛИТЬСЯ
# ============================================

@router.callback_query(F.data == "share_content")
async def share_content(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    from database.models import add_bonus_generation
    await add_bonus_generation(user_id, 1)

    if lang == "uz":
        text = "✅ Ulashganingiz uchun +1 generatsiya!"
    elif lang == "tg":
        text = "✅ +1 генерация барои мубодила!"
    else:
        text = "✅ +1 генерация за шеринг!"

    await callback.answer(text, show_alert=True)


# ============================================
# CALLBACK: ПОКУПКА ПОДПИСКИ
# ============================================

@router.callback_query(F.data.startswith("buy_"))
async def buy_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    plan = callback.data.replace("buy_", "")
    await callback.message.answer(
        "💳 Выберите способ оплаты:" if lang == "ru" else ("💳 To'lov usulini tanlang:" if lang == "uz" else "💲 Тарзи пардохтро интихоб кунед:"),
        reply_markup=get_payment_menu(lang, plan)
    )
    await callback.answer()


# ============================================
# АДМИН-КОМАНДЫ
# ============================================

@router.message(Command("admin"))
async def admin_panel(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS and str(user_id) != str(ADMIN_ID):
        return
    stats = await get_user_stats(user_id)
    await message.answer(
        f"""🔧 <b>Админ-панель Sozanda</b>

👥 Всего пользователей: {stats.get('total_users', 'N/A')}
📈 Генераций сегодня: {stats.get('today_generations', 'N/A')}
💰 Платных подписчиков: {stats.get('paid_users', 'N/A')}

Команды:
/stats — общая статистика
/broadcast — рассылка
/add_niche — добавить нишу""",
        parse_mode="HTML"
    )


# ============================================
# ОБРАБОТКА НЕИЗВЕСТНЫХ СООБЩЕНИЙ
# ============================================

@router.message()
async def unknown_message(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    user_languages[user_id] = lang

    if lang == "uz":
        text = "❓ Buyruqni tushunmadim. Pastdagi menudan foydalaning."
    elif lang == "tg":
        text = "❓ Ман фармонро нафаҳмидам. Аз менюи поён истифода баред."
    else:
        text = "❓ Я не понял команду. Используйте меню ниже."

    await message.answer(text, reply_markup=get_main_menu(lang))
