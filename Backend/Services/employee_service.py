from errors import ApiError
from app.models.employee import Employee
from app.utils.helpers import new_id


class EmployeeService:
    def __init__(self, repository): self.repository = repository
    def list(self): return self.repository.list()
    def get(self, employee_id):
        employee = self.repository.get(employee_id)
        if not employee: raise ApiError("EMPLOYEE_NOT_FOUND", "Employee was not found.", 404)
        return employee
    def create(self, payload):
        if not isinstance(payload, dict) or not all(payload.get(key) for key in ("name", "role")):
            raise ApiError("VALIDATION_ERROR", "name and role are required.", 400)
        availability = payload.get("availability", True)
        if not isinstance(availability, bool):
            raise ApiError("VALIDATION_ERROR", "availability must be true or false.", 400)
        return self.repository.create(Employee(id=new_id(), name=payload["name"], role=payload["role"], availability=availability).to_dict())
