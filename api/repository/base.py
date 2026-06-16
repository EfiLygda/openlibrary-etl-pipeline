"""
Contains main function for retrieving records associated with a given key using a structured query
"""

import psycopg2
from psycopg2.sql import SQL
from utilities.database import get_column_names

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