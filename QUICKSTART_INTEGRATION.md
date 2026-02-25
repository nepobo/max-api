# 🚀 Быстрый старт для интеграции

## Вариант 1: Копирование библиотеки (рекомендуется для простых проектов)

```bash
# 1. Скопируйте папку max_api в ваш проект
cp -r /path/to/max-api/max_api /path/to/your-project/

# 2. Установите зависимости
cd /path/to/your-project
pip install requests python-dotenv

# 3. Создайте .env файл
echo "MAX_BOT_TOKEN=your_token_here" > .env

# 4. Используйте в коде
```

```python
from max_api import MAXClient
import os

client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))
bot = client.get_me()
print(f"Бот: {bot['name']}")

# Отправка сообщения
client.send_message(chat_id=12374848, text="Привет!")
```

---

## Вариант 2: Установка как пакет

```bash
# Из Git репозитория
pip install git+https://github.com/nepobo/max-api.git

# Или локально
pip install /path/to/max-api
```

```python
from max_api import MAXClient
# Используйте как обычную библиотеку
```

---

## Вариант 3: Git Submodule (для больших проектов)

```bash
cd your-project
git submodule add https://github.com/nepobo/max-api.git libs/max-api
pip install -e libs/max-api
```

---

## Шаблон бота (копируй и используй)

```python
#!/usr/bin/env python3
"""
MAX Messenger Bot
"""
from max_api import MAXClient
from max_api.exceptions import MAXAPIException
import os
import time
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка .env
load_dotenv()


def main():
    # Инициализация
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        logger.error("MAX_BOT_TOKEN not found in .env")
        return
    
    client = MAXClient(token=token)
    
    # Запуск
    bot_info = client.get_me()
    logger.info(f"Bot '{bot_info['name']}' started!")
    
    last_marker = None
    
    try:
        while True:
            # Получение обновлений
            try:
                updates = client.get_updates(timeout=30, marker=last_marker)
            except Exception as e:
                if "timeout" in str(e).lower():
                    continue  # Timeout - это нормально
                logger.error(f"Error getting updates: {e}")
                time.sleep(5)
                continue
            
            # Обработка сообщений
            for update in updates:
                try:
                    if update.get('update_type') == 'message_created':
                        message = update['message']
                        
                        # Извлечение данных
                        chat_id = message['sender']['user_id']
                        text = message.get('body', {}).get('text', '')
                        sender_name = message['sender'].get('name', 'Unknown')
                        
                        logger.info(f"Message from {sender_name}: {text}")
                        
                        # ВАША ЛОГИКА ЗДЕСЬ
                        if text.startswith('/start'):
                            client.send_message(
                                chat_id=chat_id,
                                text="Привет! Я бот 👋"
                            )
                        elif text.startswith('/help'):
                            client.send_message(
                                chat_id=chat_id,
                                text="Доступные команды:\n/start\n/help"
                            )
                        else:
                            # Эхо
                            client.send_message(
                                chat_id=chat_id,
                                text=f"Вы написали: {text}"
                            )
                    
                    # Обновление маркера
                    if 'marker' in update:
                        last_marker = update['marker']
                
                except MAXAPIException as e:
                    logger.error(f"API error: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error: {e}", exc_info=True)
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        client.close()
        logger.info("Connection closed")


if __name__ == "__main__":
    main()
```

---

## Структура проекта

```
your-project/
├── .env                    # MAX_BOT_TOKEN=...
├── requirements.txt        # requests, python-dotenv
├── bot.py                  # Код бота (шаблон выше)
├── max_api/               # Библиотека (скопированная)
│   ├── __init__.py
│   ├── client.py
│   ├── exceptions.py
│   └── utils.py
└── README.md
```

---

## Требования

- Python 3.8+
- requests
- python-dotenv

---

## Готово! 🎉

Скопируйте код шаблона → замените `# ВАША ЛОГИКА ЗДЕСЬ` → запускайте!

```bash
python bot.py
```

---

## Документация

- [README.md](README.md) - полная документация
- [INTEGRATION.md](INTEGRATION.md) - детальная интеграция
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - структура проекта
- [docs/examples/](docs/examples/) - примеры ботов
