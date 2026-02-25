# Работа с групповыми чатами в MAX Messenger

## Типы чатов

В MAX API существует два типа chat_id:

| Тип чата | chat_id | Пример |
|----------|---------|--------|
| **Личный чат** (пользователь) | Положительное число | `12374848`, `206631906` |
| **Групповой чат** | Отрицательное число | `-987654321` |

## ⚠️ Важное требование

**Для получения событий из группового чата бот ДОЛЖЕН быть назначен администратором!**

Без прав администратора бот не будет получать:
- ❌ Сообщения из группового чата
- ❌ События в групповом чате
- ❌ Упоминания бота в группе

## Настройка бота для групповых чатов

### 1. Добавьте бота в групповой чат

1. Откройте групповой чат в MAX Messenger
2. Перейдите в настройки чата
3. Добавьте бота как участника

### 2. Назначьте бота администратором

1. В настройках группового чата найдите бота
2. Назначьте ему права администратора
3. Сохраните изменения

### 3. Проверьте работу

Отправьте сообщение в групповой чат - бот должен получить обновление.

## Получение chat_id группового чата

### Способ 1: Из обновлений

```python
from max_api import MAXClient, UpdateManager

client = MAXClient(token="your_token")
manager = UpdateManager(client)

# Отправьте сообщение в групповой чат
updates = manager.get_updates(timeout=30)

for update in updates:
    if update.get('update_type') == 'message_created':
        message = update['message']
        
        # Получатель сообщения
        recipient = message['recipient']
        chat_id = recipient['chat_id']
        chat_type = recipient['chat_type']
        
        print(f"Chat ID: {chat_id}")  # Отрицательное для группы
        print(f"Chat Type: {chat_type}")  # 'group' или 'channel'
```

### Способ 2: Бот для определения chat_id

```python
from max_api import MAXClient, UpdateManager

client = MAXClient(token="your_token")
manager = UpdateManager(client)

print("Отправьте сообщение в групповой чат...")

while True:
    try:
        updates = manager.get_updates(timeout=30)
    except Exception as e:
        if "timeout" in str(e).lower():
            continue
    
    for update in updates:
        if update.get('update_type') == 'message_created':
            message = update['message']
            recipient = message['recipient']
            sender = message['sender']
            
            chat_id = recipient['chat_id']
            chat_type = recipient.get('chat_type', 'private')
            text = message.get('body', {}).get('text', '')
            
            if chat_id < 0:  # Групповой чат
                print(f"\n📋 Групповой чат найден!")
                print(f"   Chat ID: {chat_id}")
                print(f"   Chat Type: {chat_type}")
                print(f"   Сообщение: {text}")
                print(f"   От: {sender['name']}")
                
                # Ответ в групповой чат
                client.send_message(
                    chat_id=chat_id,
                    text=f"Групповой чат ID: {chat_id}"
                )
```

## Отправка сообщений в групповой чат

### Личный чат (положительный chat_id)

```python
from max_api import MAXClient

client = MAXClient(token="your_token")

# Отправка пользователю
client.send_message(
    chat_id=12374848,  # Положительное число
    text="Привет!"
)
```

### Групповой чат (отрицательный chat_id)

```python
from max_api import MAXClient

client = MAXClient(token="your_token")

# Отправка в группу
client.send_message(
    chat_id=-987654321,  # Отрицательное число
    text="Привет группе!"
)
```

## Различия в обработке

### Структура сообщения

```python
# Личное сообщение
{
    "sender": {
        "user_id": 12374848,  # Кто отправил
        "name": "Иван"
    },
    "recipient": {
        "chat_id": 206631906,  # ID бота (получатель)
        "chat_type": "private"
    },
    "body": {"text": "Привет"}
}

# Сообщение из группы
{
    "sender": {
        "user_id": 12374848,  # Кто отправил
        "name": "Иван"
    },
    "recipient": {
        "chat_id": -987654321,  # Отрицательный ID группы
        "chat_type": "group"
    },
    "body": {"text": "Привет всем"}
}
```

### Определение типа чата

