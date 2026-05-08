from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas import UserRegister
from src.auth.exceptions import (
        EmailTaken, UsernameTaken,
        InvalidCredentials, InactiveUser
)
from src.auth.utils import (
        hash_password, create_access_token,
        create_refresh_token, verify_password
)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def register_user(db: Session, data: UserRegister) -> dict:
    if get_user_by_email(db, data.email):
        raise EmailTaken

    if get_user_by_username(db, data.username):
        raise UsernameTaken

    user = User(
            email = data.email,
            username = data.username,
            hashed_password = hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


def login_user(db: Session, email: str, password: str) -> dict:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials

    if not user.is_active:
        raise InactiveUser

    return {
        "access_token": create_access_token(user.id)
        "refresh_token": create_refresh_token(user.id)
        "token_type": "bearer",
    }


def refresh_token(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise InactiveUser

    return {
        "access_token": create_access_token(user_id)
        "refresh_token": create_refresh_token(user_id)
        "token_type": "bearer",
    }
