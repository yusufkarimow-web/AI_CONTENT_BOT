/* app.js - TojikAI Universe SPA Showcase Controller */

// 1. DATASET OF ALL 28 SCREENS OF THE DESIGN SYSTEM
const SCREENS_REGISTRY = [
    {
        id: "splash",
        num: "01",
        title: "Splash Screen",
        description: "Экран приветствия: анимированный логотип TojikAI, национальный орнамент, флаг Таджикистана и слоган.",
        category: "System",
        status: "interactive"
    },
    {
        id: "portal",
        num: "02",
        title: "Portal Opening",
        description: "Космический анимированный портал с вихрями частиц и индикатором прогресса загрузки мира TojikAI.",
        category: "System",
        status: "interactive"
    },
    {
        id: "welcome",
        num: "03",
        title: "Welcome Screen",
        description: "Интродукция с 3D-ландшафтом гор, золотым контуром, приветственным заголовком и кнопкой 'Начать путешествие'.",
        category: "System",
        status: "interactive"
    },
    {
        id: "home",
        num: "04",
        title: "Home Portal",
        description: "Главная орбитальная консоль: интерактивный глобус с орбитальными кнопками SMM-агентов ИИ.",
        category: "Core",
        status: "interactive"
    },
    {
        id: "voice",
        num: "05",
        title: "AI Voice",
        description: "Экран голосового управления: волновой визуализатор аудио, микрофон и интеллектуальное прослушивание.",
        category: "AI Magic",
        status: "interactive"
    },
    {
        id: "chat",
        num: "06",
        title: "AI Chat Assistant",
        description: "Диалоговое окно: стеклянные bubble-сообщения, аватар ИИ, пресеты вопросов и быстрые подсказки.",
        category: "AI Magic",
        status: "interactive"
    },
    {
        id: "orders",
        num: "07",
        title: "Orders Feed",
        description: "Список заказов SMM с фильтрами по статусам (Все, Активные, Выполненные) и красивыми индикаторами.",
        category: "Business",
        status: "interactive"
    },
    {
        id: "delivery",
        num: "08",
        title: "Delivery Tracking",
        description: "Карта отслеживания: векторный интерактивный маршрут, анимированная машина, время прибытия (ETA).",
        category: "Services",
        status: "interactive"
    },
    {
        id: "taxi",
        num: "09",
        title: "TojikAI Taxi",
        description: "Служба такси: выбор тарифов (Эконом/Комфорт/Премиум), точка назначения, рейтинг и карта.",
        category: "Services",
        status: "interactive"
    },
    {
        id: "restaurant",
        num: "10",
        title: "Restaurant Menu",
        description: "Служба доставки еды: сетка блюд восточной кухни, цены в Сомони, рейтинги, фильтры и корзина.",
        category: "Services",
        status: "interactive"
    },
    {
        id: "clinic",
        num: "11",
        title: "Clinic & Doctors",
        description: "Медицинский хаб: карточки докторов с рейтингами, выбор специализации и онлайн-запись.",
        category: "Services",
        status: "interactive"
    },
    {
        id: "shop",
        num: "12",
        title: "Product Shop",
        description: "Каталог товаров: плиточный интерфейс, категории товаров, корзина и мгновенный выкуп.",
        category: "Services",
        status: "interactive"
    },
    {
        id: "crm",
        num: "13",
        title: "CRM Customers",
        description: "База клиентов: карточки заказчиков, контакты, история взаимодействий и быстрые мессенджеры.",
        category: "Business",
        status: "interactive"
    },
    {
        id: "analytics",
        num: "14",
        title: "Analytics KPIs",
        description: "Мощная аналитика SMM: динамические графики, KPI-карточки, коэффициенты конверсии и удержания.",
        category: "Business",
        status: "interactive"
    },
    {
        id: "marketing",
        num: "15",
        title: "AI Marketing Hub",
        description: "Генератор контента: пресеты под соцсети (Instagram, Telegram, TikTok), шаблоны и форма запроса ИИ.",
        category: "AI Magic",
        status: "interactive"
    },
    {
        id: "education",
        num: "16",
        title: "AI Education",
        description: "Платформа обучения: курсы по SMM, IT и маркетингу, шкала прогресса, списки лекций.",
        category: "Core",
        status: "interactive"
    },
    {
        id: "documents",
        num: "17",
        title: "AI Documents",
        description: "Архив документов: список файлов контент-планов и PDF-отчетов с размерами, датами и превью.",
        category: "Core",
        status: "interactive"
    },
    {
        id: "automation",
        num: "18",
        title: "Automation Rules",
        description: "Сценарии автопостинга: настройка триггеров, таймеров и умных правил с неоновыми переключателями.",
        category: "Core",
        status: "interactive"
    },
    {
        id: "notifications",
        num: "19",
        title: "Notifications Center",
        description: "Лента оповещений: системные предупреждения, реферальные начисления и статусы выполнения задач ИИ.",
        category: "Core",
        status: "interactive"
    },
    {
        id: "premium",
        num: "20",
        title: "Premium Hub",
        description: "Преимущества TojikAI Pro: сияющий бриллиант, список суперсил подписки и золотая кнопка покупки.",
        category: "Business",
        status: "interactive"
    },
    {
        id: "profile",
        num: "21",
        title: "User Profile",
        description: "Личный кабинет: статус баланса, уровень лояльности (Бронза-Платина), аватар и настройки.",
        category: "Settings & Admin",
        status: "interactive"
    },
    {
        id: "settings",
        num: "22",
        title: "Settings Console",
        description: "Тонкая настройка: выбор языка (TG/RU/UZ), валюты (Somoni/Sum/RUB), приватность и уведомления.",
        category: "Settings & Admin",
        status: "interactive"
    },
    {
        id: "history",
        num: "23",
        title: "History Timeline",
        description: "Хроника действий: вертикальный таймлайн генераций, выплат, заказов и реферальной активности.",
        category: "Business",
        status: "interactive"
    },
    {
        id: "search",
        num: "24",
        title: "Universal Search",
        description: "Поиск по всей платформе: строка ввода, последние запросы и категории быстрого доступа.",
        category: "Core",
        status: "interactive"
    },
    {
        id: "ivr",
        num: "25",
        title: "IVR / Voice Menu",
        description: "Голосовое меню: цифровая клавиатура, голосовой гид, разделы поддержки SMM по клавишам.",
        category: "AI Magic",
        status: "interactive"
    },
    {
        id: "admin",
        num: "26",
        title: "Admin Panel",
        description: "Управление системой: общий доход, новые юзеры, лимиты, системные логи и балансы.",
        category: "Settings & Admin",
        status: "interactive"
    },
    {
        id: "subscription",
        num: "27",
        title: "Subscription Plans",
        description: "Сравнение тарифов: Basic, Pro, Premium планы с карточками сравнения фич.",
        category: "Business",
        status: "interactive"
    },
    {
        id: "support",
        num: "28",
        title: "Support Desk",
        description: "Поддержка клиентов: FAQ аккордеоны с плавным раскрытием ответов и форма тикета к разработчикам.",
        category: "Settings & Admin",
        status: "interactive"
    }
];

