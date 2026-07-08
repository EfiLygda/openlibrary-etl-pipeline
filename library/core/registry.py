"""
Central registry of event metadata shared between the producer and consumer
"""

from typing import Callable
from library.service.redis.keys import RedisKeys

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
            produces_event: bool,
    ):
        self.counter_name = counter_name
        self.max_allowable_name = max_allowable_name
        self.produces_event = produces_event

EVENTS = {

    # --- People ---
    'LIBRARIAN_HIRED': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.LIBRARIANS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.LIBRARIANS,
        produces_event=False,
    ),

    'USER_REGISTERED': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.USERS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.USERS,
        produces_event=False,
    ),

    # --- Inventory ---
    'COPY_PURCHASED': EventSpec(
        counter_name=lambda event:
            RedisKeys.Counters.edition_copies(event['data']['edition_key']),
        max_allowable_name=lambda event:
            RedisKeys.MaxAllowableValues.edition_copies(event['data']['edition_key']),
        produces_event=False,
        ),

    # --- Circulation ---
    'BORROW': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.LOANS,
        max_allowable_name=None,
        produces_event=False,
    ),

    'RETURN': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.RETURNS,
        max_allowable_name=None,
        produces_event=True, # In case of reserved copy emits BORROW from the user that reserved it
    ),

    'RENEWAL': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.RENEWALS,
        max_allowable_name=None,
        produces_event=False,
    ),

    # --- Demand ---
    'RESERVATION': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.RESERVATIONS,
        max_allowable_name=None,
        produces_event=False,
    ),
}
