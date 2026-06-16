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
) -> tuple:
    """
    Retrieve all author records associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author to retrieve
    :returns: A tuple containing:

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

    return authors, authors_column_names

def get_works_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
        limit: int | None = None,
        offset: int | None = None
) -> tuple:
    """
    Retrieve work information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the work whose works are to
        be retrieved
    :param limit: int, maximum number of records to return (used for pagination)
    :param offset: int, number of records to skip before starting to return results

    :returns: A tuple containing:

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

    # Fetch the records
    work_data, work_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='authors',
        query_filename='get_works.sql'
    )

    return work_data, work_column_names

def get_editions_by_author_key(
    connection: psycopg2.extensions.connection,
    author_key: str,
) -> tuple:
    """
    Retrieve edition information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author whose editions are to
        be retrieved
    :returns: A tuple containing:

        * `edition_data` - aggregated edition records for the author
        * `edition_column_names` - column names corresponding to the query result
    """
    query = """
    SELECT
        a.author_key,
        COUNT(e.edition_key) AS record_count,
        COALESCE(
            json_agg(
                json_build_object(
                    'edition_key', e.edition_key,
                    'title', e.title,
                    'subtitle', e.subtitle,
                    'name', e.edition_name
                )
            ) FILTER (WHERE e.edition_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        authors AS a
        LEFT JOIN authors_works AS aw
        ON a.author_key = aw.author_key
        LEFT JOIN editions AS e
        ON aw.work_key = e.work_key
    WHERE
        a.author_key = %(filter_key)s
    GROUP BY
        a.author_key
    """

    # Fetch the records
    edition_data, edition_column_names = execute_query(
        connection=connection,
        filter_key=author_key,
        query=query
    )

    return edition_data, edition_column_names

def get_author_statistics_by_author_key(
    connection: psycopg2.extensions.connection,
    author_key: str,
) -> tuple:
    """
    Retrieve author statistics information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author whose statistics are to
        be retrieved
    :returns: A tuple containing:

        * `statistics_data` - statistic records for the author
        * `statistics_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        a.author_key,
        COUNT(astat.author_key) AS record_count,
        COALESCE(
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
            ) FILTER (WHERE astat.author_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        authors AS a
        LEFT JOIN authors_statistics AS astat
        ON a.author_key = astat.author_key
    WHERE
        a.author_key = %(filter_key)s
    GROUP BY
        a.author_key
    """

    # Fetch the records
    statistics_data, statistics_column_names = execute_query(
        connection=connection,
        filter_key=author_key,
        query=query
    )

    return statistics_data, statistics_column_names

def get_author_alternative_names_by_author_key(
        connection: psycopg2.extensions.connection,
        author_key: str,
) -> tuple:
    """
    Retrieve author alternative names information associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param author_key: str, unique identifier of the author whose alternative names are to
        be retrieved
    :returns: A tuple containing:

        * `alternative_names_data` - alternative names records for the author
        * `alternative_names_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        a.author_key,
        COUNT(altnames.author_alternative_name) AS record_count,
        COALESCE(
            array_agg(altnames.author_alternative_name)
                FILTER (WHERE altnames.author_alternative_name IS NOT NULL),
            ARRAY[]::text[]
        ) AS records
    FROM
        authors AS a
        LEFT JOIN 
        authors_alternative_names AS altnames 
        ON a.author_key = altnames.author_key
    WHERE
        a.author_key = %(filter_key)s
    GROUP BY
        a.author_key
    """

    # Fetch the records
    alternative_names_data, alternative_names_column_names = execute_query(
        connection=connection,
        filter_key=author_key,
        query=query
    )

    return alternative_names_data, alternative_names_column_names
