from .base_error import BaseError

class UnauthorizedError(BaseError):
    status_code = 401
    error_code = "TFAE3"
    error_handling = "Please provide correct credentials"

    def __init__(self, message="Unauthorized"):
        super().__init__(message)
