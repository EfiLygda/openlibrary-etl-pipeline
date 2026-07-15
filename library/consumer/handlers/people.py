"""
Event handlers related to people in the library system

Handles events involving users and librarians, such as:
* User registration
* Librarian hiring
"""

import psycopg2
from kafka import KafkaProducer

from library.service.redis.operations.registry import RedisOperations
from library.consumer.handlers.paths import PEOPLE_SQL_DIR
from library.database.handler_queries import execute_handler_query


def handle_librarian_hired(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Inserts new hired librarian record to the 'librarians' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Generate new librarian ID
    new_librarian_id = f'LB-{counter}'

    # Add new ID to Redis set to be used later
    redis_operations.librarians.register_librarian(
        librarian_id=new_librarian_id
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=PEOPLE_SQL_DIR,
        sql_filename='librarian_hired.sql',
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
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Inserts new registered user record to the 'users' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Generate new user ID
    new_user_id = f'USR-{counter}'

    # Add new ID to Redis set to be used later
    redis_operations.users.register_user(
        user_id=new_user_id
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=PEOPLE_SQL_DIR,
        sql_filename='user_registered.sql',
        params={
            'user_id': new_user_id,
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )
