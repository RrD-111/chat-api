import unittest
import asyncio
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.services.message_service import send_group_message, like_message
from src.models.schemas import MessageIn, Message, User

class TestMessageService(unittest.TestCase):
    @patch('src.services.message_service.get_db_connection')
    def test_send_group_message_success(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(1,), (1, 1, "test message", 0)]
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        message_in = MessageIn(content="test message")
        current_user = User(id=1, username="testuser", is_admin=False)
        message = asyncio.run(send_group_message(1, message_in, current_user, mock_db()))
        self.assertIsInstance(message, Message)
        self.assertEqual(message.content, "test message")

    @patch('src.services.message_service.get_db_connection')
    def test_send_group_message_not_member(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None  # User is not a member
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        message_in = MessageIn(content="test message")
        current_user = User(id=1, username="testuser", is_admin=False)
        with self.assertRaises(HTTPException):
            asyncio.run(send_group_message(1, message_in, current_user, mock_db()))

    @patch('src.services.message_service.get_db_connection')
    def test_like_message_success(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(1,), (1,), (5,)]
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        current_user = User(id=1, username="testuser", is_admin=False)
        result = asyncio.run(like_message(1, current_user, mock_db()))
        self.assertEqual(result, {"likes": 5})

    @patch('src.services.message_service.get_db_connection')
    def test_like_message_not_found(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None  # Message not found
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        current_user = User(id=1, username="testuser", is_admin=False)
        with self.assertRaises(HTTPException):
            asyncio.run(like_message(1, current_user, mock_db()))

if __name__ == '__main__':
    unittest.main()