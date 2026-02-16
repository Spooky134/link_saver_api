from fastapi import status
from app.core.exceptions import BaseAppException




class PasswordNotMatch(BaseAppException):
    def __init__(self, message: str = 'Invalid credentials.'):
        super().__init__(message, status_code=401)

class MissingToken(BaseAppException):
    def __init__(self, message: str = 'Missing authentication token.'):
        super().__init__(message, status_code=401)

class TokenExpired(BaseAppException):
    def __init__(self, message: str = 'Token has expired.'):
        super().__init__(message, status_code=401)

class IncorrectFormatToken(BaseAppException):
    def __init__(self, message: str = 'Invalid token.'):
        super().__init__(message, status_code=401)

class UserNotPresent(BaseAppException):
    def __init__(self, message: str = 'Error'):
        super().__init__(message, status_code=401)
