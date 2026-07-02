"""
Builds the simulation world once
"""

import numpy as np

from utilities import execute_query
from utilities.database import db_connection, DB_NAME
from library.producer.producer_config import *


def build_context() -> dict:
    """
    Function for building the simulation world once
    """
    # -----------------------------------------------------------
    # --- Load Editions ---
    # Establish database connection
    connection = db_connection(database=DB_NAME)

    # Fetch the edition keys
    records, _ = execute_query(
        connection=connection,
        query="SELECT edition_key FROM editions;",
    )

    # Unpack the edition keys
    edition_keys = [r[0] for r in records]

    # Calculate total editions in the database
    num_editions = len(edition_keys)

    # Close database connection
    connection.close()
    # -----------------------------------------------------------

    # -----------------------------------------------------------
    # --- Simulate Maximums ---
    max_users = np.random.randint(*MAX_USERS_RANGE)
    max_librarians = np.random.randint(*MAX_LIBRARIANS_RANGE)
    # -----------------------------------------------------------

    # -----------------------------------------------------------
    # --- Copies Counts Simulation ---
    # Simulate total copies via Poisson distribution with expected
    # number of copies 2.8 (over 2 and close to 3 copies per edition)
    poisson_lambda = 2.8
    copies_counts = np.random.poisson(lam=poisson_lambda, size=num_editions)

    # Clip number of copies over a certain number
    copies_counts = np.clip(copies_counts, COPIES_PER_EDITION_RANGE[0], COPIES_PER_EDITION_RANGE[1])

    # Dictionary with edition key and number of copies pairs
    max_copies_per_edition = {
        k: int(v)
        for k, v in zip(edition_keys, copies_counts)
    }
    # -----------------------------------------------------------

    return {
        'edition_keys': edition_keys,
        'max_copies_per_edition': max_copies_per_edition,
        'max_users': max_users,
        'max_librarians': max_librarians,
    }