// STATE MANAGER
let activeScreenId = "splash";
let currentTheme = "dark";
let portalTimer = null;

// STARFIELD BACKGROUND GENERATION
function generateStarfield() {
    const container = document.getElementById('stars-container');
    container.innerHTML = '';
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    const starsCount = 100;

    for (let i = 0; i < starsCount; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        star.style.left = `${Math.random() * screenWidth}px`;
        star.style.top = `${Math.random() * screenHeight}px`;
        const size = Math.random() * 2 + 1;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.animationDelay = `${Math.random() * 3}s`;
        container.appendChild(star);
    }
}

// RENDER ALL SCREENS IN LEFT REGISTRY
function renderScreensRegistry(filterText = "") {
    const listElement = document.getElementById('screens-nav-list');
    listElement.innerHTML = '';

    const filtered = SCREENS_REGISTRY.filter(screen =>
        screen.title.toLowerCase().includes(filterText.toLowerCase()) ||
        screen.id.toLowerCase().includes(filterText.toLowerCase()) ||
        screen.category.toLowerCase().includes(filterText.toLowerCase())
    );

    filtered.forEach(screen => {
        const li = document.createElement('li');
        li.className = `screen-item ${screen.id === activeScreenId ? 'active' : ''}`;
        li.setAttribute('data-screen-id', screen.id);

        li.innerHTML = `
            <span class="screen-num">${screen.num}</span>
            <span class="screen-name">${screen.title}</span>
            <span class="screen-status-indicator ${screen.status}"></span>
        `;

        li.addEventListener('click', () => {
            selectScreen(screen.id);
        });

        listElement.appendChild(li);
    });
}

// SWITCH ACTIVE SCREEN
function selectScreen(screenId) {
    if (portalTimer) {
        clearInterval(portalTimer);
        portalTimer = null;
    }

    activeScreenId = screenId;
    const screenMeta = SCREENS_REGISTRY.find(s => s.id === screenId);

    // Update left sidebar active state
    document.querySelectorAll('.screen-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-screen-id') === screenId) {
            item.classList.add('active');
        }
    });

    // Update bottom navigation bar active tab based on active screen
    updateBottomNavState(screenId);

    // Update Phone Title & Info panel below phone
    document.getElementById('tma-screen-title').textContent = screenMeta.title;
    document.getElementById('info-screen-title').textContent = `${screenMeta.num} ${screenMeta.title}`;
    document.getElementById('info-screen-description').textContent = screenMeta.description;

    // Render exact HTML structure of active screen
    const canvas = document.getElementById('tma-main-canvas');
    canvas.innerHTML = '';

    // Smooth fade in
    canvas.style.opacity = 0;
    canvas.style.transform = "translateY(10px)";

    setTimeout(() => {
        canvas.innerHTML = getScreenTemplateHTML(screenId);
        setupScreenInteractions(screenId);
        canvas.style.opacity = 1;
        canvas.style.transform = "translateY(0)";
        canvas.style.transition = "all 0.3s cubic-bezier(0.16, 1, 0.3, 1)";
    }, 50);
}

// BOT NAVBAR SYNCHRONIZATION
function updateBottomNavState(screenId) {
    document.querySelectorAll('.tab-item').forEach(tab => {
        tab.classList.remove('active');
    });

    if (["home", "splash", "portal", "welcome"].includes(screenId)) {
        document.querySelector('[data-tab="home"]').classList.add('active');
    } else if (["marketing", "education", "documents", "automation"].includes(screenId)) {
        document.querySelector('[data-tab="services"]').classList.add('active');
    } else if (["voice", "ivr"].includes(screenId)) {
        document.querySelector('[data-tab="ai-voice"]').classList.add('active');
    } else if (["orders", "delivery", "taxi", "restaurant", "clinic", "shop"].includes(screenId)) {
        document.querySelector('[data-tab="orders"]').classList.add('active');
    } else if (["profile", "settings", "admin", "premium", "support", "history"].includes(screenId)) {
        document.querySelector('[data-tab="profile"]').classList.add('active');
    }
}

