from functools import wraps
from flask import g, request

from app.constants import EMPLOYEE_ROLE, SCHEDULER_ROLES
from errors import ApiError


def mock_role_required(*allowed_roles):
    allowed = {role.lower() for role in allowed_roles}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            role = request.headers.get("X-Role", "scheduler").lower()
            if role not in allowed:
                raise ApiError("FORBIDDEN", "This role cannot perform this action.", 403)
            g.mock_role = role
            return view(*args, **kwargs)
        return wrapped
    return decorator


def is_employee_request():
    return getattr(g, "mock_role", request.headers.get("X-Role", "scheduler").lower()) == EMPLOYEE_ROLE


def scheduler_roles():
    return tuple(SCHEDULER_ROLES)
