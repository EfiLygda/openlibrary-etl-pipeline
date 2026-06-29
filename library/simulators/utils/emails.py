"""
Module for generating random emails
"""

import random
from library.simulators.sim_config import SEED

# Seeding random functions for reproducible results
random.seed(SEED)

# Email domain names to be used at random
DOMAINS = [
    'gmail.com',
    'yahoo.com',
    'outlook.com',
    'hotmail.com',
    'icloud.com',
    'protonmail.com',
    'mail.com'
]

def generate_email(first, last):
    """
    Function for generating emails by basing them to a full name

    :param first: str, the first name
    :param last: str, the last name

    :return: str, the email based on the full name
    """

    # Different email patterns
    patterns = [
        lambda f, l: f'{f.lower()}.{l.lower()}',
        lambda f, l: f'{f[0].lower()}{l.lower()}',
        lambda f, l: f'{f.lower()}{random.randint(1, 999)}',
        lambda f, l: f'{f.lower()}.{l[0].lower()}',
    ]

    # Choosing a random email pattern and passing the first and last name
    local_part = random.choice(patterns)(first, last)

    # Choosing a random domain
    domain = random.choice(DOMAINS)

    return f'{local_part}@{domain}'
