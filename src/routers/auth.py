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
    BLACKLISTED_TOKENS.add(token)
    return {"message": "Successfully logged out"}