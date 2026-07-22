# ИНСТРУКЦИЯ И МАСТЕР-ПРОМПТ ДЛЯ ИИ: СОЗДАНИЕ ТЕЛЕГРАМ-ПЛАТФОРМЫ И TMA «TOJIKAI SMM PLATFORM» С ИНТЕГРАЦИЕЙ WHATSAPP

> **Уважаемый ИИ!** Твоя задача — сгенерировать под ключ 100% готовую к продакшену, масштабируемую, мультиязычную Telegram-платформу со встроенным веб-приложением (**Telegram Mini App — TMA**) и автоматической рассылкой в **WhatsApp**.
> Все файлы, модели данных, API-роуты, хэндлеры, интерфейсы веб-приложения и интеграционные адаптеры должны быть написаны без плейсхолдеров, заглушек или сокращений.

---

# ЧАСТЬ 1: ЦЕЛЕВАЯ АРХИТЕКТУРА И ДИЗАЙН-СИСТЕМА

```
                                  [ ПОЛЬЗОВАТЕЛЬ (Telegram Client) ]
                                                  │
                         ┌────────────────────────┴────────────────────────┐
                         ▼                                                 ▼
               ┌──────────────────┐                              ┌──────────────────┐
               │   Telegram Bot   │                              │ Telegram WebApp  │
               │ (aiogram Webhook)│                              │ (TMA - Frontend) │
               └─────────┬────────┘                              └─────────┬────────┘
                         │                                                 │
                         │             ┌────────────────────────┐          │
                         └────────────►│  FastAPI Web Gateway   │◄─────────┘
                                       │ (API / HMAC Webhooks)  │
                                       └───────────┬────────────┘
                                                   │
                ┌──────────────────────────────────┼──────────────────────────────────┐
                ▼                                  ▼                                  ▼
      ┌──────────────────┐               ┌──────────────────┐               ┌──────────────────┐
      │  Domain Services │               │ Data Repositories│               │ External Adapters│
      │ ─ SMM Generator  │               │ ─ PostgreSQL     │               │ ─ WhatsApp API   │
      │ ─ Billing Engine │               │ ─ Redis FSM/Locks│               │ ─ Click/Payme    │
      │ ─ Gamification   │               │ ─ Alembic Schema │               │ ─ Alif Mobi      │
      └──────────────────┘               └──────────────────┘               └──────────────────┘
```

## 1.1 Модульный Монолит (Modular Monolith)
Платформа строится по принципу модульного монолита на базе **FastAPI (Python 3.11+)** для бэкенда и **React / Vue / Alpine.js + Tailwind CSS** для фронтенда Telegram Mini App.

