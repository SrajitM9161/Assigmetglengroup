from flask import jsonify


def success(data=None, message="Request completed successfully.", status=200):
    """Return the API's consistent successful response envelope."""
    body = {"success": True, "message": message, "data": data if data is not None else {}}
    return jsonify(body), status


def error(code, message, status=400, details=None):
    """Return the API's consistent error response envelope."""
    payload = {"code": code, "message": message}
    if details:
        payload["details"] = details
    return jsonify({"success": False, "error": payload}), status
