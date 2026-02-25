"""
Бот для получения chat_id
Напишите боту любое сообщение, и он ответит вашим chat_id и user_id
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
        print("❌ Ошибка: MAX_BOT_TOKEN не найден в .env")
        print("\nСоздайте файл .env и добавьте:")
        print("MAX_BOT_TOKEN=ваш_токен_здесь")
        return
    
    client = MAXClient(token=token)
    
    try:
        bot_info = client.get_me()
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        print("\nПроверьте:")
        print("1. Правильность токена в .env")
        print("2. Интернет-соединение")
        print("3. Статус бота на https://business.max.ru/self")
        return
    
    print("\n" + "="*70)
    print(f"✓ Бот '{bot_info['name']}' запущен!")
    print(f"  Username: @{bot_info['username']}")
    print(f"  Bot ID: {bot_info['user_id']}")
    print("="*70)
    
    print("\n📱 КАК ПОЛУЧИТЬ CHAT_ID:")
    print("="*70)
    print(f"1. Откройте MAX на телефоне или в браузере")
    print(f"2. Найдите бота: @{bot_info['username']}")
    print(f"   или перейдите по ссылке: https://max.ru/{bot_info['username']}")
    print(f"3. Нажмите 'Начать' или 'Написать'")
    print(f"4. Напишите боту любое сообщение")
    print(f"5. Бот ответит вашим chat_id")
    print("="*70)
    
    print("\n⏳ Ожидание сообщений... (Ctrl+C для остановки)\n")
    
    last_marker = None
    users_count = 0
    
    try:
        while True:
            updates = client.get_updates(timeout=30, marker=last_marker)
            
            for update in updates:
                update_type = update.get('update_type')
                
                # Обработка запуска бота через deeplink
                if update_type == 'bot_started':
                    chat_id = update.get('chat_id')
                    user = update.get('user', {})
                    payload = update.get('payload', '')
                    
                    users_count += 1
                    
                    print(f"\n🚀 [{users_count}] Бот запущен!")
                    print(f"   👤 Пользователь: {user.get('name')}")
                    print(f"   🆔 User ID: {user.get('user_id')}")
                    print(f"   💬 Chat ID: {chat_id}")
                    if payload:
                        print(f"   📦 Payload: {payload}")
                    
                    # Отправка приветствия с chat_id
                    welcome_text = (
                        f"👋 Привет, {user.get('name')}!\n\n"
                        f"📌 **Ваша информация:**\n"
                        f"• Chat ID: `{chat_id}`\n"
                        f"• User ID: `{user.get('user_id')}`\n"
                        f"• Username: @{user.get('username', 'не указан')}\n\n"
                        f"💡 Сохраните chat_id для отправки сообщений через API!\n\n"
                        f"📝 Используйте в коде:\n"
                        f"```python\n"
                        f"client.send_message(\n"
                        f"    chat_id={chat_id},\n"
                        f"    text='Привет!'\n"
                        f")\n"
                        f"```"
                    )
                    
                    if payload:
                        welcome_text += f"\n\n📦 Получен payload: `{payload}`"
                    
                    client.send_message(
                        chat_id=chat_id,
                        text=welcome_text,
                        format="markdown"
                    )
                
                # Обработка обычных сообщений
                elif update_type == 'message_created':
                    message = update.get('message', {})
                    sender = message.get('sender', {})
                    body = message.get('body', {})
                    
                    # Получаем chat_id отправителя
                    chat_id = sender.get('user_id')
                    text = body.get('text', '')
                    
                    users_count += 1
                    
                    print(f"\n💬 [{users_count}] Получено сообщение:")
                    print(f"   👤 От: {sender.get('name')}")
                    print(f"   🆔 User ID: {sender.get('user_id')}")
                    print(f"   💬 Chat ID: {chat_id}")
                    print(f"   📝 Текст: {text[:50]}{'...' if len(text) > 50 else ''}")
                    
                    # Формирование ответа
                    response_text = (
                        f"📌 **Информация о чате:**\n\n"
                        f"👤 Ваше имя: {sender.get('name')}\n"
                        f"🆔 User ID: `{sender.get('user_id')}`\n"
                        f"💬 Chat ID: `{chat_id}`\n"
                        f"📝 Username: @{sender.get('username', 'не указан')}\n\n"
                        f"📋 Вы написали: \"{text}\"\n\n"
                        f"💡 Используйте chat_id `{chat_id}` для отправки сообщений!"
                    )
                    
                    # Отправка ответа
                    client.send_message(
                        chat_id=chat_id,
                        text=response_text,
                        format="markdown"
                    )
                    
                    print(f"   ✓ Ответ отправлен")
                
                # Обработка нажатия на кнопки
                elif update_type == 'message_callback':
                    callback = update.get('callback', {})
                    user = callback.get('user', {})
                    payload = callback.get('payload', '')
                    message = callback.get('message', {})
                    chat_id = message.get('recipient', {}).get('chat_id')
                    
                    print(f"\n🔘 Нажатие на кнопку:")
                    print(f"   👤 От: {user.get('name')}")
                    print(f"   📦 Payload: {payload}")
                    
                    if chat_id:
                        client.send_message(
                            chat_id=chat_id,
                            text=f"Вы нажали кнопку: {payload}"
                        )
                
                # Обновляем маркер
                if 'marker' in update:
                    last_marker = update['marker']
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print(f"✓ Бот остановлен. Обработано событий: {users_count}")
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    
    finally:
        client.close()


if __name__ == '__main__':
    main()
