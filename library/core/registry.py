"""
Central registry of event metadata shared between the producer and consumer
"""

from typing import Callable

from library.service.redis.keys import RedisKeys

from library.consumer.handlers import people, demand
from library.consumer.handlers import inventory
from library.consumer.handlers import circulation


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
            counter_name: Callable[[dict], str],
            max_allowable_name: Callable[[dict], str] | None,
            handler: Callable[..., tuple],
            produces_event: bool,
    ):
        self.counter_name = counter_name
        self.max_allowable_name = max_allowable_name

        self.handler = handler
        self.produces_event = produces_event

EVENTS = {

    # --- People ---
    'LIBRARIAN_HIRED': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.LIBRARIANS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.LIBRARIANS,

        handler=people.handle_librarian_hired,

        produces_event=False,
    ),

    'USER_REGISTERED': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.USERS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.USERS,

        handler=people.handle_user_registered,

        produces_event=False,
    ),

    # --- Inventory ---
    'COPY_PURCHASED': EventSpec(
        counter_name=lambda event:
            RedisKeys.Counters.edition_copies(event['data']['edition_key']),
        max_allowable_name=lambda event:
            RedisKeys.MaxAllowableValues.edition_copies(event['data']['edition_key']),

        handler=inventory.handle_copy_purchased,

        produces_event=False,
        ),

    # --- Circulation ---
    'BORROW': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.LOANS,
        max_allowable_name=None,

        handler=circulation.handle_copy_borrowed,

        produces_event=False,
    ),

    'RETURN': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.RETURNS,
        max_allowable_name=None,

        handler=circulation.handle_return_borrowed_copy,

        produces_event=True, # In case of reserved copy emits BORROW from the user that reserved it
    ),

    'RENEWAL': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.RENEWALS,
        max_allowable_name=None,

        handler=circulation.handle_renewal_of_borrowed_copy,

        produces_event=False,
    ),

    # --- Demand ---
    'RESERVATION': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.RESERVATIONS,
        max_allowable_name=None,

        handler=demand.handle_reservation_of_unavailable_copy,

        produces_event=False,
    ),
}
