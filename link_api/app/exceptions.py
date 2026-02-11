from fastapi import HTTPException, status

# TODO пересмотреть ошибки
class AppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs):
        super().__init__(
            status_code=kwargs.get('status_code', self.status_code),
            detail=kwargs.get('detail', self.detail)
        )

class ValidationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Validation error"

class NotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Object not found"

class PermissionDeniedError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied"