from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config import settings
from src.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password for storage."""

    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Check a plaintext password against a stored hash."""

    return pwd_context.verify(plain, hashed)


def _create_token(subject: str, token_type: str,
                  expires_delta: timedelta) -> str:
    """Build a signed JWT with a subject, token type, and expiry."""

    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "type": token_type, "exp": expire}

    return jwt.encode(payload, settings.JWT_SECRET,
                      algorithm = settings.JWT_ALGORITHM)


def create_access_token(user_id: int) -> str:
    """Create an access token for a user id."""

    return _create_token(
            str(user_id),
            ACCESS_TOKEN_TYPE,
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: int) -> str:
    """Create a refresh token for a user id."""

    return _create_token(
            str(user_id),
            REFRESH_TOKEN_TYPE,
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token:str, expected_type: str) -> int:
    """Decode a JWT and return its user id if the type matches."""

    try:
        payload = jwt.decode(token, settings.JWT_SECRET,
                             algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != expected_type:
            raise ValueError
        return int(payload["sub"])
    except (JWTError, ValueError, KeyError):
        from src.auth.exceptions import InvalidToken
        raise InvalidToken