// GENERATE DETAILED TEMPLATES FOR EACH OF THE 28 SCREENS
function getScreenTemplateHTML(screenId) {
    switch (screenId) {
        case "splash":
            return `
                <div class="splash-wrapper" id="click-splash-proceed">
                    <div class="splash-logo-container">
                        <div class="splash-ornament-bg"></div>
                        <div class="splash-logo-text">TojikAI</div>
                    </div>
                    <div class="splash-flag-glowing-line"></div>
                    <div class="splash-tagline">Нейросети Таджикистана</div>
                    <div class="sim-caption" style="opacity: 0.7;">Нажмите на экран для запуска...</div>
                </div>
            `;
        case "portal":
            return `
                <div class="portal-wrapper">
                    <div class="portal-vortex-container">
                        <div class="portal-vortex-ring"></div>
                        <div class="portal-vortex-ring-inner"></div>
                        <div class="portal-center-energy"></div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px; align-items: center;">
                        <div class="sim-h2 heading-grad">Открытие Портала AI</div>
                        <div class="sim-caption" id="portal-progress-percent">Загрузка космических слоев: 0%</div>
                        <div class="portal-progress-bar">
                            <div class="portal-progress-fill" id="portal-progress-filling"></div>
                        </div>
                    </div>
                </div>
            `;
        case "welcome":
            return `
                <div class="welcome-wrapper">
                    <div class="welcome-3d-scene">
                        <!-- Custom styled mountain paths drawn with SVG lines -->
                        <svg class="welcome-mountains" viewBox="0 0 300 150">
                            <path d="M10 150 L80 60 L150 150 Z" fill="none" stroke="rgba(255, 215, 0, 0.4)" stroke-width="2"/>
                            <path d="M100 150 L180 30 L260 150 Z" fill="none" stroke="rgba(255, 215, 0, 0.6)" stroke-width="2.5"/>
                            <path d="M190 150 L240 80 L290 150 Z" fill="none" stroke="rgba(255, 215, 0, 0.3)" stroke-width="1.5"/>
                            <!-- Sun circle behind -->
                            <circle cx="180" cy="50" r="15" fill="none" stroke="rgba(0, 212, 255, 0.5)" stroke-width="1.5" stroke-dasharray="3,3"/>
                        </svg>
                    </div>
                    <div class="welcome-title-box">
                        <h2 class="sim-h1 heading-grad">Добро Пожаловать</h2>
                        <p class="welcome-desc">Войдите в мир TojikAI. Управляйте бизнесом, заказывайте сервисы и генерируйте SMM контент силой искусственного интеллекта.</p>
                    </div>
                    <button class="btn-gold-brand" id="btn-welcome-start" style="margin-top: 10px;">Начать путешествие</button>
                </div>
            `;
        case "home":
            return `
                <div class="home-wrapper">
                    <div class="home-orbit-container">
                        <div class="home-globe-center">🪐</div>
                        <div class="home-orbit-ring">
                            <div class="orbital-icon-node node-1" title="Instagram">📷</div>
                            <div class="orbital-icon-node node-2" title="Telegram">📱</div>
                            <div class="orbital-icon-node node-3" title="TikTok">🎵</div>
                            <div class="orbital-icon-node node-4" title="AI Voice">🎤</div>
                        </div>
                    </div>
                    <div class="sim-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="sim-h2 heading-grad">Умные Агенты</span>
                            <span class="status-badge success">Online</span>
                        </div>
                        <p class="sim-body">Нейросетевые помощники адаптированы под рынок Таджикистана (Душанбе, Худжанд, Бохтар).</p>
                    </div>
                    <div class="grid-services-quick">
                        <div class="quick-service-btn" id="go-ai-marketing">
                            <div class="quick-service-icon">⚡</div>
                            <div class="quick-service-title">SMM Хаб</div>
                        </div>
                        <div class="quick-service-btn" id="go-ai-voice">
                            <div class="quick-service-icon">🎙️</div>
                            <div class="quick-service-title">Голос ИИ</div>
                        </div>
                    </div>
                </div>
            `;
        case "voice":
            return `
                <div class="voice-wrapper">
                    <div class="voice-status-label">СЛУШАЮ ВАС...</div>
                    <div class="voice-wave-container">
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                        <div class="voice-wave-bar"></div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px; align-items: center; width: 100%;">
                        <button class="mic-button-large">🎙️</button>
                        <div class="sim-caption" style="margin-top: 10px; text-align: center;">Назовите команду, например:<br><strong>"Создай пост для Кафе в Душанбе"</strong></div>
                    </div>
                </div>
            `;
        case "chat":
            return `
                <div class="chat-wrapper">
                    <div class="chat-history-feed" id="chat-history-container">
                        <div class="chat-bubble ai">Привет! Я AI-ассистент TojikAI. Чем могу помочь вам сегодня?</div>
                        <div class="chat-bubble user">Нужен крутой пост для рекламы кофейни</div>
                        <div class="chat-bubble ai">Отличная идея! Кофе в Душанбе сейчас в тренде. Вот вариант:<br><br><strong>☕️ Магия утра в самом сердце столицы!</strong><br>Попробуйте наш фирменный Раф с восточными специями в кафе "Ситора" в Душанбе! ✨ Доступна оплата через Alif/Click. Ссылка в профиле!</div>
                    </div>
                    <div class="chat-hints-container">
                        <div class="chat-hint-tag" data-text="Напиши контент-план">📅 План</div>
                        <div class="chat-hint-tag" data-text="Придумай хэштеги для Таджикистана">🏷️ Хэштеги</div>
                        <div class="chat-hint-tag" data-text="Где заказать такси">🚖 Такси</div>
                    </div>
                    <div class="chat-input-row">
                        <input type="text" placeholder="Задайте вопрос..." class="sim-input" style="flex-grow: 1;" id="chat-msg-input">
                        <button class="chat-send-btn" id="btn-chat-send">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        </button>
                    </div>
                </div>
            `;
        case "orders":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="tabs-filters">
                        <button class="tab-filter-btn active">Все</button>
                        <button class="tab-filter-btn">Активные</button>
                        <button class="tab-filter-btn">История</button>
                    </div>
                    <div class="item-list-container">
                        <div class="card-item-row" id="order-row-1">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 14px;">Генерация контент-плана</span>
                                <span class="sim-caption">Заказ #2194 • 15:40</span>
                            </div>
                            <span class="status-badge success">Выполнен</span>
                        </div>
                        <div class="card-item-row" id="order-row-2">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 14px;">Реклама в Telegram-канале</span>
                                <span class="sim-caption">Заказ #2199 • В процессе</span>
                            </div>
                            <span class="status-badge warning">Ожидание</span>
                        </div>
                        <div class="card-item-row">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 14px;">Доставка продуктов из магазина</span>
                                <span class="sim-caption">Заказ #2201 • В пути</span>
                            </div>
                            <span class="status-badge warning" style="background: rgba(0,212,255,0.1); color: var(--accent-cyan);">В пути</span>
                        </div>
                    </div>
                </div>
            `;
        case "delivery":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="map-canvas-container">
                        <!-- Custom vector SVG representing simulated map of Dushanbe streets -->
                        <svg class="map-svg-background" viewBox="0 0 300 180">
                            <line x1="10" y1="40" x2="290" y2="40" stroke="rgba(255,255,255,0.1)" stroke-width="4"/>
                            <line x1="50" y1="10" x2="50" y2="170" stroke="rgba(255,255,255,0.1)" stroke-width="4"/>
                            <line x1="180" y1="10" x2="180" y2="170" stroke="rgba(255,255,255,0.1)" stroke-width="4"/>
                            <line x1="10" y1="130" x2="290" y2="130" stroke="rgba(255,255,255,0.1)" stroke-width="4"/>
                            <!-- Green start dot and Red finish dot -->
                            <circle cx="50" cy="40" r="5" fill="#00E5A0"/>
                            <circle cx="180" cy="130" r="5" fill="#FF4757"/>
                        </svg>
                        <div class="map-car">🚖</div>
                        <div class="map-marker" style="top: 125px; left: 175px;"></div>
                    </div>
                    <div class="sim-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="sim-h2">Статус: Доставка SMM отчетов</span>
                            <span class="status-badge warning" style="background: rgba(0,212,255,0.1); color: var(--accent-cyan);">В пути</span>
                        </div>
                        <p class="sim-body">Курьер везет распечатанный отчет по адресу: пр. Рудаки 42, Душанбе.</p>
                        <div class="sim-caption" style="display:flex; justify-content:space-between;">
                            <span>Ориентировочное время (ETA):</span>
                            <span style="color: var(--accent-gold); font-weight:700;">12 минут</span>
                        </div>
                    </div>
                </div>
            `;
        case "taxi":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="map-canvas-container" style="height: 120px;">
                        <svg class="map-svg-background" viewBox="0 0 300 120">
                            <line x1="10" y1="60" x2="290" y2="60" stroke="rgba(255,255,255,0.06)" stroke-width="3"/>
                            <line x1="120" y1="10" x2="120" y2="110" stroke="rgba(255,255,255,0.06)" stroke-width="3"/>
                        </svg>
                        <div class="map-marker" style="top: 55px; left: 115px;">📍</div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <input type="text" placeholder="Откуда: пр. Рудаки" class="sim-input" style="padding: 8px 12px; font-size:12px;">
                        <input type="text" placeholder="Куда: Кохи Навруз" class="sim-input" style="padding: 8px 12px; font-size:12px;">
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
                        <div class="quick-service-btn" style="padding: 8px; border-color: var(--accent-cyan);">
                            <span style="font-size: 16px;">🚖</span>
                            <span class="sim-caption" style="font-weight:700;">Эконом</span>
                            <span class="sim-caption" style="color:var(--accent-cyan);">15с.</span>
                        </div>
                        <div class="quick-service-btn" style="padding: 8px;">
                            <span style="font-size: 16px;">✨</span>
                            <span class="sim-caption" style="font-weight:700;">Комфорт</span>
                            <span class="sim-caption">22с.</span>
                        </div>
                        <div class="quick-service-btn" style="padding: 8px;">
                            <span style="font-size: 16px;">👑</span>
                            <span class="sim-caption" style="font-weight:700;">Бизнес</span>
                            <span class="sim-caption">38с.</span>
                        </div>
                    </div>
                    <button class="btn-gold-brand" style="padding: 8px 12px; font-size: 13px;">Заказать Такси</button>
                </div>
            `;
        case "restaurant":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; gap: 6px; overflow-x: auto;">
                        <div class="chat-hint-tag" style="background:var(--accent-cyan); color:#000;">🔥 Популярное</div>
                        <div class="chat-hint-tag">🍢 Шашлык</div>
                        <div class="chat-hint-tag">🍛 Плов</div>
                    </div>
                    <div class="grid-catalog">
                        <div class="catalog-item-card">
                            <div class="catalog-item-img">🍛</div>
                            <span class="sim-h2" style="font-size: 13px;">Таджикский Плов</span>
                            <span class="price-text">28 сомони</span>
                            <button class="btn-primary-preview" style="padding: 4px 8px; font-size: 11px; border-radius: 8px;">В корзину</button>
                        </div>
                        <div class="catalog-item-card">
                            <div class="catalog-item-img">🍢</div>
                            <span class="sim-h2" style="font-size: 13px;">Ассорти Шашлык</span>
                            <span class="price-text">42 сомони</span>
                            <button class="btn-primary-preview" style="padding: 4px 8px; font-size: 11px; border-radius: 8px;">В корзину</button>
                        </div>
                    </div>
                </div>
            `;
        case "clinic":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="sim-h2">Запись к врачу (Душанбе)</div>
                    <div class="item-list-container">
                        <div class="card-item-row" style="flex-direction: column; align-items: flex-start; gap: 8px;">
                            <div style="display: flex; justify-content: space-between; width: 100%;">
                                <span class="sim-h2" style="font-size: 13.5px;">Доктор Сино Рахимов</span>
                                <span class="status-badge success">★ 4.9</span>
                            </div>
                            <span class="sim-caption">Кардиолог • Стаж 14 лет • Клиника Шифо</span>
                            <button class="btn-glass-brand" style="padding: 6px 12px; font-size:11.5px; width: 100%;">Записаться на прием</button>
                        </div>
                    </div>
                </div>
            `;
        case "shop":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="sim-h2">Маркет товаров TojikAI</div>
                    <div class="grid-catalog">
                        <div class="catalog-item-card">
                            <div class="catalog-item-img">🎙️</div>
                            <span class="sim-h2" style="font-size: 13px;">Микрофон ИИ</span>
                            <span class="price-text">320 сомони</span>
                            <button class="btn-primary-preview" style="padding: 4px; font-size: 11px; border-radius: 6px;">Купить</button>
                        </div>
                        <div class="catalog-item-card">
                            <div class="catalog-item-img">📘</div>
                            <span class="sim-h2" style="font-size: 13px;">Гид по SMM</span>
                            <span class="price-text">95 сомони</span>
                            <button class="btn-primary-preview" style="padding: 4px; font-size: 11px; border-radius: 6px;">Купить</button>
                        </div>
                    </div>
                </div>
            `;
        case "crm":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="sim-h2">База Клиентов SMM</div>
                    <div class="item-list-container">
                        <div class="card-item-row">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 14px;">Мухаммад Саидов</span>
                                <span class="sim-caption">Кафе "Райхон" • Душанбе</span>
                            </div>
                            <span class="status-badge success">Лид</span>
                        </div>
                        <div class="card-item-row">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 14px;">Лола Каримова</span>
                                <span class="sim-caption">Салон красоты "Лола"</span>
                            </div>
                            <span class="status-badge warning">Контакт</span>
                        </div>
                    </div>
                </div>
            `;
        case "analytics":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="kpi-grid">
                        <div class="kpi-mini-card">
                            <span class="sim-caption">Охваты</span>
                            <div class="kpi-value">+420%</div>
                        </div>
                        <div class="kpi-mini-card">
                            <span class="sim-caption">Лиды</span>
                            <div class="kpi-value">+8.4%</div>
                        </div>
                    </div>
                    <div class="sim-card" style="padding: 10px;">
                        <span class="sim-caption">График генераций SMM</span>
                        <div class="svg-chart-container">
                            <svg viewBox="0 0 300 100" width="100%" height="100%">
                                <path d="M10 90 Q75 10 150 50 T290 20" fill="none" stroke="var(--accent-cyan)" stroke-width="3" />
                                <circle cx="150" cy="50" r="4" fill="var(--accent-gold)" />
                                <line x1="10" y1="90" x2="290" y2="90" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
                            </svg>
                        </div>
                    </div>
                </div>
            `;
        case "marketing":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2 heading-grad">Генератор Контента SMM</span>
                    <div style="display: flex; flex-direction: column; gap: 6px;">
                        <span class="sim-caption">Выберите платформу</span>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px; border-color:var(--accent-cyan);">Instagram</button>
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px;">Telegram</button>
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px;">TikTok</button>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 6px;">
                        <span class="sim-caption">Тематика или Ниша</span>
                        <input type="text" placeholder="Кофе, Салон красоты, Автосалон..." class="sim-input" style="padding: 8px 12px; font-size:12px;">
                    </div>
                    <button class="btn-gold-brand" style="font-size:13px; padding: 10px;">Создать вирусный контент</button>
                </div>
            `;
        case "education":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Курсы по SMM & IT</span>
                    <div class="sim-card" style="padding: 12px;">
                        <span class="sim-h2" style="font-size: 14px;">Продвижение бизнеса в Таджикистане</span>
                        <div style="display:flex; justify-content:space-between; margin-top: 6px;">
                            <span class="sim-caption">Прогресс обучения:</span>
                            <span class="sim-caption" style="color:var(--accent-cyan); font-weight:700;">75%</span>
                        </div>
                        <div class="portal-progress-bar" style="width: 100%; margin-top: 4px;">
                            <div class="portal-progress-fill" style="width: 75%;"></div>
                        </div>
                        <button class="btn-glass-brand" style="padding: 6px; font-size:11.5px; margin-top: 10px; width: 100%;">Продолжить урок 8</button>
                    </div>
                </div>
            `;
        case "documents":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Генерированные PDF отчеты</span>
                    <div class="item-list-container">
                        <div class="card-item-row">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size:13px;">SMM_Plan_Cafe.pdf</span>
                                <span class="sim-caption">Размер: 2.4 MB • 2025-05-15</span>
                            </div>
                            <span style="font-size: 18px; cursor:pointer;">📥</span>
                        </div>
                        <div class="card-item-row">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size:13px;">Stories_Auto_Report.pdf</span>
                                <span class="sim-caption">Размер: 1.8 MB • Вчера</span>
                            </div>
                            <span style="font-size: 18px; cursor:pointer;">📥</span>
                        </div>
                    </div>
                </div>
            `;
        case "automation":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Сценарии и триггеры автопостинга</span>
                    <div class="sim-card" style="padding: 12px; gap: 10px;">
                        <div class="switch-row">
                            <span style="color:#fff; font-weight:600; font-size:13px;">Постинг в Telegram в 09:00</span>
                            <label class="custom-switch">
                                <input type="checkbox" checked>
                                <span class="switch-slider"></span>
                            </label>
                        </div>
                        <span class="sim-caption">Каждое утро ИИ создает и публикует пост в выбранные каналы.</span>
                    </div>
                    <div class="sim-card" style="padding: 12px; gap: 10px;">
                        <div class="switch-row">
                            <span style="color:#fff; font-weight:600; font-size:13px;">Парсинг отзывов о кафе</span>
                            <label class="custom-switch">
                                <input type="checkbox">
                                <span class="switch-slider"></span>
                            </label>
                        </div>
                        <span class="sim-caption">Автоматический сбор упоминаний бренда в Instagram.</span>
                    </div>
                </div>
            `;
        case "notifications":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Уведомления</span>
                    <div class="item-list-container">
                        <div class="card-item-row" style="background: rgba(0, 212, 255, 0.05); border-color: rgba(0, 212, 255, 0.15);">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 13px;">Реферальный бонус получен!</span>
                                <span class="sim-caption">Вам начислено +50 сомони за нового пользователя.</span>
                            </div>
                            <span class="sim-caption" style="color:var(--accent-gold);">10м</span>
                        </div>
                        <div class="card-item-row">
                            <div class="card-item-left">
                                <span class="sim-h2" style="font-size: 13px;">SMM отчет успешно создан</span>
                                <span class="sim-caption">Ваш PDF отчет готов к скачиванию в разделе Документы.</span>
                            </div>
                            <span class="sim-caption">2ч</span>
                        </div>
                    </div>
                </div>
            `;
        case "premium":
            return `
                <div style="display: flex; flex-direction: column; gap: 14px; text-align: center;">
                    <div class="premium-header-icon">💎</div>
                    <h2 class="sim-h1 heading-grad">TojikAI Premium</h2>
                    <p class="sim-caption">Разблокируйте безграничные возможности ИИ-генератора SMM.</p>
                    <div style="display: flex; flex-direction: column; gap: 10px; text-align: left; background: rgba(255,255,255,0.02); padding: 12px; border-radius:14px; border:1px solid rgba(255, 215, 0, 0.15);">
                        <div class="premium-feature-li">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span>Безлимитные генерации текстов/идей</span>
                        </div>
                        <div class="premium-feature-li">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span>Премиальные шаблоны и выгрузка в PDF</span>
                        </div>
                        <div class="premium-feature-li">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span>Доступ к VIP такси и сервисам доставки</span>
                        </div>
                    </div>
                    <button class="btn-gold-brand" style="margin-top: 5px;">Активировать за 49с. / мес</button>
                </div>
            `;
        case "profile":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px;">
                        <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--grad-sunset); display:flex; align-items:center; justify-content:center; font-size: 22px;">👑</div>
                        <div style="display:flex; flex-direction:column;">
                            <span class="sim-h2" style="font-size:16px;">Сомон Кодиров</span>
                            <span class="sim-caption">@somon_smm • Золотой уровень</span>
                        </div>
                    </div>
                    <div class="kpi-grid">
                        <div class="kpi-mini-card">
                            <span class="sim-caption">Баланс</span>
                            <div class="kpi-value" style="color:var(--success);">240 сомони</div>
                        </div>
                        <div class="kpi-mini-card">
                            <span class="sim-caption">Рефералы</span>
                            <div class="kpi-value">12 человек</div>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 6px;">
                        <button class="btn-glass-brand" style="text-align:left; font-size:12.5px; padding: 10px;" id="go-settings">⚙️ Настройки аккаунта</button>
                        <button class="btn-glass-brand" style="text-align:left; font-size:12.5px; padding: 10px;" id="go-support">💬 Техподдержка</button>
                    </div>
                </div>
            `;
        case "settings":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Настройки Системы</span>
                    <div class="sim-card" style="padding: 12px; gap: 10px;">
                        <span class="sim-caption" style="font-weight:700; color:#fff;">Язык Интерфейса</span>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px; border-color:var(--accent-cyan); color:var(--accent-cyan);">Русский</button>
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px;">Тоҷикӣ</button>
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px;">O'zbekcha</button>
                        </div>
                    </div>
                    <div class="sim-card" style="padding: 12px; gap: 10px;">
                        <span class="sim-caption" style="font-weight:700; color:#fff;">Основная Валюта</span>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px; border-color:var(--accent-cyan); color:var(--accent-cyan);">TJS (Сомони)</button>
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px;">UZS (Сум)</button>
                            <button class="btn-glass-brand" style="padding: 6px; font-size:11px;">RUB (Рубль)</button>
                        </div>
                    </div>
                    <button class="btn-gold-brand" style="font-size:12px; padding:8px;">Сохранить изменения</button>
                </div>
            `;
        case "history":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">История Активности</span>
                    <div class="item-list-container" style="position: relative; border-left: 1px solid rgba(255,255,255,0.08); padding-left: 14px; margin-left: 6px;">
                        <div style="position:relative; margin-bottom: 12px;">
                            <div style="position:absolute; left: -19px; top: 3px; width: 9px; height: 9px; border-radius:50%; background:var(--accent-cyan); box-shadow:0 0 6px var(--accent-cyan);"></div>
                            <span class="sim-h2" style="font-size: 13px; display:block;">Создание контент-плана для кафе</span>
                            <span class="sim-caption">Успешно сгенерировано ИИ • 15:40</span>
                        </div>
                        <div style="position:relative; margin-bottom: 12px;">
                            <div style="position:absolute; left: -19px; top: 3px; width: 9px; height: 9px; border-radius:50%; background:var(--accent-gold); box-shadow:0 0 6px var(--accent-gold);"></div>
                            <span class="sim-h2" style="font-size: 13px; display:block;">Вывод реферального бонуса</span>
                            <span class="sim-caption">+50 сомони на карту Alif • Вчера</span>
                        </div>
                    </div>
                </div>
            `;
        case "search":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <input type="text" placeholder="Поиск по TojikAI..." class="sim-input" style="width:100%;" id="search-mock-field">
                    <span class="sim-caption">Популярные запросы:</span>
                    <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                        <span class="chat-hint-tag">☕ Пост для кафе</span>
                        <span class="chat-hint-tag">🚗 Аренда авто</span>
                        <span class="chat-hint-tag">⚡ План сторис</span>
                    </div>
                </div>
            `;
        case "ivr":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px; text-align: center;">
                    <span class="voice-status-label" style="font-size: 12px;">ГОЛОСОВОЕ МЕНЮ IVR</span>
                    <div class="voice-wave-container" style="height: 40px;">
                        <div class="voice-wave-bar" style="height: 20px;"></div>
                        <div class="voice-wave-bar" style="height: 30px;"></div>
                        <div class="voice-wave-bar" style="height: 15px;"></div>
                        <div class="voice-wave-bar" style="height: 25px;"></div>
                    </div>
                    <div class="ivr-grid">
                        <div class="dial-btn">1</div>
                        <div class="dial-btn">2</div>
                        <div class="dial-btn">3</div>
                        <div class="dial-btn">4</div>
                        <div class="dial-btn">5</div>
                        <div class="dial-btn">6</div>
                        <div class="dial-btn">7</div>
                        <div class="dial-btn">8</div>
                        <div class="dial-btn">9</div>
                        <div class="dial-btn">*</div>
                        <div class="dial-btn">0</div>
                        <div class="dial-btn">#</div>
                    </div>
                </div>
            `;
        case "admin":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2 heading-grad">Админ Панель TojikAI</span>
                    <div class="kpi-grid">
                        <div class="kpi-mini-card">
                            <span class="sim-caption">Всего пользователей</span>
                            <div class="kpi-value">4,120</div>
                        </div>
                        <div class="kpi-mini-card">
                            <span class="sim-caption">Общий доход</span>
                            <div class="kpi-value" style="color:var(--success);">18,400с.</div>
                        </div>
                    </div>
                    <div class="sim-card" style="padding: 10px;">
                        <span class="sim-caption">Системные логи активности</span>
                        <div style="font-family: monospace; font-size:10px; color:#a3e635; display:flex; flex-direction:column; gap:4px; text-align:left; max-height:80px; overflow-y:auto; padding:4px;">
                            <span>[15:42] bot_polling: Active</span>
                            <span>[15:40] gen_ai: Success (user_id: 421)</span>
                            <span>[15:38] payment_gateway: Webhook TJS ok</span>
                        </div>
                    </div>
                </div>
            `;
        case "subscription":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Тарифные Планы</span>
                    <div class="sim-card" style="padding:12px; border-color: rgba(255,255,255,0.1);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="sim-h2" style="font-size:15px; color:var(--text-secondary);">Базовый (Basic)</span>
                            <span style="font-size:14px; font-weight:700;">0 сомони</span>
                        </div>
                        <span class="sim-caption">3 генерации ИИ в сутки, водяные знаки, стандартная скорость.</span>
                        <button class="btn-glass-brand" style="padding:6px; font-size:11px; margin-top:10px;">Текущий тариф</button>
                    </div>
                    <div class="sim-card" style="padding:12px; border-color: var(--accent-gold);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="sim-h2" style="font-size:15px; color:var(--accent-gold);">Премиум (Premium)</span>
                            <span style="font-size:14px; font-weight:700; color:var(--accent-gold);">49 сомони</span>
                        </div>
                        <span class="sim-caption">Безлимитный ИИ, скачивание PDF отчетов, приоритетный рендеринг.</span>
                        <button class="btn-gold-brand" style="padding:6px; font-size:11px; margin-top:10px;">Выбрать тариф</button>
                    </div>
                </div>
            `;
        case "support":
            return `
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <span class="sim-h2">Часто Задаваемые Вопросы</span>
                    <div style="display: flex; flex-direction: column; gap: 6px;">
                        <div class="faq-item" id="faq-item-1">
                            <div class="faq-question">
                                <span>Как работает SMM автогенерация?</span>
                                <span>▼</span>
                            </div>
                            <div class="faq-answer">Наш ИИ анализирует вашу нишу (например, ресторан в Душанбе) и создает вирусный контент-план, посты и сторис.</div>
                        </div>
                        <div class="faq-item" id="faq-item-2">
                            <div class="faq-question">
                                <span>Как вывести реферальные бонусы?</span>
                                <span>▼</span>
                            </div>
                            <div class="faq-answer">Вы можете вывести средства на карты Alif или Душанбе Сити при накоплении от 50 сомони.</div>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 6px; margin-top: 6px;">
                        <span class="sim-caption">Связаться с разработчиком</span>
                        <input type="text" placeholder="Опишите проблему..." class="sim-input" style="padding:8px 12px; font-size:12px;">
                        <button class="btn-gold-brand" style="padding: 8px; font-size:12px;">Отправить обращение</button>
                    </div>
                </div>
            `;
        default:
            return `<div class="sim-body">Шаблон экрана находится на стадии рендеринга.</div>`;
    }
}

