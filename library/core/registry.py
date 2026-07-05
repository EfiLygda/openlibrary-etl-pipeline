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
    ):
        self.counter_name = counter_name
        self.max_allowable_name = max_allowable_name


EVENTS = {
    'LIBRARIAN_HIRED': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.LIBRARIANS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.LIBRARIANS
    ),

    'USER_REGISTERED': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.USERS,
        max_allowable_name=lambda event: RedisKeys.MaxAllowableValues.USERS
    ),

    'COPY_PURCHASED': EventSpec(
        counter_name=lambda event:
            RedisKeys.Counters.edition_copies(event['data']['edition_key']),
        max_allowable_name=lambda event:
            RedisKeys.MaxAllowableValues.edition_copies(event['data']['edition_key'])
    ),

    'BORROW': EventSpec(
        counter_name=lambda event: RedisKeys.Counters.LOANS,
        max_allowable_name=None
    ),

    # 'RETURN': handle_return,
    # 'RESERVE': handle_reserve,
}
