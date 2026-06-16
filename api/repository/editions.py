"""
Database access layer for retrieving edition records

This module provides functions for querying the PostgreSQL database
to fetch edition-related data
"""

import psycopg2
from api.repository.base import execute_query

def get_edition_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve all edition records associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition to retrieve
    :returns: A tuple containing:

        * `editions` - list of matching records returned by the query
        * `editions_column_names` - column names corresponding to the records
    """

    # Construction of the query
    query = """
    SELECT
        *
    FROM 
        editions 
    WHERE 
        edition_key = %(filter_key)s
    """

    # Fetch the records
    editions, editions_column_names = execute_query(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return editions, editions_column_names

def get_details_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition detailed information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A tuple containing:

        * `details_data` - details records for the edition
        * `details_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT
        e.edition_key,
        COUNT(ed.edition_key) AS record_count,
        COALESCE(
            json_agg(
                json_build_object(
                    'number_of_pages', ed.number_of_pages,
                    'physical_format', ed.physical_format,
                    'physical_dimensions', ed.physical_dimensions,
                    'weight', ed.weight,
                    'language', ed.language
                )
            ) FILTER (WHERE ed.edition_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM 
        editions AS e
        LEFT JOIN editions_details AS ed
        ON e.edition_key = ed.edition_key
    WHERE 
        e.edition_key = %(filter_key)s
    GROUP BY 
        e.edition_key;
    """

    # Fetch the records
    details_data, details_column_names = execute_query(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return details_data, details_column_names

def get_contents_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition content information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose contents are to
        be retrieved
    :returns: A tuple containing:

        * `content_data` - content records for the edition
        * `content_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT
        e.edition_key,
        COUNT(ec.edition_key) AS record_count,
        COALESCE(
            json_agg(
                json_build_object(
                    'description', ec.description,
                    'notes', ec.notes,
                    'first_sentence', ec.first_sentence
                )
            ) FILTER (WHERE ec.edition_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM 
        editions AS e
        LEFT JOIN 
        editions_contents AS ec
        ON e.edition_key = ec.edition_key
    WHERE 
        e.edition_key = %(filter_key)s
    GROUP BY 
        e.edition_key;
    """

    # Fetch the records
    content_data, content_column_names = execute_query(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return content_data, content_column_names

def get_publishing_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition publishing information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose publishing details are to
        be retrieved
    :returns: A tuple containing:

        * `publishing_data` - aggregated publishing records for the edition
        * `publishing_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        e.edition_key,
        COUNT(ep.edition_key) AS record_count,
        COALESCE(
            json_agg(
                json_build_object(
                    'publish_date', ep.publish_date,
                    'publish_year', ep.publish_year,
                    'publisher', ep.publisher,
                    'publish_place', ep.publish_place,
                    'publish_country', ep.publish_country,
                    'series_title', ep.series
                )
            ) FILTER (WHERE ep.edition_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM 
        editions AS e
        LEFT JOIN editions_publishing AS ep
        ON e.edition_key = ep.edition_key
    WHERE
        e.edition_key = %(filter_key)s
    GROUP BY
        e.edition_key
    """

    # Fetch the records
    publishing_data, publishing_column_names = execute_query(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return publishing_data, publishing_column_names

def get_contributors_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve edition contributors information associated with a given edition key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param edition_key: str, unique identifier of the edition whose contributors are to
        be retrieved
    :returns: A tuple containing:

        * `contributors_data` - aggregated contributors records for the edition
        * `contributors_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        e.edition_key,
        COUNT(ec.edition_key) AS record_count,
        COALESCE(
            json_agg(
                json_build_object(
                    'contributor_name', ec.contributor_name,
                    'contributor_role', ec.contributor_role,
                    'by_statement', ec.by_statement,
                    'translated_from', ec.translated_from,
                    'translation_of', ec.translation_of
                )
            ) FILTER (WHERE ec.edition_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM 
        editions AS e
        LEFT JOIN editions_contributors AS ec
        ON e.edition_key = ec.edition_key
    WHERE 
        e.edition_key = %(filter_key)s
    GROUP BY
        e.edition_key;
    """

    # Fetch the records
    contributors_data, contributors_column_names = execute_query(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return contributors_data, contributors_column_names