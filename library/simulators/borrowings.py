"""
Borrowings simulation module

The resulting data simulate a live system snapshot of a library database

Borrowing rules:
1. Borrowing lasts 7 days
2. Maximum 1 renewal can be selected adding additional 7 days (maximum of 14 days for borrowing)
3. A copy will be marked as overdue if the difference between the borrowing day and
   the return day is more than 7 or 14 days depending on if renewal was selected
4. If more than 90 days pass after the book is overdue then it is marked as lost

Note: This module does not simulate the dates and then mark the copies status, but
      uses the results in the copies.csv and builds the historical records.

      This means that a book is already marked as BORROWED and then the script decides
      if its last borrowing should be marked as ACTIVE (not overdue) or OVERDUE.

      The same goes for a lost copy, if it marked as LOST, then the script produces
      proper dates for it to be correctly marked as LOST in the historical borrowing
      records
"""
import datetime
import os
from datetime import timedelta, datetime
from random import random, randint, seed

import numpy as np
import pandas as pd
from faker import Faker

from config.paths import LIBRARY_RAW, LIBRARY_TABLES
from utilities.io.csv_io import read_csv
from utilities.io.json_io import save_json
from utilities.logging import set_logger

from library.simulators.config import SEED, MAX_BORROWINGS_PER_EDITION, START_DT, END_DT

# ---------------------------------------------------------------------------------------
# Seeding for reproducible data
seed(SEED)
np.random.seed(SEED)
Faker.seed(SEED)

# Faker object for simulation
fake = Faker()
# ---------------------------------------------------------------------------------------

logger = set_logger('SIMULATE_BORROWINGS')

