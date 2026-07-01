"""
Configuration module for the simulations
"""

import numpy as np
from datetime import datetime, timedelta

from utilities.database import db_connection, DB_NAME
from library.producer.utils.clock import SimClock

# ---------------------------------------------------------------------------------------
# --- Chosen seed for reproducible results ---
SEED = 0
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Set up Connection to Database ---

# Establish connection
connection = db_connection(database=DB_NAME)

# Set up cursor
cursor = connection.cursor()
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Extract edition keys from the database ---

# Execute SQL query
cursor.execute("SELECT edition_key FROM editions;")

# Fetch and unpack the edition keys
EDITION_KEYS = [records[0] for records in cursor.fetchall()]

# Calculate total edition keys
NUM_EDITIONS = len(EDITION_KEYS)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Simulated clock with speed ---

# Starting and ending date of the clock
START_DATE = datetime(2020, 1,1)
END_DATE = datetime.now()

# Setting up the simulated clock
CLOCK = SimClock(start=START_DATE, end=END_DATE)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Library Timeline ---

# | Period                  | Events               | Notes                                                      |
# | ----------------------- | -------------------- | ---------------------------------------------------------- |
# | First 15 days           | Hire librarians      | 3–9 librarians depending on library size.                  |
# | First 30 days           | Purchase book copies | Hundreds or thousands of copies purchased from publishers. |
# | After 30 days           | Register users       | Members gradually join every day.                          |
# | After 31 days           | Library opens        | Borrowing, reservations and returns begin.                 |
# | Throughout 2020         | More purchases       | New books arrive monthly.                                  |
# | Throughout 2020         | New users            | Membership continues growing.                              |
# | Throughout 2020         | Librarian hiring     | Occasionally hire another librarian if needed.             |

# --- First 15 days of hiring of librarians ---
# Total maximum number of hired librarians in [3,10)
MAX_INITIAL_LIBRARIANS = np.random.randint(3,10)

# End date for hiring librarians
LIBRARIANS_HIRINGS_DEADLINE = START_DATE + timedelta(days=15)

# --- First month of purchasing copies of editions ---
# Setting up maximum number of copies
MIN_NUM_COPIES = 0
MAX_NUM_COPIES = 5

# Simulate total copies via Poisson distribution with expected
# number of copies 2.8 (over 2 and close to 3 copies per edition)
POISSON_LAMBDA = 2.8
copies_counts = np.random.poisson(lam=POISSON_LAMBDA, size=NUM_EDITIONS)

# Clip number of copies over MAX_NUM_COPIES
copies_counts = np.clip(copies_counts, MIN_NUM_COPIES, MAX_NUM_COPIES)

# Dictionary with edition key and number of copies pairs
COPIES = {
    edition_key: int(count)
    for edition_key, count in zip(EDITION_KEYS, copies_counts)
}

# End date for purchasing initial copy catalogue
INITIAL_COPIES_PURCHASING_DEADLINE = START_DATE + timedelta(days=30)

# --- Second month -> registering users ---
START_USER_REGISTRATIONS_DATE = START_DATE + timedelta(days=30)

# --- Library Opening -> borrowing, reservations start ---
LIBRARY_OPENING_DATE = START_DATE + timedelta(days=31)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Close cursor
cursor.close()

# Close database connection
connection.close()
# ---------------------------------------------------------------------------------------