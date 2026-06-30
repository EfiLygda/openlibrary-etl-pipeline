"""
Edition copies simulation module
"""

import os
import numpy as np
import pandas as pd
from faker import Faker

from config.paths import LIBRARY_RAW, LIBRARY_TABLES
from utilities.io.json_io import save_json
from utilities.logging import set_logger

from library.simulators.config import SEED, COPIES, START_DT, END_DT

# ---------------------------------------------------------------------------------------
# Seeding numpy random for reproducible data
np.random.seed(SEED)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Seeding faker for reproducible data
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()
# ---------------------------------------------------------------------------------------

logger = set_logger('SIMULATE_COPIES')

def run():

    logger.info('STAGE_START')

    # ---------------------------------------------------------------------------------------
    # --- copies ---

    # Setting up list of copies
    copies = []

    # For each edition the previously simulated number of copies is used
    for edition_key, n_copies in COPIES.items():

        # Current edition's copied
        edition_copies = []

        # For each copy a record is simulated
        for i in range(1, n_copies+1):

            copy = {

                # Copy id is kept null as it will be updated later
                'copy_id': None,

                # Use edition key
                'edition_key': edition_key,

                # Generate copy status as 'AVAILABLE', 'BORROWED', 'LOST', 'DAMAGED'
                # with respective probabilities of choice
                'status': np.random.choice(
                    ['AVAILABLE', 'BORROWED', 'LOST', 'DAMAGED'],
                    p=[0.7, 0.2, 0.05, 0.05]
                ),

                # Accusation of copy timestamp
                'timestamp': fake.date_time_between(start_date=START_DT, end_date=END_DT).isoformat()
            }

            # Add copy record to final list of current edition's copies
            edition_copies.append(copy)

        # Copy current edition's keys by timestamp
        edition_copies_ordered = sorted(edition_copies, key=lambda u: u['timestamp'])

        # Add copy ids to ordered editions
        for i, copy in enumerate(edition_copies_ordered):
            # Generate copy id (i.e. {edition_key}-00{copy_number} -> OL26338367M-001)
            copy['copy_id'] = f'{edition_key}-C{i+1}'

        # Add copies to final list
        copies += edition_copies_ordered

    # Order copies by timestamp
    copies_ordered = sorted(copies, key=lambda u: u['timestamp'])

    # Export raw records to json
    copies_filename_json = 'copies.json'
    copies_filepath_json = os.path.join(LIBRARY_RAW, copies_filename_json)
    save_json(copies_ordered, copies_filepath_json)

    # Export records to csv
    copies_df = pd.DataFrame(copies_ordered)

    copies_filename_csv = 'copies.csv'
    copies_filepath_csv = os.path.join(LIBRARY_TABLES, copies_filename_csv)
    copies_df.to_csv(copies_filepath_csv, index=False)
    # ---------------------------------------------------------------------------------------

    logger.info('STAGE_COMPLETE')
