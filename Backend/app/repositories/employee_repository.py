from app.storage.json_storage import JsonStorage


class EmployeeRepository:
    def __init__(self, path): self.storage = JsonStorage(path)
    def list(self): return self.storage.read()
    def get(self, employee_id): return next((item for item in self.list() if item["id"] == employee_id), None)
    def create(self, employee):
        records = self.list(); records.append(employee); self.storage.write(records); return employee
