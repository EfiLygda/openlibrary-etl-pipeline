"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from utilities.database import get_column_names

def get_work_by_key(
        connection: psycopg2.extensions.connection,
        work_key: str
) -> tuple:
    """
    Retrieves work records from `works` table in the database by work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param work_key: str, unique identifier used to filter work records

    :returns: tuple, containing query results and column names
    """

    # Query the database
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM works WHERE work_key = %s;
            """,
            (work_key,)
        )

        # Fetch all records as returned
        records = cursor.fetchall()

        # Fetch column names as returned
        column_names = get_column_names(cursor)

        return records, column_names