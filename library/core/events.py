"""
Central definitions of event types used by the library system
"""

from enum import Enum

class EventType(str, Enum):
    """
    Enumeration of all supported library system events.

    The enum values represent the serialized names used in event payloads
    (for example, Kafka messages). Internal code should use the enum members
    instead of raw strings.

    Example:
        EventType.BORROW

    Serialized value:
        EventType.BORROW.value -> "BORROW"
    """

    # People events
    USER_REGISTERED = "USER_REGISTERED"
    LIBRARIAN_HIRED = "LIBRARIAN_HIRED"

    # Inventory events
    COPY_PURCHASED = "COPY_PURCHASED"

    # Circulation events
    BORROW = "BORROW"
    RETURN = "RETURN"
    RENEWAL = "RENEWAL"

    # Demand events
    RESERVATION = "RESERVATION"
    RESERVATION_CANCELLED = "RESERVATION_CANCELLED"