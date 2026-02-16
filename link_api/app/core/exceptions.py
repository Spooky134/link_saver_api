class BaseAppException(Exception):
    def __init__(self, detail: str = "Server error", status_code: int = 500):
        self.detail = detail
        self.status_code = status_code

class ValidationError(BaseAppException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail, status_code=400)

class NotFoundError(BaseAppException):
    def __init__(self, detail: str = "Object not found"):
        super().__init__(detail, status_code=404)

class PermissionDeniedError(BaseAppException):
    def __init__(self, detail: str = "Access denied"):
        super().__init__(detail, status_code=403)
