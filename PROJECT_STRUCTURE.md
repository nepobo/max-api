# MAX API - Структура проекта

## 📁 Текущая структура

```
max-api/
├── max_api/                      # 🎯 ОСНОВНАЯ БИБЛИОТЕКА
│   ├── __init__.py              # Экспорты (MAXClient, exceptions)
│   ├── client.py                # MAXClient - главный класс API
│   ├── exceptions.py            # Исключения (MAXAPIException и др.)
│   └── utils.py                 # Утилиты (RateLimiter, валидация)
│
├── tests/                       # Тесты pytest
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_client.py
│   └── test_utils.py
│
├── docs/                        # 📚 Документация (опционально)
│   ├── examples/                # Примеры использования
│   │   ├── echo_bot.py         # Эхо-бот
│   │   ├── simple_bot.py       # Бот с командами
│   │   ├── get_chat_id_bot.py  # Получение chat_id
│   │   └── keyboard_example.py # Inline клавиатуры
│   ├── ALL_FIXES.md            # История исправлений
│   ├── QUICKSTART.md           # Быстрый старт
│   └── ...                      # Прочая документация
│
├── .github/
│   └── copilot-instructions.md  # Правила для GitHub Copilot
│
├── README.md                    # Главная документация
├── INTEGRATION.md               # Инструкция по интеграции
├── LICENSE                      # MIT License
├── setup.py                     # Установка пакета
├── requirements.txt             # Основные зависимости
├── requirements-dev.txt         # Dev зависимости
├── .env.example                 # Пример .env файла
├── .cursorrules                 # Правила для Cursor AI
├── .ai-context.md               # Контекст для ИИ-помощников
└── .gitignore                   # Git ignore
```

## 🎯 Что использовать

### Для интеграции в другой проект:

**Минимально необходимо:**
```
max_api/           # Скопируйте эту папку
├── __init__.py
├── client.py
├── exceptions.py
└── utils.py
```

**Зависимости:**
```bash
pip install requests python-dotenv
```

### Для установки как пакет:

```bash
# Вариант 1: Из Git
pip install git+https://github.com/nepobo/max-api.git

# Вариант 2: Локально
pip install -e .
```

## 📦 Что входит в библиотеку

### Главный класс: `MAXClient`

```python
from max_api import MAXClient

client = MAXClient(token="your_token")
```

**Методы:**
- `get_me()` - информация о боте
- `send_message(chat_id, text, ...)` - отправка сообщения
- `get_updates(timeout, marker)` - получение обновлений
- `create_subscription(url)` - создание webhook
- `get_subscriptions()` - список webhook'ов
- `delete_subscription(id)` - удаление webhook

### Исключения: `max_api.exceptions`

```python
from max_api.exceptions import (
    MAXAPIException,         # Базовое
    AuthenticationError,     # 401
    BadRequestError,         # 400
    NotFoundError,          # 404
    RateLimitError,         # 429
    ServiceUnavailableError # 503
)
```

### Утилиты: `max_api.utils`

```python
from max_api.utils import (
    RateLimiter,           # Контроль rate limit
    validate_chat_id,      # Валидация chat_id
    build_inline_keyboard, # Создание клавиатур
    format_user_mention,   # Форматирование упоминаний
    extract_chat_id        # Извлечение chat_id
)
```

## 🚀 Быстрое использование

### 1. Скопируйте папку max_api в ваш проект:

```bash
cp -r max-api/max_api /path/to/your-project/
```

### 2. Установите зависимости:

```bash
pip install requests python-dotenv
```

### 3. Используйте в коде:

```python
from max_api import MAXClient
import os

client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))
client.send_message(chat_id=123, text="Hello!")
```

## 📚 Документация и примеры

- **README.md** - главная документация
- **INTEGRATION.md** - подробная инструкция по интеграции
- **docs/examples/** - готовые примеры ботов
- **docs/QUICKSTART.md** - быстрый старт
- **docs/ALL_FIXES.md** - важные fix'ы и особенности API

## 🔧 Для разработки

```bash
# Установка с dev-зависимостями
pip install -r requirements-dev.txt

# Запуск тестов
pytest tests/ -v

# С покрытием
pytest tests/ --cov=max_api
```

## ⚠️ Важные файлы

### Для разработчиков:
- `.cursorrules` - правила для Cursor AI
- `.github/copilot-instructions.md` - правила для GitHub Copilot
- `.ai-context.md` - краткий контекст для всех ИИ

### Для пользователей:
- `README.md` - документация
- `INTEGRATION.md` - как интегрировать
- `docs/examples/` - примеры кода

## 📝 Лицензия

MIT License - свободное использование в любых проектах.

---

## Для интеграции в ваш проект:

1. Скопируйте папку `max_api/` в ваш проект
2. Установите `requests` и `python-dotenv`
3. Импортируйте и используйте: `from max_api import MAXClient`

Подробнее: [INTEGRATION.md](INTEGRATION.md)
