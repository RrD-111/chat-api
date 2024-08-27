from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from src.utils.db_util import get_db_connection
from src.services.auth_service import create_access_token, get_current_user, BLACKLISTED_TOKENS
from src.models.schemas import Token, User
import bcrypt

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_connection)):
    """
    Authenticate a user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials.

    Returns:
        Token: An access token for the authenticated user.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    with db.cursor() as cur:
        cur.execute("SELECT id, username, password, is_admin FROM users WHERE username = %s", (form_data.username,))
        user = cur.fetchone()
        if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user[2].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user[1], "is_admin": user[3]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user), token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    """
    Log out the current user by invalidating their token.

    Args:
        current_user (User): The current authenticated user.
        token (str): The current access token.

    Returns:
        dict: A message confirming successful logout.
    """
    BLACKLISTED_TOKENS.add(token)
    return {"message": "Successfully logged out"}
