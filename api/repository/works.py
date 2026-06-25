"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from api.repository.repository_engine import execute_repository_queries

def get_works_by_work_key(
        connection: psycopg2.extensions.connection,
        key: str | list[str],
        limit: int | None = None,
        offset: int | None = None,
) -> dict:
    """
    Retrieve all work records associated with a given work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param key: str | list[str], unique identifier of the work to retrieve or list of unique identifiers
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_parents` - total works returned
        * `data` - list of matching work records returned by the query
        * `column_names` - column names corresponding to the records
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=key,
        query_module='works',
        totals_query_filename='total_works.sql',
        data_query_filename='get_work.sql',
        limit=limit,
        offset=offset,
        used_for_batches=True,
        has_children=False
    )

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

        * `total_parents` - total works (used for error handling)
        * `total_children` - total authors before pagination
        * `author_data` - aggregated author records for the work
        * `author_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=work_key,
        query_module='works',
        totals_query_filename='total_authors.sql',
        data_query_filename='get_authors.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total works (used for error handling)
        * `total_children` - total editions before pagination
        * `editions_data` - aggregated edition records for the work
        * `editions_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=work_key,
        query_module='works',
        totals_query_filename='total_editions.sql',
        data_query_filename='get_editions.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total works (used for error handling)
        * `total_children` - total series before pagination
        * `series_data` - aggregated series records for the work
        * `series_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=work_key,
        query_module='works',
        totals_query_filename='total_series.sql',
        data_query_filename='get_series.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=True
    )

def get_availability_by_work_key(
    connection: psycopg2.extensions.connection,
    key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve availability information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param key: unique identifier of the work whose availability are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `data` - aggregated availability records for the work
        * `column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=key,
        query_module='works',
        totals_query_filename='total_availability.sql',
        data_query_filename='get_availability.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=True
    )

def get_ratings_by_work_key(
    connection: psycopg2.extensions.connection,
    key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve rating information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param key: unique identifier of the work whose ratings are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `data` - aggregated ratings records for the work
        * `column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=key,
        query_module='works',
        totals_query_filename='total_ratings.sql',
        data_query_filename='get_ratings.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=True
    )

def get_overview_by_work_key(
    connection: psycopg2.extensions.connection,
    key: str,
    limit: int | None = None,
    offset: int | None = None
) -> dict:
    """
    Retrieve all subject, people, places and time periods information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param key: unique identifier of the work whose editions are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `data` - aggregated subject, people, places and time periods records for the work
        * `column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=key,
        query_module='works',
        totals_query_filename='total_overview.sql',
        data_query_filename='get_overview.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=False
    )