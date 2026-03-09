from app.core.exceptions import BaseAppException


class PasswordNotMatch(BaseAppException):
    def __init__(self, message: str = 'Invalid credentials.'):
        super().__init__(message, status_code=401)

class InvalidCurrentPassword(BaseAppException):
    def __init__(self, message: str = 'Current password is incorrect.'):
        super().__init__(message, status_code=403)

class SamePasswordError(BaseAppException):
    def __init__(self, message: str = 'New password must be different from current password.'):
        super().__init__(message, status_code=400)

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
    def __init__(self, message: str = 'Invalid email or password.'):
        super().__init__(message, status_code=401)

class UserExistsError(BaseAppException):
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message, status_code=409)



