# states/content_states.py — Машина состояний (FSM) бота Sozanda
# Для Таджикистана: контент, подписки, рефералка, админка

from aiogram.fsm.state import State, StatesGroup


# ============================================
# ОСНОВНЫЕ СОСТОЯНИЯ КОНТЕНТА
# ============================================

class ContentStates(StatesGroup):
    """
    Состояния для воронки генерации контента
    """

    # Главное меню
    main_menu = State()

    # Выбор языка (при первом входе)
    language_selection = State()

    # Выбор типа контента (Reels, Post, Stories, Ideas, Hook, Caption)
    content_type_menu = State()

    # Выбор ниши бизнеса
    niche_menu = State()

    # Выбор количества идей
    count_menu = State()

    # Просмотр списка тем
    topics_menu = State()

    # Просмотр сгенерированного контента
    content_view = State()

    # Подтверждение / шеринг контента
    content_share = State()

    # История генераций
    history_view = State()


# ============================================
# СОСТОЯНИЯ ПОДПИСКИ / МОНЕТИЗАЦИИ
# ============================================

class SubscriptionStates(StatesGroup):
    """
    Состояния для оформления и управления подписками
    """

    # Просмотр тарифов
    plans_menu = State()

    # Выбор способа оплаты
    payment_method = State()

    # Ожидание подтверждения оплаты
    payment_pending = State()

    # Подтверждение оплаты админом (для ручных платежей)
    payment_confirm = State()

    # Успешная оплата
    payment_success = State()

    # Управление текущей подпиской
    manage_subscription = State()

    # Отмена подписки
    cancel_subscription = State()


# ============================================
# СОСТОЯНИЯ РЕФЕРАЛЬНОЙ СИСТЕМЫ
# ============================================

class ReferralStates(StatesGroup):
    """
    Состояния для реферальной программы
    """

    # Просмотр реферальной статистики
    referral_menu = State()

    # Просмотр списка приглашённых
    referral_list = State()

    # Вывод бонусов
    referral_withdraw = State()


# ============================================
# СОСТОЯНИЯ ПОДДЕРЖКИ
# ============================================

class SupportStates(StatesGroup):
    """
    Состояния для обращений в поддержку
    """

    # Главное меню поддержки
    support_menu = State()

    # Написание сообщения в поддержку
    support_message = State()

    # Ожидание ответа от поддержки
    support_wait = State()

    # Оценка качества поддержки
    support_rate = State()


# ============================================
# СОСТОЯНИЯ АДМИН-ПАНЕЛИ
# ============================================

class AdminStates(StatesGroup):
    """
    Состояния для администраторов бота
    """

    # Главное меню админа
    admin_main = State()

    # Просмотр статистики
    admin_stats = State()

    # Рассылка всем пользователям
    admin_broadcast = State()

    # Подтверждение рассылки
    admin_broadcast_confirm = State()

    # Управление нишами
    admin_niches = State()

    # Добавление новой ниши
    admin_add_niche = State()

    # Редактирование ниши
    admin_edit_niche = State()

    # Управление пользователями
    admin_users = State()

    # Просмотр пользователя
    admin_user_detail = State()

    # Управление платежами
    admin_payments = State()

    # Подтверждение платежа
    admin_payment_confirm = State()

    # Отправка контента дня
    admin_content_day = State()

    # Настройки бота
    admin_settings = State()


# ============================================
# СОСТОЯНИЯ ПРОФИЛЯ
# ============================================

class ProfileStates(StatesGroup):
    """
    Состояния для личного кабинета пользователя
    """

    # Главное меню профиля
    profile_menu = State()

    # Просмотр статистики
    profile_stats = State()

    # Изменение языка
    profile_language = State()

    # Изменение настроек уведомлений
    profile_notifications = State()


# ============================================
# СОСТОЯНИЯ ОПЛАТЫ (детальные)
# ============================================

class PaymentStates(StatesGroup):
    """
    Детальные состояния для процесса оплаты
    """

    # Выбор тарифа
    select_plan = State()

    # Alif Mobi
    alif_pay = State()
    alif_pay_confirm = State()

    # Humo
    humo_pay = State()
    humo_pay_confirm = State()

    # Eskhata
    eskhata_pay = State()
    eskhata_pay_confirm = State()

    # Crypto (USDT)
    crypto_pay = State()
    crypto_pay_confirm = State()

    # Telegram Stars
    stars_pay = State()
    stars_pay_confirm = State()


# ============================================
# СОСТОЯНИЯ ЕЖЕДНЕВНОГО КОНТЕНТА
# ============================================

class DailyContentStates(StatesGroup):
    """
    Состояния для ежедневного контента и челленджей
    """

    # Контент дня
    content_of_day = State()

    # Челлендж
    challenge_menu = State()
    challenge_day = State()
    challenge_complete = State()


# ============================================
# УТИЛИТА: Получить все состояния для middleware
# ============================================

def get_all_states() -> list:
    """Вернуть список всех групп состояний для проверок"""

    return [
        ContentStates,
        SubscriptionStates,
        ReferralStates,
        SupportStates,
        AdminStates,
        ProfileStates,
        PaymentStates,
        DailyContentStates,
    ]


def get_state_name(state) -> str:
    """Получить читаемое название состояния"""

    state_map = {
        # ContentStates
        "ContentStates:main_menu": "Главное меню",
        "ContentStates:language_selection": "Выбор языка",
        "ContentStates:content_type_menu": "Выбор типа контента",
        "ContentStates:niche_menu": "Выбор ниши",
        "ContentStates:count_menu": "Выбор количества",
        "ContentStates:topics_menu": "Список тем",
        "ContentStates:content_view": "Просмотр контента",
        "ContentStates:content_share": "Шеринг контента",
        "ContentStates:history_view": "История",

        # SubscriptionStates
        "SubscriptionStates:plans_menu": "Тарифы",
        "SubscriptionStates:payment_method": "Способ оплаты",
        "SubscriptionStates:payment_pending": "Ожидание оплаты",
        "SubscriptionStates:payment_confirm": "Подтверждение оплаты",
        "SubscriptionStates:payment_success": "Успешная оплата",
        "SubscriptionStates:manage_subscription": "Управление подпиской",
        "SubscriptionStates:cancel_subscription": "Отмена подписки",

        # AdminStates
        "AdminStates:admin_main": "Админ-панель",
        "AdminStates:admin_stats": "Статистика",
        "AdminStates:admin_broadcast": "Рассылка",
        "AdminStates:admin_broadcast_confirm": "Подтверждение рассылки",
        "AdminStates:admin_niches": "Ниши",
        "AdminStates:admin_add_niche": "Добавление ниши",
        "AdminStates:admin_edit_niche": "Редактирование ниши",
        "AdminStates:admin_users": "Пользователи",
        "AdminStates:admin_user_detail": "Детали пользователя",
        "AdminStates:admin_payments": "Платежи",
        "AdminStates:admin_payment_confirm": "Подтверждение платежа",
        "AdminStates:admin_content_day": "Контент дня",
        "AdminStates:admin_settings": "Настройки",

        # ProfileStates
        "ProfileStates:profile_menu": "Профиль",
        "ProfileStates:profile_stats": "Статистика профиля",
        "ProfileStates:profile_language": "Смена языка",
        "ProfileStates:profile_notifications": "Уведомления",

        # Default
        "None": "Без состояния",
    }

    state_str = str(state)
    return state_map.get(state_str, state_str)