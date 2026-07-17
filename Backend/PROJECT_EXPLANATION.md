# Mini Employee Scheduling System - Technical Walkthrough

## 1. What this project solves

This is a small Flask scheduling API. A scheduler can view employees and jobs, assign an employee to a job, view the schedule, and delete an assignment.

The frontend presents the same schedule data in both a table and a week/month calendar. The calendar is a UI view over `GET /schedule`; it does not require another backend endpoint or an external calendar service.

The central business problem is preventing invalid scheduling:

- an unavailable employee cannot be assigned;
- an employee must match a job's `requiredRole` when one is defined;
- the same employee cannot be assigned to the same job twice;
- an employee cannot be assigned to overlapping job time windows;
- back-to-back shifts are valid. For example, 08:00-12:00 and 12:00-16:00 do not overlap.

The project intentionally uses local JSON files instead of a database, as required by the assignment. There is no Kafka, Redis, cloud platform, container orchestration, or real authentication.

## 2. Architecture

```text
Client / Postman
       |
       v
Routes -> Controllers -> Services -> Repositories -> JSON Storage
                         |
                         +-> Validators / Models / Audit events
```

Each layer has one clear responsibility:

| Layer | Responsibility |
| --- | --- |
| `routes/` | Maps URLs and HTTP methods to controller methods. |
| `Controllers/` | Reads request data and returns standardized HTTP responses. |
| `Services/` | Contains business rules such as availability and overlap checks. |
| `app/repositories/` | Provides CRUD-style access without exposing JSON-file details to services. |
| `app/storage/` | Reads/writes JSON, using atomic replacement to avoid half-written files. |
| `app/models/` | Defines the Employee, Job, and Schedule domain shapes. |
| `app/validators/` | Holds reusable assignment and time-window validation functions. |
| `app/middleware/` | Handles error responses, request logs, and simple mock role checks. |

This is intentionally more structured than putting all logic in Flask route functions, but it is still small enough for an assignment.

## 3. Data files

All persistent data is stored in `app/data/`.

| File | Content |
| --- | --- |
| `employees.json` | Seeded employees with id, name, role, and availability. |
| `jobs.json` | Seeded jobs with id, name, startTime, and endTime. |
| `schedule.json` | Created assignments. It starts empty. |
| `audit.json` | Assignment create/delete events. It starts empty intentionally. |

Example employee:

```json
{
  "id": "emp-001",
  "name": "Aarav Singh",
  "role": "TCP",
  "availability": true
}
```

Example job:

```json
{
  "id": "job-001",
  "name": "Morning Traffic Control",
  "startTime": "2026-07-20T08:00:00+00:00",
  "endTime": "2026-07-20T12:00:00+00:00"
}
```

## 4. API design

The exact assignment paths are supported. `/api/...` aliases are also available for a frontend.

| Method | Endpoint | Result |
| --- | --- | --- |
| GET | `/employees` or `/api/employees` | Returns all employees. |
| GET | `/jobs` or `/api/jobs` | Returns all jobs. |
| GET | `/schedule` or `/api/schedule` | Returns assignments, optionally filtered with `?employeeId=emp-001`. |
| POST | `/assign` or `/api/assign` | Creates an assignment. |
| DELETE | `/assign/:id` or `/api/assign/:id` | Deletes an assignment. |
| GET | `/api/health` | Small service health check. |

Assignment request:

```json
{
  "employeeId": "emp-001",
  "jobId": "job-001"
}
```

Success response:

```json
{
  "success": true,
  "message": "Assignment created successfully.",
  "data": {
    "id": "...",
    "employeeId": "emp-001",
    "jobId": "job-001",
    "employeeName": "Aarav Singh",
    "role": "TCP",
    "jobName": "Morning Traffic Control",
    "startTime": "2026-07-20T08:00:00+00:00",
    "endTime": "2026-07-20T12:00:00+00:00",
    "status": "assigned"
  }
}
```

Error response:

```json
{
  "success": false,
  "error": {
    "code": "SCHEDULE_OVERLAP",
    "message": "Employee has an overlapping assignment."
  }
}
```

## 5. Assignment validation flow

When `POST /assign` is called, the application performs this sequence:

