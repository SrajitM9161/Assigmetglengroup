import time
from flask import g, request


def register_request_logger(app):
    @app.before_request
    def start_request_timer():
        g.request_started_at = time.perf_counter()

    @app.after_request
    def log_request(response):
        elapsed = (time.perf_counter() - getattr(g, "request_started_at", time.perf_counter())) * 1000
        app.logger.info("%s %s -> %s (%.1fms)", request.method, request.path, response.status_code, elapsed)
        return response
