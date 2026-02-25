"""
Пример отправки сообщения с inline-клавиатурой
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient
from max_api.utils import build_inline_keyboard
from dotenv import load_dotenv

load_dotenv()


def main():
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("Ошибка: токен не найден")
        return
    
    # Получаем chat_id из аргументов командной строки
    if len(sys.argv) < 2:
        print("Использование: python keyboard_example.py <chat_id>")
        return
    
    try:
        chat_id = int(sys.argv[1])
    except ValueError:
        print("Ошибка: chat_id должен быть числом")
        return
    
    client = MAXClient(token=token)
    
    # Пример 1: Простая клавиатура с callback-кнопками
    print("Отправка сообщения с простой клавиатурой...")
    keyboard1 = build_inline_keyboard([
        [
            {"type": "callback", "text": "Кнопка 1", "payload": "button_1"},
            {"type": "callback", "text": "Кнопка 2", "payload": "button_2"}
        ],
        [
            {"type": "callback", "text": "Кнопка 3", "payload": "button_3"}
        ]
    ])
    
    client.send_message(
        chat_id=chat_id,
        text="Выберите кнопку:",
        attachments=[keyboard1]
    )
    print("✓ Сообщение 1 отправлено")
    
    # Пример 2: Клавиатура с разными типами кнопок
    print("\nОтправка сообщения с разными типами кнопок...")
    keyboard2 = build_inline_keyboard([
        [
            {"type": "callback", "text": "📊 Статистика", "payload": "stats"},
            {"type": "callback", "text": "⚙️ Настройки", "payload": "settings"}
        ],
        [
            {"type": "link", "text": "🌐 Открыть сайт", "url": "https://max.ru"}
        ],
        [
            {"type": "request_contact", "text": "📱 Поделиться контактом"},
            {"type": "request_geo_location", "text": "📍 Моя геопозиция"}
        ]
    ])
    
    client.send_message(
        chat_id=chat_id,
        text="**Меню действий:**\n\nВыберите нужное действие из списка ниже.",
        format="markdown",
        attachments=[keyboard2]
    )
    print("✓ Сообщение 2 отправлено")
    
    # Пример 3: Клавиатура для опроса
    print("\nОтправка опроса с клавиатурой...")
    keyboard3 = build_inline_keyboard([
        [
            {"type": "callback", "text": "👍 Отлично", "payload": "rating_5"},
            {"type": "callback", "text": "😊 Хорошо", "payload": "rating_4"}
        ],
        [
            {"type": "callback", "text": "😐 Нормально", "payload": "rating_3"},
            {"type": "callback", "text": "😞 Плохо", "payload": "rating_2"}
        ],
        [
            {"type": "callback", "text": "😡 Ужасно", "payload": "rating_1"}
        ]
    ])
    
    client.send_message(
        chat_id=chat_id,
        text="❓ **Как вам наш сервис?**\n\nОцените качество обслуживания:",
        format="markdown",
        attachments=[keyboard3]
    )
    print("✓ Сообщение 3 отправлено")
    
    print(f"\n✅ Все сообщения отправлены в чат {chat_id}")
    
    client.close()


if __name__ == '__main__':
    main()
