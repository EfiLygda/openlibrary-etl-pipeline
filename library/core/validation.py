"""
Event validation module
"""

from library.core.events import EventType
from library.core.registry import EVENTS
from library.service.redis.client import RedisClient
from library.service.redis.keys import RedisKeys


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

    # Get current event's Redis counter name and maximum allowable name
    counter_name = event_spec.counter_name
    max_allowable_name = event_spec.max_allowable_name

    # Resolve hash keys if the value is stored inside a Redis hash
    counter_hash_key = event_spec.get_counter_hash_key(event)
    max_allowable_hash_key = event_spec.get_max_allowable_hash_key(event)

    # Fetch current counter value
    counter_value = redis_client.counters.get(
        name=counter_name,
        key=counter_hash_key
    )

    # Fetch maximum allowable value
    # In case a hash key is available then the value is stored in a redis hash,
    # else in a simple value
    if max_allowable_hash_key:
        max_allowable_value = redis_client.hashes.get(
            name=max_allowable_name,
            key=max_allowable_hash_key
        )
    else:
        max_allowable_value = redis_client.strings.get(name=max_allowable_name)

    # Convert fetched value to integer
    max_allowable_value = int(max_allowable_value)

    return counter_value >= max_allowable_value

def borrowed_copy_does_not_exist(event: dict) -> bool:
    """
    Determine whether a copy was selected for a borrow event, used for rejecting the event

    :param event: dict, event dictionary from Kafka

    :return: bool, true if the event should be rejected, False otherwise
    """

    if event['payload']['copy_id'] is None:
        return True

    return  False

def loan_renewal_over_max_allowable(
        redis_client: RedisClient,
        event: dict,
        max_loans: int = 1,
) -> bool:
    """
    Determine whether a loan renewal exceeds the maximum allowable count.

    :param redis_client: RedisClient, the redis client used to fetch reservation
        counters
    :param event: dict, event dictionary from Kafka
    :param max_loans: int, the maximum allowable times for renewing a loan (default: 1)

    :return: bool, True if the reservation has already been renewed the maximum
        allowable number of times, False otherwise.
    """

    # Fetch loan ID
    loan_id = event['payload']['loan_id']

    # Check if the loan renewal count is >= 1
    if redis_client.counters.get(
        name=RedisKeys.Counters.loan_renewals(loan_id)
    ) >= max_loans:
        return True
    else:
        return False

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

    # Check if a loan's renewal count is over the maximum allowable
    if event_type in [EventType.LOAN_RENEWED]:
        return loan_renewal_over_max_allowable(
            redis_client=redis_client,
            event=event
        )

    return False