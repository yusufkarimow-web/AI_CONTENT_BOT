# 📱 TojikAI SMM Platform v3.0 - ПОЛНОЕ РУКОВОДСТВО

## 🎯 ЧТО ЭТО ТАКОЕ?

**TojikAI** - это платформа, которая **автоматически создает профессиональный контент для социальных сетей** с помощью искусственного интеллекта.

Представьте: вы владелец кафе, салона красоты или магазина. Вместо того чтобы часами писать посты, вы:
1. Выбираете нишу (кафе, магазин, салон и т.д.)
2. Выбираете соцсеть (Instagram, Telegram, TikTok, YouTube)
3. Говорите цель (продажи, охваты, вовлечение)
4. **За 30 секунд получаете готовый профессиональный контент!** ✨

---

## ⚙️ СИСТЕМНЫЕ ТРЕБОВАНИЯ
✅ Linux/Mac/Windows с Docker установленным ✅ 4GB+ RAM ✅ 2+ CPU ядра ✅ 50GB свободного места на диске ✅ Интернет соединение

**Установка Docker:**
- **Ubuntu/Debian:** `sudo apt-get install docker.io docker-compose`
- **Mac:** Скачать Docker Desktop с https://docker.com
- **Windows:** Скачать Docker Desktop с https://docker.com

---

## 🔐 БЫСТРЫЙ СТАРТ (5 МИНУТ)

### Шаг 1: Скачать проект

```bash
# Распаковать ZIP файл
unzip tojikai-smm-platform-v3.0.zip
cd tojikai-smm-platform-v3.0
```

### Шаг 2: Подготовить конфигурацию

```bash
# Скопировать пример конфигурации
cp .env.example .env
```

**⚠️ ВАЖНО: Открыть .env в текстовом редакторе и заполнить:**
Что нужно заполнить в .env:

```env
# 1. TELEGRAM BOT (https://t.me/BotFather)
BOT_TOKEN=xxxx:yyyyy...  # Скопировать от BotFather

# 2. OPENAI API (https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-xxxx...  # Скопировать из OpenAI Dashboard

# 3. ПЛАТЕЖИ (для вашей страны)

# Если в Узбекистане:
CLICK_SECRET_KEY=xxxx...    # Скопировать из Click админ-панели
PAYME_SECRET_KEY=xxxx...    # Скопировать из Payme админ-панели

# Если в Таджикистане:
ALIF_SECRET_KEY=xxxx...     # Скопировать из Alif админ-панели

# 4. WHATSAPP (https://api.green-api.com)
WHATSAPP_API_TOKEN=xxxx...
WHATSAPP_INSTANCE_ID=xxxx...

# 5. БЕЗОПАСНОСТЬ (генерируются автоматически, но проверьте)
SECRET_KEY=xxxxx... # Минимум 32 символа (буквы, цифры, символы)

# 6. URL вашего сервера
PUBLIC_BASE_URL=https://api.tojikai.app
```

Где взять каждый ключ:
- **Bot Token**: @BotFather в Telegram -> `/newbot` → выбрать имя → скопировать token
- **OpenAI API Key**: https://platform.openai.com -> Sign Up → API Keys → Create → Copy
- **Click Secret**: https://click.uz -> Админ-панель → Merchant Settings → Secret Key
- **Payme Secret**: https://payme.uz -> Админ-панель → API Settings → Secret Key
- **Alif Secret**: https://alif.tj -> Админ-панель → Integration → Secret Key
- **WhatsApp Token**: https://api.green-api.com -> Sign Up → My Account → API Token

### Шаг 3: Запустить проект

```bash
# Дать права на выполнение
chmod +x deploy.sh

# ЗАПУСТИТЬ ВАЛИДАЦИЮ И РАЗВЕРТЫВАНИЕ
./deploy.sh
```

Что произойдет:
- ✅ Проверка всего кода на ошибки
- ✅ Проверка конфигурации
- ✅ Создание Docker контейнеров
- ✅ Запуск базы данных
- ✅ Запуск приложения

