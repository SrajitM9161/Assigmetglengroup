import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from Services.audit_service import AuditService
from Services.employee_service import EmployeeService
from Services.job_service import JobService
from Services.schedule_service import ScheduleService
from errors import ApiError
from app.repositories.audit_repository import AuditRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.job_repository import JobRepository
from app.repositories.schedule_repository import ScheduleRepository


class ScheduleServiceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        root = self.directory.name
        self.employees = EmployeeService(EmployeeRepository(os.path.join(root, "employees.json")))
        self.jobs = JobService(JobRepository(os.path.join(root, "jobs.json")))
        self.schedule = ScheduleService(
            ScheduleRepository(os.path.join(root, "schedule.json")), self.employees, self.jobs,
            AuditService(AuditRepository(os.path.join(root, "audit.json")))
        )
        self.employee = self.employees.create({"name": "Asha", "role": "TCP", "availability": True})

    def tearDown(self): self.directory.cleanup()

    def create_job(self, start, end):
        return self.jobs.create({"name": "Shift", "startTime": start, "endTime": end})

    def test_back_to_back_jobs_do_not_overlap(self):
        first = self.create_job("2026-07-18T09:00:00+00:00", "2026-07-18T12:00:00+00:00")
        second = self.create_job("2026-07-18T12:00:00+00:00", "2026-07-18T17:00:00+00:00")
        self.schedule.assign({"employeeId": self.employee["id"], "jobId": first["id"]})
        result = self.schedule.assign({"employeeId": self.employee["id"], "jobId": second["id"]})
        self.assertEqual(result["jobId"], second["id"])

    def test_overlapping_jobs_are_rejected(self):
        first = self.create_job("2026-07-18T09:00:00+00:00", "2026-07-18T12:00:00+00:00")
        second = self.create_job("2026-07-18T11:00:00+00:00", "2026-07-18T15:00:00+00:00")
        self.schedule.assign({"employeeId": self.employee["id"], "jobId": first["id"]})
        with self.assertRaisesRegex(ApiError, "overlapping"):
            self.schedule.assign({"employeeId": self.employee["id"], "jobId": second["id"]})


if __name__ == "__main__":
    unittest.main()
