from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserIn(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class User(BaseModel):
    id: int
    username: str
    is_admin: bool

class GroupIn(BaseModel):
    name: str

class Group(BaseModel):
    id: int
    name: str
    members: List[User]

class MessageIn(BaseModel):
    content: str

class Message(BaseModel):
    id: int
    group_id: int
    content: str
    likes: int = 0

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: Optional[bool] = None