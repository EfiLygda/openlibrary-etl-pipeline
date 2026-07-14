"""
Event handlers related to library demand.

Handles events representing user intent to access unavailable resources, such as:
* Reservation requests
"""

import os
import json

import psycopg2
from kafka import KafkaProducer

from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient

from library.consumer.handlers.paths import DEMAND_SQL_DIR

def handle_reservation_of_unavailable_copy(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Inserts new record at 'reservations' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Generate new copy ID
    new_reservation_id = f'RSRV-{counter}'

    # Add to active reservations keys
    redis_client.sets.add(
        RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
        new_reservation_id
    )

    # Add reservation ID and user ID to copy's reservation queue
    queue_data = {
        'reservation_id': new_reservation_id,
        'user_id': event['data']['user_id'],
    }

    redis_client.lists.add_to_list(
        RedisKeys.Queues.reservation_queue(event['data']['copy_id']),
        json.dumps(queue_data)
    )

    # Make a reservation hash with data
    redis_client.hashes.add_hash(
        RedisKeys.Hashes.reservation(new_reservation_id),
        mapping={
            'copy_id': event['data']['copy_id'],
            'user_id': event['data']['user_id'],
            # TODO: Maybe add more
            # 'user_id': None,
        }
    )

    # Setting up the loading query
    query_filepath = os.path.join(DEMAND_SQL_DIR, 'reservation_of_unavailable_copy.sql')

    # Execute the query
    execute_query(
        connection=connection,
        query_filepath=query_filepath,
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
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Updates reservations table after a cancellation

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Canceled reservation ID
    cancelled_reservation_id = event['data']['reservation_id']

    # The copy id from the canceled reservation
    copy_id = redis_client.hashes.get_from_hash(
        name=RedisKeys.Hashes.reservation(cancelled_reservation_id),
        key='copy_id'
    )

    # The user id from the canceled reservation
    user_id = redis_client.hashes.get_from_hash(
        name=RedisKeys.Hashes.reservation(cancelled_reservation_id),
        key='user_id'
    )

    # Move to canceled reservation ids
    redis_client.sets.move(
        source=RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
        destination=RedisKeys.Sets.CANCELLED_RESERVATIONS_IDS,
        value=cancelled_reservation_id
    )

    # Remove the reservation from the queue
    queue_item = json.dumps({
        "reservation_id": cancelled_reservation_id,
        "user_id": user_id,
    })

    # Remove the reservation from the copy's reservation queue
    redis_client.lists.remove_from_list(
        name=RedisKeys.Queues.reservation_queue(copy_id),
        value=queue_item
    )

    # Setting up the loading query
    query_filepath = os.path.join(DEMAND_SQL_DIR, 'cancellation_of_active_reservation.sql')

    # Execute the query
    execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            "reservation_id": cancelled_reservation_id,
            "cancelled_at": event['timestamp'],
            "status": 'CANCELLED',
        }
    )
