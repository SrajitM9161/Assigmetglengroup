from flask import request
from app.utils.response import success


class EmployeeController:
    def __init__(self, service): self.service = service
    def list(self): return success(self.service.list(), "Employees retrieved successfully.")
    def create(self):
        employee = self.service.create(request.get_json(silent=True))
        return success(employee, "Employee created successfully.", 201)
