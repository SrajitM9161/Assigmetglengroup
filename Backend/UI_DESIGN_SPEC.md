# Mini Employee Scheduling System - UI Design Specification

## 1. Product summary

This is a scheduling tool for assigning employees to jobs. The primary user is a Scheduler who needs to quickly find an eligible employee, select a job, create an assignment, and review or delete the schedule.

The system must make invalid assignments understandable before and after submission:

- Employees have a role: `TCP`, `LCT`, or `Supervisor`.
- An employee may be unavailable.
- Some jobs require a specific role.
- One employee cannot work two overlapping jobs.
- Different employees may work different jobs at the same time.
- Back-to-back jobs are allowed. Example: 08:00-12:00 and 12:00-16:00.

## 2. Users and permissions

### Scheduler / Admin

- View all employees, jobs, and schedule assignments.
- Search and filter employees.
- Assign an employee to a job.
- Delete an assignment.

### Employee (read-only future view)

- View only their own schedule.
- Cannot create or delete assignments.

For this assignment, role handling is mock-only. The UI can assume the main scheduling screen is opened by a Scheduler.

## 3. Primary screen: Scheduler dashboard

Use one responsive dashboard page. Desktop should prioritize a two-column assignment workspace above a full-width schedule table.

```text
+--------------------------------------------------------------+
| Mini Scheduling System                         [Scheduler]   |
+--------------------------------------------------------------+
| Employee selection              | Job selection               |
| Search [................]       | Select job [.............]  |
| Role [All v] Availability [v]   | Time: 08:00 - 12:00         |
|                                 | Required role: TCP          |
| Employee list / dropdown        |                              |
| [Selected employee details]     | [Assign Employee]           |
+--------------------------------------------------------------+
| Assigned Schedule                                              |
| Filters: [All roles v] [All employees v] [Clear]              |
| ------------------------------------------------------------- |
| Employee | Role | Job | Time slot | Status | Action           |
+--------------------------------------------------------------+
```

On mobile, stack the Employee Selection card, Job Selection card, and Assigned Schedule table vertically. The table can become cards if horizontal scrolling is undesirable.

## 4. Employee selection

### Required controls

- Search input: filters employees by name, case-insensitively.
- Role filter: `All`, `TCP`, `LCT`, `Supervisor`.
- Availability filter: `All`, `Available`, `Unavailable`.
- Employee dropdown or selectable list.

### Employee row/card content

- Name
- Role badge
- Availability badge

Suggested visual language:

| State | Suggested treatment |
| --- | --- |
| Available | Green badge: `Available` |
| Unavailable | Gray/red badge: `Unavailable`; disable selection or clearly warn |
| Role matches selected job | Optional green outline/check |
| Role does not match selected job | Optional muted/disabled row with explanation |

When an employee is selected, show a compact summary:

```text
Aarav Singh
TCP · Available
```

## 5. Job selection

### Required controls

- Job dropdown/list populated from the jobs API.
- Clearly show each job’s name and time range.

Example label:

```text
Morning Traffic Control — 08:00 to 12:00 (TCP required)
```

After selection, display:

- Job name
- Start time and end time in readable local display format
- Required role, if present

Jobs may overlap each other. This is valid: multiple employees can work different jobs at the same time. The UI only needs to prevent or explain an overlap for the selected employee.

## 6. Assignment action

### Button states

| State | Button behaviour |
| --- | --- |
| No employee selected | Disabled: `Select an employee` |
| No job selected | Disabled: `Select a job` |
| Employee unavailable | Disabled, with helper message |
| Role mismatch | Disabled, with helper message |
| Employee has overlapping shift | Disabled if calculated in UI; otherwise allow submit and show server error |
| Valid selection | Enabled: `Assign Employee` |
| Request in progress | Disabled loading state: `Assigning...` |

The backend remains the source of truth. Even when the UI pre-validates, it must show the API error if the server rejects an assignment.

### Success feedback

After success:

- Show toast: `Assignment created successfully.`
- Refresh the schedule table.
- Clear selections, or retain the selected employee if that is more convenient.

### Error feedback

Show error messages close to the assignment button and optionally as a toast.

| API error code | User-facing message |
| --- | --- |
| `EMPLOYEE_UNAVAILABLE` | `This employee is unavailable.` |
| `ROLE_MISMATCH` | `This employee does not have the required role for this job.` |
| `DUPLICATE_ASSIGNMENT` | `This employee is already assigned to this job.` |
| `SCHEDULE_OVERLAP` | `This employee already has a shift during this time.` |
| `EMPLOYEE_NOT_FOUND` / `JOB_NOT_FOUND` | `The selected item no longer exists. Please refresh and try again.` |
| `VALIDATION_ERROR` / `INVALID_REQUEST` | `Please check the selected employee and job.` |
| `DATA_STORE_ERROR` / `INTERNAL_ERROR` | `Something went wrong. Please try again.` |

## 7. Assigned schedule

### Table columns

- Employee name
- Role
- Assigned job
- Time slot
- Status
- Delete action (Scheduler/Admin only)

