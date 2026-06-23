"""
Database access layer for retrieving edition records

This module provides functions for querying the PostgreSQL database
to fetch edition-related data
"""

import psycopg2
from api.repository.base import execute_query

def get_editions_by_edition_key(
        connection: psycopg2.extensions.connection,
        edition_key: str | list[str],
        limit: int | None = None,
        offset: int | None = None,
) -> dict:
    """
    Retrieve all edition records associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str | list[str], unique identifier of the edition to retrieve or list of unique identifiers
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `editions` - list of matching records returned by the query
        * `editions_column_names` - column names corresponding to the records
    """

    # Set up the query parameters
    if isinstance(edition_key, str):
        params = {
            'filter_key': [edition_key]
        }
    elif isinstance(edition_key, list):
        params = {
            'filter_key': edition_key
        }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='total_editions.sql'
    )

    # Fetch the records
    editions, editions_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_edition.sql'
    )

    return {
        'total_editions': totals[0][0],
        'data': editions,
        'column_names': editions_column_names
    }

def get_works_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> dict:
    """
    Retrieve edition work associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A dictionary containing:

        * `total_editions` - total editions (used for error handling)
        * `total_works` - total works before pagination
        * `details_data` - details records for the edition
        * `details_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='total_works.sql'
    )

    # Fetch the records
    works_data, works_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_works.sql'
    )

    return {
        'total_editions': totals[0][0],
        'total_works': totals[0][1],
        'data': works_data,
        'column_names': works_column_names
    }

def get_details_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> dict:
    """
    Retrieve edition detailed information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A dictionary containing:

        * `total_editions` - total editions (used for error handling)
        * `total_details` - total details before pagination
        * `details_data` - details records for the edition
        * `details_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='total_details.sql'
    )

    # Fetch the records
    details_data, details_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_details.sql'
    )

    return {
        'total_editions': totals[0][0],
        'total_details': totals[0][1],
        'data': details_data,
        'column_names': details_column_names
    }

def get_contents_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> dict:
    """
    Retrieve edition content information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose contents are to
        be retrieved
    :returns: A dictionary containing:

        * `total_editions` - total editions (used for error handling)
        * `total_contents` - total contents before pagination
        * `content_data` - content records for the edition
        * `content_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='total_contents.sql'
    )

    # Fetch the records
    content_data, content_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_contents.sql'
    )

    return {
        'total_editions': totals[0][0],
        'total_contents': totals[0][1],
        'data': content_data,
        'column_names': content_column_names
    }

def get_publishing_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> dict:
    """
    Retrieve edition publishing information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose publishing details are to
        be retrieved
    :returns: A dictionary containing:

        * `total_editions` - total editions (used for error handling)
        * `total_publishing` - total publishing before pagination
        * `publishing_data` - aggregated publishing records for the edition
        * `publishing_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='total_publishing.sql'
    )

    # Fetch the records
    publishing_data, publishing_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_publishing.sql'
    )

    return {
        'total_editions': totals[0][0],
        'total_publishing': totals[0][1],
        'data': publishing_data,
        'column_names': publishing_column_names
    }

def get_contributors_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> dict:
    """
    Retrieve edition contributors information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose contributors are to
        be retrieved
    :returns: A dictionary containing:

        * `total_editions` - total editions (used for error handling)
        * `total_contributors` - total contributors before pagination
        * `contributors_data` - aggregated contributors records for the edition
        * `contributors_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': edition_key
    }

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='total_contributors.sql'
    )

    # Fetch the records
    contributors_data, contributors_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='editions',
        query_filename='get_contributors.sql'
    )

    return {
        'total_editions': totals[0][0],
        'total_contributors': totals[0][1],
        'data': contributors_data,
        'column_names': contributors_column_names
    }