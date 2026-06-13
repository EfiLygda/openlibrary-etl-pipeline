"""
Database access layer for retrieving edition records

This module provides functions for querying the PostgreSQL database
to fetch edition-related data
"""

import psycopg2
from api.repository.base import get_with_filter_key

def get_edition_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve all edition records associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition to retrieve
    :returns: A tuple containing:

        * `editions` - list of matching records returned by the query
        * `editions_column_names` - column names corresponding to the records
    """

    # Construction of the query
    query = """
    SELECT
        *
    FROM 
        editions 
    WHERE 
        edition_key = %s
    """

    # Fetch the records
    editions, editions_column_names = get_with_filter_key(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return editions, editions_column_names

def get_details_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition detailed information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A tuple containing:

        * `details_data` - aggregated work records for the author
        * `details_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT
        *
    FROM
        editions_details
    WHERE
        edition_key = %s
    """

    # Fetch the records
    details_data, details_column_names = get_with_filter_key(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return details_data, details_column_names