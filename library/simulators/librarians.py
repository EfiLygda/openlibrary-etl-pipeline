"""
Librarians simulation module
"""

import os
import pandas as pd
from faker import Faker

from config.paths import LIBRARY_RAW, LIBRARY_TABLES
from utilities.io.json_io import save_json
from utilities.logging import set_logger

from library.simulators.sim_config import SEED, MAX_LIBRARIANS
from library.simulators.utils.emails import generate_email

# ---------------------------------------------------------------------------------------
# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()
# ---------------------------------------------------------------------------------------

logger = set_logger('SIMULATE_LIBRARIANS')

def run():

    logger.info('STAGE_START')

    # ---------------------------------------------------------------------------------------
    # --- Librarians ---

    # Setting up list of librarians
    librarians = []

    for _ in range(MAX_LIBRARIANS):

        # Simulate first and last name
        first_name, last_name = fake.first_name(), fake.last_name()

        # Simulate librarian record
        librarian = {

            # Use generated first and last name
            'first_name': first_name,
            'last_name': last_name,

            # Use generated first and last name for email generation
            'email': generate_email(first_name, last_name),

            # Generate registration timestamp from before 3 years to now
            # using ISO-8601 format (i.e. "2026-06-29T14:32:10")
            'timestamp': fake.date_time_between(start_date='-3y', end_date='now').isoformat(),
        }

        # Add librarian records to final list of librarians
        librarians.append(librarian)

    # Order librarians by timestamp
    librarians_ordered = sorted(librarians, key=lambda u: u['timestamp'])

    # Export raw records to json
    librarians_filename_json = 'librarians.json'
    librarians_filepath_json = os.path.join(LIBRARY_RAW, librarians_filename_json)
    save_json(librarians_ordered, librarians_filepath_json)

    # Export records to csv
    librarians_df = pd.DataFrame(librarians_ordered)

    librarians_filename_csv = 'librarians.csv'
    librarians_filepath_csv = os.path.join(LIBRARY_TABLES, librarians_filename_csv)
    librarians_df.to_csv(librarians_filepath_csv, index=False)
    # ---------------------------------------------------------------------------------------

    logger.info('STAGE_COMPLETE')
