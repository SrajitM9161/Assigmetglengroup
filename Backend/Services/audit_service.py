from datetime import datetime, timezone
from uuid import uuid4


class AuditService:
    def __init__(self, repository): self.repository = repository

    def record(self, event_type, entity_id, metadata=None):
        return self.repository.create({
            "id": str(uuid4()), "eventType": event_type, "entityId": entity_id,
            "occurredAt": datetime.now(timezone.utc).isoformat(), "metadata": metadata or {}
        })
