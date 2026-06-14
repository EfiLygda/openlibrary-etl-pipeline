"""
Database access layer for retrieving edition records

This module provides functions for querying the PostgreSQL database
to fetch edition-related data
"""

import psycopg2
from api.repository.base import get_with_filter_key

def get_edition_by_edition_key(
    connection: psycopg2.extensions.connection,
    edition_key: str,
) -> tuple:
    """
    Retrieve all edition records associated with a given author key

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
        edition_key = %s
    """

    # Fetch the records
    editions, editions_column_names = get_with_filter_key(
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

        * `details_data` - aggregated work records for the author
        * `details_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT
        *
    FROM
        editions_details
    WHERE
        edition_key = %s
    """

    # Fetch the records
    details_data, details_column_names = get_with_filter_key(
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
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A tuple containing:

        * `content_data` - aggregated work records for the author
        * `content_column_names` - column names corresponding to the query result
    """
    # Construction of the query
    query = """
    SELECT
        *
    FROM
        editions_contents
    WHERE
        edition_key = %s
    """

    # Fetch the records
    content_data, content_column_names = get_with_filter_key(
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
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A tuple containing:

        * `publishing_data` - aggregated publishing records for the edition
        * `publishing_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        edition_key,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'publish_date', publish_date,
                'publish_year', publish_year,
                'publisher', publisher,
                'publish_place', publish_place,
                'publish_country', publish_country,
                'series_title', series
            )
        ) AS records
    FROM
        editions_publishing
    WHERE
        edition_key = %s
    GROUP BY
        edition_key
    """

    # Fetch the records
    publishing_data, publishing_column_names = get_with_filter_key(
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
    :param edition_key: str, unique identifier of the edition whose details are to
        be retrieved
    :returns: A tuple containing:

        * `contributors_data` - aggregated contributors records for the edition
        * `contributors_column_names` - column names corresponding to the query result
    """

    # Construction of the query
    query = """
    SELECT
        edition_key,
        COUNT(*) AS record_count,
        json_agg(
            json_build_object(
                'contributor_name', contributor_name,
                'contributor_role', contributor_role,
                'by_statement', by_statement,
                'translated_from', translated_from,
                'translation_of', translation_of
            )
        ) AS records
    FROM
        editions_contributors
    WHERE
        edition_key = %s
    GROUP BY
        edition_key
    """

    # Fetch the records
    contributors_data, contributors_column_names = get_with_filter_key(
        connection=connection,
        filter_key=edition_key,
        query=query
    )

    return contributors_data, contributors_column_names