from app.core.exceptions import BaseAppException


class UserExistsError(BaseAppException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, status_code=409)

class UserNotExistsError(BaseAppException):
    def __init__(self, message: str = "User doesn't exist"):
        super().__init__(message, status_code=404)
