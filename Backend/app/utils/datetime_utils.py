from datetime import datetime


def parse_iso_datetime(value, field_name):
    """Parse the assignment's ISO date-time format into a friendly API error."""
    from errors import ApiError
    if not isinstance(value, str):
        raise ApiError("VALIDATION_ERROR", f"{field_name} must be an ISO-8601 date-time string.", 400)
    try:
        result = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ApiError("VALIDATION_ERROR", f"{field_name} must be a valid ISO-8601 date-time string.", 400) from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ApiError("VALIDATION_ERROR", f"{field_name} must include a timezone offset.", 400)
    return result


def intervals_overlap(start_a, end_a, start_b, end_b):
    """End-to-start jobs are allowed; any shared time is an overlap."""
    return start_a < end_b and end_a > start_b
