"""
Тесты для UpdateManager
"""

import pytest
from max_api import MAXClient, UpdateManager, UpdateMode
from max_api.exceptions import MAXAPIException


class TestUpdateManager:
    """Тесты для UpdateManager"""
    
    def test_init_default_mode(self):
        """Тест инициализации с режимом по умолчанию"""
        client = MAXClient(token="test_token")
        manager = UpdateManager(client)
        
        assert manager.mode == UpdateMode.LONG_POLLING
        assert manager.is_long_polling is True
        assert manager.is_webhook is False
        assert manager.webhook_url is None
    
    def test_init_with_mode(self):
        """Тест инициализации с явным указанием режима"""
        client = MAXClient(token="test_token")
        manager = UpdateManager(client, mode=UpdateMode.WEBHOOK)
        
        assert manager.mode == UpdateMode.WEBHOOK
        assert manager.is_long_polling is False
        assert manager.is_webhook is True
    
    def test_switch_to_webhook_invalid_url(self):
        """Тест переключения на webhook с HTTP URL"""
        client = MAXClient(token="test_token")
        manager = UpdateManager(client)
        
        with pytest.raises(ValueError, match="HTTPS"):
            manager.switch_to_webhook("http://example.com/webhook")
    
    def test_get_updates_in_webhook_mode(self):
        """Тест вызова get_updates в режиме webhook"""
        client = MAXClient(token="test_token")
        manager = UpdateManager(client, mode=UpdateMode.WEBHOOK)
        
        with pytest.raises(RuntimeError, match="Long Polling"):
            manager.get_updates()
    
    def test_get_status_long_polling(self):
        """Тест получения статуса в режиме Long Polling"""
        client = MAXClient(token="test_token")
        manager = UpdateManager(client)
        
        status = manager.get_status()
        
        assert status['mode'] == 'long_polling'
        assert status['is_long_polling'] is True
        assert status['is_webhook'] is False
        assert 'last_marker' in status
    
    def test_repr(self):
        """Тест строкового представления"""
        client = MAXClient(token="test_token")
        manager = UpdateManager(client)
        
        assert "LongPolling" in repr(manager)