### Шаг 4: Проверить что все работает

```bash
# Открыть логи
docker-compose logs -f app

# Когда увидите "Application started" - успешно! ✅

# Открыть в браузере
https://api.tojikai.app/health
```

Должно показать:
```json
{
  "status": "healthy",
  "service": "tojikai_smm_saas",
  "version": "3.0"
}
```

### Шаг 5: Открыть Telegram Mini App
1. Откройте Telegram
2. Найдите вашего бота (`@your_bot_username`)
3. Нажмите `/start`
4. Нажмите "🚀 Открыть Mini App"

---

## 📚 КАК ПОЛЬЗОВАТЬСЯ

### Для конечного пользователя (клиента)
Сценарий: Вы владелец кафе в Душанбе

**1️⃣ Откройте бота в Telegram**
- Найдите `@tojikai_bot` (или ваш бот)
- Нажмите `/start`
- Выберите язык (Таджикский 🇹🇯)

**2️⃣ Откройте TojikAI Mini App**
- Нажмите кнопку "🚀 Открыть Mini App"
- Это веб-интерфейс в Telegram (выглядит как обычное приложение)

**3️⃣ Создайте контент (Smart Steps)**
- ШАГ 1: Выберите нишу
  - ☕ Кафе / Чайхана
  - 👕 Текстиль / Одежда
  - 🏢 Недвижимость
  - 🚗 Авто / Сервис
- ШАГ 2: Выберите платформу
  - 📸 Instagram (для фото и историй)
  - 📱 Telegram (для каналов и групп)
  - 🎵 TikTok (для коротких видео)
  - ▶️ YouTube (для развернутого контента)
- ШАГ 3: Выберите цель
  - 💰 Продажи & Заявки (получать больше клиентов)
  - 📈 Охваты & Вирусность (быть популярным)
  - 💬 Вовлечение (чтобы люди комментировали)
  - 🌟 Личный бренд (чтобы люди знали вас)
- ШАГ 4: Выберите формат
  - 🎬 Взрывной Reels (50-60 сек видео для Instagram)
  - 📄 Структурированный пост (текст с эмодзи)
  - 📖 Серия Stories (5 коротких слайдов)
  - 📅 Еженедельный План (7 постов на неделю)

**4️⃣ Расскажите о вашем бизнесе (опционально)**
- Система спросит: "Расскажите о вашем бизнесе"
- Вы можете написать: `"Мое кафе находится в центре Душанбе, известно восточной кухней"` или оставить пусто - система сама придумает

**5️⃣ Получите результат за 30 секунд! ✨**
- Вы видите готовый контент
- Кнопка "📥 Скачать PDF" - сохранить себе
- Кнопка "💬 WhatsApp" - отправить себе в WhatsApp

**6️⃣ Используйте контент**
- Копируйте текст и вставляйте в Instagram
- Используйте идеи для своих видео
- Публикуйте без изменений

### Для администратора (вас)
УПРАВЛЕНИЕ ПРОЕКТОМ

```bash
# Запустить приложение
docker-compose up -d

# Остановить приложение
docker-compose down

# Посмотреть логи приложения
docker-compose logs -f app

# Посмотреть логи базы данных
docker-compose logs -f db

# Перезагрузить приложение
docker-compose restart app

# Удалить все данные и начать с чистого листа
docker-compose down -v
docker-compose up -d
```

---

## 🔒 БЕЗОПАСНОСТЬ
Проверенные функции безопасности ✅
- ✅ Все пароли хранятся в .env (не в коде)
- ✅ Telegram API токен защищен
- ✅ OpenAI API токен защищен
- ✅ Платежи используют HTTPS
- ✅ Все платежные данные зашифрованы
- ✅ Защита от CSRF атак
- ✅ Rate limiting (макс 100 запросов в секунду)
- ✅ SQL injection защита (используем ORM)
- ✅ Логирование всех платежей
- ✅ Webhook подписи проверяются

