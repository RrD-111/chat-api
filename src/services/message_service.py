from fastapi import HTTPException
from src.utils.db_util import get_db_connection
from src.utils.query_util import SELECT_GROUP_MEMBER, INSERT_MESSAGE, SELECT_MESSAGE_GROUP, UPDATE_MESSAGE_LIKES
from src.models.schemas import MessageIn, Message, User

async def send_group_message(group_id: int, message_in: MessageIn, current_user: User, db):
    """
    Send a message to a group.

    :param group_id: The ID of the group to send the message to.
    :param message_in: The input data for creating a message.
    :param current_user: The currently authenticated user.
    :param db: The database connection.
    :return: The newly created message.
    :raises HTTPException: If the user is not a member of the group or a database error occurs.
    """
    with db.cursor() as cur:
        cur.execute(SELECT_GROUP_MEMBER, (group_id, current_user.id))
        if not cur.fetchone():
            raise HTTPException(status_code=403, detail="You are not a member of this group")
        try:
            cur.execute(INSERT_MESSAGE, (group_id, current_user.id, message_in.content))
            new_message = cur.fetchone()
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    return Message(id=new_message[0], group_id=new_message[1], content=new_message[2], likes=new_message[3])

async def like_message(message_id: int, current_user: User, db):
    """
    Like a message.

    :param message_id: The ID of the message to like.
    :param current_user: The currently authenticated user.
    :param db: The database connection.
    :return: The updated like count of the message.
    :raises HTTPException: If the message is not found or the user is not a member of the group.
    """
    with db.cursor() as cur:
        cur.execute(SELECT_MESSAGE_GROUP, (message_id,))
        group = cur.fetchone()
        if not group:
            raise HTTPException(status_code=404, detail="Message not found")
        cur.execute(SELECT_GROUP_MEMBER, (group[0], current_user.id))
        if not cur.fetchone():
            raise HTTPException(status_code=403, detail="You are not a member of this group")
        cur.execute(UPDATE_MESSAGE_LIKES, (message_id,))
        new_like_count = cur.fetchone()[0]
        db.commit()
    return {"likes": new_like_count}