### Структура Директорий Проекта:
```
tojikai_platform/
├── alembic/                  # Миграции базы данных
├── app/
│   ├── __init__.py
│   ├── main.py               # Точка входа FastAPI (интегрирует Bot Webhook, WhatsApp Webhook, Web API)
│   ├── core/
│   │   ├── config.py         # Настройки pydantic-settings (.env.example)
│   │   ├── container.py      # IoC контейнер и менеджмент зависимостей
│   │   └── errors.py         # Глобальные доменные ошибки
│   ├── db/
│   │   ├── connection.py     # Асинхронное подключение SQLAlchemy
│   │   ├── models.py         # Описание всех таблиц БД
│   │   └── session.py        # Жизненный цикл сессий БД
│   ├── api/                  # Эндпоинты бэкенда для TMA и Webhooks
│   │   ├── routes.py
│   │   ├── whatsapp_webhooks.py
│   │   └── payments.py       # Адаптеры Click, Payme, Alif
│   ├── bot/                  # Логика Telegram Бота (aiogram v3)
│   │   ├── handlers.py       # Основные команды, fallback, Q&A Assistant
│   │   ├── keyboards.py      # Клавиатуры бота
│   │   └── states.py         # Состояния aiogram FSM
│   ├── services/             # Бизнес-логика
│   │   ├── ai_generator.py   # Промптинг, хуки, разделение UZ/TJ
│   │   ├── generation_service.py # Резервирование квот и транзакции
│   │   ├── whatsapp_service.py   # Сервис отправки в WhatsApp
│   │   ├── billing_service.py    # Логика тарифов, подписок, лимитов
│   │   └── pdf_generator.py  # ReportLab генерация PDF с кириллицей (DejaVuSans)
│   ├── gamification/         # TojikAI Empire (Бизнес Империя)
│   │   ├── engine.py         # Логика игры, начисление пассивного дохода
│   │   └── actions.py        # Покупка бизнесов, наем рабочих, ивенты
│   └── static/               # TMA Фронтенд (HTML/JS/CSS статика)
│       ├── index.html        # Главный SPA-интерфейс Mini App
│       ├── app.js            # Логика TMA (авторизация через tg.initData, API-запросы)
│       └── assets/           # Логотипы (tojikai_logo_3d.png) и шрифты
├── tests/                    # Pytest тесты ( unit, integration, e2e )
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## 1.2 UX/UI Дизайн-Система для Telegram Mini App (TMA)
Фронтенд TMA должен быть бесшовным расширением интерфейса Telegram. Он должен идеально адаптироваться под цветовую схему пользователя через Telegram WebApp Theme CSS variables.

### Эстетические Требования:
- **Цветовая палитра:** Использование CSS-переменных Telegram (`var(--tg-theme-bg-color)`, `var(--tg-theme-text-color)`, `var(--tg-theme-button-color)` и т.д.).
- **Сетка и Отступы:** Использование `px-4 py-3` на мобильных экранах. Контейнеры со скруглением `rounded-2xl` или `rounded-xl`.
- **Интерактивные анимации:** Легкие CSS transitions (`transition-all duration-300`) при клике на кнопки. Плавные скелетоны (`animate-pulse`) во время ожидания AI-генерации.
- **Брендинг:** По центру верхней панели логотип `tojikai_logo_3d.png` с эффектом мягкого неонового свечения вокруг.

---

# ЧАСТЬ 2: ПОЛНАЯ ДОМЕННАЯ МОДЕЛЬ БАЗЫ ДАННЫХ (PostgreSQL)

База данных должна быть полностью нормализована вокруг сущностей пользователей, рабочих пространств (Workspaces) и транзакционных логов квот.

```sql
-- Таблица пользователей
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(64),
    first_name VARCHAR(128),
    whatsapp_number VARCHAR(32), -- Номер WhatsApp пользователя для отправки контента
    language VARCHAR(8) DEFAULT 'ru', -- ru, tg, uz
    country VARCHAR(8) DEFAULT 'uz',  -- uz, tj, ru
    last_seen_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Таблица рабочих пространств (поддержка командной работы)
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    country VARCHAR(8) DEFAULT 'uz',
    timezone VARCHAR(64) DEFAULT 'Asia/Tashkent',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Членство в рабочих пространствах
CREATE TABLE memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    role VARCHAR(16) DEFAULT 'owner', -- owner, admin, member
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_membership_user_workspace UNIQUE (user_id, workspace_id)
);

-- Тарифы и подписки
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    plan_code VARCHAR(32) DEFAULT 'free', -- free, starter, pro, team
    status VARCHAR(16) DEFAULT 'active',  -- active, past_due, cancelled, expired
    current_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    current_period_end TIMESTAMP WITH TIME ZONE, -- NULL для вечного free
    provider VARCHAR(32), -- click, payme, alif, manual
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Логи генераций
CREATE TABLE generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_type VARCHAR(32) NOT NULL, -- reels, posts, stories, content_plan, smm_package
    language VARCHAR(8) NOT NULL,
    country VARCHAR(8) NOT NULL,
    brief TEXT NOT NULL,
    niche VARCHAR(64),
    platform VARCHAR(32),
    goal VARCHAR(64),
    format VARCHAR(32),
    status VARCHAR(16) DEFAULT 'pending', -- pending, completed, failed, cancelled
    output_text TEXT,
    pdf_url VARCHAR(256),
    whatsapp_sent_status VARCHAR(16) DEFAULT 'not_sent', -- not_sent, sent, failed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Журнал транзакционного списания лимитов (Quota Ledger)
