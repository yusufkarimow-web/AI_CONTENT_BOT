# content_engine/subscription.py — Подписки и оплата (v2.0)
# Поддержка RU, TG, UZ. Работает с Alif, Humo, Click, Payme, UZCARD + WhatsApp Link

import urllib.parse
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import (
    ADMIN_IDS, ALIF_ENABLED, HUMO_ENABLED,
    CRYPTO_PAY_ENABLED, ACTIVE_PAYMENTS,
    ALIF_CARD_NUMBER, WHATSAPP_NUMBER, TARIFFS
)
from database.models import get_user, get_user_subscription, create_subscription
from keyboards.subscription_menu import (
    get_subscription_menu, get_payment_menu,
    get_payment_confirm_keyboard, get_alif_payment_keyboard
)
from keyboards.main_menu_content import get_main_menu

router = Router()

# ============================================
# ДИНАМИЧЕСКИЕ НАСТРОЙКИ СВЯЗИ
# ============================================
ADMIN_USERNAME = "sozanda_admin"

def get_whatsapp_link(plan_name: str, price_text: str, user_id: int) -> str:
    """Генерирует прямую ссылку на WhatsApp с готовым текстом обращения"""
    clean_phone = WHATSAPP_NUMBER.replace("+", "").replace(" ", "").replace("-", "").strip()
    message = f"Здравствуйте! Я хочу активировать подписку {plan_name} за {price_text} в Sozanda Bot. Мой Telegram ID: {user_id}"
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"

# ============================================
# ПРОСМОТР ТАРИФОВ
# ============================================

