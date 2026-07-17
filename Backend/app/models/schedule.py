from dataclasses import asdict, dataclass


@dataclass
class Schedule:
    id: str
    employeeId: str
    jobId: str
    startTime: str
    endTime: str
    status: str = "assigned"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
