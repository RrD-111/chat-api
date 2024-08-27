import bcrypt
from fastapi import HTTPException
from src.utils.db_util import get_db_connection
from src.utils.query_util import INSERT_USER, UPDATE_USER
from src.models.schemas import UserIn, User

async def create_user(user_in: UserIn, db):
    """
    Create a new user.

    :param user_in: The input data for creating a user.
    :param db: The database connection.
    :return: The newly created user.
    :raises HTTPException: If the username is already registered.
    """
    with db.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE username = %s", (user_in.username,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = bcrypt.hashpw(user_in.password.encode(), bcrypt.gensalt()).decode('utf-8')
        cur.execute(INSERT_USER, (user_in.username, hashed_password, user_in.is_admin))
        new_user = cur.fetchone()
        db.commit()
    return User(id=new_user[0], username=new_user[1], is_admin=new_user[2])

async def update_user(user_id: int, user_data: UserIn, db):
    """
    Update an existing user.

    :param user_id: The ID of the user to update.
    :param user_data: The updated user data.
    :param db: The database connection.
    :return: The updated user.
    :raises HTTPException: If the user is not found.
    """
    with db.cursor() as cur:
        hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt()).decode('utf-8')
        cur.execute(UPDATE_USER, (user_data.username, hashed_password, user_data.is_admin, user_id))
        updated_user = cur.fetchone()
        db.commit()
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(id=updated_user[0], username=updated_user[1], is_admin=updated_user[2])
