# Mini Employee Scheduling System

A small full-stack scheduling app built for the technical assignment. It lets a scheduler find employees, filter them by role and availability, assign them to jobs, and manage the current schedule from a table or calendar view. 

## Tech stack

- Flask REST API
- React + TypeScript + Vite
- Local JSON files for employees, jobs, schedule assignments, and audit events

## Features

- Employee name search, role filter, and availability filter
- Job selection with visible time window and required role
- Assignment validation for availability, role match, duplicate assignment, and overlapping shifts
- Schedule table with delete confirmation
- Week and month calendar views
- Clear success/error feedback

## Run locally

Open two terminals from this project folder.

### Backend

```bash
cd Backend
python -m pip install -r requirements.txt
python run.py
```

The API starts at `http://127.0.0.1:3000`.

### Frontend

```bash
cd Frontend
npm install
copy .env.example .env
npm run dev
```

Open the URL printed by Vite, usually `http://127.0.0.1:5173`.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/employees` | List employees |
| GET | `/jobs` | List jobs |
| GET | `/schedule` | List assignments |
| POST | `/assign` | Create an assignment |
| DELETE | `/assign/:id` | Delete an assignment |

The frontend uses the `/api` aliases of these same endpoints.

## Scheduling rules

- Unavailable employees cannot be assigned.
- An employee must match a job's required role, when the job defines one.
- An employee cannot be assigned to the same job twice.
- An employee cannot have overlapping shifts.
- Different employees may work different jobs during the same time window.
- Back-to-back shifts are allowed.

## Data and tests

Seed data is in `Backend/app/data/employees.json` and `Backend/app/data/jobs.json`. Assignments and audit events are written to `schedule.json` and `audit.json` when the API is used.

Run the backend tests:

```bash
cd Backend
python -m unittest discover -s tests
```


## Notes

This project uses JSON storage to match the assignment scope. The repository layer keeps file access separate from scheduling rules, making a future database swap straightforward. The role header used by the API is a local mock and is not production authentication.
