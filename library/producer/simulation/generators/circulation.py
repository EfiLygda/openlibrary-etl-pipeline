"""
Module containing event generators related to library circulation.

Includes events such as:
* Borrowing copies
* Returning copies
* Renewing loans
"""

from faker import Faker
from datetime import timedelta

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient
from library.producer.producer_config import SEED, CLOCK

# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()

def borrow_available_copy(
        redis_client: RedisClient,
        user_id: str | None = None,
        copy_id: str | None = None,

) -> dict:
    """
    Simulates an available copy's borrowing from a user

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param user_id: str | None, the user id for generating the event, if given
    :param copy_id: str | None, the copy id for generating the event, if given

    :return: dict, dictionary with the user_id, the copy_id, and the due date for returning the copy
    """

    # Choose a random user, copy when not given
    if user_id is None:
        user_id = str(redis_client.get_random_from_set(RedisKeys.Sets.USER_IDS))

    if copy_id is None:
        copy_id = str(redis_client.get_random_from_set(RedisKeys.Sets.AVAILABLE_COPIES_IDS))

    # Choose random librarian
    librarian_id = redis_client.get_random_from_set(RedisKeys.Sets.LIBRARIAN_IDS)

    return {
        'user_id': user_id,
        'copy_id': copy_id,
        'librarian_id': librarian_id,
        'due_date': (CLOCK.now() + timedelta(days=7)).isoformat()
    }

def return_copy(redis_client: RedisClient) -> dict:
    """
    Simulates a copy's return from a user

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the loan_id, user_id and the copy_id
    """

    # Choose a random active loan
    loan_id = redis_client.get_random_from_set(RedisKeys.Sets.ACTIVE_LOANS_IDS)

    return {
        'loan_id': loan_id,
    }

def renew_loan(redis_client: RedisClient):
    """
    Simulates the renewal of a loaned copy from the same user

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the loan_id, user_id and the copy_id
    """

    # Choose a random active loan
    loan_id = redis_client.get_random_from_set(RedisKeys.Sets.ACTIVE_LOANS_IDS)

    return {
        'loan_id': loan_id,
    }