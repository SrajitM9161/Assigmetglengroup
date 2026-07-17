from app.storage.json_storage import JsonStorage


class AuditRepository:
    def __init__(self, path): self.storage = JsonStorage(path)
    def list(self): return self.storage.read()
    def create(self, event):
        records = self.storage.read(); records.append(event); self.storage.write(records); return event
