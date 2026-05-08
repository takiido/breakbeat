from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.models import User
from src.auth.schemas import (
        UserRegister, UserLogin, TokenPair,
        RefreshRequest, UserOut
)
from src.auth.service import register_user, login_user, refresh_tokens
from src.auth.utils import decode_token
from src.auth.constants import REFRESH_TOKEN_TYPE
from src.auth.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data)


@router.post("/login", response_model=TokenPair)
def login(data: UserLogin, db:Session = Depends(get_db)):
    return login_user(db, data.email, data.password)


@router.post("/refresh", response_model=TokenPair)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    user_id = decode_token(data.refresh_token, REFRESH_TOKEN_TYPE)
    return refresh_tokens(db, user_id)


@router.post("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
