"""

"""

import os

import psycopg2

from config.paths import LIBRARY_ROOT
from utilities import execute_query

# Path for SQL commands used for generating data
SQL_DIR = os.path.join(LIBRARY_ROOT, 'consumer', 'sql')

def librarian_hired(
        connection: psycopg2.extensions.connection ,
        event: dict
) -> tuple:
    """

    """

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_librarian.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )

