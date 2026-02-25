"""
Тесты для утилит
"""

import pytest
from max_api.utils import (
    build_inline_keyboard,
    build_attachment,
    format_user_mention,
    parse_update_type,
    extract_message_text,
    extract_chat_id,
    validate_chat_id,
)


class TestUtils:
    """Тесты для вспомогательных функций"""
    
    def test_validate_chat_id_valid(self):
        """Тест валидации корректного chat_id"""
        # Положительные (личные чаты)
        assert validate_chat_id(123456) == 123456
        assert validate_chat_id("789012") == 789012
        
        # Отрицательные (групповые чаты)
        assert validate_chat_id(-123456) == -123456
        assert validate_chat_id("-789012") == -789012
    
    def test_validate_chat_id_invalid(self):
        """Тест валидации некорректного chat_id"""
        # Ноль недопустим
        with pytest.raises(ValueError, match="не может быть равен 0"):
            validate_chat_id(0)
        
        # Нечисловые значения
        with pytest.raises(ValueError):
            validate_chat_id("not_a_number")
    
    def test_build_attachment(self):
        """Тест создания вложения"""
        attachment = build_attachment("inline_keyboard", {"buttons": []})
        assert attachment["type"] == "inline_keyboard"
        assert "payload" in attachment
        assert attachment["payload"]["buttons"] == []
    
    def test_build_inline_keyboard(self):
        """Тест создания inline-клавиатуры"""
        buttons = [
            [
                {"type": "callback", "text": "Button 1", "payload": "btn1"},
                {"type": "callback", "text": "Button 2", "payload": "btn2"}
            ]
        ]
        
        keyboard = build_inline_keyboard(buttons)
        assert keyboard["type"] == "inline_keyboard"
        assert keyboard["payload"]["buttons"] == buttons
    
    def test_format_user_mention_markdown(self):
        """Тест форматирования упоминания пользователя (Markdown)"""
        mention = format_user_mention(123456, "John Doe", "markdown")
        assert mention == "[John Doe](max://user/123456)"
    
    def test_format_user_mention_html(self):
        """Тест форматирования упоминания пользователя (HTML)"""
        mention = format_user_mention(123456, "John Doe", "html")
        assert mention == '<a href="max://user/123456">John Doe</a>'
    
    def test_format_user_mention_invalid(self):
        """Тест форматирования с неверным типом"""
        with pytest.raises(ValueError):
            format_user_mention(123456, "John Doe", "invalid")
    
    def test_parse_update_type(self):
        """Тест извлечения типа обновления"""
        update = {"update_type": "message_created", "timestamp": 123456}
        assert parse_update_type(update) == "message_created"
        
        empty_update = {}
        assert parse_update_type(empty_update) is None
    
    def test_extract_message_text(self):
        """Тест извлечения текста сообщения"""
        update = {
            "message": {
                "body": {
                    "text": "Hello, World!"
                }
            }
        }
        assert extract_message_text(update) == "Hello, World!"
        
        empty_update = {}
        assert extract_message_text(empty_update) is None
    
    def test_extract_chat_id(self):
        """Тест извлечения chat_id"""
        # Из корневого уровня
        update1 = {"chat_id": 123456}
        assert extract_chat_id(update1) == 123456
        
        # Из сообщения
        update2 = {
            "message": {
                "recipient": {
                    "chat_id": 789012
                }
            }
        }
        assert extract_chat_id(update2) == 789012
        
        # Пустое обновление
        empty_update = {}
        assert extract_chat_id(empty_update) is None
