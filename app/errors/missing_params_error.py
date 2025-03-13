from .base_error import BaseError

class MissingParamsError(BaseError):
    status_code = 400
    error_code = "TFAE2"
    error_handling = "Please include the missing parameter."

    def __init__(self, message="Missing required parameter"):
        super().__init__(message)
