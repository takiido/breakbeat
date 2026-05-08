from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config import settings
from src.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_token(subject: str, token_type: str,
                  expires_delta: timedelta) -> str:
   
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "type": token_type, "exp": expire}
    
    return jwt.encode(payload, settings.JWT_SECRET,
                      algorithm = settings.JWT_ALGORITHM)


def create_access_token(user_id: int) -> str:
    return _create_token(
            str(user_id),
            ACCESS_TOKEN_TYPE,
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
            str(user_id),
            REFRESH_TOKEN_TYPE,
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    

def decode_token(token:str, expected_type: str) -> int:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET,
                             algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != expected_type:
            raise ValueError
        return int(payload("sub"))
    except (JWTError, ValueError, KeyError):
        from src.auth.exceptions import InvalidToken
        raise InvalidToken
