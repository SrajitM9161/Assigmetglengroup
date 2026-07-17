from errors import ApiError
from app.utils.datetime_utils import intervals_overlap


def ensure_no_overlap(start_time, end_time, assignments):
    if any(intervals_overlap(start_time, end_time, item["startTime"], item["endTime"]) for item in assignments):
        raise ApiError("SCHEDULE_OVERLAP", "Employee has an overlapping assignment.", 409)
