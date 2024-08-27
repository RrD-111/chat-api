from fastapi import APIRouter, Depends
from typing import List
from src.utils.db_util import get_db_connection
from src.services.auth_service import get_current_user
from src.services.group_service import create_group, delete_group, list_groups, add_group_members
from src.models.schemas import GroupIn, Group, User

router = APIRouter()

@router.post("/groups", response_model=Group)
async def create_group_route(group_in: GroupIn, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    """
    Create a new group.

    Args:
        group_in (GroupIn): The input data to create the group, including the group name.
        current_user (User): The user creating the group, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        Group: The newly created group with its ID, name, and members.

    Raises:
        HTTPException: If an error occurs during group creation.
    """
    return await create_group(group_in, current_user, db)

@router.delete("/groups/{group_id}")
async def delete_group_route(group_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    """
    Delete a group by its ID.

    Args:
        group_id (int): The ID of the group to be deleted.
        current_user (User): The user requesting to delete the group, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        dict: A success message indicating that the group has been deleted.

    Raises:
        HTTPException: If the user is not a member of the group or if the group is not found.
    """
    return await delete_group(group_id, current_user, db)

@router.get("/groups", response_model=List[Group])
async def list_groups_route(current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    """
    List all groups.

    Args:
        current_user (User): The user requesting the list of groups, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        List[Group]: A list of groups with their IDs, names, and members.
    """
    return await list_groups(db)

@router.post("/groups/{group_id}/members")
async def add_group_members_route(group_id: int, member_ids: List[int], current_user: User = Depends(get_current_user), db=Depends(get_db_connection)):
    """
    Add members to a group.

    Args:
        group_id (int): The ID of the group to which members are being added.
        member_ids (List[int]): A list of user IDs to add as members of the group.
        current_user (User): The user requesting to add members to the group, automatically injected by dependency.
        db: The database connection, automatically injected by dependency.

    Returns:
        dict: A success message indicating that members have been added.

    Raises:
        HTTPException: If the user is not a member of the group.
    """
    return await add_group_members(group_id, member_ids, current_user, db)
