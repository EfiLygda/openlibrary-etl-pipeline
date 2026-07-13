"""
Central registry of event metadata shared between the producer and consumer
"""

from typing import Callable

from library.service.redis.keys import RedisKeys

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
            category: str,
            generator: Callable[..., dict],
            handler: Callable[..., tuple],
            counter_name: Callable[[dict], str] | None,
            max_allowable_name: Callable[[dict], str] | None,
            produces_event: bool,
    ):

        # The event categories
        categories = [
            'PEOPLE',
            'INVENTORY',
            'CIRCULATION',
            'DEMAND'
        ]

        # The event's category
        self.category = category

        # The event's generator and handler functions
        self.generator = generator
        self.handler = handler

        # The event's redis counter name
        self.counter_name = counter_name

        # The event's redis key for the maximum allowable times
        # it should be generated
        self.max_allowable_name = max_allowable_name

        # Whether the event produces another event, or not
        self.produces_event = produces_event

EVENTS = {

    # --- People ---
    'LIBRARIAN_HIRED': EventSpec(
        category='PEOPLE',

        generator=generators.people.librarian_hired,
        handler=handlers.people.handle_librarian_hired,

        counter_name=lambda event: RedisKeys.Counters.LIBRARIANS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.LIBRARIANS,

        produces_event=False,
    ),

    'USER_REGISTERED': EventSpec(
        category='PEOPLE',

        generator=generators.people.user_registration,
        handler=handlers.people.handle_user_registered,

        counter_name=lambda event: RedisKeys.Counters.USERS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.USERS,

        produces_event=False,
    ),

    # --- Inventory ---
    'COPY_PURCHASED': EventSpec(
        category='INVENTORY',

        generator=generators.inventory.copy_purchased,
        handler=handlers.inventory.handle_copy_purchased,

        counter_name=lambda event:
            RedisKeys.Counters.edition_copies(event['data']['edition_key']),
        max_allowable_name=lambda event:
            RedisKeys.MaxAllowableValues.edition_copies(event['data']['edition_key']),

        produces_event=False,
        ),

    # --- Circulation ---
    'BORROW': EventSpec(
        category='CIRCULATION',

        generator=generators.circulation.borrow_available_copy,
        handler=handlers.circulation.handle_copy_borrowed,

        counter_name=lambda event: RedisKeys.Counters.LOANS,
        max_allowable_name=None,

        produces_event=False,
    ),

    'RETURN': EventSpec(
        category='CIRCULATION',

        generator=generators.circulation.return_copy,
        handler=handlers.circulation.handle_return_borrowed_copy,

        counter_name=lambda event: RedisKeys.Counters.RETURNS,
        max_allowable_name=None,

        produces_event=True, # In case of reserved copy emits BORROW from the user that reserved it
    ),

    'RENEWAL': EventSpec(
        category='CIRCULATION',

        generator=generators.circulation.renew_loan,
        handler=handlers.circulation.handle_renewal_of_borrowed_copy,

        counter_name=lambda event: RedisKeys.Counters.RENEWALS,
        max_allowable_name=None,

        produces_event=False,
    ),

    # --- Demand ---
    'RESERVATION': EventSpec(
        category='DEMAND',

        generator=generators.demand.reserve_unavailable_copy,
        handler=handlers.demand.handle_reservation_of_unavailable_copy,

        counter_name=lambda event: RedisKeys.Counters.RESERVATIONS,
        max_allowable_name=None,

        produces_event=False,
    ),

    'CANCELLED_RESERVATION': EventSpec(
        category='DEMAND',

        generator=generators.demand.reserve_unavailable_copy,
        handler=handlers.demand.handle_cancellation_of_active_reservation,

        counter_name=lambda event: RedisKeys.Counters.CANCELLED_RESERVATIONS,
        max_allowable_name=None,

        produces_event=False,
    ),
}
