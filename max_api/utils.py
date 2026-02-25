"""
Утилиты для работы с MAX API
"""

import time
from typing import Optional, Dict, Any
from functools import wraps


class RateLimiter:
    """Ограничитель частоты запросов (Rate Limiter)"""
    
    def __init__(self, max_requests: int = 30, time_window: float = 1.0):
        """
        Args:
            max_requests: Максимальное количество запросов
            time_window: Временное окно в секундах
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def acquire(self):
        """Ожидает, если достигнут лимит запросов"""
        now = time.time()
        
        # Удаляем старые запросы за пределами временного окна
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        # Если достигнут лимит, ждём
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.requests.pop(0)
        
        # Записываем текущий запрос
        self.requests.append(now)


def rate_limited(max_requests: int = 30, time_window: float = 1.0):
    """
    Декоратор для ограничения частоты вызовов функции
    
    Args:
        max_requests: Максимальное количество запросов
        time_window: Временное окно в секундах
    """
    limiter = RateLimiter(max_requests, time_window)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.acquire()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_chat_id(chat_id: Any) -> int:
    """
    Валидация chat_id
    
    Args:
        chat_id: ID чата
        
    Returns:
        int: Валидный chat_id
        
    Raises:
        ValueError: Если chat_id невалиден
    """
    try:
        chat_id = int(chat_id)
        if chat_id <= 0:
            raise ValueError("chat_id должен быть положительным числом")
        return chat_id
    except (TypeError, ValueError) as e:
        raise ValueError(f"Невалидный chat_id: {e}")


def build_attachment(attachment_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Создание вложения для сообщения
    
    Args:
        attachment_type: Тип вложения ('inline_keyboard', 'file', и т.д.)
        payload: Данные вложения
        
    Returns:
        dict: Готовое вложение
    """
    return {
        "type": attachment_type,
        "payload": payload
    }


def build_inline_keyboard(buttons: list) -> Dict[str, Any]:
    """
    Создание inline-клавиатуры
    
    Args:
        buttons: Список рядов кнопок. Каждый ряд - это список кнопок.
                Кнопка - это словарь с ключами: type, text, и другими в зависимости от типа.
    
    Returns:
        dict: Готовая inline-клавиатура
        
    Example:
        >>> keyboard = build_inline_keyboard([
        ...     [
        ...         {"type": "callback", "text": "Кнопка 1", "payload": "btn1"},
        ...         {"type": "callback", "text": "Кнопка 2", "payload": "btn2"}
        ...     ],
        ...     [
        ...         {"type": "link", "text": "Сайт", "url": "https://example.com"}
        ...     ]
        ... ])
    """
    return build_attachment("inline_keyboard", {"buttons": buttons})


def format_user_mention(user_id: int, name: str, format_type: str = "markdown") -> str:
    """
    Создание упоминания пользователя
    
    Args:
        user_id: ID пользователя
        name: Имя пользователя
        format_type: Тип форматирования ('markdown' или 'html')
        
    Returns:
        str: Отформатированное упоминание
        
    Example:
        >>> mention = format_user_mention(123456, "Иван Петров", "markdown")
        >>> # [Иван Петров](max://user/123456)
    """
    if format_type == "markdown":
        return f"[{name}](max://user/{user_id})"
    elif format_type == "html":
        return f'<a href="max://user/{user_id}">{name}</a>'
    else:
        raise ValueError(f"Неподдерживаемый тип форматирования: {format_type}")


def parse_update_type(update: Dict[str, Any]) -> Optional[str]:
    """
    Извлечение типа обновления
    
    Args:
        update: Объект обновления
        
    Returns:
        str: Тип обновления или None
    """
    return update.get("update_type")


def extract_message_text(update: Dict[str, Any]) -> Optional[str]:
    """
    Извлечение текста сообщения из обновления
    
    Args:
        update: Объект обновления
        
    Returns:
        str: Текст сообщения или None
    """
    message = update.get("message", {})
    body = message.get("body", {})
    return body.get("text")


def extract_chat_id(update: Dict[str, Any]) -> Optional[int]:
    """
    Извлечение chat_id из обновления
    
    Args:
        update: Объект обновления
        
    Returns:
        int: chat_id или None
    """
    # Сначала пробуем получить из корневого уровня
    chat_id = update.get("chat_id")
    if chat_id:
        return chat_id
    
    # Затем пытаемся извлечь из message
    message = update.get("message", {})
    recipient = message.get("recipient", {})
    return recipient.get("chat_id")
