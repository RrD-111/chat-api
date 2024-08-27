"""
Schema definitions for the Group Chat API.

This module contains Pydantic models used for data validation and serialization.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserIn(BaseModel):
    """Schema for user input when creating or updating a user."""
    username: str
    password: str
    is_admin: bool = False

class User(BaseModel):
    """Schema for user output."""
    id: int
    username: str
    is_admin: bool

class GroupIn(BaseModel):
    """Schema for group input when creating a group."""
    name: str

class Group(BaseModel):
    """Schema for group output."""
    id: int
    name: str
    members: List[User]

class MessageIn(BaseModel):
    """Schema for message input when creating a message."""
    content: str

class Message(BaseModel):
    """Schema for message output."""
    id: int
    group_id: int
    content: str
    likes: int = 0

class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for token payload data."""
    username: Optional[str] = None
    is_admin: Optional[bool] = None
