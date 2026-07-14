"""
Module responsible for selecting simulation events
"""

import numpy as np
from datetime import datetime

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient

from library.core.events import EventType, EventCategory

from library.producer.producer_config import (
    LIBRARIANS_HIRINGS_DEADLINE,
    LIBRARY_OPENING_DATE
)

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
            EventCategory.PEOPLE: 0.60, # LIBRARIAN_HIRED
            EventCategory.INVENTORY: 0.40, # COPY_PURCHASED
        }

    if timestamp < LIBRARY_OPENING_DATE:
        return {
            EventCategory.PEOPLE: 0.30,  # USER_REGISTERED
            EventCategory.INVENTORY: 0.70, # COPY_PURCHASED
        }

    # ----------------------------
    # CASE 1: available + borrowed exist
    # ----------------------------
    if has_available_copies and has_unavailable_copies:
        return {
            EventCategory.PEOPLE: 0.04, # LIBRARIAN_HIRED, USER_REGISTERED
            EventCategory.INVENTORY: 0.30, # COPY_PURCHASED
            EventCategory.CIRCULATION: 0.60, # BORROW, RETURN, RENEWAL
            EventCategory.DEMAND: 0.06, # RESERVATION
        }

    # ----------------------------
    # CASE 2: only available copies
    # ----------------------------
    if has_available_copies and not has_unavailable_copies:
        return {
            EventCategory.PEOPLE: 0.04, # LIBRARIAN_HIRED, USER_REGISTERED
            EventCategory.INVENTORY: 0.30, # COPY_PURCHASED
            EventCategory.CIRCULATION: 0.66, # BORROW
        }

    # ----------------------------
    # CASE 3: only borrowed copies
    # ----------------------------
    if not has_available_copies and has_unavailable_copies:
        return {
            EventCategory.PEOPLE: 0.04,  # LIBRARIAN_HIRED, USER_REGISTERED
            EventCategory.INVENTORY: 0.30,  # COPY_PURCHASED
            EventCategory.CIRCULATION: 0.48, # RETURN, RENEWAL
            EventCategory.DEMAND: 0.18, # RESERVATION
        }

    # ----------------------------
    # FALLBACK
    # ----------------------------
    return {
        EventCategory.PEOPLE: 0.30, # LIBRARIAN_HIRED, USER_REGISTERED
        EventCategory.INVENTORY: 0.70, # COPY_PURCHASED
    }

def get_event_weights(
        category: EventCategory,
        timestamp: datetime,
        has_available_copies: bool,
        has_unavailable_copies: bool,
        has_active_reservations: bool,
) -> dict:
    """
    Determines the probability distribution of events inside a specific
    event category based on the current library state

    :param category: str, the selected event category whose internal event
        probabilities should be calculated
    :param timestamp: datetime.datetime, the current simulation timestamp used to determine
        the current phase of the library lifecycle
    :param has_available_copies: bool, indicates whether there are currently
        available copies that can be borrowed
    :param has_unavailable_copies: bool, indicates whether there are currently
        borrowed/unavailable copies in the system
    :param has_active_reservations: bool, indicates whether there are currently
        active reservations in the system

    :return: dict, a dictionary mapping event names to their respective probability
        weights within the selected category
    """
    if category == EventCategory.PEOPLE:
        if timestamp <= LIBRARIANS_HIRINGS_DEADLINE:
            return {
                EventType.LIBRARIAN_HIRED: 1.0,
            }

        if timestamp < LIBRARY_OPENING_DATE:
            return {
                EventType.USER_REGISTERED: 1.0,
            }

        return {
            EventType.LIBRARIAN_HIRED: 0.10,
            EventType.USER_REGISTERED: 0.90,
        }

    if category == EventCategory.INVENTORY:
        return {
            EventType.COPY_PURCHASED: 1.0,
        }

    if category == EventCategory.DEMAND:
        # ----------------------------
        # CASE 1: active reservations
        # ----------------------------
        if has_active_reservations:
            return {
                EventType.RESERVATION_CREATED: 0.80,
                EventType.RESERVATION_CANCELLED: 0.20
            }

        # ----------------------------
        # CASE 2: no active reservations
        # ----------------------------
        else:
            return {
                EventType.RESERVATION_CREATED: 1.0,
            }

    if category == EventCategory.CIRCULATION:
        # ----------------------------
        # CASE 1: available + borrowed exist
        # ----------------------------
        if has_available_copies and has_unavailable_copies:
            return {
                EventType.COPY_BORROWED: 0.61,
                EventType.COPY_RETURNED: 0.24,
                EventType.LOAN_RENEWED: 0.15,
            }

        # ----------------------------
        # CASE 2: only available copies
        # ----------------------------
        if has_available_copies and not has_unavailable_copies:
            return {
                EventType.COPY_BORROWED: 1.0,
            }

        # ----------------------------
        # CASE 3: only borrowed copies
        # ----------------------------
        if not has_available_copies and has_unavailable_copies:
            return {
                EventType.COPY_RETURNED: 0.86,
                EventType.LOAN_RENEWED: 0.14,
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
    has_available_copies = redis_client.sets.get_set_size(RedisKeys.Sets.AVAILABLE_COPIES_IDS) > 0
    has_unavailable_copies = redis_client.sets.get_set_size(RedisKeys.Sets.UNAVAILABLE_COPIES_IDS) > 0

    # Check if there are active reservations
    has_active_reservations = redis_client.sets.get_set_size(RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS) > 0

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
        timestamp=timestamp,
        has_available_copies=has_available_copies,
        has_unavailable_copies=has_unavailable_copies,
        has_active_reservations=has_active_reservations,
    )

    # Choose a random event from the available, according to the timeline
    event_type = np.random.choice(
        list(event_weights.keys()),
        p=list(event_weights.values()),
    )

    return event_type