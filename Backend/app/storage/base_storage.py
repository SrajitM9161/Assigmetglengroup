from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Small persistence contract; repositories do not depend on JSON details."""

    @abstractmethod
    def read(self):
        raise NotImplementedError

    @abstractmethod
    def write(self, records):
        raise NotImplementedError
