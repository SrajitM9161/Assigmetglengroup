import os
import sys
import tempfile
import unittest
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app


class ApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        for filename in ("employees.json", "jobs.json", "schedule.json", "audit.json"):
            with open(os.path.join(self.directory.name, filename), "w", encoding="utf-8") as data_file:
                data_file.write("[]")
        self.client = create_app({"TESTING": True, "JSON_DATA_PATH": self.directory.name}).test_client()

    def tearDown(self):
        self.directory.cleanup()

    def test_assignment_endpoint_creates_an_audited_schedule(self):
        employee = self.client.post("/api/employees", json={"name": "Asha", "role": "TCP", "availability": True}).get_json()["data"]
        job = self.client.post("/api/jobs", json={
            "name": "Morning shift", "startTime": "2026-07-18T09:00:00+00:00",
            "endTime": "2026-07-18T17:00:00+00:00"
        }).get_json()["data"]
        response = self.client.post("/api/assign", json={"employeeId": employee["id"], "jobId": job["id"]})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.get_json()["success"])
        self.assertEqual(response.get_json()["data"]["status"], "assigned")
        schedule = self.client.get(f"/api/schedule?employeeId={employee['id']}").get_json()["data"]
        self.assertEqual(len(schedule), 1)
        with open(os.path.join(self.directory.name, "audit.json"), encoding="utf-8") as audit_file:
            audit_events = json.load(audit_file)
        self.assertEqual(audit_events[0]["eventType"], "ASSIGNMENT_CREATED")

    def test_role_mismatch_and_invalid_payload_are_rejected(self):
        employee = self.client.post("/api/employees", json={"name": "Meera", "role": "LCT", "availability": True}).get_json()["data"]
        job = self.client.post("/api/jobs", json={
            "name": "TCP shift", "startTime": "2026-07-18T09:00:00+00:00",
            "endTime": "2026-07-18T17:00:00+00:00", "requiredRole": "TCP"
        }).get_json()["data"]
        mismatch = self.client.post("/api/assign", json={"employeeId": employee["id"], "jobId": job["id"]})
        invalid = self.client.post("/api/assign", json={"employeeId": 99, "jobId": job["id"]})
        self.assertEqual(mismatch.get_json()["error"]["code"], "ROLE_MISMATCH")
        self.assertEqual(invalid.status_code, 400)

    def test_second_delete_returns_not_found_without_extra_audit_event(self):
        missing = self.client.delete("/api/assign/not-an-assignment")
        self.assertEqual(missing.status_code, 404)
        with open(os.path.join(self.directory.name, "audit.json"), encoding="utf-8") as audit_file:
            self.assertEqual(json.load(audit_file), [])


if __name__ == "__main__":
    unittest.main()
