"""
Shared repository utilities for API data access

Provides generic helper functions to standardize SQL query execution
and parameter handling
"""

import psycopg2
from api.repository.database_adapter import execute_query

def _build_params(
        filter_key: str | list[str],
        limit: int | None = None,
        offset: int | None = None,
        used_for_batches: bool = False
) -> dict:
    """
    Normalize SQL query parameters for repository execution

    This helper ensures consistent formatting of query parameters across all
    repository modules in the API layer

    It handles:
        - Conversion of single keys to list format for batch queries
        - Pagination parameters (limit / offset)
        - Consistent structure for SQL execution layer

    :param filter_key:  str | list[str], identifier(s) used in SQL filtering
    :param limit: int | None, maximum number of rows to return
    :param offset: int | None, number of rows to skip.
    :param used_for_batches: bool, whether query is executed in batch mode
    :return: dict, dictionary of SQL parameters
    """

    # Set up the query parameters
    if used_for_batches and isinstance(filter_key, str):
        # Used for when a single key is given for a batch endpoint
        params = {
            'filter_key': [filter_key]
        }
    else:
        # Used for when a key is given for simple endpoints and a
        # list of keys for a batch endpoint
        params = {
            'filter_key': filter_key
        }

    # Add limit and offset, if given
    if not limit is None:
        params['limit'] = limit

    if not offset is None:
        params['offset'] = offset

    return params

def execute_repository_queries(
        connection: psycopg2.extensions.connection,
        filter_key: str | list[str],
        query_module: str,
        data_query_filename: str,
        totals_query_filename: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        used_for_batches: bool = False,
        has_children: bool = False
):
    """
    Execute standardized repository SQL queries

    This is a shared utility used across API repository modules to execute SQL
    queries in a consistent way

    It performs two database operations:

    1. Totals query:
       Retrieves aggregated metadata such as total parents and optional child
       counts (used for pagination and validation)

    2. Data query:
       Retrieves the actual dataset corresponding to the filter criteria,
       optionally paginated via limit/offset

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param filter_key: str | list[str], filter value(s) used for SQL queries
    :param query_module: str, directory containing SQL query definitions
    :param totals_query_filename: str, SQL file used for aggregation queries
    :param data_query_filename: str, SQL file used for data retrieval
    :param limit: int | None, maximum number of rows to return
    :param offset: int | None, number of rows to skip
    :param used_for_batches: bool, whether query is executed in batch mode
    :param has_children: bool, whether totals include child entity counts

    :return: dict, raw database result structure containing:
        - total_parents (optional)
        - total_children (optional)
        - data
        - column_names
    """

    # Build the parameters dictionary
    params = _build_params(
        filter_key=filter_key,
        limit=limit,
        offset=offset,
        used_for_batches=used_for_batches
    )

    # Fetch the records and the column names
    records, column_names = execute_query(
        connection=connection,
        params=params,
        query_module=query_module,
        query_filename=data_query_filename
    )

    if not totals_query_filename:
        return {
            'data': records,
            'column_names': column_names
        }

    # Calculate total parents (and children) before pagination
    totals, _ = execute_query(
        connection=connection,
        params=params,
        query_module=query_module,
        query_filename=totals_query_filename
    )

    # If the response should have children (for relationships 1-n or 1-1)
    if has_children:
        return {
            'total_parents': totals[0][0],
            'total_children': totals[0][1],
            'data': records,
            'column_names': column_names
        }

    # Return response without children (for basic entities)
    return {
        'total_parents': totals[0][0],
        'data': records,
        'column_names': column_names
    }
