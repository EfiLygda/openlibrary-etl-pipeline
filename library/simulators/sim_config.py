"""
Configuration module for the simulations
"""

import numpy as np
from utilities.database import db_connection, DB_NAME

# --- Seed ---
SEED = 0

# --- Seeding numpy ---
np.random.seed(SEED)

# ---------------------------------------------------------------------------------------
# --- Set up Connection to Database ---

# Establish connection
connection = db_connection(database=DB_NAME)

# Set up cursor
cursor = connection.cursor()
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Extract work and edition keys from the database ---

# WORKS
# Execute SQL query
cursor.execute("SELECT work_key FROM works;")

# Fetch and unpack the work keys
WORK_KEYS = [records[0] for records in cursor.fetchall()]

# Calculate total work keys
NUM_WORKS = len(WORK_KEYS)

# EDITIONS
# Execute SQL query
cursor.execute("SELECT edition_key FROM editions;")

# Fetch and unpack the edition keys
EDITION_KEYS = [records[0] for records in cursor.fetchall()]

# Calculate total edition keys
NUM_EDITIONS = len(EDITION_KEYS)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Simulate total copies in the library ---

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
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Simulate number of users and librarians ---

# 500 <= USERS < 1000
MAX_USERS = np.random.randint(500, 1000)

# 2 <= LIBRARIANS < 15
MAX_LIBRARIANS = np.random.randint(2, 15)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Close cursor
cursor.close()

# Close database connection
connection.close()
# ---------------------------------------------------------------------------------------
