"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from psycopg2.sql import SQL
from utilities.database import get_column_names

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

    # Query the database
    with connection.cursor() as cursor:
        # Construct the query
        query = SQL(
            """
            SELECT 
                *
            FROM 
                works 
            WHERE 
                work_key = %s
            """
        )

        # Execute the query
        cursor.execute(query, (work_key,))

        # Fetch all records as returned
        works = cursor.fetchall()

        # Fetch column names as returned
        works_column_names = get_column_names(cursor)

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

    # Query the database
    with connection.cursor() as cursor:

        # Construct the query
        query = SQL(
            """
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
        )

        # Execute the query
        cursor.execute(query, (work_key,))

        # Fetch all records as returned
        author_data = cursor.fetchall()

        # Fetch column names as returned
        author_column_names = get_column_names(cursor)

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

    # Query the database
    with connection.cursor() as cursor:

        # Construct the query
        query = SQL(
            """
            SELECT 
                w.work_key,
                w.title AS work_title,
                w.subtitle AS work_subtitle,
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
        )

        # Execute the query
        cursor.execute(query, (work_key,))

        # Fetch all records as returned
        editions_data = cursor.fetchall()

        # Fetch column names as returned
        editions_column_names = get_column_names(cursor)

    return editions_data, editions_column_names



