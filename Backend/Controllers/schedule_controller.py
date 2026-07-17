from flask import request
from app.middleware.role_guard import is_employee_request
from app.utils.response import success
from errors import ApiError


class ScheduleController:
    def __init__(self, service): self.service = service
    def list(self):
        employee_id = request.args.get("employeeId")
        if is_employee_request():
            employee_id = request.headers.get("X-Employee-Id")
            if not employee_id:
                raise ApiError("EMPLOYEE_ID_REQUIRED", "Employee requests must include X-Employee-Id.", 400)
        return success(self.service.list(str(employee_id) if employee_id else None), "Schedule retrieved successfully.")
    def create(self):
        assignment = self.service.assign(request.get_json(silent=True))
        return success(assignment, "Assignment created successfully.", 201)
    def delete(self, assignment_id):
        self.service.delete(assignment_id)
        return success({}, "Assignment deleted successfully.")
