# ✅ ИСПРАВЛЕНИЕ: Unknown recipient

## Проблема
При запуске ботов возникала ошибка:
```
max_api.exceptions.BadRequestError: Unknown recipient
```

## Причина
Неправильное получение `chat_id` из обновлений. Использовалось:
```python
chat_id = message['recipient']['chat_id']  # ❌ НЕПРАВИЛЬНО
```

## Решение
Правильный способ - использовать `user_id` отправителя:
```python
chat_id = message['sender']['user_id']  # ✅ ПРАВИЛЬНО
```

## Что было исправлено

### ✅ Исправленные файлы:
- `examples/echo_bot.py`
- `examples/simple_bot.py`
- `examples/get_chat_id_bot.py`
- `START_HERE.md`
- `CHEATSHEET_CONNECT_BOT.md`

### Правильная структура обновления MAX API:

```python
update = {
    'update_type': 'message_created',
    'message': {
        'sender': {
            'user_id': 123456789,    # ← Это chat_id для ответа!
            'name': 'Имя пользователя',
            'username': 'username'
        },
        'body': {
            'text': 'Текст сообщения'
        },
        'recipient': {
            'user_id': 206631906,    # ID вашего бота
            'name': 'УК Вместе'
        }
    }
}
```

## Правильный код для ответа

```python
from max_api import MAXClient

client = MAXClient(token="YOUR_TOKEN")

updates = client.get_updates()
for update in updates:
    if update.get('update_type') == 'message_created':
        message = update['message']
        sender = message['sender']
        
        # Получаем chat_id отправителя
        chat_id = sender['user_id']  # ✅
        text = message['body']['text']
        
        # Отправляем ответ
        client.send_message(
            chat_id=chat_id,  # user_id отправителя
            text=f"Вы написали: {text}"
        )
```

## Теперь можно запускать!

```bash
# Активировать venv
source venv/bin/activate

# Запустить эхо-бота
python examples/echo_bot.py

# Запустить бота с командами
python examples/simple_bot.py

# Получить chat_id
python examples/get_chat_id_bot.py
```

## Тестирование

Напишите боту в MAX сообщение "Тест" - он должен ответить "Вы написали: Тест" ✅

---

**Все исправлено и готово к работе!** 🎉
