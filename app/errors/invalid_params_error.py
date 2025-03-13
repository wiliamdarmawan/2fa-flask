from .base_error import BaseError

class InvalidParamsError(BaseError):
    status_code = 400
    error_code = "TFAE1"
    error_handling = "Please provide a valid parameter."

    def __init__(self, message="Invalid parameters provided"):
        super().__init__(message)
