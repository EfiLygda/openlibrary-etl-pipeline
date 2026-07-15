"""
Event handlers related to library demand.

Handles events representing user intent to access unavailable resources, such as:
* Reservation requests
"""

import json
import psycopg2
from kafka import KafkaProducer

from library.service.redis.keys import RedisKeys
from library.service.redis.operations.registry import RedisOperations

from library.consumer.handlers.paths import DEMAND_SQL_DIR
from library.database.handler_queries import execute_handler_query


def handle_reservation_of_unavailable_copy(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Inserts new record at 'reservations' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Generate new copy ID
    new_reservation_id = f'RSRV-{counter}'

    # Add to active reservations keys
    redis_operations.reservations.create_reservation(
        reservation_id=new_reservation_id,
        copy_id=event['data']['copy_id'],
        user_id=event['data']['user_id']
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=DEMAND_SQL_DIR,
        sql_filename='reservation_of_unavailable_copy.sql',
        params={
            "reservation_id": new_reservation_id,
            "user_id": event['data']['user_id'],
            "copy_id": event['data']['copy_id'],
            "reserved_at": event['timestamp'],
            "fulfilled_at": None,
            "cancelled_at": None,
            "status": 'ACTIVE',
        }
    )


def handle_cancellation_of_active_reservation(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Updates reservations table after a cancellation

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Canceled reservation ID
    cancelled_reservation_id = event['data']['reservation_id']

    # Cancel the reservation in Redis
    redis_operations.reservations.cancel(
        reservation_id=cancelled_reservation_id
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=DEMAND_SQL_DIR,
        sql_filename='cancellation_of_active_reservation.sql',
        params={
            "reservation_id": cancelled_reservation_id,
            "cancelled_at": event['timestamp'],
            "status": 'CANCELLED',
        }
    )
