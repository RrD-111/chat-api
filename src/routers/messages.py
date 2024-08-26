from fastapi import APIRouter, Depends
from src.utils.db_util import get_db_connection
from src.services.auth_service import get_current_user
from src.services.message_service import send_group_message, like_message
from src.models.schemas import MessageIn, Message, User

router = APIRouter()

@router.post("/groups/{group_id}/messages", response_model=Message)
async def send_group_message_route(group_id: int, message_in: MessageIn, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    return await send_group_message(group_id, message_in, current_user, db)

@router.post("/messages/{message_id}/likes")
async def like_message_route(message_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    return await like_message(message_id, current_user, db)