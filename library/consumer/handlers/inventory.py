"""
Event handlers related to library inventory.

Handles events involving physical copies of works, such as:
* Copy purchases
"""

import os
import psycopg2

from config.paths import CONSUMER_SQL_DIR
from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.service import RedisClient


def handle_copy_purchased(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Inserts new purchased copy record to the 'copies' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new copy ID
    new_copy_id = f'{event['data']['edition_key']}-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set(
        RedisKeys.Sets.AVAILABLE_COPIES_IDS,
        new_copy_id
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'insert_copy.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'copy_id': new_copy_id,
            'edition_key': event['data']['edition_key'],
            'status': 'AVAILABLE',
            'registered_at': event['timestamp'],
        }
    )