from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from app.auth.exceptions import TokenExpired, IncorrectFormatToken

from app.config.project_config import settings


password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expire_sec: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_sec)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.SERVICE_ALGORITHM
    )
    return encoded_jwt

def validate_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.SERVICE_ALGORITHM
        )
    except JWTError:
        raise IncorrectFormatToken()

    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpired()

    user_id = payload.get("sub")
    if not user_id:
        raise IncorrectFormatToken()

    return int(user_id)