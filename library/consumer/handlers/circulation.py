"""
Event handlers related to library circulation.

Handles events involving lending workflows, such as:
* Borrowing copies
* Returning borrowed copies
* Renewing loans
"""

import json
from datetime import datetime

import psycopg2
from kafka import KafkaProducer

from library.start_library import TOPIC
from library.database.handler_queries import execute_handler_query
from library.core.events import EventType, EventTrigger

from library.service.redis.operations.registry import RedisOperations

from library.service.kafka.publisher import emit_event

from library.producer.simulation.event_factory import create_event
from library.producer.simulation.generators.circulation import borrow_available_copy

from library.consumer.handlers.paths import CIRCULATION_SQL_DIR

def handle_copy_borrowed(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Inserts new record of a copy's borrowing to the 'loans' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Generate new copy ID
    new_loan_id = f'LN-{counter}'

    # Move copy id from available to unavailable in Redis
    redis_operations.copies.borrow_copy(
        copy_id=event['data']['copy_id']
    )

    # Create new loan
    redis_operations.loans.create_active_loan(
        loan_id=new_loan_id,
        copy_id=event['data']['copy_id'],
        due_date=event['data']['due_date']
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='copy_borrowed.sql',
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

    # If the event was triggered for fulfilling a reservation
    # then update the reservations table with the new loan ID
    if event.get('trigger') == EventTrigger.RESERVATION_FULFILLMENT:

        # Execute the query
        execute_handler_query(
            connection=connection,
            event_category_dir=CIRCULATION_SQL_DIR,
            sql_filename='reservation_fulfillment.sql',
            params={
                'fulfillment_loan_id': new_loan_id,
                'reservation_id': event['data']['fulfilled_reservation_id']
            }
        )


def fulfill_copy_reservation_on_return(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        producer: KafkaProducer,
        copy_id: str,
) -> None:
    """
    Updates the 'reservations' table in the database and emits a new borrow event for
    the user that had reserved the returned copy

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param producer: KafkaProducer, producer used for emitting chain events, when needed
    :param copy_id: str, the returned copy's ID

    :return: None
    """

    # Remove and fetch reservation data from the copy's reservation queue
    item = redis_operations.reservations.pop_next(
        copy_id=copy_id
    )

    # Load reservation data
    reservation_data = json.loads(item)

    # Unpack reservation ID and user ID
    reservation_id = reservation_data['reservation_id']
    reservation_user_id = reservation_data['user_id']

    # Generate data for the new borrow event
    new_borrow_event_data = borrow_available_copy(
        redis_client=redis_operations.client,
        user_id=reservation_user_id,
        copy_id=copy_id,
        fulfilled_reservation_id=reservation_id,
    )

    # Create event envelope
    new_borrow_event = create_event(
        event_type=EventType.COPY_BORROWED,
        timestamp=datetime.fromisoformat(event['timestamp']),
        data=new_borrow_event_data,
        trigger=EventTrigger.RESERVATION_FULFILLMENT
    )

    # Move reservation id from redis active reservations to fulfilled ids
    redis_operations.reservations.fulfill(
        reservation_id=reservation_id
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='fulfill_copy_reservation_on_return.sql',
        params={
            'fulfilled_at': event['timestamp'],
            'reservation_id': reservation_id,
        }
    )

    # Finally emit new borrow event from user that reserved the copy
    emit_event(
        producer=producer,
        topic=TOPIC,
        event=new_borrow_event
    )

def handle_return_borrowed_copy(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer,
) -> None:
    """
    Updates the loan's and the respective copy's status in the database

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Fetch the loan it from the even
    loan_id = event['data']['loan_id']

    # Fetch the copy from the loan's Redis hash
    copy_id = redis_operations.loans.get_copy_id(
        loan_id=loan_id
    )

    # Move loan ID from active loans to returned loans set
    redis_operations.loans.return_loan(
        loan_id=loan_id
    )

    # Check if the copy was reserved
    copy_is_reserved = redis_operations.copies.has_copy_reservations(
        copy_id=copy_id
    )

    if copy_is_reserved:

        # Update reservations table and emit new borrow event for the user
        # that had reserved the returned copy
        fulfill_copy_reservation_on_return(
            connection=connection,
            redis_operations=redis_operations,
            event=event,
            producer=producer,
            copy_id=copy_id,
        )

        # Have to update that the reservation was fulfilled
        # The current status of the copy
        copy_status = 'UNAVAILABLE'

    else:
        # Move copy id from unavailable to available in Redis
        redis_operations.copies.return_copy(
            copy_id=copy_id
        )

        # The current status of the copy
        copy_status = 'AVAILABLE'

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='return_borrowed_copy.sql',
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
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Updates the loans due date and renewal count in 'loans' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Fetch the loan it from the even
    loan_id = event['data']['loan_id']

    # Add new due date to loan's hash
    new_due_date = redis_operations.loans.renew_loan(
        loan_id=loan_id
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='renewal_of_borrowed_copy.sql',
        params={
            'loan_id': loan_id,
            'new_due_date': new_due_date,
        }
    )
