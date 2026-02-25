# 🤖 Как подключить бота к чату в MAX

## Способы взаимодействия с ботом

### 1️⃣ Прямой чат с ботом (Личные сообщения)

После создания и модерации бота, пользователи могут найти его по:

**По имени бота:**
- Открыть MAX
- Нажать на поиск
- Ввести имя вашего бота
- Нажать "Написать" или "Начать"

**По публичной ссылке:**
- Формат: `https://max.ru/<botUsername>`
- Например: `https://max.ru/mybot_bot`

**По deeplink с параметрами:**
```
https://max.ru/<botUsername>?start=<payload>
```

Пример:
```
https://max.ru/mybot_bot?start=promo_2026
```

### 2️⃣ Добавление бота в групповой чат

#### Разрешение добавления в группы

По умолчанию боты **НЕ МОГУТ** быть добавлены в групповые чаты. Нужно включить эту функцию:

**Шаги:**
1. Перейдите на [платформу MAX для партнёров](https://business.max.ru/self)
2. Выберите вашего бота (если их несколько)
3. Перейдите в раздел **Чат-бот и мини-приложение → Настроить**
4. **Включите** возможность добавления бота в групповой чат
5. Нажмите **Сохранить**

#### Добавление бота в группу

После включения функции пользователи могут:

1. Открыть групповой чат в MAX
2. Нажать на информацию о чате (⋮ или i)
3. Выбрать "Участники" → "Добавить участника"
4. Найти бота по имени
5. Добавить бота в чат

### 3️⃣ Получение chat_id для отправки сообщений

Чтобы отправлять сообщения пользователю или в чат, вам нужен `chat_id`.

#### Способ 1: Получение из входящих сообщений

Когда пользователь пишет боту, вы получаете `chat_id`:

```python
from max_api import MAXClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))

print("Ожидание сообщений для получения chat_id...")

updates = client.get_updates(timeout=30)
for update in updates:
    if update.get('update_type') == 'message_created':
        message = update['message']
        chat_id = message['recipient']['chat_id']
        sender = message['sender']
        
        print(f"\n=== Получен chat_id ===")
        print(f"От: {sender.get('name')}")
        print(f"User ID: {sender.get('user_id')}")
        print(f"Chat ID: {chat_id}")
        print(f"=======================\n")
        
        # Теперь можете отправить ответ
        client.send_message(
            chat_id=chat_id,
            text=f"Ваш chat_id: {chat_id}"
        )
```

#### Способ 2: Получение при запуске бота (bot_started)

Когда пользователь впервые запускает бота или переходит по deeplink:

```python
updates = client.get_updates(timeout=30)
for update in updates:
    if update.get('update_type') == 'bot_started':
        chat_id = update.get('chat_id')
        user = update.get('user', {})
        payload = update.get('payload', '')
        
        print(f"Бот запущен пользователем {user.get('name')}")
        print(f"Chat ID: {chat_id}")
        print(f"Payload: {payload}")
        
        # Отправка приветственного сообщения
        client.send_message(
            chat_id=chat_id,
            text=f"Привет! Ваш chat_id: {chat_id}"
        )
```

---

## 📝 Пример: Бот для получения chat_id

Создайте файл `get_chat_id_bot.py`:

```python
"""
Бот для получения chat_id
Просто напишите боту любое сообщение, и он ответит вашим chat_id
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient
from dotenv import load_dotenv

load_dotenv()

def main():
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("Ошибка: MAX_BOT_TOKEN не найден в .env")
        return
    
    client = MAXClient(token=token)
    bot_info = client.get_me()
    
    print(f"✓ Бот '{bot_info['name']}' (@{bot_info['username']}) запущен!")
    print("\n" + "="*60)
    print("📱 Как получить chat_id:")
    print("="*60)
    print(f"1. Откройте MAX и найдите бота: @{bot_info['username']}")
    print("2. Напишите боту любое сообщение")
    print("3. Бот ответит вашим chat_id")
    print("="*60 + "\n")
    print("Ожидание сообщений... (Ctrl+C для остановки)\n")
    
    last_marker = None
    
    try:
        while True:
            updates = client.get_updates(timeout=30, marker=last_marker)
            
            for update in updates:
                update_type = update.get('update_type')
                
                # Обработка запуска бота
                if update_type == 'bot_started':
                    chat_id = update.get('chat_id')
                    user = update.get('user', {})
                    
                    print(f"🚀 Бот запущен: {user.get('name')} (ID: {user.get('user_id')})")
                    print(f"   Chat ID: {chat_id}\n")
                    
                    client.send_message(
                        chat_id=chat_id,
                        text=f"👋 Привет, {user.get('name')}!\n\n"
                             f"📌 Ваш chat_id: `{chat_id}`\n"
                             f"👤 Ваш user_id: `{user.get('user_id')}`\n\n"
                             f"Используйте chat_id для отправки сообщений через API.",
                        format="markdown"
                    )
                
                # Обработка сообщений
                elif update_type == 'message_created':
                    message = update.get('message', {})
                    sender = message.get('sender', {})
                    body = message.get('body', {})
                    recipient = message.get('recipient', {})
                    
                    chat_id = recipient.get('chat_id')
                    text = body.get('text', '')
                    
                    print(f"💬 Сообщение от {sender.get('name')}: {text}")
                    print(f"   Chat ID: {chat_id}")
                    print(f"   User ID: {sender.get('user_id')}\n")
                    
                    # Отправка chat_id пользователю
                    response = (
                        f"📌 **Ваша информация:**\n\n"
                        f"👤 Имя: {sender.get('name')}\n"
                        f"🆔 User ID: `{sender.get('user_id')}`\n"
                        f"💬 Chat ID: `{chat_id}`\n"
                        f"📝 Username: @{sender.get('username', 'не указан')}\n\n"
                        f"Сохраните chat_id для отправки сообщений через API!"
                    )
                    
                    client.send_message(
                        chat_id=chat_id,
                        text=response,
                        format="markdown"
                    )
                
                # Обновляем маркер
                if 'marker' in update:
                    last_marker = update['marker']
    
    except KeyboardInterrupt:
        print("\n\n✓ Бот остановлен")
    finally:
        client.close()


if __name__ == '__main__':
    main()
```

Запустите:
```bash
source venv/bin/activate
python examples/get_chat_id_bot.py
```

---

## 🔍 Поиск бота в MAX

### Для пользователей:

1. **Откройте MAX**
2. **Нажмите на поиск** (🔍)
3. **Введите ник бота** (например: `@mybot_bot`)
4. **Выберите бота** из результатов
5. **Нажмите "Написать"** или **"Начать"**

### QR-код для бота

Создайте QR-код со ссылкой на бота:
```
https://max.ru/<botUsername>
```

Пользователи могут отсканировать QR и сразу открыть бота.

---

## 🔗 Создание диплинков (Deep Links)

### Базовый диплинк
```
https://max.ru/<botUsername>
```

### Диплинк с параметрами (payload)
```
https://max.ru/<botUsername>?start=<payload>
```

**Примеры использования:**

**1. Реферальная система:**
```
https://max.ru/mybot_bot?start=ref_12345
```

**2. Отслеживание источника:**
```
https://max.ru/mybot_bot?start=source_instagram
https://max.ru/mybot_bot?start=source_website
```

**3. Промо-коды:**
```
https://max.ru/mybot_bot?start=promo_summer2026
```

**4. Конкретное действие:**
```
https://max.ru/mybot_bot?start=action_support
https://max.ru/mybot_bot?start=action_order
```

### Обработка payload в боте:

```python
updates = client.get_updates(timeout=30)
for update in updates:
    if update.get('update_type') == 'bot_started':
        payload = update.get('payload', '')
        chat_id = update.get('chat_id')
        
        if payload.startswith('ref_'):
            referrer_id = payload.replace('ref_', '')
            print(f"Реферал от пользователя: {referrer_id}")
            # Сохраните в базу данных
        
        elif payload.startswith('promo_'):
            promo_code = payload.replace('promo_', '')
            print(f"Использован промо-код: {promo_code}")
            # Примените промо-код
```

---

## 📊 Групповые чаты

### Особенности работы в группах:

1. **Бот видит все сообщения** в групповом чате
2. **Может отправлять сообщения** всем участникам
3. **Получает уведомления** о добавлении/удалении из группы

### Пример работы в группе:

```python
updates = client.get_updates(timeout=30)
for update in updates:
    if update.get('update_type') == 'message_created':
        message = update['message']
        recipient = message.get('recipient', {})
        chat_type = recipient.get('chat_type')  # 'dialog' или 'group'
        
        if chat_type == 'group':
            print("Сообщение из группового чата")
            # Особая логика для групп
        else:
            print("Личное сообщение")
```

---

## ⚙️ Настройка бота на платформе

### 1. Разрешить добавление в группы

**Путь:** Платформа MAX → Чат-бот и мини-приложение → Настроить

**Включите:** "Разрешить добавление в групповые чаты"

### 2. Настроить уведомления (Webhook или Long Polling)

**Long Polling** (для разработки):
```python
client.get_updates(timeout=30)
```

**Webhook** (для production):
```python
client.create_subscription(
    url="https://yourdomain.com/webhook",
    update_types=[
        "message_created",
        "message_callback",
        "bot_started",
        "message_edited",
        "message_removed"
    ]
)
```

---

## 💡 Полезные советы

### 1. Сохранение chat_id

Создайте базу данных для хранения chat_id пользователей:

```python
# Простой пример с JSON
import json

def save_chat_id(user_id, chat_id, name):
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except:
        users = {}
    
    users[str(user_id)] = {
        'chat_id': chat_id,
        'name': name
    }
    
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)
```

### 2. Массовая рассылка

```python
with open('users.json', 'r') as f:
    users = json.load(f)

for user_id, data in users.items():
    chat_id = data['chat_id']
    try:
        client.send_message(
            chat_id=chat_id,
            text="Привет! Это массовая рассылка."
        )
    except Exception as e:
        print(f"Ошибка отправки {chat_id}: {e}")
```

### 3. Команды для управления

```python
if text == '/id':
    response = f"Ваш chat_id: {chat_id}"
    client.send_message(chat_id=chat_id, text=response)
```

---

## 📱 Итоговая инструкция для пользователя

**Чтобы начать общаться с ботом:**

1. Откройте MAX
2. Найдите бота по имени: `@your_bot_name`
3. Нажмите "Начать" или "Написать"
4. Напишите любое сообщение
5. Бот ответит вам!

**Чтобы добавить бота в группу:**

1. Откройте групповой чат
2. Нажмите на информацию о чате
3. "Участники" → "Добавить"
4. Найдите бота и добавьте

---

## 🚀 Готово!

Теперь вы знаете:
✅ Как пользователи находят бота
✅ Как получить chat_id
✅ Как добавить бота в группы
✅ Как работать с deeplink'ами
✅ Как отправлять сообщения пользователям

**Следующий шаг:** Запустите `get_chat_id_bot.py` и получите ваш первый chat_id!
