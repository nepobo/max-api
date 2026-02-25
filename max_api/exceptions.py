"""
Пользовательские исключения для MAX API
"""


class MAXAPIException(Exception):
    """Базовое исключение для всех ошибок MAX API"""
    
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(MAXAPIException):
    """Ошибка аутентификации (401)"""
    
    def __init__(self, message: str = "Ошибка аутентификации. Проверьте токен.", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class BadRequestError(MAXAPIException):
    """Недействительный запрос (400)"""
    
    def __init__(self, message: str = "Недействительный запрос.", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class NotFoundError(MAXAPIException):
    """Ресурс не найден (404)"""
    
    def __init__(self, message: str = "Ресурс не найден.", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class MethodNotAllowedError(MAXAPIException):
    """Метод не допускается (405)"""
    
    def __init__(self, message: str = "Метод не допускается.", **kwargs):
        super().__init__(message, status_code=405, **kwargs)


class RateLimitError(MAXAPIException):
    """Превышено количество запросов (429)"""
    
    def __init__(self, message: str = "Превышено количество запросов. Попробуйте позже.", **kwargs):
        super().__init__(message, status_code=429, **kwargs)


class ServiceUnavailableError(MAXAPIException):
    """Сервис недоступен (503)"""
    
    def __init__(self, message: str = "Сервис временно недоступен.", **kwargs):
        super().__init__(message, status_code=503, **kwargs)
