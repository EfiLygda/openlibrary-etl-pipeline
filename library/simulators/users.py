"""
Users simulation module
"""

import os
import numpy as np
import pandas as pd
from faker import Faker

from config.paths import LIBRARY_RAW, LIBRARY_TABLES
from utilities.io.json_io import save_json

from library.simulators.sim_config import SEED, MAX_USERS
from utils.emails import generate_email

# ---------------------------------------------------------------------------------------
Faker.seed(SEED)
fake = Faker()
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Users ---

# Setting up list of users
users = []

for _ in range(MAX_USERS):

    # Simulate first and last name
    first_name, last_name = fake.first_name(), fake.last_name()

    # Simulate user record
    user = {
        # Use generated first and last name
        'first_name': first_name,
        'last_name': last_name,

        # Use generated first and last name for email generation
        'email': generate_email(first_name, last_name),

        # Generate passwords with max 10 characters
        'password': fake.password(length=10),

        # Generate registration timestamp from before 3 years to now
        # using ISO-8601 format (i.e. "2026-06-29T14:32:10")
        'timestamp': fake.date_time_between(start_date='-3y', end_date='now').isoformat(),

        # Generate whether the user is an active user or not
        # so that more users will be active by 3:1 proportion
        'is_active': bool(np.random.choice([True, True, True, False]))
    }

    # Add user records to final list of users
    users.append(user)

# Order users by timestamp
users_ordered = sorted(users, key=lambda u: u['timestamp'])

# Export raw records to json
users_filename_json = 'users.json'
users_filepath_json = os.path.join(LIBRARY_RAW, users_filename_json)
save_json(users_ordered, users_filepath_json)

# Export records to csv
users_df = pd.DataFrame(users_ordered)

users_filename_csv = 'users.csv'
users_filepath_csv = os.path.join(LIBRARY_TABLES, users_filename_csv)
users_df.to_csv(users_filepath_csv, index=False)
# ---------------------------------------------------------------------------------------
