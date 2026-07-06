"""
Datetime utilities module
"""

from datetime import datetime, timedelta

def add_days_to_str_date(
        date: str,
        days: int,
) -> str:
    """
    Add a number of days to an ISO 8601 datetime string

    :param date: str, ISO 8601 formatted datetime string (e.g. "2026-07-06T12:34:56")
    :param days: int, number of days to add (can be negative to subtract days)

    :return: str, ISO 8601 formatted datetime string after adding the given number of days
    """

    # Convert string from ISO format to datetime object
    dt = datetime.fromisoformat(date)

    # Add days and convert to ISO format
    return (dt + timedelta(days=days)).isoformat()