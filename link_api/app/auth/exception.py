from app.exceptions import AppException
from fastapi import status

class PasswordNotMatch(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid credentials.'

class MissingToken(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Missing authentication token.'

class TokenExpired(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token has expired.'

class IncorrectFormatToken(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token.'

class UserNotPresent(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED