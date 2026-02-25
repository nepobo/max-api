# 🤖 Шпаргалка: Подключение бота к чату MAX

## ⚡ Быстрый старт

### 1. Запустите бота для получения chat_id
```bash
source venv/bin/activate
python examples/get_chat_id_bot.py
```

### 2. Откройте MAX и найдите бота
- Откройте MAX (телефон/браузер)
- Поиск → введите username бота (показан при запуске)
- Нажмите "Начать" или "Написать"

### 3. Напишите боту любое сообщение
Бот ответит вашим `chat_id` и `user_id`

### 4. Используйте chat_id для отправки сообщений
```python
from max_api import MAXClient
client = MAXClient(token="YOUR_TOKEN")
client.send_message(chat_id=123456789, text="Привет!")
```

---

## 📋 Где взять информацию о боте

### Способ 1: Быстрая команда
```bash
source venv/bin/activate
python quick_bot_info.py
```

### Способ 2: Подробная информация
```bash
bash bot-info.sh
# или
source venv/bin/activate
python examples/get_bot_info.py
```

### Способ 3: Одна строка в терминале
```bash
source venv/bin/activate
python -c "from max_api import MAXClient; from dotenv import load_dotenv; import os; load_dotenv(); bot = MAXClient(os.getenv('MAX_BOT_TOKEN')).get_me(); print(f\"Имя: {bot['name']}\nUsername: @{bot['username']}\nСсылка: https://max.ru/{bot['username']}\")"
```

### Способ 4: В Python коде
```python
from max_api import MAXClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))
bot = client.get_me()

print(f"Имя: {bot['name']}")
print(f"Username: @{bot['username']}")
print(f"ID: {bot['user_id']}")
print(f"Ссылка: https://max.ru/{bot['username']}")
```

---

## 🔗 Публичная ссылка на бота

Формат: `https://max.ru/<username>`

Поделитесь этой ссылкой с пользователями!

---

## 💬 Типы чатов

| Тип | Описание | Как получить chat_id |
|-----|----------|---------------------|
| **dialog** | Личный чат с пользователем | Пользователь пишет боту |
| **group** | Групповой чат | Добавьте бота в группу* |
| **channel** | Канал | Добавьте бота в канал* |

\* *Требуется включить в настройках бота на платформе MAX*

---

## ⚙️ Включение групповых чатов

1. Перейдите: https://business.max.ru/self
2. Выберите бота
3. **Чат-бот и мини-приложение** → **Настроить**
4. **Включите** "Разрешить добавление в групповые чаты"
5. **Сохранить**

---

## 🎯 Получение chat_id - все способы

### Способ 1: Через get_chat_id_bot.py
```bash
python examples/get_chat_id_bot.py
# Напишите боту → получите chat_id
```

### Способ 2: Через консольное приложение
```bash
python -m console_app.main
# Выберите "2. Слушать входящие сообщения"
# Напишите боту → увидите chat_id в консоли
```

### Способ 3: Через код
```python
updates = client.get_updates()
for update in updates:
    if update.get('update_type') == 'message_created':
        chat_id = update['message']['recipient']['chat_id']
        print(f"Chat ID: {chat_id}")
```

---

## 📤 Отправка сообщения

```python
from max_api import MAXClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))

# Простое сообщение
client.send_message(
    chat_id=123456789,
    text="Привет!"
)

# С форматированием
client.send_message(
    chat_id=123456789,
    text="**Жирный** и *курсив*",
    format="markdown"
)

# С клавиатурой
from max_api.utils import build_inline_keyboard

keyboard = build_inline_keyboard([
    [{"type": "callback", "text": "Кнопка", "payload": "btn1"}]
])

client.send_message(
    chat_id=123456789,
    text="Выберите действие:",
    attachments=[keyboard]
)
```

---

## 🔍 Поиск бота в MAX

### Для пользователя:
1. Откройте MAX
2. Нажмите 🔍 (поиск)
3. Введите `@username_бота`
4. Выберите бота
5. "Начать" или "Написать"

### Через QR-код:
Создайте QR-код со ссылкой: `https://max.ru/<username>`

---

## 🎨 Deeplink с параметрами

### Создание ссылки:
```
https://max.ru/<username>?start=<payload>
```

### Примеры:
```
https://max.ru/mybot?start=promo_2026
https://max.ru/mybot?start=ref_12345
https://max.ru/mybot?start=source_instagram
```

### Обработка в боте:
```python
if update.get('update_type') == 'bot_started':
    payload = update.get('payload', '')
    if payload == 'promo_2026':
        # Применить промо-код
        pass
```

---

## 🚀 Готовые команды

### Запуск бота для получения chat_id:
```bash
source venv/bin/activate
python examples/get_chat_id_bot.py
```

### Запуск эхо-бота:
```bash
source venv/bin/activate
python examples/echo_bot.py
```

### Запуск бота с командами:
```bash
source venv/bin/activate
python examples/simple_bot.py
```

### Отправка сообщения с клавиатурой:
```bash
source venv/bin/activate
python examples/keyboard_example.py <chat_id>
```

---

## 📞 Важные ссылки

- **Платформа MAX**: https://business.max.ru/self
- **Документация API**: https://dev.max.ru/docs-api
- **Помощь**: https://dev.max.ru/help

---

## ❓ FAQ

**Q: Как узнать username бота?**
```bash
python -c "from max_api import MAXClient; from dotenv import load_dotenv; import os; load_dotenv(); print(MAXClient(os.getenv('MAX_BOT_TOKEN')).get_me()['username'])"
```

**Q: Как получить chat_id?**
Запустите `python examples/get_chat_id_bot.py` и напишите боту

**Q: Бот не отвечает?**
- Проверьте токен в `.env`
- Убедитесь что бот прошёл модерацию
- Проверьте интернет-соединение

**Q: Как добавить бота в группу?**
1. Включите функцию на платформе MAX
2. В группе: Участники → Добавить → Найдите бота

**Q: Нужен ли chat_id для каждого пользователя?**
Да, у каждого чата (пользователя/группы) свой уникальный chat_id

---

## 📝 Шаблон для своего бота

```python
from max_api import MAXClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))

print("Бот запущен!")

last_marker = None
while True:
    updates = client.get_updates(timeout=30, marker=last_marker)
    
    for update in updates:
        if update.get('update_type') == 'message_created':
            message = update['message']
            chat_id = message['recipient']['chat_id']
            text = message['body']['text']
            
            # Ваша логика здесь
            client.send_message(chat_id=chat_id, text=f"Вы написали: {text}")
        
        if 'marker' in update:
            last_marker = update['marker']
```

---

**Готово! Теперь вы можете подключить бота к любому чату в MAX! 🎉**
