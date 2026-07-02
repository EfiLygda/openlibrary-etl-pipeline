"""
Module for generating events
"""

import os
import uuid
import numpy as np
from datetime import datetime

import psycopg2

from config.paths import LIBRARY_ROOT
from utilities.database import execute_query

from library.producer.producer_config import (
    CLOCK,
    LIBRARIANS_HIRINGS_DEADLINE,
    INITIAL_COPIES_PURCHASING_DEADLINE,
    LIBRARY_OPENING_DATE
)

from library.producer.scenario_generators import (
    user_registration,
    librarian_hired,
    copy_purchased,
    borrow,
    return_,
    reservation
)

# Path for SQL commands used for generating data
sql_dir = os.path.join(LIBRARY_ROOT, 'producer', 'sql')

# Mapping event names to their respective generation functions
EVENT_GENERATION_MAPPINGS = {
    'USER_REGISTERED': user_registration,
    'LIBRARIAN_HIRED': librarian_hired,
    'COPY_PURCHASED': copy_purchased,
    'BORROW': borrow,
    'RETURN': return_,
    'RESERVE': reservation,
}

def get_event_weights_by_timeline(timestamp: datetime) -> dict:
    """
    Builds the right weight dictionary considering the timestamps in the library timeline context

    :param timestamp: datetime.datetime, the timestamp used

    :return: dict, dictionary with keys the proper events in the timeline and their
        respective weights in probabilities
    """

    if timestamp <= LIBRARIANS_HIRINGS_DEADLINE:
        return {
            'LIBRARIAN_HIRED': 0.6,
            'COPY_PURCHASED': 0.4,
        }
    elif LIBRARIANS_HIRINGS_DEADLINE < timestamp <= INITIAL_COPIES_PURCHASING_DEADLINE:
        return {
            'COPY_PURCHASED': 1
        }
    elif INITIAL_COPIES_PURCHASING_DEADLINE <= timestamp < LIBRARY_OPENING_DATE:
        return {
            'COPY_PURCHASED': 0.2,
            'USER_REGISTERED': 0.8
        }
    elif timestamp >= LIBRARY_OPENING_DATE:
        return {
            'USER_REGISTERED': 0.03,
            'COPY_PURCHASED': 0.08,
            'BORROW': 0.52,
            'RETURN': 0.30,
            'RESERVE': 0.06,
            'LIBRARIAN_HIRED': 0.01
        }
    else:
        raise ValueError('No event is set up for this date')

def generate_event(
        connection: psycopg2.extensions.connection
) -> dict:
    """
    Function that generates an event

    :param connection: psycopg2.extensions.connection, the connection used for fetching data
        from the database

    :returns: dict, dictionary with:
        * 'event_id': a universally unique identifier
        * 'event_type': the type of the event
        * 'timestamp': the event's timestamp
        * 'data': additional data
    """

    # The 'current' timestamp (of course using the simulation clock)
    timestamp = CLOCK.now()

    # Fetching the proper event weights for current timestamp
    weights = get_event_weights_by_timeline(timestamp)

    # Convert event names and weights to lists
    event_type = list(weights.keys())
    event_weights = list(weights.values())

    # Choose a random proper event using the weights
    event_type = np.random.choice(event_type, p=event_weights)

    # If the event type is 'USER_REGISTERED', 'LIBRARIAN_HIRED', 'COPY_PURCHASED'
    # no additional data is needed and their respective generating functions are called
    if event_type in ['USER_REGISTERED', 'LIBRARIAN_HIRED', 'COPY_PURCHASED']:
        data = EVENT_GENERATION_MAPPINGS[event_type]()

    # If the event type is 'BORROW' then additional data are needed and
    # randomly fetched from the database
    elif event_type == 'BORROW':

        # Fetch random user from the database
        user_data, _ = execute_query(
            connection=connection,
            query_filepath=os.path.join(sql_dir, 'random_user_id.sql')
        )

        # Fetch random copy from the database
        copy_data, _ = execute_query(
            connection=connection,
            query_filepath=os.path.join(sql_dir, 'random_copy_id.sql')
        )

        # If a user's data and a copy's data were available then generate
        # the events data
        if user_data and copy_data:

            data = borrow(
                user_id=user_data[0][0],
                copy_id=copy_data[0][0],
            )

        # Else return null data
        else:
            data = None

    # Placeholder
    else:
        data = None

    # Return the event
    return {
      'event_id': str(uuid.uuid4()), # Universally Unique Identifier
      'event_type': str(event_type),
      'timestamp': timestamp.isoformat(),
      'data': data
    }