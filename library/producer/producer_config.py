"""
Producer configuration for the simulation
"""

from datetime import datetime, timedelta

from library.producer.utils.clock import SimClock

# ---------------------------------------------------------------------------------------
# --- Chosen seed for reproducible results ---
SEED = 0
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
# | First 15 days           | Hire librarians      | Hire librarians depending on library size.                 |
# | First 30 days           | Purchase book copies | Hundreds or thousands of copies purchased from publishers. |
# | After 31 days           | Register users       | Members gradually join every day.                          |
# | After 31 days           | Library opens        | Borrowing, reservations and returns begin.                 |
# | Throughout 2020         | More purchases       | New books arrive monthly.                                  |
# | Throughout 2020         | New users            | Membership continues growing.                              |
# | Throughout 2020         | Librarian hiring     | Occasionally hire another librarian if needed.             |

# End date for hiring librarians
LIBRARIANS_HIRINGS_DEADLINE = START_DATE + timedelta(days=15)

# Library Opening -> user registration, borrowing, reservations start
LIBRARY_OPENING_DATE = START_DATE + timedelta(days=31)
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Setting up ranges ---

MAX_USERS_RANGE = (500, 1000)
MAX_LIBRARIANS_RANGE = (2, 15)
COPIES_PER_EDITION_RANGE = (0,5)
# ---------------------------------------------------------------------------------------
