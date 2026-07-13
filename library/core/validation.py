"""
Event validation module
"""

from library.core.events import EventType
from library.core.registry import EVENTS
from library.service.redis.client import RedisClient

def is_over_max_allowed(
        redis_client: RedisClient,
        event: dict
) -> bool:
    """
    Determine whether an event should be rejected based on Redis counters

    :param redis_client: RedisClient, the redis client used to fetch counters
        and configuration values
    :param event: dict, event dictionary from Kafka

    :return: bool, true if the event should be rejected, False otherwise
    """

    # Save current event's type
    event_type = event['event_type']

    # Fetch event spec
    event_spec = EVENTS[event_type]

    # Get the current event's counter and max allowable name for Redis
    counter_name = event_spec.counter_name(event)
    max_allowable_name = event_spec.max_allowable_name(event)

    # Get the current event's counter and max_allowable values
    counter_value = redis_client.get_counter(counter_name)
    max_allowable_value = int(redis_client.get_value(max_allowable_name))

    # In case the current event's counter is over the maximum
    # allowable value then the generated event is rejected
    if counter_value >= max_allowable_value:
        return True

    return False

def borrowed_copy_does_not_exist(event: dict) -> bool:
    """
    Determine whether a copy was selected for a borrow event, used for rejecting the event

    :param event: dict, event dictionary from Kafka

    :return: bool, true if the event should be rejected, False otherwise
    """

    if event['data']['copy_id'] is None:
        return True

    return  False

def reject_event(
        redis_client: RedisClient,
        event: dict
) -> bool:
    """
    Determine whether an event should be rejected or not

    :param redis_client: RedisClient, the redis client used to fetch counters
        and configuration values
    :param event: dict, event dictionary from Kafka

    :return: bool, true if the event should be rejected, False otherwise.
    """

    # Save current event's type
    event_type = event['event_type']

    # Use maximum allowable event counts for 'LIBRARIAN_HIRED', 'USER_REGISTERED', 'COPY_PURCHASED'
    # and reject
    if event_type in [
        EventType.LIBRARIAN_HIRED,
        EventType.USER_REGISTERED,
        EventType.COPY_PURCHASED
    ]:
        return is_over_max_allowed(
            redis_client=redis_client,
            event=event
        )

    # Check if no copy was available to borrow and reject
    if event_type in [EventType.COPY_BORROWED]:
        return borrowed_copy_does_not_exist(event=event)

    return False