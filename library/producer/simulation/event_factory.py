"""
Module responsible for creating standardized event objects
"""

import uuid
from datetime import datetime

def create_event(
        event_type: str,
        timestamp: datetime,
        data: dict
) -> dict:
    """
    Creates a standardized event dictionary with a unique identifier

    :param event_type: str, the type or name of the event.
    :param timestamp: datetime, the date and time when the event occurred.
    :param data: dict, a dictionary containing the event-specific payload.

    :returns: dict, a dictionary representing the event with the following keys:
        * 'event_id': str, a universally unique identifier
        * 'event_type': str, the type of the event
        * 'timestamp': str, the event's timestamp
        * 'data': dict, additional data
    """

    # Return the event
    return {
      'event_id': str(uuid.uuid4()), # Universally Unique Identifier
      'event_type': event_type,
      'timestamp': timestamp.isoformat(),
      'data': data
    }