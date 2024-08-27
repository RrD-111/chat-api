from fastapi import HTTPException
from src.utils.db_util import get_db_connection
from src.utils.query_util import INSERT_GROUP, INSERT_GROUP_MEMBER, SELECT_GROUP_MEMBER, DELETE_GROUP, SELECT_GROUPS
from src.models.schemas import GroupIn, Group, User

async def create_group(group_in: GroupIn, current_user: User, db):
    """
    Create a new group.

    :param group_in: The input data for creating a group.
    :param current_user: The currently authenticated user.
    :param db: The database connection.
    :return: The newly created group.
    """
    with db.cursor() as cur:
        cur.execute(INSERT_GROUP, (group_in.name,))
        new_group = cur.fetchone()
        cur.execute(INSERT_GROUP_MEMBER, (new_group[0], current_user.id))
        db.commit()
    return Group(id=new_group[0], name=new_group[1], members=[current_user])

async def delete_group(group_id: int, current_user: User, db):
    """
    Delete a group.

    :param group_id: The ID of the group to delete.
    :param current_user: The currently authenticated user.
    :param db: The database connection.
    :return: A message indicating the successful deletion of the group.
    :raises HTTPException: If the user is not a member of the group or the group is not found.
    """
    with db.cursor() as cur:
        cur.execute(SELECT_GROUP_MEMBER, (group_id, current_user.id))
        if not cur.fetchone():
            raise HTTPException(status_code=403, detail="You are not a member of this group")
        cur.execute(DELETE_GROUP, (group_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Group not found")
        db.commit()
    return {"message": "Group deleted successfully"}

async def list_groups(db):
    """
    List all groups.

    :param db: The database connection.
    :return: A list of all groups.
    """
    with db.cursor() as cur:
        cur.execute(SELECT_GROUPS)
        groups = []
        for row in cur.fetchall():
            members = [User(id=id, username=username, is_admin=is_admin) for id, username, is_admin in zip(row[2], row[3], row[4]) if id is not None]
            groups.append(Group(id=row[0], name=row[1], members=members))
    return groups

async def add_group_members(group_id: int, member_ids: list[int], current_user: User, db):
    """
    Add members to a group.

    :param group_id: The ID of the group to add members to.
    :param member_ids: The list of user IDs to add as members.
    :param current_user: The currently authenticated user.
    :param db: The database connection.
    :return: A message indicating the successful addition of members.
    :raises HTTPException: If the user is not a member of the group.
    """
    with db.cursor() as cur:
        cur.execute(SELECT_GROUP_MEMBER, (group_id, current_user.id))
        if not cur.fetchone():
            raise HTTPException(status_code=403, detail="You are not a member of this group")
        for member_id in member_ids:
            cur.execute(INSERT_GROUP_MEMBER, (group_id, member_id))
        db.commit()
    return {"message": "Members added successfully"}
