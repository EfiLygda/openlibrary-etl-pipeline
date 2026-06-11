"""
Table names grouping by entities works, authors and editions, internal validation/get functions
and get_by_entity_key that retrieves records from a given table in the database by its entity key

Note: 'entity key' is not primary key for each table but only for the three main
tables `works`, `authors` and `editions`
"""

import psycopg2
from psycopg2.sql import Identifier, SQL
from utilities.database import get_column_names

# Table grouping by entities 'works', 'authors' and 'editions'
# Note: 'key' is not primary key for each table but only for the three main dimension tables
ENTITY_MAP = {
    'works': {
        'key': 'work_key',
        'tables': [
            'works',
            'authors_works',
            'works_ratings',
            'works_series',
            'works_availability',
            'works_subjects',
            'works_people',
            'works_places',
            'works_time_periods'
        ]
    },
    'authors': {
        'key': 'author_key',
        'tables': [
            'authors',
            'authors_alternative_names',
            'authors_statistics'
        ]
    },
    'editions': {
        'key': 'edition_key',
        'tables': [
            'editions',
            'editions_contributors',
            'editions_publishing',
            'editions_contents',
            'editions_details'
        ]
    },
}

def _validate_entity(entity:str) -> None:
    """
    Validate that an entity exists in ENTITY_MAP

    :param entity: str, entity name to validate
    :raises ValueError: if entity is not defined in ENTITY_MAP
    """

    if entity not in ENTITY_MAP.keys():
        raise ValueError(
            f'\'entity\' must be in {list(ENTITY_MAP.keys())}, \'{entity}\' was given'
        )

def _validate_entity_table(
        table_name: str,
        entity: str
) -> None:
    """
    Validate that a table belongs to a given entity group

    :param table_name: str, database table name
    :param entity: str, entity group name
    :raises ValueError: ff table_name is not part of the entity's tables
    """

    # Fetch current entity's table names
    entity_table_names = ENTITY_MAP[entity]['tables']

    if table_name not in entity_table_names:
        raise ValueError(
            f'\'table_name\' must be in {entity_table_names}, \'{table_name}\' was given'
        )

def _get_entity_key(entity:str) -> str:
    """
    Return the key column name for an entity (Note: not necessarily the primary key)

    :param entity: str, entity group name
    :return: str, entity key column name
    """

    # Validate the entity' name
    _validate_entity(entity)

    return ENTITY_MAP[entity]['key']

def _get_entity_table(
        table_name: str,
        entity: str
) -> list[str]:
    """
    Return all valid tables for an entity group after validation

    :param table_name: str, database table name to validate
    :param entity: str, entity group name
    :return: list[str], list of valid table names for the entity
    :raises ValueError: If table_name is not part of the entity group
    """
    # Validate current entity and table name
    _validate_entity(entity)
    _validate_entity_table(table_name, entity)

    # Fetch entity table name
    entity_table_names = ENTITY_MAP[entity]['tables']

    return entity_table_names

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
    entity_key_name = _get_entity_key(entity)

    # Validate table names that are in the entity's group
    _validate_entity_table(
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
