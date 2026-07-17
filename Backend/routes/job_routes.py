from flask import Blueprint
from app.middleware.role_guard import mock_role_required


def create_job_blueprint(controller):
    blueprint = Blueprint("jobs", __name__)
    list_jobs = mock_role_required("admin", "scheduler", "employee")(controller.list)
    create_job = mock_role_required("admin", "scheduler")(controller.create)
    blueprint.get("/jobs")(list_jobs)
    blueprint.get("/api/jobs")(list_jobs)
    blueprint.post("/jobs")(create_job)
    blueprint.post("/api/jobs")(create_job)
    return blueprint