Example row:

| Employee | Role | Job | Time slot | Status | Action |
| --- | --- | --- | --- | --- | --- |
| Aarav Singh | TCP | Morning Traffic Control | Jul 20, 08:00-12:00 | Assigned | Delete |

Use a status badge:

- `Assigned`: green/blue
- `Pending`: amber, only if manual approval mode is enabled

### Schedule states

- Loading: show table skeleton rows.
- Empty: show `No assignments yet. Select an employee and job to create the first schedule entry.`
- Error: show a retry action.
- Loaded: sortable table is optional; no pagination is needed for this assignment.

### Delete interaction

Use a small confirmation dialog:

```text
Remove assignment?
Remove Aarav Singh from Morning Traffic Control?

[Cancel] [Delete assignment]
```

After a successful delete, remove the row and show `Assignment deleted successfully.`

## 8. API contract for the frontend

Base URL during local development:

```text
http://127.0.0.1:3000/api
```

All responses use the same envelope:

```json
{
  "success": true,
  "message": "...",
  "data": {}
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "SCHEDULE_OVERLAP",
    "message": "Employee has an overlapping assignment."
  }
}
```

### GET `/employees`

```json
{
  "success": true,
  "data": [
    {
      "id": "emp-001",
      "name": "Aarav Singh",
      "role": "TCP",
      "availability": true
    }
  ]
}
```

### GET `/jobs`

```json
{
  "success": true,
  "data": [
    {
      "id": "job-001",
      "name": "Morning Traffic Control",
      "startTime": "2026-07-20T08:00:00+00:00",
      "endTime": "2026-07-20T12:00:00+00:00",
      "requiredRole": "TCP"
    }
  ]
}
```

### GET `/schedule`

Optional employee filter: `/schedule?employeeId=emp-001`

```json
{
  "success": true,
  "data": [
    {
      "id": "assignment-id",
      "employeeId": "emp-001",
      "jobId": "job-001",
      "employeeName": "Aarav Singh",
      "role": "TCP",
      "jobName": "Morning Traffic Control",
      "startTime": "2026-07-20T08:00:00+00:00",
      "endTime": "2026-07-20T12:00:00+00:00",
      "status": "assigned"
    }
  ]
}
```

### POST `/assign`

```json
{
  "employeeId": "emp-001",
  "jobId": "job-001"
}
```

### DELETE `/assign/{assignmentId}`

No request body.

## 9. Calendar view

The application also includes a calendar view of the assigned schedule. It uses the same `GET /schedule` data as the table; no additional backend endpoint or external calendar service is required.

### Calendar controls

- View switch: `Week` and `Month`.
- Previous and next navigation arrows.
- Current date/week label.
- Optional filters: employee, role, and status.
- `Today` button to return to the current date.

### Calendar events

Each assignment appears as an event positioned from `startTime` to `endTime`.

Event content should show:

```text
Morning Traffic Control
Aarav Singh · TCP
08:00 - 12:00
```

Use the employee role or assignment status for subtle event colouring, but always include text so the calendar does not depend on colour alone. Clicking an event can open a small detail popover with the employee, job, full time range, status, and a delete action for schedulers.

### Calendar rules

- Multiple jobs may appear in the same time period when they belong to different employees.
- The backend prevents two overlapping events for the same employee.
- Calendar timestamps are stored as ISO-8601 UTC strings. The UI should format them in the viewer's local timezone using the browser date/time formatter.
- The schedule table and calendar must refresh together after assignment creation or deletion.

### Empty calendar state

```text
No assignments in this period.
Choose another week/month or create a new assignment.
```

## 10. Suggested frontend state

```text
employees: Employee[]
jobs: Job[]
schedule: Assignment[]

searchText: string
roleFilter: "All" | "TCP" | "LCT" | "Supervisor"
availabilityFilter: "All" | "Available" | "Unavailable"
selectedEmployeeId: string | null
selectedJobId: string | null
calendarView: "week" | "month"
calendarDate: Date

loading: { employees, jobs, schedule, assigning, deleting }
error: string | null
```

No global state library is necessary. `useState` and `useEffect` are sufficient for this assignment; a small API service module keeps fetch calls organized.

## 11. Visual direction

- Professional operations dashboard, calm and clean rather than a complex enterprise admin panel.
- Use one primary accent color for actions; reserve red for destructive actions/errors and green for availability/success.
- Use clear spacing and readable table typography.
- Role and status badges should be visually distinct but accessible.
- Do not rely on color alone: include text labels and icons where helpful.
- Meet basic accessibility: visible focus states, associated labels, keyboard-accessible controls, and adequate contrast.

## 12. Important design decisions

- Do not display technical JSON errors or stack traces.
- Do not imply that all overlapping jobs are invalid. Only an overlap for the same employee is invalid.
- Do not allow an unavailable employee to appear as normally selectable.
- Role filtering is a convenience; the backend role check remains authoritative.
- The backend supports CORS for `/api` routes, so the React app can run on a different local port.
