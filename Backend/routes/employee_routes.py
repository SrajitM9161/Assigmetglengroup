from flask import Blueprint
from app.middleware.role_guard import mock_role_required


def create_employee_blueprint(controller):
    blueprint = Blueprint("employees", __name__)
    list_employees = mock_role_required("admin", "scheduler", "employee")(controller.list)
    create_employee = mock_role_required("admin", "scheduler")(controller.create)
    blueprint.get("/employees")(list_employees)
    blueprint.get("/api/employees")(list_employees)
    blueprint.post("/employees")(create_employee)
    blueprint.post("/api/employees")(create_employee)
    return blueprint
