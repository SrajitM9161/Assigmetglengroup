from app.storage.json_storage import JsonStorage


class ScheduleRepository:
    def __init__(self, path): self.storage = JsonStorage(path)
    def list(self): return self.storage.read()
    def get(self, assignment_id): return next((item for item in self.list() if item["id"] == assignment_id), None)
    def for_employee(self, employee_id): return [item for item in self.list() if item["employeeId"] == employee_id]
    def create(self, assignment):
        records = self.list(); records.append(assignment); self.storage.write(records); return assignment
    def delete(self, assignment_id):
        records = self.list(); remaining = [item for item in records if item["id"] != assignment_id]
        if len(records) == len(remaining): return False
        self.storage.write(remaining); return True
