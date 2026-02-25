"""
Скрипт для отладки структуры обновлений MAX API
Показывает полную структуру полученных обновлений
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient
from dotenv import load_dotenv

load_dotenv()


def main():
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("❌ Токен не найден в .env")
        return
    
    client = MAXClient(token=token)
    bot_info = client.get_me()
    
    print("="*70)
    print(f"Бот '{bot_info['name']}' запущен!")
    print("="*70)
    print("\n📝 Отправьте боту сообщение в MAX...")
    print("Будет показана полная структура обновления\n")
    print("Ожидание... (Ctrl+C для остановки)\n")
    
    last_marker = None
    
    try:
        while True:
            updates = client.get_updates(timeout=30, marker=last_marker)
            
            for update in updates:
                print("\n" + "="*70)
                print("📬 ПОЛУЧЕНО ОБНОВЛЕНИЕ:")
                print("="*70)
                
                # Красивый вывод JSON
                print(json.dumps(update, indent=2, ensure_ascii=False))
                
                print("\n" + "="*70)
                print("🔍 АНАЛИЗ СТРУКТУРЫ:")
                print("="*70)
                
                update_type = update.get('update_type')
                print(f"\n📌 update_type: {update_type}")
                
                if update_type == 'message_created':
                    message = update.get('message', {})
                    
                    print(f"\n👤 SENDER:")
                    sender = message.get('sender', {})
                    print(f"   user_id: {sender.get('user_id')}")
                    print(f"   name: {sender.get('name')}")
                    print(f"   username: {sender.get('username')}")
                    
                    print(f"\n📨 RECIPIENT:")
                    recipient = message.get('recipient', {})
                    print(f"   user_id: {recipient.get('user_id')}")
                    print(f"   chat_id: {recipient.get('chat_id')}")
                    print(f"   chat_type: {recipient.get('chat_type')}")
                    
                    print(f"\n💬 BODY:")
                    body = message.get('body', {})
                    print(f"   text: {body.get('text')}")
                    
                    print(f"\n✅ ДЛЯ ОТВЕТА ИСПОЛЬЗОВАТЬ:")
                    print(f"   chat_id = {sender.get('user_id')} (sender.user_id)")
                    
                    # Попробуем найти правильный chat_id
                    print(f"\n🔍 ПОИСК ПРАВИЛЬНОГО chat_id:")
                    print(f"   sender.user_id: {sender.get('user_id')}")
                    print(f"   recipient.chat_id: {recipient.get('chat_id')}")
                    
                    # Проверяем, есть ли chat_id на верхнем уровне
                    if 'chat_id' in update:
                        print(f"   update.chat_id: {update.get('chat_id')}")
                    
                    if 'chat_id' in message:
                        print(f"   message.chat_id: {message.get('chat_id')}")
                
                if 'marker' in update:
                    last_marker = update['marker']
                
                print("\n" + "="*70 + "\n")
    
    except KeyboardInterrupt:
        print("\n\n✓ Отладка завершена")
    finally:
        client.close()


if __name__ == '__main__':
    main()
