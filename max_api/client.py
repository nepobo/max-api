"""
Основной клиент для работы с MAX API
"""

import time
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin

from .exceptions import (
    MAXAPIException,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    MethodNotAllowedError,
    RateLimitError,
    ServiceUnavailableError,
)
from .utils import RateLimiter, validate_chat_id


class MAXClient:
    """Клиент для работы с MAX Messenger API"""
    
    def __init__(
        self,
        token: str,
        base_url: str = "https://platform-api.max.ru",
        timeout: int = 30,
        max_requests_per_second: int = 30
    ):
        """
        Инициализация клиента MAX API
        
        Args:
            token: Токен бота
            base_url: Базовый URL API (по умолчанию https://platform-api.max.ru)
            timeout: Таймаут запросов в секундах
            max_requests_per_second: Максимальное количество запросов в секунду
        """
        self.token = token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.rate_limiter = RateLimiter(max_requests=max_requests_per_second, time_window=1.0)
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Выполнение HTTP запроса к API
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE, PATCH)
            endpoint: Конечная точка API (например, '/me')
            params: Query параметры
            json_data: JSON данные для тела запроса
            
        Returns:
            dict: Ответ от API
            
        Raises:
            MAXAPIException: При ошибке запроса
        """
        # Применяем rate limiting
        self.rate_limiter.acquire()
        
        # Формируем полный URL
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        try:
            response = self._session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout
            )
            
            # Обработка ошибок HTTP
            self._handle_response(response)
            
            # Возвращаем JSON если есть содержимое
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.Timeout:
            raise MAXAPIException(f"Превышено время ожидания ({self.timeout}s)")
        except requests.exceptions.ConnectionError:
            raise MAXAPIException("Ошибка подключения к серверу MAX API")
        except requests.exceptions.RequestException as e:
            raise MAXAPIException(f"Ошибка запроса: {str(e)}")
    
    def _handle_response(self, response: requests.Response):
        """
        Обработка ответа от API и генерация соответствующих исключений
        
        Args:
            response: Объект ответа requests
            
        Raises:
            MAXAPIException: Соответствующее исключение в зависимости от кода ответа
        """
        if response.status_code == 200:
            return
        
        # Пытаемся извлечь детали ошибки из ответа
        try:
            error_data = response.json()
            error_message = error_data.get('message', '') or error_data.get('error', '')
        except:
            error_message = response.text or response.reason
        
        # Генерируем соответствующее исключение
        if response.status_code == 400:
            raise BadRequestError(error_message, response=error_data if 'error_data' in locals() else None)
        elif response.status_code == 401:
            raise AuthenticationError(error_message, response=error_data if 'error_data' in locals() else None)
        elif response.status_code == 404:
            raise NotFoundError(error_message, response=error_data if 'error_data' in locals() else None)
        elif response.status_code == 405:
            raise MethodNotAllowedError(error_message, response=error_data if 'error_data' in locals() else None)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response=error_data if 'error_data' in locals() else None)
        elif response.status_code == 503:
            raise ServiceUnavailableError(error_message, response=error_data if 'error_data' in locals() else None)
        else:
            raise MAXAPIException(
                f"Ошибка API (HTTP {response.status_code}): {error_message}",
                status_code=response.status_code,
                response=error_data if 'error_data' in locals() else None
            )
    
    # === Информация о боте ===
    
    def get_me(self) -> Dict[str, Any]:
        """
        Получение информации о боте
        
        Returns:
            dict: Информация о боте (user_id, name, username, is_bot, last_activity_time)
            
        Example:
            >>> bot = client.get_me()
            >>> print(bot['name'])
            'My Bot'
        """
        return self._make_request('GET', '/me')
    
    # === Работа с сообщениями ===
    
    def send_message(
        self,
        chat_id: int,
        text: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
        format: Optional[str] = None,
        link_preview: bool = True,
        notify: bool = True
    ) -> Dict[str, Any]:
        """
        Отправка сообщения в чат
        
        Args:
            chat_id: ID пользователя (user_id) или чата (chat_id)
            text: Текст сообщения
            attachments: Список вложений (inline_keyboard, файлы и т.д.)
            format: Формат текста ('markdown' или 'html')
            link_preview: Показывать ли превью ссылок
            notify: Уведомлять ли участников чата
            
        Returns:
            dict: Отправленное сообщение
            
        Example:
            >>> message = client.send_message(
            ...     chat_id=123456789,
            ...     text="**Привет!**",
            ...     format="markdown"
            ... )
        """
        chat_id = validate_chat_id(chat_id)
        
        # user_id передается как query-параметр
        params = {
            "user_id": chat_id
        }
        
        if not link_preview:
            params["disable_link_preview"] = True
        
        # Тело запроса
        message_body = {
            "text": text
        }
        
        if format:
            message_body["format"] = format
        
        if not notify:
            message_body["notify"] = False
        
        if attachments:
            message_body["attachments"] = attachments
        
        return self._make_request('POST', '/messages', params=params, json_data=message_body)
    
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        Получение сообщения по ID
        
        Args:
            message_id: ID сообщения
            
        Returns:
            dict: Информация о сообщении
        """
        return self._make_request('GET', f'/messages/{message_id}')
    
    def edit_message(
        self,
        message_id: str,
        text: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
        format: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Редактирование сообщения
        
        Args:
            message_id: ID сообщения для редактирования
            text: Новый текст сообщения
            attachments: Новые вложения
            format: Формат текста ('markdown' или 'html')
            
        Returns:
            dict: Обновленное сообщение
        """
        message_body = {"text": text}
        
        if format:
            message_body["format"] = format
        
        if attachments is not None:
            message_body["attachments"] = attachments
        
        return self._make_request('PUT', f'/messages/{message_id}', json_data=message_body)
    
    def delete_message(self, message_id: str) -> Dict[str, Any]:
        """
        Удаление сообщения
        
        Args:
            message_id: ID сообщения для удаления
            
        Returns:
            dict: Результат удаления
        """
        return self._make_request('DELETE', f'/messages/{message_id}')
    
    # === Получение обновлений (Long Polling) ===
    
    def get_updates(
        self,
        limit: Optional[int] = None,
        timeout: int = 30,
        marker: Optional[int] = None,
        update_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получение обновлений через Long Polling
        
        Args:
            limit: Максимальное количество обновлений для получения
            timeout: Таймаут ожидания в секундах (long polling)
            marker: Маркер последнего полученного обновления
            update_types: Список типов обновлений для получения
                         (message_created, message_callback, bot_started, и т.д.)
            
        Returns:
            list: Список обновлений
            
        Example:
            >>> updates = client.get_updates(timeout=30, limit=10)
            >>> for update in updates:
            ...     if update['update_type'] == 'message_created':
            ...         print(update['message']['body']['text'])
        """
        params = {}
        
        if limit is not None:
            params['limit'] = limit
        
        if timeout:
            params['timeout'] = timeout
        
        if marker is not None:
            params['marker'] = marker
        
        if update_types:
            params['types'] = ','.join(update_types)
        
        result = self._make_request('GET', '/updates', params=params)
        
        # API возвращает {'updates': [...], 'marker': ...}
        if isinstance(result, dict):
            return result.get('updates', [])
        
        return result if isinstance(result, list) else []
    
    # === Управление подписками (Webhook) ===
    
    def create_subscription(
        self,
        url: str,
        update_types: Optional[List[str]] = None,
        version: str = "1.0"
    ) -> Dict[str, Any]:
        """
        Создание подписки на обновления (Webhook)
        
        Args:
            url: URL для получения вебхуков (только HTTPS)
            update_types: Типы обновлений для получения
            version: Версия API
            
        Returns:
            dict: Информация о созданной подписке
            
        Note:
            URL должен использовать протокол HTTPS
        """
        subscription_data = {
            "url": url,
            "version": version
        }
        
        if update_types:
            subscription_data["update_types"] = update_types
        
        return self._make_request('POST', '/subscriptions', json_data=subscription_data)
    
    def get_subscriptions(self) -> List[Dict[str, Any]]:
        """
        Получение списка активных подписок
        
        Returns:
            list: Список подписок
        """
        result = self._make_request('GET', '/subscriptions')
        
        if isinstance(result, dict):
            return result.get('subscriptions', [])
        
        return result if isinstance(result, list) else []
    
    def delete_subscription(self, url: str) -> Dict[str, Any]:
        """
        Удаление подписки
        
        Args:
            url: URL подписки для удаления
            
        Returns:
            dict: Результат удаления
        """
        return self._make_request('DELETE', '/subscriptions', params={'url': url})
    
    # === Вспомогательные методы ===
    
    def close(self):
        """Закрытие сессии"""
        if self._session:
            self._session.close()
    
    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие при выходе из контекста"""
        self.close()
