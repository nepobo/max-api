"""
Тесты для MAXClient
"""

import pytest
import responses
from max_api import MAXClient
from max_api.exceptions import (
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента"""
    return MAXClient(token="test_token_12345")


@pytest.fixture
def mock_bot_info():
    """Мок-данные о боте"""
    return {
        "user_id": 123456,
        "name": "Test Bot",
        "username": "test_bot",
        "is_bot": True,
        "last_activity_time": 1737500130100
    }


class TestMAXClient:
    """Тесты для класса MAXClient"""
    
    def test_client_initialization(self):
        """Тест инициализации клиента"""
        client = MAXClient(token="test_token")
        assert client.token == "test_token"
        assert client.base_url == "https://platform-api.max.ru"
        assert client.timeout == 30
    
    def test_client_custom_base_url(self):
        """Тест с пользовательским base_url"""
        client = MAXClient(token="test_token", base_url="https://custom-api.max.ru")
        assert client.base_url == "https://custom-api.max.ru"
    
    @responses.activate
    def test_get_me_success(self, client, mock_bot_info):
        """Тест успешного получения информации о боте"""
        responses.add(
            responses.GET,
            "https://platform-api.max.ru/me",
            json=mock_bot_info,
            status=200
        )
        
        result = client.get_me()
        assert result == mock_bot_info
        assert result['name'] == "Test Bot"
        assert result['is_bot'] is True
    
    @responses.activate
    def test_get_me_authentication_error(self, client):
        """Тест ошибки аутентификации"""
        responses.add(
            responses.GET,
            "https://platform-api.max.ru/me",
            json={"error": "Invalid token"},
            status=401
        )
        
        with pytest.raises(AuthenticationError):
            client.get_me()
    
    @responses.activate
    def test_send_message_success(self, client):
        """Тест успешной отправки сообщения"""
        mock_response = {
            "message_id": "msg_12345",
            "timestamp": 1737500130100
        }
        
        responses.add(
            responses.POST,
            "https://platform-api.max.ru/messages",
            json=mock_response,
            status=200
        )
        
        result = client.send_message(chat_id=123456789, text="Test message")
        assert result['message_id'] == "msg_12345"
    
    @responses.activate
    def test_send_message_bad_request(self, client):
        """Тест отправки сообщения с неверными данными"""
        responses.add(
            responses.POST,
            "https://platform-api.max.ru/messages",
            json={"error": "Invalid chat_id"},
            status=400
        )
        
        with pytest.raises(BadRequestError):
            client.send_message(chat_id=123, text="Test")
    
    @responses.activate
    def test_get_updates_success(self, client):
        """Тест получения обновлений"""
        mock_updates = {
            "updates": [
                {
                    "update_type": "message_created",
                    "timestamp": 1737500130100,
                    "message": {
                        "body": {"text": "Hello"}
                    }
                }
            ],
            "marker": 100
        }
        
        responses.add(
            responses.GET,
            "https://platform-api.max.ru/updates",
            json=mock_updates,
            status=200
        )
        
        result = client.get_updates()
        assert len(result) == 1
        assert result[0]['update_type'] == "message_created"
    
    @responses.activate
    def test_rate_limit_error(self, client):
        """Тест обработки ошибки превышения лимита запросов"""
        responses.add(
            responses.GET,
            "https://platform-api.max.ru/me",
            json={"error": "Rate limit exceeded"},
            status=429
        )
        
        with pytest.raises(RateLimitError):
            client.get_me()
    
    def test_context_manager(self):
        """Тест использования клиента как контекстного менеджера"""
        with MAXClient(token="test_token") as client:
            assert client is not None
            assert client.token == "test_token"
    
    def test_validate_chat_id(self):
        """Тест валидации chat_id"""
        from max_api.utils import validate_chat_id
        
        assert validate_chat_id(123456) == 123456
        assert validate_chat_id("123456") == 123456
        
        with pytest.raises(ValueError):
            validate_chat_id(-1)
        
        with pytest.raises(ValueError):
            validate_chat_id("invalid")
