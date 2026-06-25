"""
Database access layer for retrieving edition records

This module provides functions for querying the PostgreSQL database
to fetch edition-related data
"""

import psycopg2
from api.repository.repository_engine import execute_repository_queries

def get_editions_by_edition_key(
        connection: psycopg2.extensions.connection,
        keys: str | list[str],
        limit: int | None = None,
        offset: int | None = None,
) -> dict:
    """
    Retrieve all edition records associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param keys: str | list[str], unique identifier of the edition to retrieve or list of unique identifiers
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `editions` - list of matching records returned by the query
        * `editions_column_names` - column names corresponding to the records
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=keys,
        query_module='editions',
        totals_query_filename='total_editions.sql',
        data_query_filename='get_edition.sql',
        limit=limit,
        offset=offset,
        used_for_batches=True,
        has_children=False
    )

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

        * `total_parents` - total editions (used for error handling)
        * `total_children` - total works before pagination
        * `details_data` - details records for the edition
        * `details_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=edition_key,
        query_module='editions',
        totals_query_filename='total_works.sql',
        data_query_filename='get_works.sql',
        # limit=limit,
        # offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total editions (used for error handling)
        * `total_children` - total details before pagination
        * `details_data` - details records for the edition
        * `details_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=edition_key,
        query_module='editions',
        totals_query_filename='total_details.sql',
        data_query_filename='get_details.sql',
        # limit=limit,
        # offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total editions (used for error handling)
        * `total_children` - total contents before pagination
        * `content_data` - content records for the edition
        * `content_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=edition_key,
        query_module='editions',
        totals_query_filename='total_contents.sql',
        data_query_filename='get_contents.sql',
        # limit=limit,
        # offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total editions (used for error handling)
        * `total_children` - total publishing before pagination
        * `publishing_data` - aggregated publishing records for the edition
        * `publishing_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=edition_key,
        query_module='editions',
        totals_query_filename='total_publishing.sql',
        data_query_filename='get_publishing.sql',
        # limit=limit,
        # offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total editions (used for error handling)
        * `total_children` - total contributors before pagination
        * `contributors_data` - aggregated contributors records for the edition
        * `contributors_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=edition_key,
        query_module='editions',
        totals_query_filename='total_contributors.sql',
        data_query_filename='get_contributors.sql',
        # limit=limit,
        # offset=offset,
        used_for_batches=False,
        has_children=True
    )