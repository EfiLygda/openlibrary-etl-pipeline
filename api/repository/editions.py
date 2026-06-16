"""
Database access layer for retrieving edition records

This module provides functions for querying the PostgreSQL database
to fetch edition-related data
"""

import psycopg2
from api.repository.base import execute_query

def get_edition_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve all edition records associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition to retrieve
    :returns: A tuple containing:

        * `editions` - list of matching records returned by the query
        * `editions_column_names` - column names corresponding to the records
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Fetch the records
    editions, editions_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_edition.sql'
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

        * `details_data` - details records for the edition
        * `details_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Fetch the records
    details_data, details_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_details.sql'
    )

    return details_data, details_column_names

def get_contents_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition content information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose contents are to
        be retrieved
    :returns: A tuple containing:

        * `content_data` - content records for the edition
        * `content_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Fetch the records
    content_data, content_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_contents.sql'
    )

    return content_data, content_column_names

def get_publishing_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition publishing information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose publishing details are to
        be retrieved
    :returns: A tuple containing:

        * `publishing_data` - aggregated publishing records for the edition
        * `publishing_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Fetch the records
    publishing_data, publishing_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_publishing.sql'
    )

    return publishing_data, publishing_column_names

def get_contributors_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition contributors information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose contributors are to
        be retrieved
    :returns: A tuple containing:

        * `contributors_data` - aggregated contributors records for the edition
        * `contributors_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Fetch the records
    contributors_data, contributors_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_contributors.sql'
    )

    return contributors_data, contributors_column_names