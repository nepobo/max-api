"""
Простой бот с командами
Отвечает на команды /start, /help, /info
"""

import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient
from max_api.utils import build_inline_keyboard
from dotenv import load_dotenv

load_dotenv()


def handle_start(client, chat_id, user_name):
    """Обработка команды /start"""
    text = f"Привет, {user_name}! 👋\n\nЯ простой бот для демонстрации MAX API."
    
    # Создаем клавиатуру с кнопками
    keyboard = build_inline_keyboard([
        [
            {"type": "callback", "text": "📊 Статистика", "payload": "stats"},
            {"type": "callback", "text": "ℹ️ О боте", "payload": "about"}
        ],
        [
            {"type": "link", "text": "🌐 Документация MAX", "url": "https://dev.max.ru/docs-api"}
        ]
    ])
    
    client.send_message(chat_id=chat_id, text=text, attachments=[keyboard])


def handle_help(client, chat_id):
    """Обработка команды /help"""
    text = """
📖 **Доступные команды:**

/start - Начать работу с ботом
/help - Показать это сообщение
/info - Информация о боте
/time - Текущее время

Вы также можете просто написать мне любое сообщение!
    """.strip()
    
    client.send_message(chat_id=chat_id, text=text, format="markdown")


def handle_info(client, chat_id, bot_info):
    """Обработка команды /info"""
    text = f"""
🤖 **Информация о боте**

Имя: {bot_info['name']}
Username: @{bot_info['username']}
ID: {bot_info['user_id']}

Этот бот создан с использованием библиотеки max-api для Python.
    """.strip()
    
    client.send_message(chat_id=chat_id, text=text, format="markdown")


def handle_time(client, chat_id):
    """Обработка команды /time"""
    now = datetime.now()
    text = f"🕐 Текущее время: {now.strftime('%H:%M:%S')}\n📅 Дата: {now.strftime('%d.%m.%Y')}"
    client.send_message(chat_id=chat_id, text=text)


def handle_callback(client, callback):
    """Обработка нажатия на inline-кнопку"""
    payload = callback.get('payload', '')
    user = callback.get('user', {})
    message = callback.get('message', {})
    chat_id = message.get('recipient', {}).get('chat_id')
    
    if not chat_id:
        return
    
    if payload == 'stats':
        text = "📊 **Статистика бота:**\n\nСообщений обработано: 42\nПользователей: 10\nВремя работы: 2 часа"
        client.send_message(chat_id=chat_id, text=text, format="markdown")
    
    elif payload == 'about':
        text = "ℹ️ **О боте:**\n\nЭто демонстрационный бот, созданный для примера работы с MAX API."
        client.send_message(chat_id=chat_id, text=text, format="markdown")


def main():
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("Ошибка: токен не найден")
        return
    
    client = MAXClient(token=token)
    bot_info = client.get_me()
    
    print(f"Бот '{bot_info['name']}' запущен!")
    print("Ожидание сообщений...")
    print("-" * 60)
    
    last_marker = None
    
    try:
        while True:
            try:
                updates = client.get_updates(timeout=30, marker=last_marker)
            except Exception as e:
                if "Превышено время ожидания" in str(e) or "timed out" in str(e).lower():
                    continue
                else:
                    print(f"\nОшибка: {e}")
                    print("Повторная попытка через 5 секунд...")
                    time.sleep(5)
                    continue
            
            for update in updates:
                update_type = update.get('update_type')
                
                # Обработка сообщений
                if update_type == 'message_created':
                    message = update.get('message', {})
                    sender = message.get('sender', {})
                    body = message.get('body', {})
                    text = body.get('text', '').strip()
                    
                    # Получаем chat_id отправителя
                    chat_id = sender.get('user_id')
                    
                    print(f"Сообщение от {sender.get('name')} (chat_id: {chat_id}): {text}")
                    
                    if not chat_id:
                        continue
                    
                    # Обработка команд
                    if text == '/start':
                        handle_start(client, chat_id, sender.get('name', 'друг'))
                    
                    elif text == '/help':
                        handle_help(client, chat_id)
                    
                    elif text == '/info':
                        handle_info(client, chat_id, bot_info)
                    
                    elif text == '/time':
                        handle_time(client, chat_id)
                    
                    elif text:
                        # Ответ на обычное сообщение
                        response = f"Вы написали: '{text}'\n\nИспользуйте /help для списка команд."
                        client.send_message(chat_id=chat_id, text=response)
                
                # Обработка callback-событий (нажатия на кнопки)
                elif update_type == 'message_callback':
                    callback = update.get('callback', {})
                    print(f"Callback: {callback.get('payload')}")
                    handle_callback(client, callback)
                
                # Обработка запуска бота
                elif update_type == 'bot_started':
                    user = update.get('user', {})
                    chat_id = update.get('chat_id')
                    print(f"Бот запущен пользователем {user.get('name')}")
                    
                    if chat_id:
                        handle_start(client, chat_id, user.get('name', 'друг'))
                
                # Обновляем маркер
                if 'marker' in update:
                    last_marker = update['marker']
    
    except KeyboardInterrupt:
        print("\n\nБот остановлен")
    finally:
        client.close()


if __name__ == '__main__':
    main()
