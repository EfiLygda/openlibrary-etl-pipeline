"""
Event validation module
"""

from library.core.registry import EVENTS
from library.service.redis.service import RedisClient

def reject_event(
        redis_client: RedisClient,
        event: dict
) -> bool:
    """
    Determine whether an event should be rejected based on Redis counters

    :param redis_client: RedisClient, the redis client used to fetch counters
        and configuration values
    :param event: dict, event dictionary from Kafka

    :return: bool, true if the event should be rejected, False otherwise.
    """

    # Save current event's type
    event_type = event['event_type']

    # Get the current event's counter and max allowable name for Redis
    counter_name = EVENTS[event_type].counter_name(event)
    max_allowable_name = EVENTS[event_type].max_allowable_name(event)

    # Get the current event's counter and max_allowable values
    counter_value = redis_client.get_counter(counter_name)
    max_allowable_value = int(redis_client.get_value(max_allowable_name))

    # In case the current event's counter is over the maximum
    # allowable value then the generated event is rejected
    if counter_value >= max_allowable_value:
        return True

    return False