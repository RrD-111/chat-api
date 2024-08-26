import unittest
import asyncio
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.services.group_service import create_group, delete_group, list_groups
from src.models.schemas import GroupIn, Group, User

class TestGroupService(unittest.TestCase):
    @patch('src.services.group_service.get_db_connection')
    def test_create_group_success(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, "testgroup")
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        group_in = GroupIn(name="testgroup")
        current_user = User(id=1, username="testuser", is_admin=False)
        group = asyncio.run(create_group(group_in, current_user, mock_db()))
        self.assertIsInstance(group, Group)
        self.assertEqual(group.name, "testgroup")

    @patch('src.services.group_service.get_db_connection')
    def test_delete_group_success(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)  # User is a member
        mock_cursor.rowcount = 1  # Group was deleted
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        current_user = User(id=1, username="testuser", is_admin=False)
        result = asyncio.run(delete_group(1, current_user, mock_db()))
        self.assertEqual(result, {"message": "Group deleted successfully"})

    @patch('src.services.group_service.get_db_connection')
    def test_delete_group_not_member(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None  # User is not a member
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        current_user = User(id=1, username="testuser", is_admin=False)
        with self.assertRaises(HTTPException):
            asyncio.run(delete_group(1, current_user, mock_db()))

    @patch('src.services.group_service.get_db_connection')
    def test_list_groups(self, mock_db):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, "group1", [1], ["user1"], [False]),
            (2, "group2", [1, 2], ["user1", "user2"], [False, True])
        ]
        mock_db.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        groups = asyncio.run(list_groups(mock_db()))
        self.assertIsInstance(groups, list)
        self.assertEqual(len(groups), 2)
        self.assertIsInstance(groups[0], Group)
        self.assertEqual(groups[0].name, "group1")
        self.assertEqual(len(groups[1].members), 2)

if __name__ == '__main__':
    unittest.main()