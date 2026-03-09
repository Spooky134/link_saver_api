from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from app.auth.exceptions import TokenExpired, IncorrectFormatToken

from app.core.config import settings


password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expire_min: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.auth.secret_key,
        algorithm=settings.auth.algorithm
    )
    return encoded_jwt

def validate_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=settings.auth.algorithm
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


def validate_reset_password_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=settings.auth.algorithm
        )
    except JWTError:
        raise IncorrectFormatToken()

    if payload.get("type") != "password_reset":
        raise IncorrectFormatToken()

    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpired()

    user_id = payload.get("sub")
    if not user_id:
        raise IncorrectFormatToken()

    return int(user_id)

def create_password_reset_token(user_id: int) -> str:
    return create_access_token(
        {"sub": str(user_id), "type": "password_reset"},
        expire_min=15,
    )