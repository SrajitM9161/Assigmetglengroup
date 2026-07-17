from app.storage.json_storage import JsonStorage


class JobRepository:
    def __init__(self, path): self.storage = JsonStorage(path)
    def list(self): return self.storage.read()
    def get(self, job_id): return next((item for item in self.list() if item["id"] == job_id), None)
    def create(self, job):
        records = self.list(); records.append(job); self.storage.write(records); return job
