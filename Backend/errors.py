class ApiError(Exception):
    """Expected business or request error, rendered by Flask's error handler."""

    def __init__(self, code, message, status=400, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details


class DataStoreError(ApiError):
    def __init__(self, message="Local JSON data could not be read safely."):
        super().__init__("DATA_STORE_ERROR", message, 500)
