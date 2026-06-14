"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from api.repository.base import get_with_filter_key

def get_works_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str,
) -> tuple:
    """
    Retrieve all work records associated with a given work key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param work_key: str, unique identifier of the work to retrieve
    :returns: A tuple containing:

        * `works` - list of matching work records returned by the query
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
        w.work_key,
        COUNT(a.author_key) AS record_count,
        COALESCE(
            json_agg(
                json_build_object(
                    'author_key', a.author_key,
                    'author_name', a.author_name,
                    'birth_year', a.birth_year,
                    'death_year', a.death_year
                )
            ) FILTER (WHERE a.author_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM 
        works AS w
        LEFT JOIN authors_works AS aw
        ON w.work_key = aw.work_key
        LEFT JOIN authors AS a
        ON aw.author_key = a.author_key 
    WHERE 
        w.work_key = %s
    GROUP BY
        w.work_key
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
    Retrieve series information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose series are to
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


def get_availability_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str
) -> tuple:
    """
    Retrieve availability information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose availability are to
        be retrieved
    :returns: A tuple containing:

        * `availability_data` - aggregated availability records for the work
        * `availability_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT 
        w.work_key,
        w.title,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'ebook_access', wa.ebook_access,
                'has_fulltext', wa.has_fulltext,
                'has_public_scan', wa.has_public_scan
            )
        ) AS records
    FROM 
        works AS w
        INNER JOIN works_availability AS wa
        ON w.work_key = wa.work_key 
    WHERE
        w.work_key = %s
    GROUP BY 
        w.work_key
    """

    # Fetch the records
    availability_data, availability_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return availability_data, availability_column_names

def get_ratings_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str
) -> tuple:
    """
    Retrieve rating information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose ratings are to
        be retrieved
    :returns: A tuple containing:

        * `ratings_data` - aggregated ratings records for the work
        * `ratings_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT 
        w.work_key,
        w.title,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'ratings_count_1', wr.ratings_count_1,
                'ratings_count_2', wr.ratings_count_2,
                'ratings_count_3', wr.ratings_count_3,
                'ratings_count_4', wr.ratings_count_4,
                'ratings_count_5', wr.ratings_count_5
            )
        ) AS records
    FROM 
        works AS w
        INNER JOIN works_ratings AS wr
        ON w.work_key = wr.work_key 
    WHERE
        w.work_key = %s
    GROUP BY 
        w.work_key
    """

    # Fetch the records
    ratings_data, ratings_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return ratings_data, ratings_column_names

def get_overview_by_work_key(
    connection: psycopg2.extensions.connection,
    work_key: str
) -> tuple:
    """
    Retrieve all subject, people, places and time periods information associated with a given work key

    :param connection: active PostgreSQL database connection
    :param work_key: unique identifier of the work whose editions are to
        be retrieved
    :returns: A tuple containing:

        * `subject_data` - aggregated subject, people, places and time periods records for the work
        * `subject_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT 
        w.work_key,
        w.title,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'subjects', ws.subjects,
                'people', wpl.people,
                'places', wpc.places,
                'time_periods', wtp.time_periods
            )
        ) AS records
    FROM 
        works w
        LEFT JOIN 
        (
            SELECT work_key, array_agg(subject) AS subjects
            FROM works_subjects
            GROUP BY work_key
        ) ws ON w.work_key = ws.work_key
        LEFT JOIN 
        (
            SELECT work_key, array_agg(person) AS people
            FROM works_people
            GROUP BY work_key
        ) wpl ON w.work_key = wpl.work_key
        LEFT JOIN (
            SELECT work_key, array_agg(place) AS places
            FROM works_places
            GROUP BY work_key
        ) wpc ON w.work_key = wpc.work_key
        LEFT JOIN (
            SELECT work_key, array_agg(time_period) AS time_periods
            FROM works_time_periods
            GROUP BY work_key 
        ) wtp ON w.work_key = wtp.work_key
    WHERE
        w.work_key = %s
    GROUP BY 
        w.work_key
    """

    # Fetch the records
    subject_data, subject_column_names = get_with_filter_key(
        connection=connection,
        filter_key=work_key,
        query=query
    )

    return subject_data, subject_column_names