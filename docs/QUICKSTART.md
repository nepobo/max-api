# Руководство по быстрому старту

## 1. Установка

### Из исходников

```bash
git clone https://github.com/nepobo/max-api.git
cd max-api
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

## 2. Получение токена бота

1. Зарегистрируйтесь на [платформе MAX для партнёров](https://business.max.ru/self)
2. Создайте чат-бота
3. После модерации получите токен в разделе "Интеграция → Получить токен"

## 3. Настройка

Создайте файл `.env` в корне проекта:

```env
MAX_BOT_TOKEN=ваш_токен_здесь
```

## 4. Первый бот

Создайте файл `my_first_bot.py`:

```python
from max_api import MAXClient
import os
from dotenv import load_dotenv

load_dotenv()

# Создание клиента
client = MAXClient(token=os.getenv('MAX_BOT_TOKEN'))

# Получение информации о боте
bot = client.get_me()
print(f"Бот: {bot['name']}")

# Прослушивание сообщений
print("Ожидание сообщений...")
while True:
    updates = client.get_updates(timeout=30)
    
    for update in updates:
        if update.get('update_type') == 'message_created':
            message = update['message']
            chat_id = message['recipient']['chat_id']
            text = message['body']['text']
            
            # Отправляем ответ
            client.send_message(
                chat_id=chat_id,
                text=f"Вы написали: {text}"
            )
```

Запустите бота:

```bash
python my_first_bot.py
```

## 5. Использование консольного приложения

```bash
python -m console_app.main
```

Или после установки пакета:

```bash
max-console
```

## 6. Примеры

В папке `examples/` находятся готовые примеры:

- `echo_bot.py` - простой эхо-бот
- `simple_bot.py` - бот с командами
- `keyboard_example.py` - примеры работы с клавиатурой

Запуск примера:

```bash
python examples/echo_bot.py
```

## 7. Тестирование

Запуск тестов:

```bash
pytest tests/
```

С покрытием:

```bash
pytest tests/ --cov=max_api --cov-report=html
```

## Следующие шаги

- Изучите [полную документацию API](https://dev.max.ru/docs-api)
- Посмотрите примеры в папке `examples/`
- Прочитайте README.md для подробной информации
