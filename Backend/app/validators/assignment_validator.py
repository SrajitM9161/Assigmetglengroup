from errors import ApiError


def ensure_employee_can_be_assigned(employee, job, assignments):
    if not isinstance(employee.get("availability"), bool):
        raise ApiError("DATA_INTEGRITY_ERROR", "Employee availability data is invalid.", 500)
    if not employee["availability"]:
        raise ApiError("EMPLOYEE_UNAVAILABLE", "Employee is unavailable.", 409)
    required_role = job.get("requiredRole")
    if required_role and employee.get("role", "").lower() != required_role.lower():
        raise ApiError("ROLE_MISMATCH", "Employee role does not meet the job requirement.", 409)
    if any(item["jobId"] == job["id"] for item in assignments):
        raise ApiError("DUPLICATE_ASSIGNMENT", "Employee is already assigned to this job.", 409)


def validate_assignment_payload(payload):
    if not isinstance(payload, dict):
        raise ApiError("INVALID_REQUEST", "Request body must be a JSON object.", 400)
    unexpected = set(payload) - {"employeeId", "jobId"}
    if unexpected:
        raise ApiError("VALIDATION_ERROR", "Only employeeId and jobId are allowed.", 400)
    employee_id = payload.get("employeeId")
    job_id = payload.get("jobId")
    if not all(isinstance(value, str) and value.strip() for value in (employee_id, job_id)):
        raise ApiError("VALIDATION_ERROR", "employeeId and jobId must be non-empty strings.", 400)
    return employee_id.strip(), job_id.strip()
