"""
Database access layer for retrieving work records via search

This module provides functions for querying the PostgreSQL database
"""

import psycopg2
from api.repository.base import execute_query

def search(
        connection: psycopg2.extensions.connection,
        q: str,
        limit: int | None = None,
        offset: int | None = None
):

    # Set up the query parameters
    params = {
        'query': q
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