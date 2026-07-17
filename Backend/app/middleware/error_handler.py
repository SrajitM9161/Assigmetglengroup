import logging

from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from errors import ApiError
from app.utils.response import error

def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(exc):
        return error(exc.code, exc.message, exc.status, exc.details)

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc):
        return error("VALIDATION_ERROR", "Request payload is invalid.", 400, exc.messages)

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return error("NOT_FOUND" if exc.code == 404 else "HTTP_ERROR", exc.description, exc.code)

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc):
        app.logger.exception("Unhandled application error")
        return error("INTERNAL_ERROR", "An unexpected error occurred.", 500)
