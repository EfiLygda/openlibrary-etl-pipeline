"""
Central registry of event metadata shared between the producer and system
"""
from typing import Callable

from library.service.redis.keys import RedisKeys
from library.core.events import EventType, EventCategory
from library.producer.simulation import generators
from library.consumers.system import handlers

class EventSpec:
    """
    Stores metadata associated with a specific event type

    :param category: EventCategory, category the event belongs to

    :param generator: Callable[..., dict], function that generates the
        event payload
    :param handler: Callable[..., None], function that processes the
        event

    :param counter_name: str | None, Redis key used to track the number
        of times the event has occurred
    :param counter_hash_key: Callable[[dict], str] | None, function that
        receives an event dictionary and returns the Redis hash field for
        the event counter. If None, the counter is stored as a normal
        Redis key

    :param max_allowable_name: str | None, Redis key used to store the
        maximum allowable value for the event counter
    :param max_allowable_hash_key: Callable[[dict], str] | None, function
        that receives an event dictionary and returns the Redis hash
        field for the maximum allowable value. If None, the value is
        stored as a normal Redis key

    :param produces_event: bool, whether handling this event produces
        another event
    """

    def __init__(
            self,

            category: EventCategory,

            generator: Callable[..., dict],
            handler: Callable[..., None],

            counter_name: str | None,
            counter_hash_key: Callable[[dict], str] | None,

            max_allowable_name: str | None,
            max_allowable_hash_key: Callable[[dict], str] | None,

            produces_event: bool,
    ):

        # The event's category
        self.category = category

        # The event's generator and handler functions
        self.generator = generator
        self.handler = handler

        # The event's redis counter name
        self.counter_name = counter_name
        self.counter_hash_key = counter_hash_key

        # The event's redis key for the maximum allowable times
        # it should be generated
        self.max_allowable_name = max_allowable_name
        self.max_allowable_hash_key = max_allowable_hash_key

        # Whether the event produces another event, or not
        self.produces_event = produces_event

    def get_counter_hash_key(self, event: dict) -> str | None:
        """
        Resolve the Redis hash field for the event counter

        :param event: dict, event dictionary

        :return: str | None, the Redis hash field for the event counter, or
            None if the counter is stored as a normal Redis key
        """
        if self.counter_hash_key is not None:
            return self.counter_hash_key(event)
        else:
            return None

    def get_max_allowable_hash_key(self, event: dict) -> str | None:
        """
        Resolve the Redis hash field for the maximum allowable value

        :param event: dict, event dictionary

        :return: str | None, the Redis hash field for the maximum allowable
            value, or None if the value is stored as a normal Redis key
        """
        if self.max_allowable_hash_key is not None:
            return self.max_allowable_hash_key(event)
        else:
            return None

EVENTS = {

    # --- People ---
    EventType.LIBRARIAN_HIRED: EventSpec(
        category=EventCategory.PEOPLE,

        generator=generators.people.librarian_hired,
        handler=handlers.people.handle_librarian_hired,

        counter_name=RedisKeys.Counters.LIBRARIANS,
        counter_hash_key=None,

        max_allowable_name=RedisKeys.Strings.MAX_LIBRARIANS,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    EventType.USER_REGISTERED: EventSpec(
        category=EventCategory.PEOPLE,

        generator=generators.people.user_registration,
        handler=handlers.people.handle_user_registered,

        counter_name=RedisKeys.Counters.USERS,
        counter_hash_key=None,

        max_allowable_name=RedisKeys.Strings.MAX_USERS,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    # --- Inventory ---
    EventType.COPY_PURCHASED: EventSpec(
        category=EventCategory.INVENTORY,

        generator=generators.inventory.copy_purchased,
        handler=handlers.inventory.handle_copy_purchased,

        counter_name=RedisKeys.Hashes.COUNTER_EDITION_COPIES,
        counter_hash_key=lambda event: event['payload']['edition_key'],

        max_allowable_name=RedisKeys.Hashes.MAX_EDITION_COPIES,
        max_allowable_hash_key=lambda event: event['payload']['edition_key'],

        produces_event=False,
        ),

    # --- Circulation ---
    EventType.COPY_BORROWED: EventSpec(
        category=EventCategory.CIRCULATION,

        generator=generators.circulation.borrow_available_copy,
        handler=handlers.circulation.handle_copy_borrowed,

        counter_name=RedisKeys.Counters.LOANS,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    EventType.COPY_RETURNED: EventSpec(
        category=EventCategory.CIRCULATION,

        generator=generators.circulation.return_copy,
        handler=handlers.circulation.handle_return_borrowed_copy,

        counter_name=RedisKeys.Counters.RETURNS,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        # In case the return is overdue then it emits FINE_ISSUED for the loan
        # In case of reserved copy emits COPY_BORROWED from the user that reserved it
        produces_event=True,
    ),

    EventType.LOAN_RENEWED: EventSpec(
        category=EventCategory.CIRCULATION,

        generator=generators.circulation.renew_loan,
        handler=handlers.circulation.handle_renewal_of_borrowed_copy,

        counter_name=RedisKeys.Counters.RENEWALS,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    EventType.FINE_ISSUED: EventSpec(
        category=EventCategory.CIRCULATION,

        generator=generators.circulation.issue_fine,
        handler=handlers.circulation.handle_fine_issued,

        counter_name=RedisKeys.Counters.ISSUED_FINES,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    EventType.FINE_PAID: EventSpec(
        category=EventCategory.CIRCULATION,

        generator=generators.circulation.pay_fine,
        handler=handlers.circulation.handle_fine_paid,

        counter_name=RedisKeys.Counters.PAID_FINES,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    # --- Demand ---
    EventType.RESERVATION_CREATED: EventSpec(
        category=EventCategory.DEMAND,

        generator=generators.demand.reserve_unavailable_copy,
        handler=handlers.demand.handle_reservation_of_unavailable_copy,

        counter_name=RedisKeys.Counters.RESERVATIONS,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        produces_event=False,
    ),

    EventType.RESERVATION_CANCELLED: EventSpec(
        category=EventCategory.DEMAND,

        generator=generators.demand.cancel_reservation,
        handler=handlers.demand.handle_cancellation_of_active_reservation,

        counter_name=RedisKeys.Counters.CANCELLED_RESERVATIONS,
        counter_hash_key=None,

        max_allowable_name=None,
        max_allowable_hash_key=None,

        produces_event=False,
    ),
}
