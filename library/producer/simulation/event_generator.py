"""
Module for generating events
"""

import os
import uuid
import numpy as np
from datetime import datetime

from config.paths import LIBRARY_ROOT

from library.service.redis.service import RedisClient

from library.producer.producer_config import (
    CLOCK,
    LIBRARIANS_HIRINGS_DEADLINE,
    LIBRARY_OPENING_DATE
)

from library.producer.simulation.scenario_generators import (
    user_registration,
    librarian_hired,
    copy_purchased,
    borrow_available_copy,
    return_,
    reservation
)


# Path for SQL commands used for generating data
sql_dir = os.path.join(LIBRARY_ROOT, 'producer', '../sql')

# Mapping event names to their respective generation functions
EVENT_GENERATION_MAPPINGS = {
    'USER_REGISTERED': user_registration,
    'LIBRARIAN_HIRED': librarian_hired,
    'COPY_PURCHASED': copy_purchased,
    'BORROW': borrow_available_copy,
    # 'RETURN': return_,
    # 'RESERVE': reservation,
}

def get_event_weights_by_timeline(
        redis_client: RedisClient,
        timestamp: datetime
) -> dict:
    """
    Builds the right weight dictionary considering the timestamps in the library timeline context

    :param redis_client: RedisClient, the redis client used to fetch counters
        and configuration values
    :param timestamp: datetime.datetime, the timestamp used

    :return: dict, dictionary with keys the proper events in the timeline and their
        respective weights in probabilities
    """

    if timestamp <= LIBRARIANS_HIRINGS_DEADLINE:
        return {
            'LIBRARIAN_HIRED': 0.6,
            'COPY_PURCHASED': 0.4,
        }

    if timestamp < LIBRARY_OPENING_DATE:
        return {
            'COPY_PURCHASED': 0.3,
            'USER_REGISTERED': 0.7
        }

    has_available_copies = len(redis_client.get_set('copies:available:ids')) > 0
    has_unavailable_copies = len(redis_client.get_set('copies:unavailable:ids')) > 0

    base = {
        "LIBRARIAN_HIRED": 0.01,
        "COPY_PURCHASED": 0.08,
        "USER_REGISTERED": 0.03,
        "BORROW": 0.0,
        "RETURN": 0.0,
        "RESERVE": 0.0,
    }

    if has_available_copies and has_unavailable_copies:
        return {
            **base,
            "BORROW": 0.52,
            "RETURN": 0.30,
            "RESERVE": 0.06,
        }

    if has_available_copies and not has_unavailable_copies:
        return {
            **base,
            "BORROW": 0.88,
        }

    if not has_available_copies and has_unavailable_copies:
        return {
            **base,
            "RETURN": 0.70,
            "RESERVE": 0.18,
        }

    # fallback (still full distribution, librarian included)
    return {
        "LIBRARIAN_HIRED": 0.02,
        "COPY_PURCHASED": 0.20,
        "USER_REGISTERED": 0.78,
        "BORROW": 0.0,
        "RETURN": 0.0,
        "RESERVE": 0.0,
    }


def generate_event(redis_client: RedisClient) -> dict:
    """
    Function that generates an event

    :param redis_client: RedisClient, the redis client used to fetch counters
        and configuration values

    :returns: dict, dictionary with:
        * 'event_id': a universally unique identifier
        * 'event_type': the type of the event
        * 'timestamp': the event's timestamp
        * 'data': additional data
    """

    # The 'current' timestamp (of course using the simulation clock)
    timestamp = CLOCK.now()

    # Fetching the proper event weights for current timestamp
    weights = get_event_weights_by_timeline(
        redis_client=redis_client,
        timestamp=timestamp
    )

    # Convert event names and weights to lists
    event_type = list(weights.keys())
    event_weights = list(weights.values())

    # Choose a random proper event using the weights
    event_type = np.random.choice(event_type, p=event_weights)

    # Generate the event's data via its event type
    data = EVENT_GENERATION_MAPPINGS[event_type](redis_client=redis_client)

    # Return the event
    return {
      'event_id': str(uuid.uuid4()), # Universally Unique Identifier
      'event_type': str(event_type),
      'timestamp': timestamp.isoformat(),
      'data': data
    }