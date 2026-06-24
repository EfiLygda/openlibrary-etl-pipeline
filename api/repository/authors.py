"""
Database access layer for retrieving author records

This module provides functions for querying the PostgreSQL database
to fetch author-related data
"""

import psycopg2
from api.repository.repository_engine import execute_repository_queries

def get_authors_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str | list[str],
        limit: int | None = None,
        offset: int | None = None,
) -> dict:
    """
    Retrieve all author records associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author to retrieve
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_authors` - total authors (used for error handling)
        * `authors` - list of matching records returned by the query
        * `authors_column_names` - column names corresponding to the records
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=author_key,
        query_module='authors',
        totals_query_filename='total_authors.sql',
        data_query_filename='get_author.sql',
        limit=limit,
        offset=offset,
        used_for_batches=True,
        has_children=False
    )

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

        * `total_parents` - total authors (used for error handling)
        * `total_children` - total works before pagination
        * `work_data` - aggregated work records for the author
        * `work_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
        connection=connection,
        filter_key=author_key,
        query_module='authors',
        totals_query_filename='total_works.sql',
        data_query_filename='get_works.sql',
        limit=limit,
        offset=offset,
        used_for_batches=False,
        has_children=True
    )

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

        * `total_parents` - total authors (used for error handling)
        * `total_children` - total editions before pagination
        * `edition_data` - aggregated edition records for the author
        * `edition_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
            connection=connection,
            filter_key=author_key,
            query_module='authors',
            totals_query_filename='total_editions.sql',
            data_query_filename='get_editions.sql',
            limit=limit,
            offset=offset,
            used_for_batches=False,
            has_children=True
        )

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

        * `total_parents` - total authors (used for error handling)
        * `total_children` - total statistics records before pagination
        * `statistics_data` - statistic records for the author
        * `statistics_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
            connection=connection,
            filter_key=author_key,
            query_module='authors',
            totals_query_filename='total_statistics.sql',
            data_query_filename='get_statistics.sql',
            limit=limit,
            offset=offset,
            used_for_batches=False,
            has_children=True
        )

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

        * `total_parents` - total authors (used for error handling)
        * `total_children` - total alternative names before pagination
        * `alternative_names_data` - alternative names records for the author
        * `alternative_names_column_names` - column names corresponding to the query result
    """

    return execute_repository_queries(
            connection=connection,
            filter_key=author_key,
            query_module='authors',
            totals_query_filename='total_alternative_names.sql',
            data_query_filename='get_alternative_names.sql',
            limit=limit,
            offset=offset,
            used_for_batches=False,
            has_children=True
        )