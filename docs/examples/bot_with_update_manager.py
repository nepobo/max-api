#!/usr/bin/env python3
"""
Пример использования UpdateManager для управления режимами получения обновлений.

Демонстрирует:
- Использование Long Polling (для разработки)
- Переключение на Webhook (для production)
- Получение статуса режима
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from max_api import MAXClient, UpdateManager, UpdateMode
from max_api.exceptions import MAXAPIException
from dotenv import load_dotenv

load_dotenv()


def example_long_polling():
    """Пример использования Long Polling (для разработки)"""
    print("="*60)
    print("ПРИМЕР: Long Polling (режим разработки)")
    print("="*60)
    
    token = os.getenv('MAX_BOT_TOKEN')
    client = MAXClient(token=token)
    
    # Создаём менеджер обновлений в режиме Long Polling (по умолчанию)
    manager = UpdateManager(client, mode=UpdateMode.LONG_POLLING)
    
    bot_info = client.get_me()
    print(f"\n✅ Бот '{bot_info['name']}' запущен в режиме Long Polling")
    print(f"📊 Статус: {manager.get_status()}")
    print("\nОжидание сообщений... (Ctrl+C для остановки)\n")
    
    try:
        message_count = 0
        max_messages = 3  # Обработаем 3 сообщения для примера
        
        while message_count < max_messages:
            try:
                # Получаем обновления через менеджер
                updates = manager.get_updates(timeout=30)
                
                for update in updates:
                    if update.get('update_type') == 'message_created':
                        message = update['message']
                        chat_id = message['sender']['user_id']
                        text = message.get('body', {}).get('text', '')
                        
                        print(f"📨 Получено: {text}")
                        
                        client.send_message(
                            chat_id=chat_id,
                            text=f"Long Polling режим: {text}"
                        )
                        
                        message_count += 1
                        print(f"✅ Ответ отправлен ({message_count}/{max_messages})\n")
            
            except Exception as e:
                if "timeout" in str(e).lower():
                    print("⏱️  Timeout (нормально для Long Polling)")
                    continue
                raise
    
    except KeyboardInterrupt:
        print("\n\n👋 Остановлено")
    finally:
        client.close()


def example_webhook():
    """Пример настройки Webhook (для production)"""
    print("\n" + "="*60)
    print("ПРИМЕР: Webhook (режим production)")
    print("="*60)
    
    token = os.getenv('MAX_BOT_TOKEN')
    client = MAXClient(token=token)
    
    # Создаём менеджер в режиме Long Polling
    manager = UpdateManager(client, mode=UpdateMode.LONG_POLLING)
    
    bot_info = client.get_me()
    print(f"\n✅ Бот '{bot_info['name']}' запущен")
    print(f"📊 Текущий режим: {manager.mode.value}")
    
    # Ваш HTTPS URL для webhook (замените на реальный)
    webhook_url = "https://your-domain.com/webhook"
    
    print(f"\n🔄 Переключение на Webhook режим...")
    print(f"📡 URL: {webhook_url}")
    
    try:
        # Переключаемся на Webhook
        subscription = manager.switch_to_webhook(webhook_url)
        
        print(f"\n✅ Webhook настроен!")
        print(f"📊 Подписка ID: {subscription.get('id')}")
        print(f"📊 URL: {subscription.get('url')}")
        print(f"📊 Статус: {manager.get_status()}")
        
        # Получаем информацию о webhook
        webhook_info = manager.get_webhook_info()
        if webhook_info:
            print(f"\n📋 Информация о webhook:")
            print(f"   ID: {webhook_info.get('id')}")
            print(f"   URL: {webhook_info.get('url')}")
            print(f"   Создан: {webhook_info.get('created_at', 'N/A')}")
        
        # Демонстрация: попытка использовать get_updates в режиме Webhook
        print("\n⚠️  Попытка вызвать get_updates() в режиме Webhook...")
        try:
            manager.get_updates()
        except RuntimeError as e:
            print(f"❌ Ошибка (ожидаемо): {e}")
        
        # Переключение обратно на Long Polling
        print("\n🔄 Переключение обратно на Long Polling...")
        manager.switch_to_long_polling()
        print(f"✅ Режим изменён: {manager.mode.value}")
        print(f"📊 Статус: {manager.get_status()}")
    
    except ValueError as e:
        print(f"❌ Ошибка валидации: {e}")
    except MAXAPIException as e:
        print(f"❌ Ошибка API: {e}")
    finally:
        client.close()


def example_mode_switching():
    """Пример переключения между режимами"""
    print("\n" + "="*60)
    print("ПРИМЕР: Переключение между режимами")
    print("="*60)
    
    token = os.getenv('MAX_BOT_TOKEN')
    client = MAXClient(token=token)
    
    # Начинаем с Long Polling
    manager = UpdateManager(client)
    
    print(f"\n1️⃣  Начальный режим: {manager.mode.value}")
    print(f"   Long Polling? {manager.is_long_polling}")
    print(f"   Webhook? {manager.is_webhook}")
    
    # Переключаемся на Webhook
    webhook_url = "https://example.com/webhook"
    print(f"\n2️⃣  Переключение на Webhook...")
    
    try:
        manager.switch_to_webhook(webhook_url)
        print(f"   ✅ Режим: {manager.mode.value}")
        print(f"   📡 URL: {manager.webhook_url}")
        
        # Удаляем webhook и возвращаемся к Long Polling
        print(f"\n3️⃣  Удаление webhook...")
        manager.delete_webhook()
        print(f"   ✅ Режим: {manager.mode.value}")
        print(f"   Long Polling? {manager.is_long_polling}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        client.close()


def main():
    """Главная функция"""
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("❌ MAX_BOT_TOKEN не найден в .env")
        return
    
    print("\n🤖 MAX API - UpdateManager Examples\n")
    
    # Выбор примера
    print("Выберите пример:")
    print("1. Long Polling (разработка)")
    print("2. Webhook (production)")
    print("3. Переключение между режимами")
    
    choice = input("\nВведите номер (1-3) или Enter для всех: ").strip()
    
    if choice == "1":
        example_long_polling()
    elif choice == "2":
        example_webhook()
    elif choice == "3":
        example_mode_switching()
    else:
        # Запускаем все примеры по очереди (кроме Long Polling с ожиданием)
        example_webhook()
        example_mode_switching()
        print("\n✅ Все примеры выполнены!")


if __name__ == "__main__":
    main()
