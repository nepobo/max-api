"""
Менеджер для управления режимами получения обновлений (Long Polling / Webhook)
"""

from enum import Enum
from typing import Optional, Callable, Dict, Any
import logging

logger = logging.getLogger(__name__)


class UpdateMode(Enum):
    """Режимы получения обновлений"""
    LONG_POLLING = "long_polling"
    WEBHOOK = "webhook"


class UpdateManager:
    """
    Менеджер для управления получением обновлений от MAX API.
    
    Поддерживает два режима:
    - Long Polling: для разработки и тестирования
    - Webhook: для production окружения
    
    Использовать одновременно Long Polling и Webhook нельзя.
    """
    
    def __init__(self, client, mode: UpdateMode = UpdateMode.LONG_POLLING):
        """
        Args:
            client: Экземпляр MAXClient
            mode: Режим получения обновлений (по умолчанию Long Polling)
        """
        self.client = client
        self._mode = mode
        self._webhook_url: Optional[str] = None
        self._webhook_subscription_id: Optional[int] = None
        self._last_marker: Optional[str] = None
    
    @property
    def mode(self) -> UpdateMode:
        """Текущий режим получения обновлений"""
        return self._mode
    
    @property
    def is_long_polling(self) -> bool:
        """Проверка, используется ли Long Polling"""
        return self._mode == UpdateMode.LONG_POLLING
    
    @property
    def is_webhook(self) -> bool:
        """Проверка, используется ли Webhook"""
        return self._mode == UpdateMode.WEBHOOK
    
    @property
    def webhook_url(self) -> Optional[str]:
        """URL webhook'а (если настроен)"""
        return self._webhook_url
    
    def switch_to_long_polling(self) -> None:
        """
        Переключиться на режим Long Polling.
        
        Если активен Webhook, он будет удалён.
        Рекомендуется для разработки и тестирования.
        """
        if self._mode == UpdateMode.WEBHOOK:
            # Удаляем webhook перед переключением
            if self._webhook_subscription_id:
                try:
                    self.client.delete_subscription(self._webhook_subscription_id)
                    logger.info(f"Webhook удалён (ID: {self._webhook_subscription_id})")
                except Exception as e:
                    logger.warning(f"Не удалось удалить webhook: {e}")
            
            self._webhook_url = None
            self._webhook_subscription_id = None
        
        self._mode = UpdateMode.LONG_POLLING
        logger.info("Переключено на режим Long Polling")
    
    def switch_to_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """
        Переключиться на режим Webhook.
        
        Args:
            webhook_url: URL для получения webhook уведомлений (только HTTPS)
        
        Returns:
            Информация о созданной подписке
        
        Raises:
            ValueError: Если URL не использует HTTPS
            MAXAPIException: При ошибке создания webhook
        
        Note:
            Webhook поддерживает только HTTPS (включая самоподписанные сертификаты).
            HTTP не поддерживается.
            Рекомендуется для production окружения.
        """
        if not webhook_url.startswith('https://'):
            raise ValueError(
                "Webhook URL должен использовать протокол HTTPS. "
                "HTTP не поддерживается MAX API."
            )
        
        # Если уже есть webhook, сначала удаляем его
        if self._webhook_subscription_id:
            try:
                self.client.delete_subscription(self._webhook_subscription_id)
                logger.info(f"Старый webhook удалён (ID: {self._webhook_subscription_id})")
            except Exception as e:
                logger.warning(f"Не удалось удалить старый webhook: {e}")
        
        # Создаём новый webhook
        subscription = self.client.create_subscription(url=webhook_url)
        
        self._mode = UpdateMode.WEBHOOK
        self._webhook_url = webhook_url
        self._webhook_subscription_id = subscription.get('id')
        
        logger.info(f"Webhook настроен: {webhook_url} (ID: {self._webhook_subscription_id})")
        
        return subscription
    
    def get_updates(
        self,
        timeout: int = 30,
        marker: Optional[str] = None
    ) -> list:
        """
        Получить обновления (только для Long Polling режима).
        
        Args:
            timeout: Таймаут ожидания новых обновлений (секунды)
            marker: Маркер последнего обработанного обновления
        
        Returns:
            Список обновлений
        
        Raises:
            RuntimeError: Если вызван в режиме Webhook
            MAXAPIException: При ошибке API
        
        Note:
            Timeout - это нормальное поведение Long Polling.
            Если нет новых сообщений, запрос завершится по таймауту.
        """
        if self._mode != UpdateMode.LONG_POLLING:
            raise RuntimeError(
                "get_updates() доступен только в режиме Long Polling. "
                "Текущий режим: Webhook. Используйте switch_to_long_polling() "
                "для переключения."
            )
        
        # Используем сохранённый маркер, если не передан явно
        if marker is None:
            marker = self._last_marker
        
        updates = self.client.get_updates(timeout=timeout, marker=marker)
        
        # Обновляем маркер
        for update in updates:
            if 'marker' in update:
                self._last_marker = update['marker']
        
        return updates
    
    def get_webhook_info(self) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о текущем webhook.
        
        Returns:
            Информация о webhook или None, если webhook не настроен
        """
        if self._webhook_subscription_id:
            subscriptions = self.client.get_subscriptions()
            for sub in subscriptions:
                if sub.get('id') == self._webhook_subscription_id:
                    return sub
        return None
    
    def delete_webhook(self) -> None:
        """
        Удалить текущий webhook и переключиться на Long Polling.
        """
        if self._webhook_subscription_id:
            self.client.delete_subscription(self._webhook_subscription_id)
            logger.info(f"Webhook удалён (ID: {self._webhook_subscription_id})")
            self._webhook_subscription_id = None
            self._webhook_url = None
        
        self._mode = UpdateMode.LONG_POLLING
        logger.info("Переключено на режим Long Polling")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Получить текущий статус менеджера обновлений.
        
        Returns:
            Словарь с информацией о текущем режиме и настройках
        """
        status = {
            'mode': self._mode.value,
            'is_long_polling': self.is_long_polling,
            'is_webhook': self.is_webhook,
        }
        
        if self.is_webhook:
            status.update({
                'webhook_url': self._webhook_url,
                'webhook_subscription_id': self._webhook_subscription_id,
            })
        else:
            status['last_marker'] = self._last_marker
        
        return status
    
    def __repr__(self) -> str:
        if self.is_webhook:
            return f"<UpdateManager mode=Webhook url={self._webhook_url}>"
        return f"<UpdateManager mode=LongPolling>"
