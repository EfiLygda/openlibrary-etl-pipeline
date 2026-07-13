"""
Module responsible for generating simulation events
"""

from library.core.registry import EVENTS
from library.service.redis.client import RedisClient
from library.producer.producer_config import CLOCK
from library.producer.simulation.event_selection import get_event_by_timeline
from library.producer.simulation.event_factory import create_event
from library.producer.simulation import generators

def generate_event(redis_client: RedisClient) -> dict:
    """
    Function that generates an event

    :param redis_client: RedisClient, the redis client used to fetch counters
        and configuration values

    :returns: dict, dictionary with:
        * 'event_id': str, a universally unique identifier
        * 'event_type': str, the type of the event
        * 'timestamp': str, the event's timestamp
        * 'data': dict, additional data
    """

    # The 'current' timestamp (of course using the simulation clock)
    timestamp = CLOCK.now()

    # Get a random event type to generate, according to the timeline
    event_type = get_event_by_timeline(
        redis_client=redis_client,
        timestamp=timestamp
    )

    # Generate the event's data via its event spec
    data = EVENTS[event_type].generator(redis_client=redis_client)

    return create_event(
        event_type=str(event_type),
        timestamp=timestamp,
        data=data
    )