def run():

    logger.info('STAGE_START')

    # ---------------------------------------------------------------------------------------
    # --- Borrowings ---

    # Load users, librarians and copies data
    users = read_csv(os.path.join(LIBRARY_TABLES, 'users.csv'))
    librarians = read_csv(os.path.join(LIBRARY_TABLES, 'librarians.csv'))
    copies = read_csv(os.path.join(LIBRARY_TABLES, 'copies.csv'))

    # List to use for choosing users and librarians randomly
    user_ids = users.user_id.values
    librarian_ids = librarians.librarian_id.values

    # Setting up list of borrowings
    borrowings = []

    # For each copy simulate lending history
    for k, current_copy in copies.iterrows():

        # Keep current copy's borrowings in a list
        current_copy_borrowings = []

        # Simulate the current copy's number of lendings
        current_copy_n_borrowings = int(np.random.randint(0, MAX_BORROWINGS_PER_EDITION))

        # If no borrowings will be simulated for current copy then move to the next one
        if current_copy_n_borrowings == 0:
            continue

        # For each lending build the borrowing record
        for i in range(1, current_copy_n_borrowings+1):

            # Choose random user
            borrowing_user = users.sample(1).squeeze()

            # Extract user id
            user_id = borrowing_user.user_id

            # Use the user's registration date as the start of the simulated borrow dat
            user_registration_timestamp = datetime.fromisoformat(borrowing_user.timestamp)

            # Simulate borrow data for current lending
            borrow_date = fake.date_time_between(start_date=user_registration_timestamp, end_date=END_DT)

            # Simulate whether an extension will be made
            renewal = random() < 0.30

            # Build due date for returning the copy
            # If an extension was made add 14 days to original borrow date
            # else the original 7 days for borrowing a copy
            due_date = borrow_date + timedelta(days=14 if renewal else 7)

            # Build user's return date for the copy
            # If an extension was made then add random days between [7, 14]
            # else between [1, 7]
            days_after_borrow = randint(7 if renewal else 1, 14 if renewal else 7)
            return_date = borrow_date + timedelta(days=days_after_borrow)

            # Build the borrowing record
            borrowing = {
                'loan_id': None,
                'user_id': user_id, # np.random.choice(user_ids), # user_id,
                'copy_id': current_copy.copy_id,
                'borrow_date': borrow_date.isoformat(),
                'due_date': due_date.isoformat(),
                'return_date': return_date.isoformat(),
                'status': 'RETURNED',
                'renewal_count': 1 if renewal else 0,
                'processed_by': np.random.choice(librarian_ids)
            }

            # Add current borrowing to the current copy's borrowing record
            current_copy_borrowings.append(borrowing)

        # Sort by borrowing date the records for the current copy
        current_copy_borrowings_ordered = sorted(current_copy_borrowings, key=lambda u: u['borrow_date'])

        # --- Corrections for special cases (BORROWED and LOST) ---
        # If the current copy was simulated at the previous stage (copies.csv) as 'BORROWED'
        # then its last record will statue as 'ACTIVE' and no return date
        if current_copy.status == 'BORROWED':

            # Find last borrowing record
            last_borrowing_record = current_copy_borrowings_ordered[-1]

            # Calculate maximum days for return, taking into consideration the
            # already simulated renewal count (7 for no renewal, 14 with renewal)
            max_days_for_return = 14 if last_borrowing_record['renewal_count'] == 1 else 7

            # Convert due date to datetime object with the right format
            due_date = datetime.fromisoformat(last_borrowing_record['due_date'])

            # Check if the borrowed copy is overdue
            # If it then mark it so, else mark it as active
            if (datetime.today() - due_date).days >  max_days_for_return:
                last_borrowing_record['status'] = 'OVERDUE'
            else:
                last_borrowing_record['status'] = 'ACTIVE'

            # In any case no return date should be used
            last_borrowing_record['return_date'] = None

        # If the current copy was simulated at the previous stage (copies.csv) as 'LOST'
        # then its last record will statue as 'LOST' and no return date
        if current_copy.status == 'LOST':

            # Find last borrowing record
            last_borrowing_record = current_copy_borrowings_ordered[-1]

            # NOTE: for LOST copies it is imperative that the last record's dates should
            #       be simulated from the start as to preserve LOST status from the last
            #       possible date from today

            # In case the copy was marked as lost, then 90 days were passed after it
            # was first overdue, and then we add 14 day more to catch possible renewal
            borrow_date = fake.date_time_between(start_date=user_registration_timestamp, end_date='-104d')

            # Simulate whether an extension will be made
            renewal = random() < 0.30

            # Build due date for returning the copy
            # If an extension was made add 14 days to original borrow date
            # else the original 7 days for borrowing a copy
            due_date = borrow_date + timedelta(days=14 if renewal else 7)

            # Build user's return date for the copy
            # If an extension was made then add random days between [7, 14]
            # else between [1, 7]
            days_after_borrow = randint(7 if renewal else 1, 14 if renewal else 7)
            return_date = borrow_date + timedelta(days=days_after_borrow)

            # Update fields of interest
            last_borrowing_record['borrow_date'] = borrow_date.isoformat()
            last_borrowing_record['due_date'] = due_date.isoformat()
            last_borrowing_record['return_date'] = return_date.isoformat()
            last_borrowing_record['status'] = 'LOST'
            last_borrowing_record['return_date'] = None

        # Add the current copy's borrowing records to the final list
        borrowings += current_copy_borrowings_ordered

    # Order borrowings by timestamp
    borrowings_ordered = sorted(borrowings, key=lambda u: u['borrow_date'])

    # Update user id
    for i, borrowing in enumerate(borrowings_ordered):
        borrowing['loan_id'] = f'BR-{i + 1}'

    # Export raw records to json
    borrowings_filename_json = 'borrowings.json'
    borrowings_filepath_json = os.path.join(LIBRARY_RAW, borrowings_filename_json)
    save_json(borrowings_ordered, borrowings_filepath_json)

    # Export records to csv
    borrowings_df = pd.DataFrame(borrowings_ordered)

    borrowings_filename_csv = 'borrowings.csv'
    borrowings_filepath_csv = os.path.join(LIBRARY_TABLES, borrowings_filename_csv)
    borrowings_df.to_csv(borrowings_filepath_csv, index=False)
    # ---------------------------------------------------------------------------------------

    logger.info('STAGE_COMPLETE')
