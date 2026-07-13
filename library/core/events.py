"""
Central definitions of event types and categories used by the library system
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
    COPY_BORROWED = "COPY_BORROWED"
    COPY_RETURNED = "COPY_RETURNED"
    LOAN_RENEWED = "LOAN_RENEWED"

    # Demand events
    RESERVATION_CREATED = "RESERVATION_CREATED"
    RESERVATION_CANCELLED = "RESERVATION_CANCELLED"

    def __str__(self):
        """
        Return the serialized event category name.

        This allows the enum to behave like its string value when
        used by libraries that internally call str().
        """
        return self.value


class EventCategory(str, Enum):
    """
    Enumeration of all supported event categories.

    Event categories group related events by their business domain.

    Example:
        EventCategory.CIRCULATION

    Serialized value:
        EventCategory.CIRCULATION.value -> "CIRCULATION"
    """

    PEOPLE = "PEOPLE"
    INVENTORY = "INVENTORY"
    CIRCULATION = "CIRCULATION"
    DEMAND = "DEMAND"

    def __str__(self):
        """
        Return the serialized event category name.

        This allows the enum to behave like its string value when
        used by libraries that internally call str().
        """
        return self.value
