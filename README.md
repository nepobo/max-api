# MAX Messenger API Client

Python-библиотека для работы с MAX Messenger API.

## Установка

```bash
pip install git+https://github.com/yourusername/max-api.git
```

Или для разработки:

```bash
git clone https://github.com/yourusername/max-api.git
cd max-api
pip install -e .
```

## Быстрый старт

```python
from max_api import MAXClient
import os

# Создание клиента
client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))

# Получение информации о боте
bot = client.get_me()
print(f"Бот: {bot['name']}")

# Отправка сообщения
client.send_message(
    chat_id=12374848,
    text="Привет!",
    format="markdown"
)

# Получение обновлений (Long Polling)
updates = client.get_updates(timeout=30, marker=last_marker)
for update in updates:
    if update.get('update_type') == 'message_created':
        message = update['message']
        chat_id = message['sender']['user_id']
        text = message.get('body', {}).get('text', '')
        print(f"Получено: {text}")
```

## Основные методы

### Информация о боте
```python
bot_info = client.get_me()
```

### Отправка сообщения
```python
client.send_message(
    chat_id=user_id,           # ID пользователя
    text="Текст сообщения",    # Текст
    format="markdown",         # Опционально: markdown/html
    attachments=[]            # Опционально: вложения
)
```

### Получение обновлений
```python
# Long Polling (для разработки)
updates = client.get_updates(timeout=30, marker=last_marker)

# Webhook (для production)
client.create_subscription(url="https://your-server.com/webhook")
```

## Обработка ошибок

```python
from max_api.exceptions import (
    MAXAPIException,
    AuthenticationError,
    RateLimitError
)

try:
    client.send_message(chat_id=123, text="Hi")
except RateLimitError:
    print("Превышен лимит запросов")
except AuthenticationError:
    print("Неверный токен")
except MAXAPIException as e:
    print(f"Ошибка API: {e}")
```

## Шаблон бота

```python
from max_api import MAXClient
import os
import time

client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))
print(f"Бот '{client.get_me()['name']}' запущен!")

last_marker = None

try:
    while True:
        try:
            updates = client.get_updates(timeout=30, marker=last_marker)
        except Exception as e:
            if "timeout" in str(e).lower():
                continue  # Timeout - это нормально
            print(f"Ошибка: {e}")
            time.sleep(5)
            continue
        
        for update in updates:
            if update.get('update_type') == 'message_created':
                message = update['message']
                chat_id = message['sender']['user_id']
                text = message.get('body', {}).get('text', '')
                
                # Ваша логика здесь
                client.send_message(chat_id=chat_id, text=f"Получено: {text}")
            
            if 'marker' in update:
                last_marker = update['marker']

except KeyboardInterrupt:
    print("\nБот остановлен")
finally:
    client.close()
```

## Важные особенности MAX API

⚠️ **Критические моменты:**

1. **Отправка сообщений**: `user_id` передаётся как query-параметр в URL
2. **Получение chat_id**: используйте `message['sender']['user_id']` для ответа
3. **Long Polling timeout**: timeout через 30 секунд - это нормальное поведение, не ошибка
4. **Rate Limit**: 30 запросов в секунду (автоматически контролируется)

## Конфигурация

Создайте `.env` файл:

```env
MAX_BOT_TOKEN=your_bot_token_here
```

Или передайте токен напрямую:

```python
client = MAXClient(token="your_token")
```

## Документация

- Полная документация: [docs/](docs/)
- Примеры использования: [docs/examples/](docs/examples/)
- MAX API документация: https://dev.max.ru/docs-api

## Зависимости

- Python 3.8+
- requests
- python-dotenv

## Лицензия

MIT License - см. [LICENSE](LICENSE)

## Поддержка

Для вопросов и багрепортов используйте GitHub Issues.

---

**Для использования в вашем проекте:**

```bash
pip install git+https://github.com/yourusername/max-api.git
```

```python
from max_api import MAXClient
# Используйте как обычную библиотеку
```
