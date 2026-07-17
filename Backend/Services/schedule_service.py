import threading

from app.constants import ASSIGNMENT_STATUS_ASSIGNED, ASSIGNMENT_STATUS_PENDING
from app.models.schedule import Schedule
from app.utils.datetime_utils import parse_iso_datetime
from app.utils.helpers import new_id
from app.validators.assignment_validator import ensure_employee_can_be_assigned, validate_assignment_payload
from app.validators.schedule_validator import ensure_no_overlap


class ScheduleService:
    _schedule_lock = threading.RLock()
    def __init__(self, schedule_repository, employee_service, job_service, audit_service, approval_mode="auto"):
        self.repository = schedule_repository
        self.employee_service = employee_service
        self.job_service = job_service
        self.audit_service = audit_service
        self.approval_mode = approval_mode

    def list(self, employee_id=None):
        assignments = self.repository.for_employee(employee_id) if employee_id else self.repository.list()
        return [self._with_display_values(assignment) for assignment in assignments]

    def assign(self, payload):
        # The lock makes read-check-write and its audit event one in-process operation.
        with self._schedule_lock:
            employee_id, job_id = validate_assignment_payload(payload)
            employee = self.employee_service.get(employee_id)
            job = self.job_service.get(job_id)
            if not all(isinstance(job.get(field), str) for field in ("startTime", "endTime")):
                from errors import ApiError
                raise ApiError("DATA_INTEGRITY_ERROR", "Job time data is invalid.", 500)
            existing = self.repository.for_employee(employee["id"])
            ensure_employee_can_be_assigned(employee, job, existing)
            job_start = parse_iso_datetime(job["startTime"], "job.startTime")
            job_end = parse_iso_datetime(job["endTime"], "job.endTime")
            existing_times = [{**item, "startTime": parse_iso_datetime(item.get("startTime"), "schedule.startTime"), "endTime": parse_iso_datetime(item.get("endTime"), "schedule.endTime")} for item in existing]
            ensure_no_overlap(job_start, job_end, existing_times)
            status = ASSIGNMENT_STATUS_PENDING if self.approval_mode.lower() == "manual" else ASSIGNMENT_STATUS_ASSIGNED
            assignment = Schedule(id=new_id(), employeeId=employee["id"], jobId=job["id"], startTime=job["startTime"], endTime=job["endTime"], status=status).to_dict()
            self.repository.create(assignment)
            self.audit_service.record("ASSIGNMENT_CREATED", assignment["id"], {"employeeId": employee["id"], "jobId": job["id"], "status": status})
            return self._with_display_values(assignment)

    def _with_display_values(self, assignment):
        employee = self.employee_service.get(assignment["employeeId"])
        job = self.job_service.get(assignment["jobId"])
        return {**assignment, "employeeName": employee["name"], "role": employee["role"], "jobName": job["name"]}

    def delete(self, assignment_id):
        from errors import ApiError
        with self._schedule_lock:
            if not self.repository.delete(assignment_id): raise ApiError("ASSIGNMENT_NOT_FOUND", "Assignment was not found.", 404)
            self.audit_service.record("ASSIGNMENT_DELETED", assignment_id)
