"""
Database access layer for retrieving author records

This module provides functions for querying the PostgreSQL database
to fetch author-related data
"""

import psycopg2
from api.repository.base import get_with_filter_key

def get_author_by_author_key(
    connection: psycopg2.extensions.connection,
    author_key: str,
) -> tuple:
    """
    Retrieve all author records associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author to retrieve
    :returns: A tuple containing:

        * `authors` - list of matching records returned by the query
        * `authors_column_names` - column names corresponding to the records
    """

    # Construction of the query
    query = """
    SELECT
        *
    FROM 
        authors 
    WHERE 
        author_key = %s
    """

    # Fetch the records
    authors, authors_column_names = get_with_filter_key(
        connection=connection,
        filter_key=author_key,
        query=query
    )

    return authors, authors_column_names

def get_works_by_author_key(
    connection: psycopg2.extensions.connection,
    author_key: str,
) -> tuple:
    """
    Retrieve work information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the work whose authors are to
        be retrieved
    :returns: A tuple containing:

        * `work_data` - aggregated work records for the author
        * `work_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        a.author_key,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'work_key', w.work_key,
                'title', w.title,
                'subtitle', w.subtitle,
                'edition_count', w.edition_count,
                'first_publish_year', w.first_publish_year
            )
            ORDER BY w.first_publish_year DESC NULLS LAST
        ) AS records
    FROM
        authors AS a
        INNER JOIN authors_works AS aw
        ON a.author_key = aw.author_key
        INNER JOIN works AS w
        ON aw.work_key = w.work_key
    WHERE
        a.author_key = %s
    GROUP BY
        a.author_key
    """

    # Fetch the records
    work_data, work_column_names = get_with_filter_key(
        connection=connection,
        filter_key=author_key,
        query=query
    )

    return work_data, work_column_names

def get_author_statistics_by_author_key(
    connection: psycopg2.extensions.connection,
    author_key: str,
) -> tuple:
    """
    Retrieve author statistics information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the work whose authors are to
        be retrieved
    :returns: A tuple containing:

        * `statistics_data` - statistic records for the author
        * `statistics_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        a.author_key,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'top_work', astat.top_work,
                'work_count', astat.work_count,
                
                'ratings_count_1', astat.ratings_count_1,
                'ratings_count_2', astat.ratings_count_2,
                'ratings_count_3', astat.ratings_count_3,
                'ratings_count_4', astat.ratings_count_4,
                'ratings_count_5', astat.ratings_count_5,
                
                'readinglog_count', astat.readinglog_count,
                'want_to_read_count', astat.want_to_read_count,
                'currently_reading_count', astat.currently_reading_count,
                'already_read_count', astat.already_read_count
            )
        ) AS records
    FROM
        authors AS a
        INNER JOIN authors_statistics AS astat
        ON a.author_key = astat.author_key
    WHERE
        a.author_key = %s
    GROUP BY
        a.author_key
    """

    # Fetch the records
    statistics_data, statistics_column_names = get_with_filter_key(
        connection=connection,
        filter_key=author_key,
        query=query
    )

    return statistics_data, statistics_column_names