@router.message(F.text.in_([
    "⭐ Premium", "⭐ Премиум", "⭐ Premium obuna",
    "⭐ Премиум тарифҳо", "⭐ Premium тарифҳо"
]))
async def show_plans(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"
    country = user.get("country", "uz") if user else "uz"

    prices = {
        "oson": TARIFFS["oson"].price_monthly,
        "pro": TARIFFS["pro"].price_monthly,
        "business": TARIFFS["business"].price_monthly,
    }

    if lang == "uz":
        text = f"""⭐ <b>Premium obunalar</b>

🆓 <b>Free</b> — kuniga 3 ta generatsiya
   Suv belgisi (watermark) bilan

💚 <b>Oson</b> — <code>{prices['oson']:,}</code> UZS/oy (yoki 29 somoni)
   • Kuniga 20 ta generatsiya
   • Suv belgisiz (no watermark)
   • Barcha sohalar (nishalar)

💎 <b>Professional</b> — <code>{prices['pro']:,}</code> UZS/oy (yoki 79 somoni)
   • Cheksiz generatsiyalar
   • Suv belgisiz (no watermark)
   • Barcha sohalar + Premium tezlik

🏢 <b>Business</b> — <code>{prices['business']:,}</code> UZS/oy (yoki 199 somoni)
   • Professional barcha imkoniyatlari
   • White-label va API kirish

💳 To'lov usullari: Click, Payme, UZCARD, HUMO, Alif Mobi, USDT"""

    elif lang == "tg":
        text = f"""⭐ <b>Обунаҳои Premium</b>

🆓 <b>Free</b> — 3 генерация/рӯз
   Нишони обуна (watermark)

💚 <b>Oson</b> — <code>{29}</code> сомонӣ/моҳ
   • 20 генерация/рӯз
   • Бе watermark
   • Ҳама нишаҳо

💎 <b>Professional</b> — <code>{79}</code> сомонӣ/моҳ
   • Беҳад генерация
   • Бе watermark
   • Ҳама нишаҳо + аввалият

🏢 <b>Business</b> — <code>{199}</code> сомонӣ/моҳ
   • Ҳама аз Professional
   • White-label + API

💳 Тарзи пардохт: Alif Mobi, Humo, UZCARD, USDT"""
    else:
        # Русский язык с учетом страны пользователя
        if country == "uz":
            text = f"""⭐ <b>Premium подписки (Узбекистан)</b>

🆓 <b>Free</b> — 3 генерации/день
   Водяной знак на контенте

💚 <b>Oson</b> — <code>{prices['oson']:,}</code> UZS/мес
   • 20 генераций/день
   • Без водяного знака
   • Все ниши

💎 <b>Professional</b> — <code>{prices['pro']:,}</code> UZS/мес
   • Безлимит генераций
   • Без водяного знака
   • Все ниши + приоритетная скорость

🏢 <b>Business</b> — <code>{prices['business']:,}</code> UZS/мес
   • Всё из Professional
   • White-label и API доступ

💳 Способы оплаты: Click, Payme, UZCARD, HUMO, USDT"""
        else:
            text = f"""⭐ <b>Premium подписки (Таджикистан)</b>

🆓 <b>Free</b> — 3 генерации/день
   Водяной знак на контенте

💚 <b>Oson</b> — <code>{29}</code> сомони/мес
   • 20 генераций/день
   • Без водяного знака
   • Все ниши

💎 <b>Professional</b> — <code>{79}</code> сомони/мес
   • Безлимит генераций
   • Без водяного знака
   • Все ниши + приоритетная скорость

🏢 <b>Business</b> — <code>{199}</code> сомони/мес
   • Всё из Professional
   • White-label и API доступ

💳 Способы оплаты: Alif Mobi, Душанбе Сити, Humo, USDT"""

    await message.answer(text, reply_markup=get_subscription_menu(lang), parse_mode="HTML")


# ============================================
# ВЫБОР ТАРИФА → СПОСОБ ОПЛАТЫ
# ============================================

@router.callback_query(F.data.startswith("buy_"))
async def select_payment(callback: CallbackQuery):
    plan = callback.data.replace("buy_", "")

    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    # Проверяем, не активен ли уже тариф
    sub = await get_user_subscription(user_id)
    if sub and sub.get("plan") == plan and sub.get("is_active"):
        if lang == "uz":
            text = "✅ Sizda ushbu tarif allaqachon faollashtirilgan!"
        elif lang == "tg":
            text = "✅ Шумо аллакай ин тарифро доред!"
        else:
            text = "✅ У вас уже активен этот тариф!"
        await callback.answer(text, show_alert=True)
        return

    await callback.message.edit_text(
        "💳 Выберите способ оплаты:" if lang == "ru" else ("Sizga qulay to'lov usulini tanlang:" if lang == "uz" else "💲 Тарзи пардохтро интихоб кунед:"),
        reply_markup=get_payment_menu(lang, plan)
    )
    await callback.answer()


# ============================================
# ВЫБОР СПОСОБА ОПЛАТЫ
# ============================================

@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    data = callback.data.replace("pay_", "").split("_")
    method = data[0]
    plan = data[1] if len(data) > 1 else "oson"

    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    # Проверяем, доступен ли способ оплаты
    if method == "alif" and not ALIF_ENABLED:
        await _show_manual_payment(callback, method, plan, lang)
        return

    if method in ["humo", "eskhata"] and not HUMO_ENABLED:
        await _show_coming_soon(callback, method, lang)
        return

    if method == "crypto" and not CRYPTO_PAY_ENABLED:
        await _show_coming_soon(callback, method, lang)
        return

    if method == "stars":
        await _show_coming_soon(callback, method, lang)
        return

    # Alif работает — показываем реальную оплату
    if method == "alif":
        await _show_alif_payment(callback, plan, lang)
        return

    # UZCARD/Click/Payme для Узбекистана
    if method == "uzcard":
        await _show_uzcard_payment(callback, plan, lang)
        return

    # Fallback
    await _show_manual_payment(callback, method, plan, lang)


# ============================================
# ALIF ОПЛАТА (РАБОЧАЯ)
# ============================================

async def _show_alif_payment(callback: CallbackQuery, plan: str, lang: str):
    """Показывает реальные реквизиты Alif для оплаты"""

    price = 29 if plan == "oson" else (79 if plan == "pro" else 199)
    plan_name = {"oson": "Oson", "pro": "Professional", "business": "Business"}.get(plan, plan)

    if lang == "uz":
        text = f"""💳 <b>Alif Mobi orqali to'lov</b>

📋 <b>To'lov ma'lumotlari:</b>
• Tarif: {plan_name}
• Summa: <code>{price}</code> somoni (yoki unga teng UZS)
• Karta raqami: <code>{ALIF_CARD_NUMBER}</code>
• Nomi: SOZANDA BOT

📝 <b>Qanday to'lanadi:</b>
1. Alif Mobi ilovasini oching
2. "Перевод" bo'limini tanlang
3. Yuqoridagi karta raqamini kiriting
4. Summani kiritib, to'lovni tasdiqlang
5. To'lov chekini (skrinshot) adminga yuboring

⏳ Tekshirilgandan so'ng tarif faollashadi (1-5 daqiqa)"""
    elif lang == "tg":
        text = f"""💳 <b>Пардохт тавассути Alif Mobi</b>

📋 <b>Маълумоти пардохт:</b>
• Тариф: {plan_name}
• Сумма: <code>{price}</code> сомонӣ
• Корт: <code>{ALIF_CARD_NUMBER}</code>
• Ном: SOZANDA BOT

📝 <b>Тартиби пардохт:</b>
1. Alif Mobi кушоед
2. "Перевод" -ро интихоб кунед
3. Рақами кортро ворид кунед
4. Суммаро тасдиқ кунед
5. Скриншоти пардохт фиристед

⏳ Пас аз санҷиш, тариф фаъол мешавад (1-5 дақиқа)"""
    else:
        text = f"""💳 <b>Оплата через Alif Mobi / Card</b>

📋 <b>Реквизиты:</b>
• Тариф: {plan_name}
• Сумма: <code>{price}</code> сомони
• Карта Alif: <code>{ALIF_CARD_NUMBER}</code>
• Получатель: SOZANDA BOT

📝 <b>Как оплатить:</b>
1. Откройте Alif Mobi или любой мобильный банк
2. Выберите "Перевод на карту"
3. Введите номер карты выше
4. Подтвердите сумму
5. Пришлите скриншот оплаты

⏳ После проверки тариф активируется (1-5 минут)"""

    # Создаем красивую кнопку связи через WhatsApp и Telegram
    wa_link = get_whatsapp_link(plan_name, f"{price} somoni", callback.from_user.id)
    buttons = [
        [InlineKeyboardButton(text="✅ Ман пардохт кардам" if lang == "tg" else ("✅ To'lov qildim" if lang == "uz" else "✅ Я оплатил"), callback_data=f"payment_done_alif_{plan}")],
        [InlineKeyboardButton(text="💬 WhatsApp Support 🟢" if lang == "ru" else "💬 WhatsApp Дастгирӣ 🟢", url=wa_link)],
        [InlineKeyboardButton(text="💬 Telegram Support 🔵", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton(text="⬅️ Бозгашт" if lang == "tg" else ("⬅️ Ortga" if lang == "uz" else "⬅️ Назад"), callback_data="pay_back")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
    await callback.answer()


# ============================================
# UZCARD / CLICK / PAYME (ДЛЯ УЗБЕКИСТАНА)
# ============================================

async def _show_uzcard_payment(callback: CallbackQuery, plan: str, lang: str):
    """Показывает реквизиты UZCARD/HUMO для ручной оплаты в Узбекистане"""

    price_uzs = TARIFFS[plan].price_monthly
    plan_name = {"oson": "Oson", "pro": "Professional", "business": "Business"}.get(plan, plan)

    # Используем номер карты Alif или пишем универсальное сообщение о переводе
    if lang == "uz":
        text = f"""💳 <b>UZCARD / HUMO (Click / Payme) orqali to'lov</b>

📋 <b>To'lov ma'lumotlari:</b>
• Tarif: {plan_name}
• Summa: <code>{price_uzs:,}</code> UZS
• To'lov usuli: Click / Payme / UZCARD transfer

⚠️ <b>To'lovni amalga oshirish uchun adminga yozing yoki quyidagi WhatsApp/Telegram havolasidan foydalaning.</b>

📝 <b>Sizga darhol to'lov kartasi va chekni qabul qilish havolasi yuboriladi:</b>
1. Quyidagi qo'llab-quvvatlash tugmalaridan birini bosing
2. To'lov rekvizitlarini oling va o'tkazmani bajaring
3. Chekni yuboring, tarifingiz 1-5 daqiqada faollashadi!"""
    else:
        text = f"""💳 <b>Оплата через UZCARD / HUMO (Узбекистан)</b>

📋 <b>Детали платежа:</b>
• Тариф: {plan_name}
• Сумма: <code>{price_uzs:,}</code> UZS

⚠️ <b>Для получения реквизитов UZCARD/HUMO обратитесь в службу поддержки.</b>

📝 <b>Инструкция:</b>
1. Нажмите кнопку поддержки ниже (WhatsApp или Telegram)
2. Получите номер карты для перевода
3. Отправьте скриншот чека, и мы сразу активируем тариф!"""

    wa_link = get_whatsapp_link(plan_name, f"{price_uzs:,} UZS", callback.from_user.id)
    buttons = [
        [InlineKeyboardButton(text="💬 Написать в WhatsApp 🟢" if lang == "ru" else "💬 WhatsApp orqali yozish 🟢", url=wa_link)],
        [InlineKeyboardButton(text="💬 Написать в Telegram 🔵" if lang == "ru" else "💬 Telegram orqali yozish 🔵", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton(text="✅ To'lov qildim (Chekni yubordim)" if lang == "uz" else "✅ Я оплатил (Отправил чек)", callback_data=f"payment_done_uzcard_{plan}")],
        [InlineKeyboardButton(text="⬅️ Ortga" if lang == "uz" else "⬅️ Назад", callback_data="pay_back")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
    await callback.answer()


# ============================================
# РУЧНАЯ ОПЛАТА (FALLBACK)
# ============================================

async def _show_manual_payment(callback: CallbackQuery, method: str, plan: str, lang: str):
    """Ручная оплата с инструкцией"""

    price = 29 if plan == "oson" else (79 if plan == "pro" else 199)
    price_text = f"{price} сомони" if lang != "uz" else f"{TARIFFS[plan].price_monthly:,} UZS"
    plan_name = {"oson": "Oson", "pro": "Professional", "business": "Business"}.get(plan, plan)

    method_names = {
        "alif": "Alif Mobi",
        "humo": "Humo Online",
        "eskhata": "Eskhata",
        "crypto": "USDT (TRC-20)",
        "stars": "Telegram Stars"
    }

    if lang == "uz":
        text = f"""💳 <b>Qo'lda to'lash — {method_names.get(method, method)}</b>

📋 <b>Ma'lumotlar:</b>
• Tarif: {plan_name}
• Summa: {price_text}
• To'lov turi: {method_names.get(method, method)}

⚠️ <b>Avtomatik to'lov vaqtincha ishlamayapti.</b>

📝 <b>Nima qilish kerak:</b>
1. To'lovni quyidagi qo'llab-quvvatlash bo'limi orqali kelishib oling
2. To'lov skrinshotini yuboring
3. Tarif 5-10 daqiqada faollashadi!"""
    elif lang == "tg":
        text = f"""💳 <b>Пардохти дастӣ — {method_names.get(method, method)}</b>

📋 <b>Маълумот:</b>
• Тариф: {plan_name}
• Сумма: {price_text}
• Тарз: {method_names.get(method, method)}

⚠️ <b>Пардохти автоматикӣ муваққатан дастрас нест.</b>

📝 <b>Чӣ кор кунед:</b>
1. Пардохтро ба корт ё тавассути админ гузаронед
2. Скриншот фиристед ба админ
3. Дар 5-10 дақиқа тариф фаъол мешавад"""
    else:
        text = f"""💳 <b>Ручная оплата — {method_names.get(method, method)}</b>

📋 <b>Информация:</b>
• Тариф: {plan_name}
• Сумма: {price_text}
• Способ: {method_names.get(method, method)}

⚠️ <b>Автоматическая оплата временно недоступна.</b>

📝 <b>Что делать:</b>
1. Совершите перевод через поддержку
2. Пришлите скриншот чека администратору
3. В течение 5-10 минут тариф будет активирован!"""

    wa_link = get_whatsapp_link(plan_name, price_text, callback.from_user.id)
    buttons = [
        [InlineKeyboardButton(text="💬 WhatsApp 🟢", url=wa_link)],
        [InlineKeyboardButton(text="💬 Telegram 🔵", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton(text="✅ To'lov qildim" if lang == "uz" else ("✅ Ман пардохт кардам" if lang == "tg" else "✅ Я оплатил"), callback_data=f"payment_done_manual_{plan}")],
        [InlineKeyboardButton(text="⬅️ Ortga" if lang == "uz" else ("⬅️ Бозгашт" if lang == "tg" else "⬅️ Назад"), callback_data="pay_back")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
    await callback.answer()


# ============================================
# СКОРО БУДЕТ ДОСТУПНО
# ============================================

async def _show_coming_soon(callback: CallbackQuery, method: str, lang: str):
    """Показывает 'Скоро будет доступно'"""

    method_names = {
        "humo": "Humo Online",
        "eskhata": "Eskhata",
        "crypto": "USDT (TRC-20)",
        "stars": "Telegram Stars"
    }
    name = method_names.get(method, method)

    if lang == "uz":
        text = f"""⏳ <b>{name} — Tez kunda ishga tushadi</b>

Ushbu to'lov usuli hozirda sozlanmoqda.

💳 Hozirda siz <b>Click/Payme, UZCARD, Alif Mobi</b> orqali to'lashingiz mumkin."""
    elif lang == "tg":
        text = f"""⏳ <b>{name} — дар ҳоли тайёрӣ</b>

Ин усули пардохт ба зудӣ дастрас мешавад.

💳 Ҳоло метавонед тавассути <b>Alif Mobi</b> пардохт кунед."""
    else:
        text = f"""⏳ <b>{name} — скоро в работе</b>

Этот способ оплаты скоро будет доступен.

💳 Сейчас можно оплатить через <b>Alif Mobi</b> или <b>Click/Payme</b>."""

    await callback.message.edit_text(
        text,
        reply_markup=get_payment_menu(lang, "oson"),  # Возвращаем к выбору
        parse_mode="HTML"
    )
    await callback.answer()


# ============================================
# ПОДТВЕРЖДЕНИЕ ОПЛАТЫ
# ============================================

@router.callback_query(F.data.startswith("payment_done_"))
async def confirm_payment_done(callback: CallbackQuery):
    payment_id = callback.data.replace("payment_done_", "")

    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    # Отправляем уведомление админу
    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                admin_id,
                f"""🔔 <b>Новый платёж на проверку!</b>

👤 Пользователь: {user_id}
📝 ID платежа: {payment_id}
📱 @{callback.from_user.username or 'нет username'}

⚡ Проверьте и активируйте тариф.""",
                parse_mode="HTML"
            )
        except Exception:
            pass

    if lang == "uz":
        text = """⏳ <b>To'lov tekshirishga yuborildi!</b>

Admin to'lovni 1-10 daqiqa ichida tekshiradi.

📩 Tezoq faollashtirish uchun to'lov chekini (skrinshot) @sozanda_admin ga yuboring."""
    elif lang == "tg":
        text = """⏳ <b>Пардохт фиристода шуд!</b>

Админ санҷиш мекунад (1-10 дақиқа).

📩 Скриншоти пардохтро ба @sozanda_admin фиристед барои зудтарин коркард."""
    else:
        text = """⏳ <b>Платёж отправлен на проверку!</b>

Админ проверит в течение 1-10 минут.

📩 Пришлите скриншот оплаты @sozanda_admin для ускорения."""

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer("✅ Отправлено админу" if lang == "ru" else "✅ Yuborildi", show_alert=True)


@router.callback_query(F.data == "payment_cancel")
async def cancel_payment(callback: CallbackQuery):
    """Отмена оплаты — возврат в меню"""
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    await callback.message.edit_text(
        "❌ To'lov bekor qilindi." if lang == "uz" else ("❌ Пардохт бекор шуд." if lang == "tg" else "❌ Оплата отменена."),
        reply_markup=get_subscription_menu(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "pay_back")
async def back_to_plans(callback: CallbackQuery):
    """Назад к выбору тарифов"""
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ru") if user else "ru"

    await callback.message.edit_text(
        "⭐ Premium obunalar:" if lang == "uz" else ("⭐ Premium тарифҳо:" if lang == "tg" else "⭐ Premium тарифы:"),
        reply_markup=get_subscription_menu(lang)
    )
    await callback.answer()
