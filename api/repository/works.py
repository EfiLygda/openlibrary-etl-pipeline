"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from psycopg2.sql import SQL
from utilities.database import get_column_names


def get_with_filter_key(
        connection: psycopg2.extensions.connection,
        filter_key: str,
        query: str
):
    """
        Retrieve all records associated with a given key using a structured query

        :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
        :param filter_key: str, unique identifier of the work to retrieve
        :param query: str, the filtering query used

        :returns: A tuple containing:

            * `data` - list of matching records returned by the query
            * `data_column_names` - column names corresponding to the records

        """

    # Query the database
    with connection.cursor() as cursor:
        # Construct the query
        query_to_execute = SQL(query)

        # Execute the query
        cursor.execute(query_to_execute, (filter_key,))

        # Fetch all records as returned
        data = cursor.fetchall()

        # Fetch column names as returned
        data_column_names = get_column_names(cursor)

    return data, data_column_names

def get_works_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
) -> tuple:
    """
    Retrieve all work records associated with a given work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param work_key: str, unique identifier of the work to retrieve
    :returns: A tuple containing:

        * `works` - list of matching records returned by the query
        * `works_column_names` - column names corresponding to the records
    """

    # Construction of the query
    query = """
    SELECT
        *
    FROM 
        works 
    WHERE 
        work_key = %s
    """

    # Fetch the records
    works, works_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return works, works_column_names

def get_authors_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
) -> tuple:
    """
    Retrieve author information associated with a given work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param work_key: str, unique identifier of the work whose authors are to
        be retrieved
    :returns: A tuple containing:

        * `author_data` - aggregated author records for the work
        * `author_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT 
        aw.work_key,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'author_key', a.author_key,
                'author_name', a.author_name,
                'birth_year', a.birth_year,
                'death_year', a.death_year
            )
        ) AS records
    FROM 
        authors_works AS aw
        LEFT JOIN authors AS a
        ON aw.author_key = a.author_key 
    WHERE 
        aw.work_key = %s
    GROUP BY
        aw.work_key
    """

    # Fetch the records
    author_data, author_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return author_data, author_column_names

def get_editions_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str
) -> tuple:
    """
    Retrieve edition information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose editions are to
        be retrieved
    :returns: A tuple containing:

        * `editions_data` - aggregated edition records for the work
        * `editions_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT 
        w.work_key,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'edition_key', e.edition_key,
                'title', e.title,
                'subtitle', e.subtitle,
                'name', e.edition_name
            )
        ) AS records
    FROM 
        works AS w
        LEFT JOIN editions AS e
        ON w.work_key = e.work_key 
    WHERE
        w.work_key = %s
    GROUP BY 
        w.work_key
    """

    # Fetch the records
    editions_data, editions_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return editions_data, editions_column_names

def get_series_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str
) -> tuple:
    """
    Retrieve edition information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose editions are to
        be retrieved
    :returns: A tuple containing:

        * `series_data` - aggregated series records for the work
        * `series_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT 
        w.work_key,
        w.title,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'series_key', ws.series_key,
                'series_position', ws.series_position,
                'series_name', ws.series_name
            )
        ) AS records
    FROM 
        works AS w
        INNER JOIN works_series AS ws
        ON w.work_key = ws.work_key 
    WHERE
        w.work_key = %s
    GROUP BY 
        w.work_key
    """

    # Fetch the records
    series_data, series_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return series_data, series_column_names


