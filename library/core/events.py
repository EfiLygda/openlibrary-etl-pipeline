"""
Central definitions of event types and categories used by the library system
"""

from enum import Enum

class StringEnum(str, Enum):
    """
    Base class for string-backed enumerations.

    String enums serialize to their value when converted to a string,
    making them convenient for logging, JSON serialization, and external
    interfaces such as Kafka events.
    """

    def __str__(self) -> str:
        """
        Return the object's string value.

        This allows the enum to behave like its string value when
        used by libraries that internally call str().
        """
        return self.value

class EventType(StringEnum):
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
    COPY_REPORTED_LOST = "COPY_REPORTED_LOST"
    LOAN_RENEWED = "LOAN_RENEWED"
    FINE_ISSUED = "FINE_ISSUED"
    FINE_PAID = "FINE_PAID"

    # Demand events
    RESERVATION_CREATED = "RESERVATION_CREATED"
    RESERVATION_CANCELLED = "RESERVATION_CANCELLED"


class EventCategory(StringEnum):
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

class EventTrigger(StringEnum):
    """
    Enumeration of triggers describing why an event was produced.

    Triggers provide additional context for an event, indicating whether it
    was generated directly by the simulation or as a consequence of handling
    another event.
    """

    RESERVATION_FULFILLMENT = "RESERVATION_FULFILLMENT"
    OVERDUE_LOAN_RETURN = "OVERDUE_LOAN_RETURN"
