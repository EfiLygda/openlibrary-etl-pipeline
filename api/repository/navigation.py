"""
Database access layer for retrieving link records

This module provides functions for querying the PostgreSQL database
to fetch navigation-related data
"""

import psycopg2

def exists_with_filter_key_by_entity_type(
        connection: psycopg2.extensions.connection,
        filter_key: str,
        key_type: str
) -> tuple:
    """
    Retrieve all author records associated with a given author key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param filter_key: str, unique identifier of the entity to retrieve
    :param key_type: str, entity type to retrieve
    :returns: A tuple containing:

        * `authors` - list of matching records returned by the query
        * `authors_column_names` - column names corresponding to the records
    """

    queries = {
        'work': """SELECT EXISTS ( SELECT 1 FROM works WHERE work_key = %(filter_key)s )""",
        'author': """SELECT EXISTS ( SELECT 1 FROM authors WHERE author_key = %(filter_key)s )""",
        'edition': """SELECT EXISTS ( SELECT 1 FROM editions WHERE edition_key = %(filter_key)s )""",
    }

    query = queries[key_type]

    # Fetch the records
    with connection.cursor() as cursor:

        cursor.execute(
            query,
            vars={
                'filter_key': filter_key
            }
        )

        return cursor.fetchone()[0]
