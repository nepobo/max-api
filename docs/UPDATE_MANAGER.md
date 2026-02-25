# UpdateManager - Управление режимами получения обновлений

## Обзор

MAX API поддерживает два способа получения обновлений от сервера:

1. **Long Polling** - для разработки и тестирования
2. **Webhook** - для production окружения

**⚠️ Важно**: Использовать одновременно Long Polling и Webhook **нельзя** - выберите один из типов.

## Отличия технологий

| Параметр | Long Polling | Webhook |
|----------|-------------|---------|
| **Принцип работы** | Периодические запросы к серверу | Сервер сам отправляет данные |
| **Использование** | Разработка и тестирование | Production окружение |
| **Протокол** | HTTP/HTTPS | Только HTTPS |
| **Задержка** | Зависит от timeout (обычно 30 сек) | Мгновенная |
| **Нагрузка** | Выше (постоянные запросы) | Ниже (push-уведомления) |
| **Настройка** | Не требуется | Требуется публичный HTTPS URL |

## Быстрый старт

### Long Polling (разработка)

```python
from max_api import MAXClient, UpdateManager, UpdateMode

client = MAXClient(token="your_token")
manager = UpdateManager(client, mode=UpdateMode.LONG_POLLING)

# Получение обновлений
while True:
    try:
        updates = manager.get_updates(timeout=30)
        
        for update in updates:
            # Обработка обновлений
            print(update)
    
    except Exception as e:
        if "timeout" in str(e).lower():
            continue  # Timeout - это нормально
```

### Webhook (production)

```python
from max_api import MAXClient, UpdateManager

client = MAXClient(token="your_token")
manager = UpdateManager(client)

# Настройка webhook
webhook_url = "https://your-domain.com/webhook"
subscription = manager.switch_to_webhook(webhook_url)

print(f"Webhook настроен: {subscription['id']}")

# Теперь MAX будет отправлять обновления на ваш URL
```

## UpdateMode

Enum с двумя значениями:

```python
from max_api import UpdateMode

UpdateMode.LONG_POLLING  # Режим Long Polling
UpdateMode.WEBHOOK       # Режим Webhook
```

## UpdateManager API

### Инициализация

```python
from max_api import MAXClient, UpdateManager, UpdateMode

client = MAXClient(token="your_token")

# По умолчанию - Long Polling
manager = UpdateManager(client)

# Или явно указать режим
manager = UpdateManager(client, mode=UpdateMode.WEBHOOK)
```

### Свойства

```python
# Текущий режим
manager.mode  # UpdateMode.LONG_POLLING или UpdateMode.WEBHOOK

# Проверки режима
manager.is_long_polling  # True/False
manager.is_webhook       # True/False

# URL webhook (если настроен)
manager.webhook_url  # "https://..." или None
```

### Методы

#### `switch_to_long_polling()`

Переключиться на режим Long Polling.

```python
manager.switch_to_long_polling()
# Если был активен Webhook, он будет удалён
```

#### `switch_to_webhook(webhook_url)`

Переключиться на режим Webhook.

```python
subscription = manager.switch_to_webhook("https://your-domain.com/webhook")

print(subscription['id'])    # ID подписки
print(subscription['url'])   # URL webhook
```

**Требования к URL:**
- ✅ Только HTTPS (включая самоподписанные сертификаты)
- ❌ HTTP не поддерживается

**Raises:**
- `ValueError` - если URL не HTTPS
- `MAXAPIException` - при ошибке API

#### `get_updates(timeout, marker)`

Получить обновления (только в режиме Long Polling).

```python
updates = manager.get_updates(timeout=30, marker=last_marker)
```

**Параметры:**
- `timeout` (int) - таймаут ожидания (секунды, по умолчанию 30)
- `marker` (str, optional) - маркер последнего обновления

**Raises:**
- `RuntimeError` - если вызван в режиме Webhook

**Note**: Timeout - нормальное поведение! Если нет новых сообщений, запрос завершится по таймауту.

#### `get_webhook_info()`

Получить информацию о текущем webhook.

```python
info = manager.get_webhook_info()

if info:
    print(info['id'])
    print(info['url'])
    print(info['created_at'])
```

**Returns**: `dict` с информацией или `None`, если webhook не настроен.

#### `delete_webhook()`

Удалить webhook и переключиться на Long Polling.

```python
manager.delete_webhook()
# Автоматически переключает на Long Polling
```

#### `get_status()`

Получить статус менеджера.

```python
status = manager.get_status()

print(status)
# {
#     'mode': 'long_polling',
#     'is_long_polling': True,
#     'is_webhook': False,
#     'last_marker': '...'
# }
```

## Примеры использования

### Пример 1: Бот с Long Polling

```python
from max_api import MAXClient, UpdateManager
import os

client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))
manager = UpdateManager(client)

bot_info = client.get_me()
print(f"Бот '{bot_info['name']}' запущен (Long Polling)")

try:
    while True:
        try:
            updates = manager.get_updates(timeout=30)
        except Exception as e:
            if "timeout" in str(e).lower():
                continue
            print(f"Ошибка: {e}")
            continue
        
        for update in updates:
            if update.get('update_type') == 'message_created':
                message = update['message']
                chat_id = message['sender']['user_id']
                text = message['body']['text']
                
                client.send_message(chat_id=chat_id, text=f"Эхо: {text}")

except KeyboardInterrupt:
    print("Бот остановлен")
finally:
    client.close()
```

