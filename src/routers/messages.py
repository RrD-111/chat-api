from fastapi import APIRouter, Depends
from src.utils.db_util import get_db_connection
from src.services.auth_service import get_current_user
from src.services.message_service import send_group_message, like_message
from src.models.schemas import MessageIn, Message, User

router = APIRouter()

@router.post("/groups/{group_id}/messages", response_model=Message)
async def send_group_message_route(group_id: int, message_in: MessageIn, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    """
    Send a message to a specific group.

    Args:
        group_id (int): The ID of the group to which the message is being sent.
        message_in (MessageIn): The input data for the message, including its content.
        current_user (User): The user sending the message, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        Message: The newly created message with its ID, group ID, content, and like count.

    Raises:
        HTTPException: If the user is not a member of the group or if there is a database error.
    """
    return await send_group_message(group_id, message_in, current_user, db)

@router.post("/messages/{message_id}/likes")
async def like_message_route(message_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    """
    Like a specific message.

    Args:
        message_id (int): The ID of the message to be liked.
        current_user (User): The user liking the message, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        dict: A dictionary containing the updated like count of the message.

    Raises:
        HTTPException: If the message is not found or if the user is not a member of the group associated with the message.
    """
    return await like_message(message_id, current_user, db)
