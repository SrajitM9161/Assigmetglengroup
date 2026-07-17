from dataclasses import asdict, dataclass


@dataclass
class Job:
    id: str
    name: str
    startTime: str
    endTime: str
    requiredRole: str | None = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