### Пример 2: Настройка Webhook

```python
from max_api import MAXClient, UpdateManager

client = MAXClient(token="your_token")
manager = UpdateManager(client)

# Настройка webhook
webhook_url = "https://your-server.com/webhook"
subscription = manager.switch_to_webhook(webhook_url)

print(f"✅ Webhook настроен:")
print(f"   ID: {subscription['id']}")
print(f"   URL: {subscription['url']}")
print(f"   Статус: {manager.get_status()}")

# Проверка информации
info = manager.get_webhook_info()
print(f"Webhook активен: {info['url']}")
```

### Пример 3: Переключение режимов

```python
from max_api import MAXClient, UpdateManager, UpdateMode

client = MAXClient(token="your_token")

# Начинаем с Long Polling
manager = UpdateManager(client, mode=UpdateMode.LONG_POLLING)
print(f"Режим: {manager.mode.value}")

# Переключаемся на Webhook
manager.switch_to_webhook("https://example.com/webhook")
print(f"Режим: {manager.mode.value}")
print(f"Webhook URL: {manager.webhook_url}")

# Возвращаемся на Long Polling
manager.switch_to_long_polling()
print(f"Режим: {manager.mode.value}")
```

### Пример 4: Webhook с Flask

```python
from flask import Flask, request, jsonify
from max_api import MAXClient, UpdateManager

app = Flask(__name__)

client = MAXClient(token="your_token")
manager = UpdateManager(client)

# Настраиваем webhook при запуске
webhook_url = "https://your-domain.com/webhook"
manager.switch_to_webhook(webhook_url)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    
    if update.get('update_type') == 'message_created':
        message = update['message']
        chat_id = message['sender']['user_id']
        text = message['body']['text']
        
        # Отправляем ответ
        client.send_message(chat_id=chat_id, text=f"Получено: {text}")
    
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
```

### Пример 5: Webhook с FastAPI

```python
from fastapi import FastAPI, Request
from max_api import MAXClient, UpdateManager

app = FastAPI()

client = MAXClient(token="your_token")
manager = UpdateManager(client)

@app.on_event("startup")
async def startup():
    # Настраиваем webhook при старте приложения
    webhook_url = "https://your-domain.com/webhook"
    subscription = manager.switch_to_webhook(webhook_url)
    print(f"Webhook настроен: {subscription['id']}")

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    
    if update.get('update_type') == 'message_created':
        message = update['message']
        chat_id = message['sender']['user_id']
        text = message['body']['text']
        
        client.send_message(chat_id=chat_id, text=f"FastAPI: {text}")
    
    return {"ok": True}

@app.on_event("shutdown")
async def shutdown():
    # Удаляем webhook при остановке
    manager.delete_webhook()
    client.close()
```

## Best Practices

### Для разработки

✅ **Используйте Long Polling:**
- Не требует публичного URL
- Легко запускать локально
- Простая отладка

```python
manager = UpdateManager(client, mode=UpdateMode.LONG_POLLING)

while True:
    updates = manager.get_updates(timeout=30)
    # Обработка...
```

### Для production

✅ **Используйте Webhook:**
- Меньше нагрузка на сервер
- Мгновенная доставка сообщений
- Масштабируемость

```python
manager = UpdateManager(client)
manager.switch_to_webhook("https://your-domain.com/webhook")

# Настройте веб-сервер для приёма POST запросов
```

### Обработка ошибок

```python
from max_api.exceptions import MAXAPIException

try:
    manager.switch_to_webhook("https://example.com/webhook")
except ValueError as e:
    print(f"Неверный URL: {e}")
except MAXAPIException as e:
    print(f"Ошибка API: {e}")
```

### Graceful Shutdown

```python
import signal
import sys

def signal_handler(sig, frame):
    print("\nОстановка бота...")
    if manager.is_webhook:
        manager.delete_webhook()
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

## Требования к Webhook URL

### ✅ Поддерживается:
- HTTPS с валидным сертификатом: `https://example.com/webhook`
- HTTPS с самоподписанным сертификатом: `https://192.168.1.100:8443/webhook`
- Любой порт: `https://example.com:8443/webhook`

### ❌ Не поддерживается:
- HTTP: `http://example.com/webhook` - вызовет `ValueError`
- localhost без HTTPS: `http://localhost:5000/webhook`

## Troubleshooting

### Ошибка: "get_updates() доступен только в режиме Long Polling"

```python
# Проверьте режим
if manager.is_long_polling:
    updates = manager.get_updates()
else:
    manager.switch_to_long_polling()
    updates = manager.get_updates()
```

### Webhook не получает обновления

1. Проверьте, что URL доступен извне
2. Убедитесь, что используется HTTPS
3. Проверьте статус webhook:

```python
info = manager.get_webhook_info()
print(info)
```

### Переключение между режимами не работает

```python
# Сначала получите статус
status = manager.get_status()
print(status)

# Явно удалите webhook
if manager.is_webhook:
    manager.delete_webhook()

# Переключитесь на нужный режим
manager.switch_to_long_polling()
```

## См. также

- [Основная документация MAX API](https://dev.max.ru/docs-api)
- [Примеры ботов](../examples/)
- [Long Polling Timeout](LONG_POLLING_TIMEOUT.md)
- [Webhook Best Practices](https://dev.max.ru/docs-api/webhooks)
