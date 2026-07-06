"""
Module containing event generators related to library demand

Includes events such as:
* Reservation requests
"""

from faker import Faker

from library.service.redis.keys import RedisKeys
from library.service.redis.service import RedisClient
from library.producer.producer_config import SEED, CLOCK

# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()

def reservation(
        redis_client: RedisClient,
        user_id: int,
        copy_id: str
) -> dict:
    """
    Simulates a copy's reservation from a user

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param user_id: str, the user's id that reserved the copy
    :param copy_id: str, the copy's id that was reserved

    :return: dict, dictionary with the user_id and the copy_id
    """

    return {
        'user_id': user_id,
        'copy_id': copy_id,
    }