```python
def handle_message(message):
    recipient = message['recipient']
    chat_id = recipient['chat_id']
    chat_type = recipient.get('chat_type', 'private')
    
    if chat_id < 0:
        # Групповой чат
        print(f"Сообщение из группы {chat_id}")
        # Особая логика для групп
    else:
        # Личный чат
        print(f"Личное сообщение от {chat_id}")
        # Обычная обработка
```

### Ответ зависит от типа чата

```python
from max_api import MAXClient

def reply_to_message(client, message):
    recipient = message['recipient']
    sender = message['sender']
    text = message['body']['text']
    
    chat_id = recipient['chat_id']
    
    if chat_id < 0:
        # Групповой чат - можно упомянуть отправителя
        response = f"@{sender['username']}, получено: {text}"
        client.send_message(chat_id=chat_id, text=response)
    else:
        # Личный чат - обычный ответ
        response = f"Получено: {text}"
        client.send_message(chat_id=chat_id, text=response)
```

## Пример бота для работы с группами

```python
from max_api import MAXClient, UpdateManager, UpdateMode
import os

client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))
manager = UpdateManager(client, mode=UpdateMode.LONG_POLLING)

bot_info = client.get_me()
print(f"Бот '{bot_info['name']}' запущен")
print("Не забудьте назначить бота администратором в групповых чатах!")

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
            
            sender = message['sender']
            recipient = message['recipient']
            body = message.get('body', {})
            
            chat_id = recipient['chat_id']
            chat_type = recipient.get('chat_type', 'private')
            text = body.get('text', '')
            
            sender_name = sender.get('name', 'Unknown')
            
            # Определяем тип чата
            is_group = chat_id < 0
            chat_label = "группа" if is_group else "личка"
            
            print(f"[{chat_label}] {sender_name}: {text}")
            
            # Обработка команд
            if text.startswith('/'):
                command = text.split()[0]
                
                if command == '/start':
                    response = f"Привет! Это {'групповой' if is_group else 'личный'} чат"
                    client.send_message(chat_id=chat_id, text=response)
                
                elif command == '/chatid':
                    response = f"Chat ID: {chat_id}\nТип: {chat_type}"
                    client.send_message(chat_id=chat_id, text=response)
            
            else:
                # Эхо
                response = f"Эхо: {text}"
                client.send_message(chat_id=chat_id, text=response)
```

## Частые проблемы

### ❌ Бот не получает сообщения из группы

**Причина**: Бот не назначен администратором

**Решение**: 
1. Откройте групповой чат
2. Настройки → Участники
3. Найдите бота
4. Назначьте администратором

### ❌ Ошибка "Невалидный chat_id" для группы

**Причина**: Старая версия библиотеки не поддерживала отрицательные chat_id

**Решение**: Обновите библиотеку
```bash
pip install --upgrade git+https://github.com/nepobo/max-api.git
```

### ❌ Бот отвечает не в ту группу

**Причина**: Используется неправильный chat_id

**Решение**: Всегда используйте `recipient['chat_id']` для ответа:
```python
chat_id = message['recipient']['chat_id']  # ПРАВИЛЬНО
# НЕ sender['user_id'] для групповых чатов!
```

## Лучшие практики

### ✅ Проверяйте тип чата

```python
def get_reply_chat_id(message):
    """Получить chat_id для ответа"""
    return message['recipient']['chat_id']
```

### ✅ Логируйте информацию о чате

```python
chat_id = recipient['chat_id']
chat_type = recipient.get('chat_type', 'private')
is_group = chat_id < 0

logger.info(f"Message from {'group' if is_group else 'user'} {chat_id}")
```

### ✅ Разная логика для групп и личных чатов

```python
if chat_id < 0:
    # Групповая логика: может быть много участников
    handle_group_message(message)
else:
    # Личная логика: один на один
    handle_private_message(message)
```

## Резюме

| Параметр | Личный чат | Групповой чат |
|----------|-----------|---------------|
| **chat_id** | Положительный | Отрицательный |
| **chat_type** | `"private"` | `"group"` или `"channel"` |
| **Права бота** | Не требуются | **Администратор!** |
| **Получение событий** | Автоматически | Только если администратор |
| **Ответ** | `sender['user_id']` или `recipient['chat_id']` | `recipient['chat_id']` |

**🎯 Главное правило**: Для работы с групповыми чатами бот ДОЛЖЕН быть администратором!
