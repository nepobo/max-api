"""
Простой эхо-бот
Повторяет все сообщения, которые ему отправляют пользователи
"""

import sys
import os
import time

# Добавляем родительскую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

def main():
    # Получение токена
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("Ошибка: токен не найден. Установите переменную MAX_BOT_TOKEN")
        return
    
    # Создание клиента
    client = MAXClient(token=token)
    
    # Получение информации о боте
    bot_info = client.get_me()
    print(f"Бот '{bot_info['name']}' запущен!")
    print("Ожидание сообщений... (Ctrl+C для остановки)")
    print("-" * 60)
    
    last_marker = None
    
    try:
        while True:
            try:
                # Получение обновлений
                updates = client.get_updates(timeout=30, marker=last_marker)
            except Exception as e:
                # Long Polling timeout - это нормально, просто продолжаем
                if "Превышено время ожидания" in str(e) or "timed out" in str(e).lower():
                    continue
                else:
                    print(f"\nОшибка при получении обновлений: {e}")
                    print("Повторная попытка через 5 секунд...")
                    time.sleep(5)
                    continue
            
            for update in updates:
                update_type = update.get('update_type')
                
                # Обработка новых сообщений
                if update_type == 'message_created':
                    message = update.get('message', {})
                    sender = message.get('sender', {})
                    body = message.get('body', {})
                    text = body.get('text', '')
                    
                    # Получаем chat_id отправителя для ответа
                    chat_id = sender.get('user_id')
                    
                    print(f"\nПолучено сообщение от {sender.get('name')} (chat_id: {chat_id}): {text}")
                    
                    if text and chat_id:
                        # Отправляем обратно то же сообщение
                        response_text = f"Вы написали: {text}"
                        client.send_message(chat_id=chat_id, text=response_text)
                        print(f"Ответ отправлен в чат {chat_id}")
                
                # Обновляем маркер
                if 'marker' in update:
                    last_marker = update['marker']
    
    except KeyboardInterrupt:
        print("\n\nБот остановлен")
    finally:
        client.close()


if __name__ == '__main__':
    main()
