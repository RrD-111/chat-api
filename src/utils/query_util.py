
"""
SQL query utility module.

This module contains SQL queries used throughout the application.
"""

SELECT_USER_BY_USERNAME = "SELECT id, username, password, is_admin FROM users WHERE username = %s"
INSERT_USER = "INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s) RETURNING id, username, is_admin"
UPDATE_USER = "UPDATE users SET username = %s, password = %s, is_admin = %s WHERE id = %s RETURNING id, username, is_admin"
INSERT_GROUP = "INSERT INTO groups (name) VALUES (%s) RETURNING id, name"
INSERT_GROUP_MEMBER = "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)"
SELECT_GROUP_MEMBER = "SELECT user_id FROM group_members WHERE group_id = %s AND user_id = %s"
DELETE_GROUP = "DELETE FROM groups WHERE id = %s"
SELECT_GROUPS = """
    SELECT g.id, g.name, array_agg(u.id), array_agg(u.username), array_agg(u.is_admin)
    FROM groups g
    JOIN group_members gm ON g.id = gm.group_id
    JOIN users u ON gm.user_id = u.id
    GROUP BY g.id, g.name
"""
INSERT_MESSAGE = "INSERT INTO messages (group_id, user_id, content) VALUES (%s, %s, %s) RETURNING id, group_id, content, likes"
SELECT_MESSAGE_GROUP = "SELECT group_id FROM messages WHERE id = %s"
UPDATE_MESSAGE_LIKES = "UPDATE messages SET likes = likes + 1 WHERE id = %s RETURNING likes"
