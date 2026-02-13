from fastapi import status
from app.exceptions import AppException

class UserExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"

class UserNotExistsError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User doesn't exist"
