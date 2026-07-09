"""
Module responsible for generating simulation events
"""

from library.service.redis.client import RedisClient
from library.producer.producer_config import CLOCK
from library.producer.simulation.event_selection import get_event_by_timeline
from library.producer.simulation.event_factory import create_event
from library.producer.simulation import generators

# Mapping event names to their respective generation functions
EVENT_GENERATION_MAPPINGS = {
    'USER_REGISTERED': generators.people.user_registration,
    'LIBRARIAN_HIRED': generators.people.librarian_hired,
    'COPY_PURCHASED': generators.inventory.copy_purchased,
    'BORROW': generators.circulation.borrow_available_copy,
    'RETURN': generators.circulation.return_copy,
    'RENEWAL': generators.circulation.renew_loan,
    'RESERVATION': generators.demand.reserve_unavailable_copy,
}

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

    # Generate the event's data via its event type
    data = EVENT_GENERATION_MAPPINGS[event_type](redis_client=redis_client)

    return create_event(
        event_type=str(event_type),
        timestamp=timestamp,
        data=data
    )