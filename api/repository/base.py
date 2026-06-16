"""
Contains main function for retrieving records associated with a given key using a structured query
"""

import os
import psycopg2
from psycopg2.sql import SQL

from config import ROOT_DIR
from utilities.database import get_column_names

def read_query(
        router: str,
        filename: str
):
    """
    Load a SQL query from the repository SQL directory

    This function reads a `.sql` file from the structured SQL folder
    api/repository/sql/<router>/<filename>.sql and returns its raw
    SQL content as a string

    :param router: str, the domain or module name (e.g. "authors", "works", "editions")
                        used to locate the correct SQL subfolder
    :param filename: str, name of the SQL file to load

    :returns: str, the raw SQL query string read from the file
    """

    # Build absolute path to SQL file inside repository structure
    filepath = os.path.join(ROOT_DIR, 'api', 'repository', 'sql', router, filename)

    # Read SQL file
    with open(filepath, encoding='utf-8', mode='r') as f:
        sql = f.read()

    return sql

def get_with_filter_key(
        connection: psycopg2.extensions.connection,
        filter_key: str,
        query: str,
        limit: int | None = None,
        offset: int | None = None,
) -> tuple:
    """
    Retrieve all records associated with a given key using a structured query

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param filter_key: str, unique identifier of the record to retrieve
    :param query: str, the filtering query used

    :returns: A tuple containing:

        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    params = {'filter_key': filter_key}

    if limit is not None:
        params['limit'] = limit

    if offset is not None:
        params['offset'] = offset

    # Query the database
    with connection.cursor() as cursor:

        # Construct the query
        query_to_execute = SQL(query)

        # Execute the query
        cursor.execute(
            query=query_to_execute,
            vars=params
        )

        # Fetch all records as returned
        data = cursor.fetchall()

        # Fetch column names as returned
        data_column_names = get_column_names(cursor)

    return data, data_column_names