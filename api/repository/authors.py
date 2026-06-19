"""
Database access layer for retrieving author records

This module provides functions for querying the PostgreSQL database
to fetch author-related data
"""

import psycopg2
from api.repository.base import execute_query

def get_author_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
) -> dict:
    """
    Retrieve all author records associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author to retrieve
    :returns: A dictionary containing:

        * `authors` - list of matching records returned by the query
        * `authors_column_names` - column names corresponding to the records
    """

    # Set up the query parameters
    params = {
        'filter_key': author_key
    }

    # Fetch the records
    authors, authors_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='get_author.sql'
    )

    return {
        'data': authors,
        'column_names': authors_column_names
    }

def get_works_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
        limit: int | None = None,
        offset: int | None = None
) -> dict:
    """
    Retrieve work information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the work whose works are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_authors` - total authors (used for error handling)
        * `total_works` - total works before pagination
        * `work_data` - aggregated work records for the author
        * `work_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': author_key
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='total_works.sql'
    )

    # Fetch the records
    work_data, work_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='get_works.sql'
    )

    return {
        'total_authors': totals[0][0],
        'total_works': totals[0][1],
        'data': work_data,
        'column_names': work_column_names
    }

def get_editions_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
        limit: int | None = None,
        offset: int | None = None
) -> dict:
    """
    Retrieve edition information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author whose editions are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_authors` - total authors (used for error handling)
        * `total_editions` - total editions before pagination
        * `edition_data` - aggregated edition records for the author
        * `edition_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': author_key
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total editions before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='total_editions.sql'
    )

    # Fetch the records
    edition_data, edition_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='get_editions.sql'
    )

    return {
        'total_authors': totals[0][0],
        'total_editions': totals[0][1],
        'data': edition_data,
        'column_names': edition_column_names
    }

def get_author_statistics_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
        limit: int | None = None,
        offset: int | None = None
) -> dict:
    """
    Retrieve author statistics information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author whose statistics are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `statistics_data` - statistic records for the author
        * `statistics_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': author_key
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Fetch the records
    statistics_data, statistics_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='get_statistics.sql'
    )

    return {
        'data': statistics_data,
        'column_names': statistics_column_names
    }

def get_author_alternative_names_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
        limit: int | None = None,
        offset: int | None = None
) -> dict:
    """
    Retrieve author alternative names information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author whose alternative names are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `alternative_names_data` - alternative names records for the author
        * `alternative_names_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': author_key
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Fetch the records
    alternative_names_data, alternative_names_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='get_alternative_names.sql'
    )

    return {
        'data': alternative_names_data,
        'column_names': alternative_names_column_names
    }
