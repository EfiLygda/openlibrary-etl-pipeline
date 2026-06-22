"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from api.repository.base import execute_query

def get_works_by_work_key(
        connection: psycopg2.extensions.connection,
        work_key: str | list[str],
        limit: int | None = None,
        offset: int | None = None,
) -> dict:
    """
    Retrieve all work records associated with a given work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param work_key: str, unique identifier of the work to retrieve
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `data` - list of matching work records returned by the query
        * `column_names` - column names corresponding to the records
    """

    # Set up the query parameters
    if isinstance(work_key, str):
        params = {
            'filter_key': [work_key]
        }
    elif isinstance(work_key, list):
        params = {
            'filter_key': work_key
        }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='total_works.sql'
    )

    # Fetch the records
    works, works_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_work.sql'
    )

    return {
        'total_works': totals[0][0],
        'data': works,
        'column_names': works_column_names
    }

def get_authors_by_work_key(
        connection: psycopg2.extensions.connection,
        work_key: str,
        limit: int | None = None,
        offset: int | None = None
) -> dict:
    """
    Retrieve author information associated with a given work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param work_key: str, unique identifier of the work whose authors are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_works` - total works (used for error handling)
        * `total_authors` - total authors before pagination
        * `author_data` - aggregated author records for the work
        * `author_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': work_key,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total authors before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='total_authors.sql'
    )

    # Fetch the records
    author_data, author_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_authors.sql'
    )

    return {
        'total_works': totals[0][0],
        'total_authors': totals[0][1],
        'data': author_data,
        'column_names': author_column_names
    }

def get_editions_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve edition information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose editions are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_works` - total works (used for error handling)
        * `total_editions` - total editions before pagination
        * `editions_data` - aggregated edition records for the work
        * `editions_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': work_key,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total editions before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='total_editions.sql'
    )

    # Fetch the records
    editions_data, editions_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_editions.sql'
    )

    return {
        'total_works': totals[0][0],
        'total_editions': totals[0][1],
        'data': editions_data,
        'column_names': editions_column_names
    }

def get_series_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve series information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose series are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_works` - total works (used for error handling)
        * `total_series` - total series before pagination
        * `series_data` - aggregated series records for the work
        * `series_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': work_key,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total series before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='total_series.sql'
    )

    # Fetch the records
    series_data, series_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_series.sql'
    )

    return {
        'total_works': totals[0][0],
        'total_series': totals[0][1],
        'data': series_data,
        'column_names': series_column_names
    }

def get_availability_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve availability information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose availability are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `data` - aggregated availability records for the work
        * `column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': work_key,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Fetch the records
    availability_data, availability_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_availability.sql'
    )

    return {
        'data': availability_data,
        'column_names': availability_column_names
    }

def get_ratings_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve rating information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose ratings are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `data` - aggregated ratings records for the work
        * `column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': work_key,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Fetch the records
    ratings_data, ratings_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_ratings.sql'
    )

    return {
        'data': ratings_data,
        'column_names': ratings_column_names
    }

def get_overview_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve all subject, people, places and time periods information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose editions are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `subject_data` - aggregated subject, people, places and time periods records for the work
        * `subject_column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'filter_key': work_key,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Fetch the records
    subject_data, subject_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='works',
        query_filename='get_overview.sql'
    )

    return {
        'data': subject_data,
        'column_names': subject_column_names
    }