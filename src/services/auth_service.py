import os
from dotenv import load_dotenv
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.utils.db_util import get_db_connection
from src.models.schemas import TokenData, User

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

BLACKLISTED_TOKENS = set()

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a new access token.

    Args:
        data (dict): The payload to encode in the token.
        expires_delta (timedelta, optional): The expiration time of the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db_connection)):
    """
    Get the current authenticated user.

    Args:
        token (str): The JWT token.
        db: The database connection.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token in BLACKLISTED_TOKENS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, is_admin=is_admin)
    except jwt.PyJWTError:
        raise credentials_exception
    
    with db.cursor() as cur:
        cur.execute("SELECT id, username, is_admin FROM users WHERE username = %s", (token_data.username,))
        user = cur.fetchone()
    
    if user is None:
        raise credentials_exception
    return User(id=user[0], username=user[1], is_admin=user[2])

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated admin user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The authenticated admin user.

    Raises:
        HTTPException: If the user is not an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
