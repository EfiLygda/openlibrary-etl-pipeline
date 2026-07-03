"""
Central registry of event metadata shared between the producer and consumer
"""

from typing import Callable

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
            max_allowable_name: Callable[[dict], str],
    ):
        self.counter_name = counter_name
        self.max_allowable_name = max_allowable_name


EVENTS = {
    'LIBRARIAN_HIRED': EventSpec(
        counter_name=lambda event: 'counter:librarians',
        max_allowable_name=lambda event: 'max:librarians'
    ),

    'USER_REGISTERED': EventSpec(
        counter_name=lambda event: 'counter:users',
        max_allowable_name=lambda event: 'max:users'
    ),

    'COPY_PURCHASED': EventSpec(
        counter_name=lambda event:
            f'counter:edition:{event['data']['edition_key']}:copies',
        max_allowable_name=lambda event:
            f'max:edition:{event['data']['edition_key']}:copies'
    ),

    # 'BORROW': handle_borrow,
    # 'RETURN': handle_return,
    # 'RESERVE': handle_reserve,
}
