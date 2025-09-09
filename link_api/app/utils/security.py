from datetime import datetime, timedelta
from app.config.project_config import settings
from jose import jwt

SECRET_KEY = settings.SECRET_KEY  # Должен быть надежным и храниться в env переменных
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token():
    # Генерируем случайную строку для refresh token
    import secrets
    return secrets.token_urlsafe(32)