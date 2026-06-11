"""
get_by_entity_key that retrieves records from a given table in the database by its entity key

Note: 'entity key' is not primary key for each table but only for the three main
tables `works`, `authors` and `editions`
"""

import psycopg2
from psycopg2.sql import SQL, Identifier

from utilities.database import get_column_names
from api.core.entities import get_entity_key, validate_entity_table

def get_by_entity_key(
        connection: psycopg2.extensions.connection,
        table_name: str,
        entity: str,
        key: str
) -> tuple:
    """
    Retrieves records from a given table in the database by key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param table_name: str, unique identifier used for a table name
    :param entity: str, table grouping (values: 'works', 'authors', 'editions')
    :param key: str, unique identifier used to filter records

    :returns: tuple, containing query results and column names
    """

    # Fetch entity's key name
    entity_key_name = get_entity_key(entity)

    # Validate table names that are in the entity's group
    validate_entity_table(
        table_name=table_name,
        entity=entity
    )

    # Query the database
    with connection.cursor() as cursor:

        # Construct the query
        # Note:
        # 1. psycopg2.sql.SQL is used in order to make a query template
        #    using a certain table and its entity's key
        # 2. psycopg2.sql.Identifier is used for safe injection
        query = SQL(
            'SELECT * FROM {} WHERE {} = %s'
            ).format(
            Identifier(table_name),
            Identifier(entity_key_name)
        )

        # Execute the query
        cursor.execute(query, (key,))

        # Fetch all records as returned
        records = cursor.fetchall()

        # Fetch column names as returned
        column_names = get_column_names(cursor)

        return records, column_names
