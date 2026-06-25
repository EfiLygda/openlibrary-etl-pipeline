"""
Database access layer for retrieving work records via search

This module provides functions for querying the PostgreSQL database
"""

import psycopg2
from api.repository.database_adapter import execute_query

def search(
        connection: psycopg2.extensions.connection,
        q: str,
        year: int | None = None,
        lang: str | None = None,
        published_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None
):
    """
    Search for works based on a query and optional filtering parameters

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param q: str, free-text search query used to match works
    :param year: int | None, optional filter to restrict results to a specific publication year
    :param lang: str | None, optional filter to restrict results by language code
    :param published_by: str | None, optional filter to restrict results by publisher name or identifier
    :param limit: int | None, maximum number of records to return (used for pagination)
    :param offset: int | None, number of records to skip before starting to return results

    :returns: A dictionary containing:

        * `total_results` - total number of matching works before pagination
        * `data` - list of work records returned by the query
        * `column_names` - column names corresponding to the query result
    """

    # Set up the query parameters
    params = {
        'query': q,
        'year': year,
        'lang': lang,
        'published_by': published_by,
    }

    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    # Calculate total works before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module='search',
        query_filename='search_works_total.sql'
    )

    # Fetch the records
    work_data, work_column_names = execute_query(
        connection=connection,
        params=params,
        query_module='search',
        query_filename='search_works.sql'
    )

    return {
        'total_results': totals[0][0],
        'data': work_data,
        'column_names': work_column_names
    }