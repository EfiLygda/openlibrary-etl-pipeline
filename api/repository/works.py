"""
Database access layer for retrieving work records

This module provides functions for querying the PostgreSQL database
to fetch work-related data
"""

import psycopg2
from api.repository.base import get_by_entity_key

def get_work_by_key(
    connection: psycopg2.extensions.connection,
    work_key: str
) -> tuple:
    """
    """
    return get_by_entity_key(
        connection=connection,
        table_name='works',
        entity='works',
        key=work_key
    )



