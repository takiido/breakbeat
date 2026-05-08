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
    """Return the user that matches an email, if any."""

    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Return the user that matches a username, if any."""

    return db.query(User).filter(User.username == username).first()


def register_user(db: Session, data: UserRegister) -> dict:
    """Create a user and return the initial token pair."""

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
    """Validate credentials and return a fresh token pair."""

    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials

    if not user.is_active:
        raise InactiveUser

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


def refresh_tokens(db: Session, user_id: int) -> dict:
    """Issue a new token pair for an active user id."""

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise InactiveUser

    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
        "token_type": "bearer",
    }