// SETUP INTERACTIVE HANDLERS INSIDE SIMULATED PHONE VIEW
function setupScreenInteractions(screenId) {
    if (screenId === "splash") {
        const proceedEl = document.getElementById('click-splash-proceed');
        if (proceedEl) {
            proceedEl.addEventListener('click', () => {
                selectScreen("portal");
            });
        }
    } else if (screenId === "portal") {
        let percent = 0;
        const percentLabel = document.getElementById('portal-progress-percent');
        const fillBar = document.getElementById('portal-progress-filling');

        portalTimer = setInterval(() => {
            percent += Math.floor(Math.random() * 15) + 5;
            if (percent >= 100) {
                percent = 100;
                clearInterval(portalTimer);
                portalTimer = null;
                setTimeout(() => {
                    selectScreen("welcome");
                }, 400);
            }
            if (percentLabel) percentLabel.textContent = `Загрузка космических слоев: ${percent}%`;
            if (fillBar) fillBar.style.width = `${percent}%`;
        }, 150);
    } else if (screenId === "welcome") {
        const startBtn = document.getElementById('btn-welcome-start');
        if (startBtn) {
            startBtn.addEventListener('click', () => {
                selectScreen("home");
            });
        }
    } else if (screenId === "home") {
        const marketingBtn = document.getElementById('go-ai-marketing');
        if (marketingBtn) {
            marketingBtn.addEventListener('click', () => {
                selectScreen("marketing");
            });
        }
        const voiceBtn = document.getElementById('go-ai-voice');
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => {
                selectScreen("voice");
            });
        }
    } else if (screenId === "chat") {
        const sendBtn = document.getElementById('btn-chat-send');
        const msgInput = document.getElementById('chat-msg-input');
        const historyContainer = document.getElementById('chat-history-container');

        const sendMessage = (text) => {
            if (!text.trim()) return;

            // Add user message bubble
            const userBubble = document.createElement('div');
            userBubble.className = "chat-bubble user";
            userBubble.textContent = text;
            historyContainer.appendChild(userBubble);

            msgInput.value = '';
            historyContainer.scrollTop = historyContainer.scrollHeight;

            // Simulated typing trigger
            setTimeout(() => {
                const aiBubble = document.createElement('div');
                aiBubble.className = "chat-bubble ai";
                aiBubble.innerHTML = `<em>Генерирую умный ответ...</em>`;
                historyContainer.appendChild(aiBubble);
                historyContainer.scrollTop = historyContainer.scrollHeight;

                setTimeout(() => {
                    aiBubble.innerHTML = `✨ <strong>Готово! Специально для вас:</strong><br><br>Вот адаптированный маркетинговый слоган по запросу "${text}". Мы внедрили Tone of Voice, хэштеги #Душанбе #Таджикистан и CTA с оплатой через карты Alif.`;
                    historyContainer.scrollTop = historyContainer.scrollHeight;
                }, 1000);
            }, 500);
        };

        if (sendBtn && msgInput) {
            sendBtn.addEventListener('click', () => {
                sendMessage(msgInput.value);
            });
            msgInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    sendMessage(msgInput.value);
                }
            });
        }

        // Quick tags click
        document.querySelectorAll('.chat-hint-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const text = tag.getAttribute('data-text');
                sendMessage(text);
            });
        });
    } else if (screenId === "profile") {
        const settingsBtn = document.getElementById('go-settings');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => {
                selectScreen("settings");
            });
        }
        const supportBtn = document.getElementById('go-support');
        if (supportBtn) {
            supportBtn.addEventListener('click', () => {
                selectScreen("support");
            });
        }
    } else if (screenId === "support") {
        document.querySelectorAll('.faq-item').forEach(item => {
            item.addEventListener('click', () => {
                item.classList.toggle('open');
            });
        });
    }
}