Что НЕ должны делать:
❌ НИКОГДА не пишите:
```python
# ПЛОХО (небезопасно!)
TOKEN = "xyzabc123"
API_KEY = "sk-12345"
```

✅ ВСЕГДА используйте переменные окружения:
```python
# ХОРОШО (безопасно)
TOKEN = settings.bot_token  # Из .env файла
API_KEY = settings.openai_api_key  # Из .env файла
```

Если украли токен/ключ:
1. СРАЗУ отозвать ключ на сервисе:
   - Click: https://click.uz → regenerate
   - Payme: https://payme.uz → regenerate
   - Alif: https://alif.tj → regenerate
   - OpenAI: https://platform.openai.com → delete & create new
   - Telegram: @BotFather → /delete → /newbot
2. Обновить `.env` файл с новыми ключами
3. Перезагрузить приложение:
```bash
docker-compose restart app
```

---

## 💰 МОНЕТИЗАЦИЯ
Модель доходов:
1. **Подписки (70% доходов)**
   - Клиенты платят за тарифы
   - Click/Payme берут комиссию 2-3%
   - Остаток — ваша прибыль
   - *Пример (Узбекистан):* Клиент платит: 29,900 UZS (Starter), Click берет комиссию: 598 UZS (2%), Вы получаете: 29,302 UZS
2. **Реферальная программа (20% доходов)**
   - Когда клиент A приносит клиента B
   - Вы получаете 10% комиссии от платежей B
3. **Премиум функции (10% доходов)**
   - Доп. анализ контента
   - Экспорт в документы Word/Excel
   - Custom branding

---

## 🐛 РЕШЕНИЕ ПРОБЛЕМ

### Проблема 1: Docker не запускается
```bash
# Проверить Docker установлен ли
docker --version

# Если не установлен:
# Ubuntu: sudo apt-get install docker.io
# Mac: https://docs.docker.com/desktop/install/mac-install/

# Если ошибка прав доступа:
sudo usermod -aG docker $USER
newgrp docker
```

### Проблема 2: "Connection refused" при открытии приложения
```bash
# Приложение еще запускается, подождать 30 секунд
# Затем проверить логи:
docker-compose logs app

# Если видите ошибку с БД:
docker-compose restart db
docker-compose restart app

# Подождать еще 30 сек и попробовать снова
```

### Проблема 3: "Permission denied" ошибка
```bash
# Дать права на папку
chmod -R 755 .

# Дать права на скрипт
chmod +x deploy.sh

# Запустить заново
./deploy.sh
```

---

## 📞 ПОДДЕРЖКА И КОНТАКТЫ
Если что-то не работает:
1. Проверить логи: `docker-compose logs -f app | grep -i error`
2. Проверить `.env` переменные: `docker-compose exec app env | grep BOT`
3. Перезагрузить: `docker-compose down && docker-compose up -d && docker-compose logs -f app`

- 📧 Email: support@tojikai.app
- 💬 Telegram: @tojikai_support
- 🌐 WhatsApp: +992 (91) 000-00-00

---

## 📋 ЧЕКЛИСТ ПЕРЕД ЗАПУСКОМ
- [ ] Docker установлен (`docker --version` работает)
- [ ] `.env` файл заполнен всеми ключами
- [ ] Все ключи скопированы из сервисов (Bot Token, OpenAI и т.д.)
- [ ] Запущен `./deploy.sh` без ошибок
- [ ] Логи показывают "Application started"
- [ ] URL `https://api.tojikai.app/health` работает
- [ ] Telegram бот отвечает на `/start`
- [ ] Mini App открывается в Telegram
- [ ] Кнопки работают (создание контента)
- [ ] PDF скачивается
- [ ] WhatsApp интеграция работает

Версия: 3.0.0
Разработано: TojikAI Team
Поддержка: support@tojikai.app
Создано с ❤️ для бизнеса в Средней Азии
