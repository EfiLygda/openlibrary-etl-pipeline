"""
Module containing event generators related to the library inventory

Includes events such as:
* Copy purchases
"""

from faker import Faker

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient
from library.producer.producer_config import SEED

# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()

def copy_purchased(redis_client: RedisClient) -> dict:
    """
    Simulates the purchase of a copy

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the new copy's original edition key
    """

    # Choose a random edition for purchasing a copy
    edition_key = redis_client.get_random_from_set(
        RedisKeys.Sets.EDITION_KEYS
    )

    return {
        # Use edition key
        'edition_key': str(edition_key),
    }