// TOP AND BOTTOM NAVIGATION BAR LINK HOOKS
function setupNavigationHooks() {
    // Top Nav back button
    document.getElementById('tma-back-button').addEventListener('click', () => {
        // Simple history back navigation simulator
        if (activeScreenId === "support" || activeScreenId === "settings" || activeScreenId === "admin") {
            selectScreen("profile");
        } else if (activeScreenId === "marketing" || activeScreenId === "education" || activeScreenId === "documents" || activeScreenId === "automation") {
            selectScreen("home");
        } else if (activeScreenId === "delivery" || activeScreenId === "taxi" || activeScreenId === "restaurant" || activeScreenId === "clinic" || activeScreenId === "shop") {
            selectScreen("orders");
        } else if (activeScreenId === "welcome") {
            selectScreen("portal");
        } else if (activeScreenId === "portal") {
            selectScreen("splash");
        } else {
            selectScreen("home");
        }
    });

    // Bottom tab bar clicks
    document.querySelectorAll('.tab-item').forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            if (targetTab === "home") {
                selectScreen("home");
            } else if (targetTab === "services") {
                selectScreen("marketing");
            } else if (targetTab === "ai-voice") {
                selectScreen("voice");
            } else if (targetTab === "orders") {
                selectScreen("orders");
            } else if (targetTab === "profile") {
                selectScreen("profile");
            }
        });
    });

    // Scroll opacity dynamic header inside phone
    const canvas = document.getElementById('tma-main-canvas');
    const header = document.getElementById('tma-top-navigation');
    canvas.addEventListener('scroll', () => {
        if (canvas.scrollTop > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Search screens in registry sidebar
    const searchField = document.getElementById('screen-search');
    searchField.addEventListener('input', (e) => {
        renderScreensRegistry(e.target.value);
    });
}

// IN-HUD COMPONENTS LINK HOOKS
function setupHUDInteractivePreviews() {
    // Switch preview change
    const demoSwitch = document.getElementById('demo-switch');
    if (demoSwitch) {
        demoSwitch.addEventListener('change', (e) => {
            // Trigger a message/glowing notification change or log
            console.log("Switch active:", e.target.checked);
        });
    }
}

// INIT APPLICATION
window.addEventListener('DOMContentLoaded', () => {
    generateStarfield();
    renderScreensRegistry();
    selectScreen("splash");
    setupNavigationHooks();
    setupHUDInteractivePreviews();

    // Re-generate stars on resize
    window.addEventListener('resize', generateStarfield);
});
