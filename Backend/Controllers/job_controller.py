from flask import request
from app.utils.response import success


class JobController:
    def __init__(self, service): self.service = service
    def list(self): return success(self.service.list(), "Jobs retrieved successfully.")
    def create(self):
        job = self.service.create(request.get_json(silent=True))
        return success(job, "Job created successfully.", 201)
