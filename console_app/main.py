"""
Основное консольное приложение для работы с MAX Messenger
"""

import sys
import os
from datetime import datetime
from typing import Optional

# Добавляем родительскую директорию в путь для импорта max_api
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Заглушки если colorama не установлена
    class Fore:
        GREEN = YELLOW = RED = BLUE = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = RESET_ALL = ''
    class Back:
        BLACK = ''

from max_api import MAXClient, MAXAPIException
from console_app.config import config


class ConsoleApp:
    """Консольное приложение для работы с MAX"""
    
    def __init__(self):
        self.client: Optional[MAXClient] = None
        self.running = False
        self.bot_info = None
        self.last_marker = None
    
    def print_header(self):
        """Вывод заголовка приложения"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
        print(f"{Style.BRIGHT}{Fore.CYAN}  MAX Messenger - Консольное приложение для чат-ботов")
        print(f"{Style.BRIGHT}{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def print_menu(self):
        """Вывод главного меню"""
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}Главное меню:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1.{Fore.WHITE} Отправить сообщение")
        print(f"  {Fore.GREEN}2.{Fore.WHITE} Слушать входящие сообщения (Long Polling)")
        print(f"  {Fore.GREEN}3.{Fore.WHITE} Информация о боте")
        print(f"  {Fore.GREEN}4.{Fore.WHITE} Получить последние обновления")
        print(f"  {Fore.GREEN}0.{Fore.WHITE} Выход\n")
    
    def print_bot_info(self):
        """Вывод информации о боте"""
        if not self.bot_info:
            print(f"{Fore.RED}Информация о боте не загружена{Style.RESET_ALL}")
            return
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}Информация о боте:{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}ID:{Fore.WHITE} {self.bot_info.get('user_id')}")
        print(f"  {Fore.YELLOW}Имя:{Fore.WHITE} {self.bot_info.get('name')}")
        print(f"  {Fore.YELLOW}Username:{Fore.WHITE} {self.bot_info.get('username')}")
        print(f"  {Fore.YELLOW}Это бот:{Fore.WHITE} {'Да' if self.bot_info.get('is_bot') else 'Нет'}")
        
        if 'last_activity_time' in self.bot_info:
            timestamp = self.bot_info['last_activity_time'] / 1000  # Преобразуем из миллисекунд
            dt = datetime.fromtimestamp(timestamp)
            print(f"  {Fore.YELLOW}Последняя активность:{Fore.WHITE} {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def print_message(self, update: dict):
        """Красивый вывод сообщения"""
        update_type = update.get('update_type', 'unknown')
        timestamp = update.get('timestamp', 0) / 1000
        dt = datetime.fromtimestamp(timestamp)
        time_str = dt.strftime('%H:%M:%S')
        
        if update_type == 'message_created':
            message = update.get('message', {})
            sender = message.get('sender', {})
            sender_name = sender.get('name', 'Unknown')
            body = message.get('body', {})
            text = body.get('text', '')
            
            print(f"\n{Fore.GREEN}[{time_str}] 📨 Новое сообщение{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}От:{Fore.WHITE} {sender_name} (ID: {sender.get('user_id')})")
            print(f"  {Fore.YELLOW}Текст:{Fore.WHITE} {text}")
            
            # Вложения
            attachments = message.get('attachments', [])
            if attachments:
                print(f"  {Fore.YELLOW}Вложения:{Fore.WHITE} {len(attachments)}")
        
        elif update_type == 'message_callback':
            callback = update.get('callback', {})
            user = callback.get('user', {})
            user_name = user.get('name', 'Unknown')
            payload = callback.get('payload', '')
            
            print(f"\n{Fore.BLUE}[{time_str}] 🔘 Нажатие на кнопку{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}От:{Fore.WHITE} {user_name} (ID: {user.get('user_id')})")
            print(f"  {Fore.YELLOW}Payload:{Fore.WHITE} {payload}")
        
        elif update_type == 'bot_started':
            user = update.get('user', {})
            user_name = user.get('name', 'Unknown')
            payload = update.get('payload', '')
            
            print(f"\n{Fore.MAGENTA}[{time_str}] 🚀 Бот запущен пользователем{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Пользователь:{Fore.WHITE} {user_name} (ID: {user.get('user_id')})")
            if payload:
                print(f"  {Fore.YELLOW}Payload:{Fore.WHITE} {payload}")
        
        else:
            print(f"\n{Fore.CYAN}[{time_str}] 📬 Обновление: {update_type}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Данные:{Fore.WHITE} {update}")
    
    def initialize(self) -> bool:
        """Инициализация приложения"""
        try:
            # Валидация конфигурации
            config.validate()
            
            # Создание клиента
            self.client = MAXClient(
                token=config.BOT_TOKEN,
                base_url=config.API_URL,
                timeout=config.API_TIMEOUT
            )
            
            # Получение информации о боте
            print(f"{Fore.YELLOW}Подключение к MAX API...{Style.RESET_ALL}")
            self.bot_info = self.client.get_me()
            
            print(f"{Fore.GREEN}✓ Успешно подключено!{Style.RESET_ALL}")
            print(f"  Бот: {Style.BRIGHT}{self.bot_info.get('name')}{Style.RESET_ALL} (@{self.bot_info.get('username')})")
            
            return True
            
        except ValueError as e:
            print(f"{Fore.RED}Ошибка конфигурации: {e}{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Создайте файл .env со следующим содержимым:{Style.RESET_ALL}")
            print(f"  MAX_BOT_TOKEN=ваш_токен_здесь")
            return False
        
        except MAXAPIException as e:
            print(f"{Fore.RED}Ошибка API: {e}{Style.RESET_ALL}")
            return False
        
        except Exception as e:
            print(f"{Fore.RED}Неожиданная ошибка: {e}{Style.RESET_ALL}")
            return False
    
    def send_message_interactive(self):
        """Интерактивная отправка сообщения"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}Отправка сообщения{Style.RESET_ALL}")
        
        try:
            # Ввод chat_id
            chat_id_str = input(f"{Fore.YELLOW}Введите ID чата: {Fore.WHITE}").strip()
            if not chat_id_str:
                print(f"{Fore.RED}ID чата не может быть пустым{Style.RESET_ALL}")
                return
            
            try:
                chat_id = int(chat_id_str)
            except ValueError:
                print(f"{Fore.RED}ID чата должен быть числом{Style.RESET_ALL}")
                return
            
            # Ввод текста
            text = input(f"{Fore.YELLOW}Введите текст сообщения: {Fore.WHITE}").strip()
            if not text:
                print(f"{Fore.RED}Текст сообщения не может быть пустым{Style.RESET_ALL}")
                return
            
            # Отправка
            print(f"{Fore.YELLOW}Отправка...{Style.RESET_ALL}")
            result = self.client.send_message(chat_id=chat_id, text=text)
            
            print(f"{Fore.GREEN}✓ Сообщение отправлено!{Style.RESET_ALL}")
            print(f"  Message ID: {result.get('message_id', 'N/A')}")
            
        except MAXAPIException as e:
            print(f"{Fore.RED}Ошибка при отправке: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Неожиданная ошибка: {e}{Style.RESET_ALL}")
    
    def listen_messages(self):
        """Прослушивание входящих сообщений"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}Прослушивание сообщений{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Нажмите Ctrl+C для остановки{Style.RESET_ALL}\n")
        
        try:
            while True:
                try:
                    # Получение обновлений
                    updates = self.client.get_updates(
                        timeout=config.POLLING_TIMEOUT,
                        limit=config.POLLING_LIMIT,
                        marker=self.last_marker
                    )
                    
                    # Обработка обновлений
                    for update in updates:
                        self.print_message(update)
                        
                        # Обновляем маркер
                        if 'marker' in update:
                            self.last_marker = update['marker']
                    
                    # Если есть обновления, показываем разделитель
                    if updates:
                        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
                
                except MAXAPIException as e:
                    print(f"{Fore.RED}Ошибка API: {e}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Повторная попытка через 5 секунд...{Style.RESET_ALL}")
                    import time
                    time.sleep(5)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Прослушивание остановлено{Style.RESET_ALL}")
    
    def get_last_updates(self):
        """Получить последние обновления без ожидания"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}Получение последних обновлений{Style.RESET_ALL}\n")
        
        try:
            updates = self.client.get_updates(timeout=1, limit=10, marker=self.last_marker)
            
            if not updates:
                print(f"{Fore.YELLOW}Нет новых обновлений{Style.RESET_ALL}")
                return
            
            print(f"{Fore.GREEN}Получено обновлений: {len(updates)}{Style.RESET_ALL}")
            
            for update in updates:
                self.print_message(update)
                
                if 'marker' in update:
                    self.last_marker = update['marker']
        
        except MAXAPIException as e:
            print(f"{Fore.RED}Ошибка API: {e}{Style.RESET_ALL}")
    
    def run(self):
        """Запуск приложения"""
        self.print_header()
        
        # Инициализация
        if not self.initialize():
            return
        
        self.running = True
        
        # Главный цикл
        while self.running:
            self.print_menu()
            
            try:
                choice = input(f"{Fore.CYAN}Выберите действие: {Fore.WHITE}").strip()
                
                if choice == '1':
                    self.send_message_interactive()
                
                elif choice == '2':
                    self.listen_messages()
                
                elif choice == '3':
                    self.print_bot_info()
                
                elif choice == '4':
                    self.get_last_updates()
                
                elif choice == '0':
                    print(f"\n{Fore.YELLOW}Выход...{Style.RESET_ALL}")
                    self.running = False
                
                else:
                    print(f"{Fore.RED}Неверный выбор. Попробуйте снова.{Style.RESET_ALL}")
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Прервано пользователем{Style.RESET_ALL}")
                self.running = False
            
            except Exception as e:
                print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
        
        # Закрытие клиента
        if self.client:
            self.client.close()
        
        print(f"\n{Fore.GREEN}Спасибо за использование MAX Console App!{Style.RESET_ALL}\n")


def main():
    """Точка входа в приложение"""
    app = ConsoleApp()
    app.run()


if __name__ == '__main__':
    main()
