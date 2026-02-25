#!/usr/bin/env python3
"""
Скрипт для получения информации о боте по токену
Использование: python get_bot_info.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient, MAXAPIException
from dotenv import load_dotenv

load_dotenv()


def get_bot_info_from_token(token):
    """Получение информации о боте по токену"""
    try:
        client = MAXClient(token=token)
        bot_info = client.get_me()
        return bot_info, None
    except MAXAPIException as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)


def print_bot_info(bot_info):
    """Красивый вывод информации о боте"""
    print("\n" + "="*70)
    print("🤖 ИНФОРМАЦИЯ О БОТЕ")
    print("="*70)
    
    print(f"\n📝 Основная информация:")
    print(f"   Имя:       {bot_info.get('name', 'N/A')}")
    print(f"   Username:  @{bot_info.get('username', 'N/A')}")
    print(f"   ID:        {bot_info.get('user_id', 'N/A')}")
    print(f"   Это бот:   {'Да' if bot_info.get('is_bot') else 'Нет'}")
    
    if 'last_activity_time' in bot_info:
        from datetime import datetime
        timestamp = bot_info['last_activity_time'] / 1000
        dt = datetime.fromtimestamp(timestamp)
        print(f"   Последняя активность: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n🔗 Публичная ссылка:")
    print(f"   https://max.ru/{bot_info.get('username', 'N/A')}")
    
    print(f"\n📱 QR-код для пользователей:")
    print(f"   Создайте QR-код со ссылкой выше")
    
    print(f"\n💬 Deeplink с параметрами:")
    print(f"   https://max.ru/{bot_info.get('username', 'N/A')}?start=<payload>")
    
    print(f"\n🔍 Как пользователи могут найти бота:")
    print(f"   1. Поиск в MAX: @{bot_info.get('username', 'N/A')}")
    print(f"   2. Прямая ссылка: https://max.ru/{bot_info.get('username', 'N/A')}")
    print(f"   3. QR-код с этой ссылкой")
    
    print("\n" + "="*70 + "\n")


def main():
    print("\n" + "="*70)
    print("🔍 Получение информации о боте по токену")
    print("="*70)
    
    # Проверяем токен в .env
    token = os.getenv('MAX_BOT_TOKEN')
    
    if not token:
        print("\n❌ Токен не найден в .env файле")
        print("\nВыберите один из вариантов:")
        print("1. Создайте файл .env и добавьте: MAX_BOT_TOKEN=ваш_токен")
        print("2. Введите токен вручную ниже")
        print()
        
        choice = input("Ввести токен вручную? (y/n): ").strip().lower()
        if choice == 'y':
            token = input("\nВведите токен бота: ").strip()
            if not token:
                print("\n❌ Токен не может быть пустым")
                return
        else:
            print("\n❌ Операция отменена")
            return
    
    print("\n⏳ Получение информации...")
    
    bot_info, error = get_bot_info_from_token(token)
    
    if error:
        print(f"\n❌ Ошибка: {error}")
        print("\nВозможные причины:")
        print("1. Неверный токен")
        print("2. Токен устарел или был обновлён")
        print("3. Нет подключения к интернету")
        print("4. Проблемы с API MAX")
        print("\nПроверьте токен на https://business.max.ru/self")
        return
    
    print("\n✅ Информация получена успешно!")
    print_bot_info(bot_info)
    
    # Сохранение в файл (опционально)
    save = input("Сохранить информацию в файл? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"bot_info_{bot_info.get('username', 'unknown')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Информация о боте\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Имя: {bot_info.get('name')}\n")
            f.write(f"Username: @{bot_info.get('username')}\n")
            f.write(f"ID: {bot_info.get('user_id')}\n")
            f.write(f"Публичная ссылка: https://max.ru/{bot_info.get('username')}\n")
            f.write(f"\nТокен (первые 10 символов): {token[:10]}...\n")
        
        print(f"\n✅ Информация сохранена в файл: {filename}")


if __name__ == '__main__':
    main()
