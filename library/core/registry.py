"""
Central registry of event metadata shared between the producer and consumer
"""
from typing import Callable

from library.service.redis.keys import RedisKeys
from library.core.events import EventType, EventCategory
from library.producer.simulation import generators
from library.consumer import handlers

class EventSpec:
    """
    Stores metadata associated with a specific event type.

    :param counter_name:
        Function that receives an event dict and returns the Redis key
        for the event counter.

    :param max_allowable_name:
        Function that receives an event dict and returns the Redis key
        for the maximum allowed value.
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
        counter_hash_key=lambda event: event['data']['edition_key'],

        max_allowable_name=RedisKeys.Hashes.MAX_EDITION_COPIES,
        max_allowable_hash_key=lambda event: event['data']['edition_key'],

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

        produces_event=True, # In case of reserved copy emits BORROW from the user that reserved it
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