1. Verify that `employeeId` and `jobId` are present in the JSON body.
2. Find the employee; return `EMPLOYEE_NOT_FOUND` if absent.
3. Find the job; return `JOB_NOT_FOUND` if absent.
4. Reject an employee whose `availability` is `false` with `EMPLOYEE_UNAVAILABLE`.
5. Reject a role mismatch with `ROLE_MISMATCH` when the job has a `requiredRole`.
6. Reject a duplicate employee/job pair with `DUPLICATE_ASSIGNMENT`.
7. Parse the ISO-8601 job times; invalid times return `VALIDATION_ERROR` rather than a server error.
8. Compare the proposed time window with every existing assignment for that employee.
9. Save the assignment to `schedule.json`.
10. Write `ASSIGNMENT_CREATED` to `audit.json`.
11. Return the consistent success response.

The overlap formula is:

```text
newStart < existingEnd AND newEnd > existingStart
```

This is important because it allows adjacent shifts while rejecting genuine overlaps.

## 6. Error handling and logging

`ApiError` represents expected business errors. The centralized error handler converts it to the response envelope with the correct HTTP code.

| Situation | HTTP status | Error code |
| --- | ---: | --- |
| Missing/invalid request data | 400 | `VALIDATION_ERROR` or `INVALID_REQUEST` |
| Employee/job does not exist | 404 | `EMPLOYEE_NOT_FOUND` / `JOB_NOT_FOUND` |
| Unavailable employee | 409 | `EMPLOYEE_UNAVAILABLE` |
| Duplicate or overlap | 409 | `DUPLICATE_ASSIGNMENT` / `SCHEDULE_OVERLAP` |
| Unexpected server problem | 500 | `INTERNAL_ERROR` |

The request logger records request method, path, response status, and elapsed time. Unexpected exceptions are logged with a stack trace.

JSON reads reject malformed files or non-array data with `DATA_STORE_ERROR`; the application does not silently erase corrupted data. Assignment and deletion are protected by one in-process lock, which makes their read/check/write/audit flow atomic for this assignment's single Flask process. A database transaction would replace that lock in a multi-process production deployment.

## 7. Audit trail

The audit trail is intentionally event-based and small:

```json
{
  "id": "...",
  "eventType": "ASSIGNMENT_CREATED",
  "entityId": "assignment-id",
  "occurredAt": "2026-07-20T08:00:00+00:00",
  "metadata": {
    "employeeId": "emp-001",
    "jobId": "job-001",
    "status": "assigned"
  }
}
```

`ASSIGNMENT_DELETED` is recorded on deletion. The file is empty before the first real schedule change; no dummy audit events were seeded.

## 8. Optional assignment-sized additions

These are kept deliberately light and can be described as extensions, not production security:

- **Mock RBAC:** `X-Role: admin`, `scheduler`, or `employee`. Missing headers default to scheduler for local development. This is not authentication.
- **Approval mode:** `APPROVAL_MODE=auto` creates `assigned` records; `APPROVAL_MODE=manual` creates `pending` records.
- **Schemas:** the `app/schemas/` folder documents expected payload shapes. Per project choice, runtime validation uses small explicit validators/services rather than Marshmallow schemas.

## 9. How to demonstrate it

1. From `Backend`, run `python run.py`.
2. Import `Mini_Scheduling_System.postman_collection.json` into Postman.
3. Run **Get employees** and **Get jobs** to show JSON-backed data.
4. Run **Assign available employee**. Show the success response and `schedule.json` / `audit.json` updates.
5. Run **Reject unavailable employee**. Explain the `409 EMPLOYEE_UNAVAILABLE` response.
6. Run **Reject overlapping job** after the successful assignment. Explain the overlap formula.
7. Run **Delete last assignment** and show the delete audit event.

If the assignment request was already run, use a different available employee/job pair or delete the prior assignment first; duplicate assignments are correctly rejected.

## 10. Testing and trade-offs

Run tests from `Backend`:

```bash
python -m unittest discover -s tests
```

The suite covers back-to-back schedules, overlap rejection, assignment creation, JSON persistence, audit creation, and the REST flow.

For a real production system, JSON storage would be replaced with a database, real user authentication would replace the mock header, and concurrent write handling would need database transactions. Those are consciously outside this two-day assignment scope.
