"""
Event handlers related to library demand.

Handles events representing user intent to access unavailable resources, such as:
* Reservation requests
"""

import os
import psycopg2

from config.paths import CONSUMER_SQL_DIR
from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.service import RedisClient

def handle_reservation_of_unavailable_copy(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Inserts new record at 'reservations' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new copy ID
    new_reservation_id = f'RSRV-{counter}'

    # Add to active reservations keys
    redis_client.add_to_set(
        RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
        new_reservation_id
    )

    # Add user to copy's reservation queue
    redis_client.add_to_list(
        RedisKeys.Queues.reservation_queue(event['data']['copy_id']),
        event['data']['user_id']
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'insert_reservation.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            "reservation_id": new_reservation_id,
            "user_id": event['data']['user_id'],
            "copy_id": event['data']['copy_id'],
            "reserved_at": event['timestamp'],
            "fulfilled_at": None,
            "cancelled_at": None,
            "status": 'ACTIVE', # 'ACTIVE', 'FULFILLED', 'CANCELLED', 'EXPIRED'
        }
    )