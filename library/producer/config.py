"""
Configuration module for the simulations
"""

from datetime import datetime

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
# NUM_EDITIONS = len(EDITION_KEYS)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Chosen starting and ending date of simulations ---

START_DATE = datetime(2020, 1,1)
END_DATE = datetime.now()

# Setting up the simulated clock
CLOCK = SimClock(START_DATE)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Event weights definitions ---

INITIAL_EVENT_WEIGHTS = {
    'USER_REGISTERED': 0.35,
    'COPY_PURCHASED': 0.30,
    'BORROW': 0.15,
    'RETURN': 0.10,
    'RESERVE': 0.08,
    'LIBRARIAN_HIRED': 0.02
}

FINAL_EVENT_WEIGHTS = {
    'USER_REGISTERED': 0.03,
    'COPY_PURCHASED': 0.08,
    'BORROW': 0.52,
    'RETURN': 0.30,
    'RESERVE': 0.06,
    'LIBRARIAN_HIRED': 0.01
}
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Close cursor
cursor.close()

# Close database connection
connection.close()
# ---------------------------------------------------------------------------------------