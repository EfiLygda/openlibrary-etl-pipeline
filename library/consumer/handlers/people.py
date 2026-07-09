"""
Event handlers related to people in the library system

Handles events involving users and librarians, such as:
* User registration
* Librarian hiring
"""

import os
import psycopg2

from kafka import KafkaProducer

from config.paths import CONSUMER_SQL_DIR
from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient

def handle_librarian_hired(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> tuple:
    """
    Inserts new hired librarian record to the 'librarians' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new librarian ID
    new_librarian_id = f'LB-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set(
        RedisKeys.Sets.LIBRARIAN_IDS,
        new_librarian_id
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'insert_librarian.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'librarian_id': new_librarian_id,
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )

def handle_user_registered(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> tuple:
    """
    Inserts new registered user record to the 'users' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new user ID
    new_user_id = f'USR-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set(
        RedisKeys.Sets.USER_IDS,
        new_user_id
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'insert_user.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'user_id': new_user_id,
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )