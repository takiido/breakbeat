from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database import get_db
from src.auth.models import User
from src.auth.utils import decode_token
from src.auth.constants import ACCESS_TOKEN_TYPE
from src.auth.exceptions import InvalidToken, InactiveUser


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:

    user_id = decode_token(credentials.credentials, ACCESS_TOKEN_TYPE)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise InvalidToken
    if not user.is_active:
        raise InactiveUser
    return user
