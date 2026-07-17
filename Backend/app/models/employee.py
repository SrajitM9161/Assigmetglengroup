from dataclasses import asdict, dataclass


@dataclass
class Employee:
    id: str
    name: str
    role: str
    availability: bool = True

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
