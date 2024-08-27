from fastapi import APIRouter, Depends
from src.utils.db_util import get_db_connection
from src.services.auth_service import get_current_admin_user
from src.services.user_service import create_user, update_user
from src.models.schemas import UserIn, User

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user_route(user_in: UserIn, current_user: User = Depends(get_current_admin_user), db=Depends(get_db_connection)):
     """
    Create a new user.

    Args:
        user_in (UserIn): The input data for the new user, including username, password, and admin status.
        current_user (User): The admin user creating the new user, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        User: The newly created user with its ID, username, and admin status.

    Raises:
        HTTPException: If the username is already registered or if there is a database error.
    """
    return await create_user(user_in, db)

@router.put("/users/{user_id}", response_model=User)
async def update_user_route(user_id: int, user_data: UserIn, current_user: User = Depends(get_current_admin_user), db=Depends(get_db_connection)):
    """
    Update an existing user's information.

    Args:
        user_id (int): The ID of the user to be updated.
        user_data (UserIn): The new data for the user, including username, password, and admin status.
        current_user (User): The admin user updating the user, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        User: The updated user with its ID, username, and admin status.

    Raises:
        HTTPException: If the user ID does not exist in the database or if there is a database error.
    """
    return await update_user(user_id, user_data, db)
