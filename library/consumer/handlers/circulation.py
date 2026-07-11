"""
Event handlers related to library circulation.

Handles events involving lending workflows, such as:
* Borrowing copies
* Returning borrowed copies
* Renewing loans
"""

import os
import json
from datetime import datetime

import psycopg2

from kafka import KafkaProducer

from config.paths import CONSUMER_SQL_DIR
from library.producer.simulation.event_factory import create_event
from library.producer.simulation.generators.circulation import borrow_available_copy
from library.service.kafka.publisher import emit_event
from library.start_library import TOPIC
from library.utils.dates import add_days_to_str_date
from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient


def handle_copy_borrowed(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> tuple:
    """
    Inserts new record of a copy's borrowing to the 'loans' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new copy ID
    new_loan_id = f'LN-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set(
        RedisKeys.Sets.ACTIVE_LOANS_IDS,
        new_loan_id
    )

    # Setting up loan's hash
    redis_client.add_hash(
        RedisKeys.Hashes.loan(new_loan_id),
        mapping={
            'copy_id': event['data']['copy_id'],
            'due_date': event['data']['due_date'],
            # TODO: Maybe add more
            # 'user_id': None,
        }
    )

    # Move copy id from available to unavailable in Redis
    redis_client.move_sets(
        source=RedisKeys.Sets.AVAILABLE_COPIES_IDS,
        destination=RedisKeys.Sets.UNAVAILABLE_COPIES_IDS,
        value=event['data']['copy_id']
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'insert_loan_update_copies.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'loan_id': new_loan_id,
            'user_id': event['data']['user_id'],
            'copy_id': event['data']['copy_id'],

            'borrow_date': event['timestamp'],
            'due_date': event['data']['due_date'],
            'return_date': None,

            'renewal_count': 0,
            'status': 'ACTIVE', # "ACTIVE | RETURNED"
            'loan_processed_by':  event['data']['librarian_id']
        }
    )

def fulfill_copy_reservation_on_return(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        producer: KafkaProducer,
        copy_id: str,
) -> tuple:
    """
    Updates the 'reservations' table in the database and emits a new borrow event for
    the user that had reserved the returned copy

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param producer: KafkaProducer, producer used for emitting chain events, when needed
    :param copy_id: str, the returned copy's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Remove and fetch reservation data from the copy's reservation queue
    item = redis_client.pop_from_list(
        name=RedisKeys.Queues.reservation_queue(copy_id=copy_id)
    )

    # Load reservation data
    reservation_data = json.loads(item)

    # Unpack reservation ID and user ID
    reservation_id = reservation_data['reservation_id']
    reservation_user_id = reservation_data['user_id']

    # Generate data for the new borrow event
    new_borrow_event_data = borrow_available_copy(
        redis_client=redis_client,
        user_id=reservation_user_id,
        copy_id=copy_id
    )

    # Create event envelope
    new_borrow_event = create_event(
        event_type='BORROW',
        timestamp=datetime.fromisoformat(event['timestamp']),
        data=new_borrow_event_data
    )

    # Emit new borrow event from user that reserved it
    emit_event(
        producer=producer,
        topic=TOPIC,
        event=new_borrow_event
    )

    # Remove reservation id from redis active reservations set
    redis_client.remove_from_set(
        RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
        reservation_id
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'return_reserved_update_reservations.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'fulfilled_at': event['timestamp'],
            'reservation_id': reservation_id,
        }
    )


def handle_return_borrowed_copy(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer,
) -> tuple:
    """
    Updates the loan's and the respective copy's status in the database

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Fetch the loan it from the even
    loan_id = event['data']['loan_id']

    # Fetch the copy from the loan's Redis hash
    copy_id = str(
        redis_client.get_from_hash(
            name=RedisKeys.Hashes.loan(loan_id),
            key='copy_id'
        )
    )

    # Move loan ID from active loans to returned loans set
    redis_client.move_sets(
        RedisKeys.Sets.ACTIVE_LOANS_IDS,
        RedisKeys.Sets.RETURNED_LOANS_IDS,
        loan_id
    )

    # Check if the copy was reserved
    copy_is_reserved = redis_client.length_of_list(
            RedisKeys.Queues.reservation_queue(copy_id)
    ) > 0

    if copy_is_reserved:

        # Update reservations table and emit new borrow event for the user
        # that had reserved the returned copy
        fulfill_copy_reservation_on_return(
            connection=connection,
            redis_client=redis_client,
            event=event,
            producer=producer,
            copy_id=copy_id,
        )

        # Have to update that the reservation was fulfilled
        # The current status of the copy
        copy_status = 'UNAVAILABLE'

    else:
        # Move copy id from unavailable to available in Redis
        redis_client.move_sets(
            source=RedisKeys.Sets.UNAVAILABLE_COPIES_IDS,
            destination=RedisKeys.Sets.AVAILABLE_COPIES_IDS,
            value=copy_id
        )

        # The current status of the copy
        copy_status = 'AVAILABLE'

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'return_update_loans_update_copies.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'loan_id': loan_id,
            'copy_id': copy_id,
            'return_date': event['timestamp'],
            'librarian_id': event['data']['librarian_id'],
            'status': copy_status
        }
    )

def handle_renewal_of_borrowed_copy(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> tuple:
    """
    Updates the loans due date and renewal count in 'loans' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Fetch the loan it from the even
    loan_id = event['data']['loan_id']

    # Build new due date after renewal
    new_due_date = add_days_to_str_date(
        date=str(
            redis_client.get_from_hash(
                name=RedisKeys.Hashes.loan(loan_id),
                key='due_date'
            )
        ),
        days=7
    )

    # Add new due date to loan's hash
    redis_client.set_in_hash(
        name=RedisKeys.Hashes.loan(loan_id),
        key='due_date',
        value=new_due_date
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'renewal_update_loans.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'loan_id': loan_id,
            'new_due_date': new_due_date,
        }
    )