import json
import os
import tempfile
import threading

from errors import DataStoreError
from app.storage.base_storage import BaseStorage


class JsonStorage(BaseStorage):
    _file_lock = threading.RLock()

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with self._file_lock:
            if not os.path.exists(self.file_path):
                return []
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    records = json.load(file)
            except (OSError, json.JSONDecodeError) as exc:
                raise DataStoreError(f"Could not read {os.path.basename(self.file_path)}.") from exc
            if not isinstance(records, list):
                raise DataStoreError(f"{os.path.basename(self.file_path)} must contain a JSON array.")
            return records

    def write(self, records):
        with self._file_lock:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            fd, temporary_path = tempfile.mkstemp(dir=os.path.dirname(self.file_path), suffix=".json")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as file:
                    json.dump(records, file, indent=2)
                os.replace(temporary_path, self.file_path)
            except OSError as exc:
                raise DataStoreError(f"Could not write {os.path.basename(self.file_path)}.") from exc
            finally:
                if os.path.exists(temporary_path):
                    os.unlink(temporary_path)
