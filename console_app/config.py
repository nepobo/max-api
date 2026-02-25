"""
Конфигурация консольного приложения
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """Конфигурация приложения"""
    
    # Токен бота
    BOT_TOKEN = os.getenv('MAX_BOT_TOKEN', '')
    
    # Настройки API
    API_URL = os.getenv('MAX_API_URL', 'https://platform-api.max.ru')
    API_TIMEOUT = int(os.getenv('MAX_API_TIMEOUT', '30'))
    
    # Настройки Long Polling
    POLLING_TIMEOUT = int(os.getenv('POLLING_TIMEOUT', '30'))
    POLLING_LIMIT = int(os.getenv('POLLING_LIMIT', '100'))
    
    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
    
    @classmethod
    def validate(cls):
        """Проверка конфигурации"""
        if not cls.BOT_TOKEN:
            raise ValueError(
                "Токен бота не найден! "
                "Установите переменную окружения MAX_BOT_TOKEN "
                "или создайте файл .env с этой переменной."
            )
        
        return True


# Создание глобального экземпляра конфигурации
config = Config()
