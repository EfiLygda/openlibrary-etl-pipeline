"""
Module responsible for creating standardized event objects
"""

import uuid
from datetime import datetime

def create_event(
        event_type: str,
        timestamp: datetime,
        payload: dict,
        trigger: str | None = None,
) -> dict:
    """
    Creates a standardized event dictionary with a unique identifier

    :param event_type: str, the type or name of the event.
    :param timestamp: datetime, the date and time when the event occurred.
    :param payload: dict, a dictionary containing the event-specific payload.
    :param trigger: str, indicates what caused the event to be generated
        (e.g., 'RESERVATION_FULFILLMENT'). ``None`` if the event
        was generated directly rather than triggered by another event.

    :returns: dict, a dictionary representing the event with the following keys:
        * 'event_id': str, a universally unique identifier
        * 'event_type': str, the type of the event
        * 'timestamp': str, the event's timestamp
        * 'payload': dict, additional data
    """

    event = {
        'event_id': str(uuid.uuid4()),
        'event_type': event_type,
        'timestamp': timestamp.isoformat(),
        'payload': payload,
    }

    if trigger is not None:
        event['trigger'] = trigger

    return event