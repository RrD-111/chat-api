import unittest
import asyncio
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.services.user_service import create_user, update_user
from src.models.schemas import UserIn, User

class TestUserService(unittest.TestCase):
    @patch('src.services.user_service.get_db_connection')
    def test_create_user_success(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [None, (1, "testuser", False)]  # First None for username check, then return new user
        mock_cursor.execute.return_value = None
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        user_in = UserIn(username="testuser", password="testpass")
        user = asyncio.run(create_user(user_in, mock_db()))
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")

    @patch('src.services.user_service.get_db_connection')
    def test_create_user_username_exists(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)  # Username exists
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        user_in = UserIn(username="testuser", password="testpass")
        with self.assertRaises(HTTPException):
            asyncio.run(create_user(user_in, mock_db()))

    @patch('src.services.user_service.get_db_connection')
    def test_update_user_success(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, "updateduser", False)
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        user_data = UserIn(username="updateduser", password="newpass")
        user = asyncio.run(update_user(1, user_data, mock_db()))
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "updateduser")

    @patch('src.services.user_service.get_db_connection')
    def test_update_user_not_found(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        user_data = UserIn(username="updateduser", password="newpass")
        with self.assertRaises(HTTPException):
            asyncio.run(update_user(1, user_data, mock_db()))

if __name__ == '__main__':
    unittest.main()