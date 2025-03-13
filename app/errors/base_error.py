class BaseError(Exception):
    status_code = 500
    error_code = "TFAE0"
    error_handling = "Please contact our team for further assistance"

    def __init__(self, message="An unexpected error occurred"):
        self.message = message