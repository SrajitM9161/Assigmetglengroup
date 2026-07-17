from app.models.job import Job
from app.utils.datetime_utils import parse_iso_datetime
from app.utils.helpers import new_id
from errors import ApiError


class JobService:
    def __init__(self, repository): self.repository = repository
    def list(self): return self.repository.list()
    def get(self, job_id):
        job = self.repository.get(job_id)
        if not job: raise ApiError("JOB_NOT_FOUND", "Job was not found.", 404)
        return job
    def create(self, payload):
        if not isinstance(payload, dict) or not all(payload.get(key) for key in ("name", "startTime", "endTime")):
            raise ApiError("VALIDATION_ERROR", "name, startTime, and endTime are required.", 400)
        start_time = parse_iso_datetime(payload["startTime"], "startTime")
        end_time = parse_iso_datetime(payload["endTime"], "endTime")
        if end_time <= start_time:
            raise ApiError("VALIDATION_ERROR", "endTime must be later than startTime.", 400)
        required_role = payload.get("requiredRole")
        if required_role is not None and (not isinstance(required_role, str) or not required_role.strip()):
            raise ApiError("VALIDATION_ERROR", "requiredRole must be a non-empty string when supplied.", 400)
        return self.repository.create(Job(id=new_id(), name=payload["name"], startTime=payload["startTime"], endTime=payload["endTime"], requiredRole=required_role.strip() if required_role else None).to_dict())
