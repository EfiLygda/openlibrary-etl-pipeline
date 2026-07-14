"""
Module containing event generators related to library demand

Includes events such as:
* Reservation requests
"""

from faker import Faker

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient
from library.producer.producer_config import SEED, CLOCK

# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()

def reserve_unavailable_copy(redis_client: RedisClient) -> dict:
    """
    Simulates an unavailable copy's reservation from a user

    :param redis_client: RedisClient, the redis client used to fetch configuration values

    :return: dict, dictionary with the user_id and the copy_id
    """

    # Choose a random user, copy and librarian
    user_id = redis_client.sets.random(RedisKeys.Sets.USER_IDS)
    copy_id = redis_client.sets.random(RedisKeys.Sets.UNAVAILABLE_COPIES_IDS)

    return {
        'user_id': user_id,
        'copy_id': copy_id,
    }

def cancel_reservation(redis_client: RedisClient) -> dict:
    """
    Simulates an active reservation's cancellation

    :param redis_client: RedisClient, the redis client used to fetch configuration values

    :return: dict, dictionary with the reservation_id
    """

    # Fetch random active reservation to cancel
    reservation_id = redis_client.sets.random(RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS)

    return {
        'reservation_id': reservation_id
    }