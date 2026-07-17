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

def overdue_days(
        due_date: str,
        returned_date: str
) -> int:
    """
    Calculate the number of overdue days between a due date and a return date.

    Returns 0 if the item was returned on time or early.

    :param due_date: str, ISO 8601 formatted due date
    :param returned_date: str, ISO 8601 formatted return date

    :return: int, number of overdue days
    """

    # Convert strings from ISO format to datetime objects
    due = datetime.fromisoformat(due_date)
    returned = datetime.fromisoformat(returned_date)

    return max(0, (returned - due).days)
