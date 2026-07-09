"""
Module for generating events
"""

import uuid
import numpy as np
from datetime import datetime

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient

from library.producer.producer_config import (
    CLOCK,
    LIBRARIANS_HIRINGS_DEADLINE,
    LIBRARY_OPENING_DATE
)

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

def get_category_weights_by_timeline(
        timestamp: datetime,
        has_available_copies: bool,
        has_unavailable_copies: bool,
) -> dict:
    """
    Determines the probability distribution of event categories based on
    the current simulation timeline and library state

    :param timestamp: datetime.datetime, the current simulation timestamp used to determine
        the current phase of the library lifecycle
    :param has_available_copies: bool, indicates whether there are currently available copies that can
        be borrowed
    :param has_unavailable_copies: bool, indicates whether there are currently borrowed/unavailable copies
        in the system

    :return: dict, a dictionary mapping event categories to their respective
        probability weights
    """

    if timestamp <= LIBRARIANS_HIRINGS_DEADLINE:
        return {
            'PEOPLE': 0.6, # LIBRARIAN_HIRED
            'INVENTORY': 0.4, # COPY_PURCHASED
        }

    if timestamp < LIBRARY_OPENING_DATE:
        return {
            'INVENTORY': 0.3, # COPY_PURCHASED
            'PEOPLE': 0.7, # USER_REGISTERED
        }

    # ----------------------------
    # CASE 1: available + borrowed exist
    # ----------------------------
    if has_available_copies and has_unavailable_copies:
        return {
            'PEOPLE': 0.04, # LIBRARIAN_HIRED: 0.01, USER_REGISTERED: 0.03
            'INVENTORY': 0.08, # COPY_PURCHASED: 0.08
            'CIRCULATION': 0.82, # BORROW: O.5, RETURN: 0.2, RENEWAL: 0.12
            'DEMAND': 0.06, # RESERVATION: 0.06
        }

    # ----------------------------
    # CASE 2: only available copies
    # ----------------------------
    if has_available_copies and not has_unavailable_copies:
        return {
            'PEOPLE': 0.04, # LIBRARIAN_HIRED: 0.01, USER_REGISTERED: 0.03
            'INVENTORY': 0.08, # COPY_PURCHASED: 0.08
            'CIRCULATION': 0.88, # BORROW: 0.88
        }

    # ----------------------------
    # CASE 3: only borrowed copies
    # ----------------------------
    if not has_available_copies and has_unavailable_copies:
        return {
            'PEOPLE': 0.04,  # LIBRARIAN_HIRED: 0.01, USER_REGISTERED: 0.03
            'INVENTORY': 0.08,  # COPY_PURCHASED: 0.08
            'CIRCULATION': 0.70, # RETURN: 0.60, RENEWAL: 0.10
            'DEMAND': 0.18, # RESERVATION: 0.18
        }

    # ----------------------------
    # FALLBACK
    # ----------------------------
    return {
        'PEOPLE': 0.80, # LIBRARIAN_HIRED: 0.02, USER_REGISTERED: 0.78
        'INVENTORY': 0.20, # COPY_PURCHASED: 0.20
    }

def get_event_weights(
        category: str,
        has_available_copies: bool,
        has_unavailable_copies: bool,
) -> dict:
    """
    Determines the probability distribution of events inside a specific
    event category based on the current library state

    :param category: str, the selected event category whose internal event
        probabilities should be calculated
    :param has_available_copies: bool, indicates whether there are currently
        available copies that can be borrowed
    :param has_unavailable_copies: bool, indicates whether there are currently
        borrowed/unavailable copies in the system

    :return: dict, a dictionary mapping event names to their respective probability
        weights within the selected category
    """
    if category == 'PEOPLE':
        return {
            'LIBRARIAN_HIRED': 0.25,
            'USER_REGISTERED': 0.75
        }

    if category == "INVENTORY":
        return {
            "COPY_PURCHASED": 1.0,
        }

    if category == "DEMAND":
        return {
            "RESERVATION": 1.0,
        }

    # ----------------------------
    # CASE 1: available + borrowed exist
    # ----------------------------
    if has_available_copies and has_unavailable_copies:
        return {
            "BORROW": 0.61,
            "RETURN": 0.24,
            "RENEWAL": 0.15,
        }

    # ----------------------------
    # CASE 2: only available copies
    # ----------------------------
    if has_available_copies and not has_unavailable_copies:
        return {
            "BORROW": 1.0,
        }

    # ----------------------------
    # CASE 3: only borrowed copies
    # ----------------------------
    if not has_available_copies and has_unavailable_copies:
        return {
            "RETURN": 0.86,
            "RENEWAL": 0.14,
        }

    return {}

def get_event_by_timeline(
        redis_client: RedisClient,
        timestamp: datetime
) -> str:
    """
    Selects an event type based on the current simulation timeline and
    library state

    The function first determines the available event categories and their
    probabilities, selects a category, then selects a specific event within
    that category according to its probability distribution

    :param redis_client: RedisClient, the Redis client used to fetch the current
        library state, including available and unavailable copy counters
    :param timestamp: datetime.datetime, the current simulation timestamp used to
        determine the appropriate event category probabilities

    :return: str, the selected event type name
    """

    # Check if there are available or unavailable copies
    has_available_copies = redis_client.get_set_size(RedisKeys.Sets.AVAILABLE_COPIES_IDS) > 0
    has_unavailable_copies = redis_client.get_set_size(RedisKeys.Sets.UNAVAILABLE_COPIES_IDS) > 0

    # Fetch the category weights according to the timeline
    category_weights = get_category_weights_by_timeline(
        timestamp=timestamp,
        has_available_copies=has_available_copies,
        has_unavailable_copies=has_unavailable_copies,
    )

    # Choose a random event category that should be available,
    # according to the timeline
    category = np.random.choice(
        list(category_weights.keys()),
        p=list(category_weights.values()),
    )

    # Get the event weights for the current event category
    event_weights = get_event_weights(
        category=category,
        has_available_copies=has_available_copies,
        has_unavailable_copies=has_unavailable_copies,
    )

    # Choose a random event from the available, according to the timeline
    event_type = np.random.choice(
        list(event_weights.keys()),
        p=list(event_weights.values()),
    )

    return event_type

def create_event(
        event_type: str,
        timestamp: datetime,
        data: dict
) -> dict:
    """
    Creates a standardized event dictionary with a unique identifier

    :param event_type: str, the type or name of the event.
    :param timestamp: datetime, the date and time when the event occurred.
    :param data: dict, a dictionary containing the event-specific payload.

    :returns: dict, a dictionary representing the event with the following keys:
        * 'event_id': str, a universally unique identifier
        * 'event_type': str, the type of the event
        * 'timestamp': str, the event's timestamp
        * 'data': dict, additional data
    """

    # Return the event
    return {
      'event_id': str(uuid.uuid4()), # Universally Unique Identifier
      'event_type': event_type,
      'timestamp': timestamp.isoformat(),
      'data': data
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