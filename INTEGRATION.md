# Интеграция MAX API в ваш проект

## Установка

### Вариант 1: Из Git репозитория (рекомендуется)

```bash
pip install git+https://github.com/nepobo/max-api.git
```

### Вариант 2: Как локальный пакет

```bash
# Скопируйте папку max_api в ваш проект
cp -r /path/to/max-api/max_api /path/to/your-project/

# Установите зависимости
pip install requests python-dotenv
```

### Вариант 3: Как submodule

```bash
cd your-project
git submodule add https://github.com/nepobo/max-api.git libs/max-api
pip install -e libs/max-api
```

## Структура проекта после интеграции

### Вариант с установкой через pip:
```
your-project/
├── .env                    # Токен бота
├── requirements.txt        # max-api в зависимостях
├── main.py
└── bot/
    ├── __init__.py
    ├── handlers.py         # Обработчики сообщений
    └── max_bot.py          # Интеграция с MAX
```

### Вариант с локальной копией:
```
your-project/
├── .env
├── max_api/               # Скопированная библиотека
│   ├── __init__.py
│   ├── client.py
│   ├── exceptions.py
│   └── utils.py
├── bot/
│   └── max_bot.py
└── main.py
```

## Пример интеграции

### 1. Создайте файл `bot/max_bot.py`:

```python
"""
Модуль интеграции с MAX Messenger
"""
from max_api import MAXClient
from max_api.exceptions import MAXAPIException, RateLimitError
import os
import time
import logging

logger = logging.getLogger(__name__)


class MAXBot:
    """Обёртка для работы с MAX Messenger"""
    
    def __init__(self, token: str = None):
        self.token = token or os.getenv('MAX_BOT_TOKEN')
        if not self.token:
            raise ValueError("MAX_BOT_TOKEN not found")
        
        self.client = MAXClient(token=self.token)
        self.last_marker = None
        
    def start(self):
        """Запуск бота"""
        bot_info = self.client.get_me()
        logger.info(f"MAX Bot '{bot_info['name']}' started")
        return bot_info
    
    def send_message(self, chat_id: int, text: str, **kwargs):
        """Отправка сообщения с retry"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return self.client.send_message(
                    chat_id=chat_id,
                    text=text,
                    **kwargs
                )
            except RateLimitError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            except MAXAPIException as e:
                logger.error(f"Failed to send message: {e}")
                raise
    
    def get_updates(self, timeout: int = 30):
        """Получение обновлений с обработкой timeout"""
        try:
            updates = self.client.get_updates(
                timeout=timeout,
                marker=self.last_marker
            )
            
            # Обновляем маркер
            for update in updates:
                if 'marker' in update:
                    self.last_marker = update['marker']
            
            return updates
            
        except Exception as e:
            if "timeout" in str(e).lower():
                return []  # Нормальный timeout, возвращаем пустой список
            raise
    
    def process_message(self, message: dict) -> dict:
        """Извлечение данных из сообщения"""
        return {
            'chat_id': message['sender']['user_id'],
            'text': message.get('body', {}).get('text', ''),
            'sender_name': message['sender'].get('name', 'Unknown'),
            'message_id': message.get('message_id'),
        }
    
    def close(self):
        """Закрытие соединения"""
        self.client.close()
```

### 2. Создайте `bot/handlers.py`:

```python
"""
Обработчики команд и сообщений
"""
import logging

logger = logging.getLogger(__name__)


class MessageHandler:
    """Обработчик сообщений"""
    
    def __init__(self, max_bot):
        self.bot = max_bot
    
    def handle_message(self, msg_data: dict):
        """Обработка входящего сообщения"""
        text = msg_data['text']
        chat_id = msg_data['chat_id']
        
        logger.info(f"Message from {msg_data['sender_name']}: {text}")
        
        # Ваша логика обработки
        if text.startswith('/'):
            self.handle_command(chat_id, text)
        else:
            self.handle_text(chat_id, text)
    
    def handle_command(self, chat_id: int, text: str):
        """Обработка команд"""
        command = text.split()[0].lower()
        
        if command == '/start':
            self.bot.send_message(
                chat_id=chat_id,
                text="Привет! Я бот."
            )
        elif command == '/help':
            self.bot.send_message(
                chat_id=chat_id,
                text="Доступные команды:\n/start\n/help"
            )
    
    def handle_text(self, chat_id: int, text: str):
        """Обработка обычного текста"""
        # Ваша логика
        self.bot.send_message(
            chat_id=chat_id,
            text=f"Получено: {text}"
        )
```

### 3. Создайте `main.py`:

```python
"""
Главный файл приложения
"""
import os
import logging
from dotenv import load_dotenv
from bot.max_bot import MAXBot
from bot.handlers import MessageHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()


def main():
    # Создание бота
    bot = MAXBot()
    handler = MessageHandler(bot)
    
    # Запуск
    bot.start()
    logger.info("Bot started, waiting for messages...")
    
    try:
        while True:
            # Получение обновлений
            updates = bot.get_updates(timeout=30)
            
            # Обработка
            for update in updates:
                if update.get('update_type') == 'message_created':
                    message = update['message']
                    msg_data = bot.process_message(message)
                    handler.handle_message(msg_data)
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}", exc_info=True)
    finally:
        bot.close()


if __name__ == "__main__":
    main()
```

### 4. Создайте `.env`:

```env
MAX_BOT_TOKEN=your_token_here
```

### 5. Добавьте в `requirements.txt`:

```txt
# Если установили через pip
max-api @ git+https://github.com/nepobo/max-api.git

# Или если используете локальную копию
requests>=2.31.0
python-dotenv>=1.0.0
```

## Запуск

```bash
python main.py
```

## Расширенная интеграция

### С FastAPI (для webhook):

```python
from fastapi import FastAPI, Request
from bot.max_bot import MAXBot

app = FastAPI()
bot = MAXBot()

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    
    if update.get('update_type') == 'message_created':
        message = update['message']
        msg_data = bot.process_message(message)
        # Обработка сообщения
        bot.send_message(
            chat_id=msg_data['chat_id'],
            text="Ответ"
        )
    
    return {"ok": True}
```

### С Django:

```python
# bot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .max_bot import MAXBot

bot = MAXBot()

@csrf_exempt
@require_http_methods(["POST"])
def webhook(request):
    update = json.loads(request.body)
    
    if update.get('update_type') == 'message_created':
        message = update['message']
        msg_data = bot.process_message(message)
        # Обработка
        bot.send_message(
            chat_id=msg_data['chat_id'],
            text="Ответ"
        )
    
    return JsonResponse({"ok": True})
```

## Советы

1. **Используйте webhook в production**, Long Polling только для разработки
2. **Обрабатывайте timeout** - это нормальное поведение
3. **Добавьте retry логику** для отправки сообщений
4. **Логируйте всё** - это поможет при отладке
5. **Храните токен в .env**, не коммитьте его

## Документация

Полная документация и примеры: [docs/](docs/)
