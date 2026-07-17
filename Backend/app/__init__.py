import logging
import os
from flask import Flask

from app.config import Config
from app.extensions import cors


def create_app(test_config=None):
    # Imports live here so domain models can be used independently in tests.
    from app.middleware.error_handler import register_error_handlers
    from app.middleware.request_logger import register_request_logger
    from app.repositories.audit_repository import AuditRepository
    from app.repositories.employee_repository import EmployeeRepository
    from app.repositories.job_repository import JobRepository
    from app.repositories.schedule_repository import ScheduleRepository
    from Services.audit_service import AuditService
    from Services.employee_service import EmployeeService
    from Services.job_service import JobService
    from Services.schedule_service import ScheduleService
    from Controllers.employee_controller import EmployeeController
    from Controllers.job_controller import JobController
    from Controllers.schedule_controller import ScheduleController
    from routes.employee_routes import create_employee_blueprint
    from routes.job_routes import create_job_blueprint
    from routes.schedule_routes import create_schedule_blueprint
    app = Flask(__name__)

    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    logging.basicConfig(level=Config.LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": "*"}}
    )

    register_error_handlers(app)
    register_request_logger(app)

    data_path = app.config["JSON_DATA_PATH"]
    employee_service = EmployeeService(EmployeeRepository(os.path.join(data_path, "employees.json")))
    job_service = JobService(JobRepository(os.path.join(data_path, "jobs.json")))
    audit_service = AuditService(AuditRepository(os.path.join(data_path, "audit.json")))
    schedule_service = ScheduleService(ScheduleRepository(os.path.join(data_path, "schedule.json")), employee_service, job_service, audit_service, app.config["APPROVAL_MODE"])
    app.register_blueprint(create_employee_blueprint(EmployeeController(employee_service)))
    app.register_blueprint(create_job_blueprint(JobController(job_service)))
    app.register_blueprint(create_schedule_blueprint(ScheduleController(schedule_service)))

    @app.get("/api/health")
    def health_check():
        return {
            "success": True,
            "message": "Scheduling service is healthy.",
            "data": {"service": app.config["APP_NAME"]}
        }

    return app
