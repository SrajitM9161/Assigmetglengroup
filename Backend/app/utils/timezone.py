from datetime import timezone


def to_utc_iso(value):
    """Store timezone-aware datetimes in a single UTC representation."""
    return value.astimezone(timezone.utc).isoformat()
