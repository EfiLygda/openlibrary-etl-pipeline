"""
Module containing all simulated events
"""

from faker import Faker
from datetime import timedelta

from library.service.redis.service import RedisClient
from library.producer.producer_config import SEED, CLOCK
from library.producer.utils.emails import generate_email

# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()

def user_registration(redis_client: RedisClient) -> dict:
    """
    Simulates a new users registration

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the new user's first and last name and his/hers email
    """

    # Simulate first and last name
    first_name, last_name = fake.first_name(), fake.last_name()

    return {
        # Use generated first and last name
        'first_name': first_name,
        'last_name': last_name,

        # Use generated first and last name for email generation
        'email': generate_email(first_name, last_name),
    }

def librarian_hired(redis_client: RedisClient) -> dict:
    """
    Simulates a librarians hiring

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the new librarian's first and last name and his/hers email
    """

    # Simulate first and last name
    first_name, last_name = fake.first_name(), fake.last_name()

    return {
        # Use generated first and last name
        'first_name': first_name,
        'last_name': last_name,

        # Use generated first and last name for email generation
        'email': generate_email(first_name, last_name),
    }

def copy_purchased(redis_client: RedisClient) -> dict:
    """
    Simulates the purchase of a copy

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the new copy's original edition key
    """

    # Choose a random edition for purchasing a copy
    edition_key = redis_client.get_random_from_set('editions:keys')

    return {
        # Use edition key
        'edition_key': str(edition_key),
    }

def borrow_available_copy(redis_client: RedisClient) -> dict:
    """
    Simulates an available copy's borrowing from a user

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :return: dict, dictionary with the user_id, the copy_id, and the due date for returning the copy
    """

    # Choose a random user and copy
    user_id = redis_client.get_random_from_set('users:ids')
    copy_id = redis_client.get_random_from_set('copies:available:ids')
    librarian_id = redis_client.get_random_from_set('librarians:ids')

    return {
        'user_id': user_id,
        'copy_id': copy_id,
        'librarian_id': librarian_id,
        'due_date': (CLOCK.now() + timedelta(days=7)).isoformat()
    }

def return_(
        redis_client: RedisClient,
        loan_id: int,
        user_id: int,
        copy_id: str
) -> dict:
    """
    Simulates a copy's return from a user

    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param loan_id: str, the borrowing id that was returned
    :param user_id: str, the user's id that borrowed the copy
    :param copy_id: str, the copy's id that was borrowed

    :return: dict, dictionary with the loan_id, user_id and the copy_id
    """

    return {
        'loan_id': loan_id,
        'user_id': user_id,
        'copy_id': copy_id,
    }

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
