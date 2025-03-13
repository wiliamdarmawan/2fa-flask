from flask import jsonify
from .invalid_params_error import InvalidParamsError
from .missing_params_error import MissingParamsError
from .unauthorized_error import UnauthorizedError
from .base_error import BaseError
from flask_limiter.errors import RateLimitExceeded

def register_error_handlers(app):
    def format_error_response(error_message, error_code="TFAE0", status_code=500, error_handling="Please contact our team for further assistance"):
        response = jsonify(
            {
                "errors": [
                    {
                        "error": error_message,
                        "errorCode": error_code,
                        "errorHandling": error_handling
                    }
                ]
            }
        )
        response.status_code = status_code
        return response


    @app.errorhandler(BaseError)
    def handle_base_error(error):
        return format_error_response(error.message, error.error_code, error.status_code, error.error_handling)

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return format_error_response("An unexpected error occurred")
    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        return format_error_response("Rate limit exceeded", "TFAE4", 429, "Please wait before requesting another OTP")


