"""
Module containing event generators related to people in the library system

Includes events such as:
* User registrations
* Librarian hirings
"""

from faker import Faker

from library.service.redis.service import RedisClient
from library.producer.producer_config import SEED
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