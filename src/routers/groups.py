from fastapi import APIRouter, Depends
from typing import List
from src.utils.db_util import get_db_connection
from src.services.auth_service import get_current_user
from src.services.group_service import create_group, delete_group, list_groups, add_group_members
from src.models.schemas import GroupIn, Group, User

router = APIRouter()

@router.post("/groups", response_model=Group)
async def create_group_route(group_in: GroupIn, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    return await create_group(group_in, current_user, db)

@router.delete("/groups/{group_id}")
async def delete_group_route(group_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    return await delete_group(group_id, current_user, db)

@router.get("/groups", response_model=List[Group])
async def list_groups_route(current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    return await list_groups(db)

@router.post("/groups/{group_id}/members")
async def add_group_members_route(group_id: int, member_ids: List[int], current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    return await add_group_members(group_id, member_ids, current_user, db)