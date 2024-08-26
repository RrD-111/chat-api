from fastapi import APIRouter, Depends
from src.utils.db_util import get_db_connection
from src.services.auth_service import get_current_admin_user
from src.services.user_service import create_user, update_user
from src.models.schemas import UserIn, User

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user_route(user_in: UserIn, current_user: User = Depends(get_current_admin_user), db=Depends(get_db_connection)):
    return await create_user(user_in, db)

@router.put("/users/{user_id}", response_model=User)
async def update_user_route(user_id: int, user_data: UserIn, current_user: User = Depends(get_current_admin_user), db=Depends(get_db_connection)):
    return await update_user(user_id, user_data, db)