CREATE TABLE usage_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    generation_id UUID REFERENCES generations(id) ON DELETE SET NULL,
    metric VARCHAR(32) DEFAULT 'generation',
    units INT DEFAULT 1,
    status VARCHAR(16) DEFAULT 'reserved', -- reserved, committed, reversed
    idempotency_key VARCHAR(128) UNIQUE NOT NULL,
    description VARCHAR(256),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Таблица платежей
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
    provider VARCHAR(32) NOT NULL, -- click, payme, alif
    provider_event_id VARCHAR(128),
    reference VARCHAR(64) UNIQUE NOT NULL,
    plan_code VARCHAR(32) NOT NULL,
    status VARCHAR(16) DEFAULT 'pending', -- pending, paid, failed, cancelled
    amount_minor INT NOT NULL, -- в тиинах, пулах, копейках
    currency VARCHAR(3) NOT NULL, -- UZS, TJS, RUB
    paid_at TIMESTAMP WITH TIME ZONE,
    provider_payload JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_payments_provider_event UNIQUE (provider, provider_event_id)
);

-- -------------------------------------------------------------
-- ТАБЛИЦЫ ДЛЯ ИГРЫ "TOJIKAI EMPIRE" (Бизнес Империя)
-- -------------------------------------------------------------
CREATE TABLE empire_user_stats (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    balance NUMERIC(15, 2) DEFAULT 1000.00, -- Валюта адаптируется под страну (UZS/TJS/RUB)
    xp INT DEFAULT 0,
    level INT DEFAULT 1,
    passive_income_per_hour NUMERIC(15, 2) DEFAULT 0.00,
    referral_count INT DEFAULT 0,
    referral_tier VARCHAR(16) DEFAULT 'Bronze', -- Bronze, Silver, Gold, Platinum
    unlocked_cities TEXT[] DEFAULT '{}', -- ['Dushanbe', 'Tashkent']
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE empire_businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    city VARCHAR(64) NOT NULL, -- Dushanbe, Khujand, Bokhtar, Kulob, Tashkent, Samarkand, Bukhara
    business_type VARCHAR(64) NOT NULL, -- cafe, beauty_salon, textile, cargo, auto_service
    level INT DEFAULT 1,
    base_income_per_hour NUMERIC(15, 2) NOT NULL,
    current_income_per_hour NUMERIC(15, 2) NOT NULL,
    manager_hired BOOLEAN DEFAULT FALSE,
    marketer_hired BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

# ЧАСТЬ 3: ИНТЕРАКТИВНЫЙ SMM МАРКЕТИНГОВЫЙ ПАКЕТ «УМНЫЕ ШАГИ»

Пользователь в TMA или через пошаговый бот проходит 4 интерактивных шага для автоматического создания кастомного контента.

## 3.1 Путь Onboarding-Генерации («Умные Шаги»)
1. **Шаг 1: Выбор Ниши (Niche)**
   Показывается сетка из локализованных ниш (не менее 8 на страну):
   - *Узбекистан:* Кафе/Чайхана, Текстиль/Одежда, Недвижимость (Новостройки Ташкента), Автосалон/Сервис, Uzum-Маркетплейс, Строительство, Салон Красоты, Cargo-Китай.
   - *Таджикистан:* Савдои яклухт (Опт Корвон/Панджшанбе), Карго (Китай/Турция), Сохтмон (Стройматериалы), Курутобхона/Чайхана, Свадебный Салон (Атлас/Чакан), Туризм (Варзоб/Помир), Салон Зебоӣ, Автобозор.
2. **Шаг 2: Платформа (Platform)**
   - Instagram, Telegram-Канал, TikTok, YouTube.
3. **Шаг 3: Цель (Goal)**
   - Продажи и заявки, Охваты и вирусы, Вовлечение аудитории, Экспертный личный бренд.
4. **Шаг 4: Формат (Format)**
   - Одиночный взрывной Reels, Структурированный пост с CTA, Серия из 5 Stories прогрева, Готовый Еженедельный Контент-План (7 дней).

```python
# Промпт для сборки кастомного промпта "Умные шаги"
def construct_smm_package_prompt(niche: str, platform: str, goal: str, format_type: str, country: str) -> str:
    return f"""
Тебе нужно собрать ИНТЕГРАЛЬНЫЙ SMM-МАРКЕТИНГОВЫЙ ПАКЕТ для ниши: {niche}.
Выбранная площадка: {platform}
Основная цель продвижения: {goal}
Желаемый формат контента: {format_type}
Географический контекст рынка: {country.upper()}

Требования к генерации пакета:
1. ВИРУСНЫЙ ХУК: Подбери CTR-оптимизированный хук с учетом локального сленга и реалий (например, Click/Payme/Uzum для UZ или Alif Mobi/Корвон для TJ).
2. СТРАТЕГИЯ КОНКУРЕНТОВ: Напиши 2 предложения о том, как отстроиться от местных конкурентов в {country}.
3. ТЕКСТ ПОД КЛЮЧ: Сгенерируй готовый текст согласно формату {format_type}. Текст должен содержать эмодзи, абзацы и 2 альтернативных Call To Action (например: "Напишите в Директ" и "Жмите ссылку в описании").
4. ХЕШТЕГИ: Сделай подборку из 7-10 гео-зависимых хештегов.
"""
```

---

# ЧАСТЬ 4: WHATSAPP И СЕРВЕРНАЯ PDF-ГЕНЕРАЦИЯ ПОД КЛЮЧ

После генерации пакета, система должна уметь отправлять красивый брендированный PDF-отчет напрямую пользователю в WhatsApp.

## 4.1 Интеграционный Сервис WhatsApp API
Этот сервис использует предоставленный токен Ватсап API (например, через провайдеры Green-API, Chat-API или официальный WhatsApp Business Cloud API) для автоматической доставки сгенерированного пакета.

```python
# app/services/whatsapp_service.py
import httpx
import structlog
from pydantic import SecretStr

logger = structlog.get_logger(__name__)

class WhatsAppService:
    def __init__(self, api_url: str, token: SecretStr):
        self.api_url = api_url.rstrip("/")
        self.token = token

    async def send_message_with_pdf(self, phone: str, text: str, pdf_url: str | None = None) -> bool:
        """Отправка сообщения с текстом и ссылкой на PDF-отчет пользователю"""
        if not phone:
            logger.error("whatsapp_phone_missing")
            return False

        clean_phone = "".join(filter(str.isdigit, phone))

        # URL для отправки через API-провайдер (например, Green API)
        url_text = f"{self.api_url}/waInstance{self.token.get_secret_value()}/sendMessage"
        payload_text = {
            "chatId": f"{clean_phone}@c.us",
            "message": text
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url_text, json=payload_text)
                if res.status_code != 200:
                    logger.error("whatsapp_text_send_failed", status=res.status_code, body=res.text)
                    return False

                # Если передан PDF отчет, отправляем файл
                if pdf_url:
                    url_file = f"{self.api_url}/waInstance{self.token.get_secret_value()}/sendFileByUrl"
                    payload_file = {
                        "chatId": f"{clean_phone}@c.us",
                        "urlFile": pdf_url,
                        "fileName": "TojikAI_SMM_Package.pdf",
                        "caption": "Ваш готовый SMM Маркетинговый Пакет в формате PDF 🚀"
                    }
                    await client.post(url_file, json=payload_file)

                logger.info("whatsapp_delivery_success", phone=clean_phone)
                return True
        except Exception as e:
            logger.exception("whatsapp_integration_exception", error=str(e))
            return False
```

## 4.2 Генератор PDF с Поддержкой Кириллицы (ReportLab)
Для предотвращения багов с кодировкой (отображение квадратиков вместо букв в кириллице и таджикском/узбекском алфавитах), PDF рендерится с использованием TrueType шрифта `DejaVuSans.ttf`, загружаемого локально.

```python
# app/services/pdf_generator.py
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_branded_pdf(output_path: str, user_name: str, content_type: str, content_text: str):
    """Генерация PDF-файла отчета для SMM-пакета с поддержкой кириллицы"""

    # Регистрация TrueType шрифта для 100% стабильного рендеринга Cyrillic/Tajik
    font_path = "assets/fonts/DejaVuSans.ttf"
    if not os.path.exists(font_path):
        # Fallback на системные пути или кастомные директории
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=45, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Кастомные стили с поддержкой зарегистрированного шрифта
    title_style = ParagraphStyle(
        'PDFTitle',
        parent=styles['Heading1'],
        fontName='DejaVuSans',
        fontSize=22,
        leading=26,
        textColor='#1E1B4B', # Глубокий индиго
        spaceAfter=15
    )

    body_style = ParagraphStyle(
        'PDFBody',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=11,
        leading=16,
        textColor='#374151', # Серый сланец
        spaceAfter=10
    )

    meta_style = ParagraphStyle(
        'PDFMeta',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=10,
        leading=14,
        textColor='#2563EB', # Синий акцент
        spaceAfter=15
    )

    story = []

    # Добавление логотипа (если доступен)
    logo_path = "assets/tojikai_logo_light.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=120, height=40))
        story.append(Spacer(1, 15))

    story.append(Paragraph("<b>TojikAI SMM Marketing Platform</b>", title_style))
    story.append(Paragraph(f"<b>Пакет:</b> {content_type.upper()}<br/><b>Создано для:</b> {user_name}<br/><b>Дата:</b> {os.getenv('DATE_OVERRIDE', 'Автоматически')}", meta_style))
    story.append(Spacer(1, 10))

    # Форматирование и вставка основного сгенерированного AI текста
    for block in content_text.split("\n\n"):
        block_clean = block.replace("\n", "<br/>")
        story.append(Paragraph(block_clean, body_style))
        story.append(Spacer(1, 5))

    doc.build(story)
```

---

# ЧАСТЬ 5: ЛОКАЛИЗОВАННЫЙ БИЛЛИНГ И ПЛАТЕЖНЫЕ ШЛЮЗЫ (Click, Payme, Alif)

Платформа должна уметь обрабатывать асинхронные callback-запросы от локальных эквайеров в Узбекистане и Таджикистане. Все транзакции идемпотентны.

```
       [ Click / Payme / Alif Mobi ] ─── (Signed HTTPS Callback) ───► [ /api/payments/callback ]
                                                                                   │
                                                                         (Verify Signature)
                                                                                   │
                                                                        [ BillingService Engine ]
                                                                                   │
                                                                   ┌───────────────┴───────────────┐
                                                                   ▼                               ▼
                                                        [ Active Subscription ]         [ Quota Limits Upgrade ]
```

## 5.1 Click (Узбекистан) - Код Обработчика (FastAPI)
```python
# app/api/payments/click.py
import hashlib
from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.services.billing_service import BillingService
from app.core.config import get_settings

router = APIRouter()

@router.post("/callback/click")
async def click_payment_callback(
    click_trans_id: str = Form(...),
    service_id: str = Form(...),
    click_paydoc_id: str = Form(...),
    merchant_trans_id: str = Form(...),
    amount: float = Form(...),
    action: int = Form(...),
    error: int = Form(...),
    error_note: str = Form(...),
    sign_time: str = Form(...),
    sign_string: str = Form(...),
    db: AsyncSession = Depends(get_db_session)
):
    settings = get_settings()
    # Click MD5 хеширование для проверки подписи
    secret = settings.click_secret_key.get_secret_value()
    # Формула Click: md5(click_trans_id + service_id + secret_key + merchant_trans_id + amount + action + sign_time)
    raw_sign = f"{click_trans_id}{service_id}{secret}{merchant_trans_id}{amount}{action}{sign_time}"
    expected_sign = hashlib.md5(raw_sign.encode("utf-8")).hexdigest()

    if sign_string != expected_sign:
        raise HTTPException(status_code=400, detail="INVALID_SIGNATURE")

    if error != 0:
        return {"error": error, "error_note": error_note}

    # Идемпотентная активация подписки через доменный сервис
    billing_service = BillingService(db)
    if action == 1: # Выполнение платежа
        success = await billing_service.apply_payment(
            reference=merchant_trans_id,
            provider="click",
            amount_minor=int(amount * 100),
            provider_event_id=click_trans_id
        )
        if not success:
            return {"error": -1, "error_note": "Transaction activation failed"}

    return {
        "click_trans_id": click_trans_id,
        "merchant_trans_id": merchant_trans_id,
        "error": 0,
        "error_note": "Success"
    }
```

## 5.2 Alif Mobi (Таджикистан) - Код Обработчика (FastAPI)
```python
# app/api/payments/alif.py
from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.services.billing_service import BillingService
import hmac
import hashlib

router = APIRouter()

class AlifCallbackPayload(BaseModel):
    transaction_id: str
    order_id: str
    amount: float
    currency: str
    status: str

@router.post("/callback/alif")
async def alif_payment_callback(
    payload: AlifCallbackPayload,
    x_alif_signature: str = Header(...),
    db: AsyncSession = Depends(get_db_session)
):
    # Верификация HMAC-SHA256 подписи от Alif Mobi
    settings = get_settings()
    secret = settings.alif_secret_key.get_secret_value()
    raw_body = payload.model_dump_json(exclude_none=True).encode("utf-8")
    expected_signature = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()

    if x_alif_signature != expected_signature:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED_SIGNATURE")

    if payload.status == "success":
        billing_service = BillingService(db)
        success = await billing_service.apply_payment(
            reference=payload.order_id,
            provider="alif",
            amount_minor=int(payload.amount * 100),
            provider_event_id=payload.transaction_id
        )
        if not success:
            raise HTTPException(status_code=400, detail="PAYMENT_APPLY_FAILED")

    return {"status": "ok", "message": "Transaction verified and processed"}
```

---

# ЧАСТЬ 6: ГЕЙМИФИКАЦИЯ И ДУШЕВНЫЙ ИНТЕЛЛЕКТУАЛЬНЫЙ ПОМОЩНИК

## 6.1 TojikAI Empire (Бизнес Империя)
Платформа содержит интерактивную, глубоко локализованную Mini App-игру, мотивирующую пользователей заходить на платформу ежедневно и получать бонусы.
- **Локальные города для разблокировки:** Душанбе, Худжанд, Бохтар, Куляб, Ташкент, Самарканд, Бухара.
- **Типы бизнесов:** Курутобхона, Семейная Чайхана, Салон Зебоӣ, Текстильная Фабрика, Карго-доставка из Гуанчжоу, Сергели Автосервис.
- **Персонал:** Возможность нанимать Менеджеров, Маркетологов, Водителей, Юристов. Каждый нанятый сотрудник увеличивает процент пассивного дохода.
- **Ивенты:** Случайные локальные события (например, "В Душанбе хлынул сильный дождь, продажи в Варзобской зоне отдыха упали, но выросли в чайхане Рохат. Выберите решение...").

## 6.2 🤖 AI Помощник Q&A
Интегрированный в бота и Mini App экспертный чат-бот на базе OpenAI GPT-4o-mini:
- **Мультиязычный саппорт:** Мгновенный ответ на сложные бизнес-вопросы на русском, таджикском (кириллица) и узбекском (латиница) языках.
- **Экспорт в 1 клик:** Снизу каждого ответа AI-помощника выводятся inline-кнопки быстрого действия:
  - 📝 *Сделать постом* -> Перенаправляет текст в генератор постов.
  - 🎬 *Создать сценарий Reels* -> Превращает совет в пошаговый Reels.
  - 📑 *Создать Stories* -> Разбирает контент на 5 экранов Stories.

---

# ЧАСТЬ 7: ОФФЛАЙН БАЗА ПРЕМИУМ-ПРЕСЕТОВ SMM МАРКЕТОЛОГА

В целях экономии токенов и обеспечения 100% стабильной работы даже при падении внешних API, платформа содержит готовую локализованную базу данных лучших шаблонов (`app/data/smm_memory_db.py`):

```python
# app/data/smm_memory_db.py
PREMIUM_EXPERT_PRESETS = {
    "uz": {
        "cafe": {
            "weekly_plan": "Dushanba: Novza dagi kafemizdan issiq non va somsa jarayoni Reels. Chorshanba: Oilaviy tadbirlar uchun stol band qilish. Juma: Juma ayyomi tabrigi va maxsus palov aksiyasi.",
            "posts": "Siz hali Toshkentdagi eng mazali tandir somsani tatib ko'rmadingizmi? Bizning somsa tandirdan uzilgan zahoti stolingizga tortiladi! Kelib ko'ring yoki buyurtma bering.",
            "reels": "Ssenariy: Kamera yaqin masofadan qarsillayotgan somsa kesilishini ko'rsatadi. Ovoz: 'Ushbu ovozni eshityapsizmi? Bu haqiqiy o'zbek somsasi!'",
        }
    },
    "tj": {
        "wholesale": {
            "weekly_plan": "Душанбе Корвон: Душанбе - Интихоби моли нав аз Чин. Чоршанбе - Рӯзи тахфифҳои яклухт барои мағозаҳои Худҷанд ва Кӯлоб. Ҷумъа - Тарзи бастабандии бор ва фиристодан.",
            "posts": "Савдои яклухт дар бозори Корвон! Либосҳои босифати кӯдакона ва калонсолон мустақим аз корхонаҳои Чин ва Туркия бо нархҳои дастрас.",
            "reels": "Сценарий: Камера анбори калони либосҳоро дар Корвон нишон медиҳад. Диктор: 'Мехоҳед мағозаи худро бо моли серхаридор пур кунед? Мо ба шумо кумак мекунем!'",
        }
    }
}
```

---

# ЧАСТЬ 8: ШАБЛОН ДЛЯ РАБОТЫ ИИ (СТАРТОВЫЙ КОД ПОД КЛЮЧ)

Используй этот готовый код `app/main.py` для инициализации бэкенда платформы:

```python
# app/main.py
import structlog
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from app.core.config import get_settings
from app.api.routes import router as api_router

logger = structlog.get_logger(__name__)

app = FastAPI(title="TojikAI SMM SaaS Platform", version="3.0")
settings = get_settings()

# Подключение TMA фронтенда (Статических файлов)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Роуты API
app.include_router(api_router, prefix="/api")

# Инициализация Бота и Диспетчера
bot = Bot(token=settings.bot_token.get_secret_value())
storage = RedisStorage.from_url(settings.redis_url) if settings.redis_url else None
dp = Dispatcher(storage=storage)

@app.on_event("startup")
async def on_startup():
    logger.info("platform_starting_up")
    # Установка Webhook для Telegram
    if settings.run_mode == "webhook":
        webhook_url = f"{settings.public_base_url}{settings.telegram_webhook_path}"
        await bot.set_webhook(
            url=webhook_url,
            secret_token=settings.telegram_webhook_secret.get_secret_value(),
            allowed_updates=settings.telegram_allowed_updates
        )
        logger.info("telegram_webhook_configured", url=webhook_url)

@app.post(settings.telegram_webhook_path)
async def telegram_webhook(request: Request):
    """Прием обновлений от Telegram Bot API"""
    secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if not secret_header or secret_header != settings.telegram_webhook_secret.get_secret_value():
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized"})

    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tojikai_smm_saas_v3"}
```

---

# ИНСТРУКЦИЯ ДЛЯ ВЫПОЛНЕНИЯ:
1. Скопируй этот файл, вставь свои точные токены (`BOT_TOKEN`, `WHATSAPP_API_TOKEN`, `CLICK_SECRET`, `ALIF_SECRET`) в файл `.env`.
2. Запусти контейнеры: `docker compose up -d --build`.
3. Отправь этот файл в ИИ, и он сгенерирует для тебя полностью готовую платформу со всеми экранами Mini App и функциями!
🚀 **Удачного запуска бизнеса!**
