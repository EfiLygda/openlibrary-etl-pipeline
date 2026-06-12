"""
Table names grouping by entities works, authors and editions, internal validation/get functions

Note: 'entity key' is not primary key for each table but a key column (foreign or not) in a table
"""

# Table grouping by entities 'works', 'authors' and 'editions'
# Note: 'key' is not primary key for each table but only for the three main dimension tables
ENTITY_MAP = {
    'works': {
        'key': 'work_key',
        'tables': [
            'works',
            'works_ratings',
            'works_series',
            'works_availability',
            'works_subjects',
            'works_people',
            'works_places',
            'works_time_periods',
            'authors_works'
        ]
    },
    'authors': {
        'key': 'author_key',
        'tables': [
            'authors',
            'authors_alternative_names',
            'authors_statistics',
            'authors_works'
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

def validate_entity(entity:str) -> None:
    """
    Validate that an entity exists in ENTITY_MAP

    :param entity: str, entity name to validate
    :raises ValueError: if entity is not defined in ENTITY_MAP
    """

    if entity not in ENTITY_MAP.keys():
        raise ValueError(
            f'\'entity\' must be in {list(ENTITY_MAP.keys())}, \'{entity}\' was given'
        )

def validate_entity_table(
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

def get_entity_key(entity:str) -> str:
    """
    Return the key column name for an entity (Note: not necessarily the primary key)

    :param entity: str, entity group name
    :return: str, entity key column name
    """

    # Validate the entity' name
    validate_entity(entity)

    return ENTITY_MAP[entity]['key']

def get_entity_table(
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
    validate_entity(entity)
    validate_entity_table(table_name, entity)

    # Fetch entity table name
    entity_table_names = ENTITY_MAP[entity]['tables']

    return entity_table_names
