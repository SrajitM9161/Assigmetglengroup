from flask import Blueprint
from app.middleware.role_guard import mock_role_required


def create_schedule_blueprint(controller):
    blueprint = Blueprint("schedules", __name__)
    read_schedule = mock_role_required("admin", "scheduler", "employee")(controller.list)
    create_assignment = mock_role_required("admin", "scheduler")(controller.create)
    delete_assignment = mock_role_required("admin", "scheduler")(controller.delete)
    # PRD endpoints plus descriptive aliases for frontend readability.
    blueprint.get("/schedule")(read_schedule)
    blueprint.get("/api/schedule")(read_schedule)
    blueprint.get("/api/assignments")(read_schedule)
    blueprint.post("/assign")(create_assignment)
    blueprint.post("/api/assign")(create_assignment)
    blueprint.post("/api/assignments")(create_assignment)
    blueprint.delete("/assign/<assignment_id>")(delete_assignment)
    blueprint.delete("/api/assign/<assignment_id>")(delete_assignment)
    blueprint.delete("/api/assignments/<assignment_id>")(delete_assignment)
    return blueprint
