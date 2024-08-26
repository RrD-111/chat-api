import unittest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.services.auth_service import create_access_token, get_current_user
from src.models.schemas import User, TokenData
import jwt

class TestAuthService(unittest.TestCase):
    def test_create_access_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        self.assertIsInstance(token, str)

    @patch('src.services.auth_service.jwt.decode')
    @patch('src.services.auth_service.get_db_connection')
    def test_get_current_user_success(self, mock_db, mock_jwt_decode):
        mock_jwt_decode.return_value = {"sub": "testuser", "is_admin": False}
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, "testuser", False)
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        user = asyncio.run(get_current_user("fake_token", mock_db()))
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")

    @patch('src.services.auth_service.jwt.decode')
    def test_get_current_user_invalid_token(self, mock_jwt_decode):
        mock_jwt_decode.side_effect = jwt.PyJWTError("Invalid token")
        with self.assertRaises(HTTPException) as context:
            asyncio.run(get_current_user("fake_token", Mock()))
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Could not validate credentials")

if __name__ == '__main__':
    unittest.main()