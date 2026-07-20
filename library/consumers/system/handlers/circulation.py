"""
Event handlers related to library circulation.

Handles events involving lending workflows, such as:
* Borrowing copies
* Returning borrowed copies
* Renewing loans
"""

import json
from datetime import datetime

from library.service.kafka.config import TOPIC
from library.database.handler_queries import execute_handler_query
from library.core.events import EventType, EventTrigger
from library.utils.dates import overdue_days

from library.service.kafka.publisher import emit_event

from library.producer.simulation.event_factory import create_event
from library.producer.simulation.generators.circulation import borrow_available_copy, issue_fine

from library.consumers.system.handlers.paths import CIRCULATION_SQL_DIR
from library.consumers.system.handlers.dependencies import HandlerDependencies

def handle_copy_borrowed(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Inserts new record of a copy's borrowing to the 'loans' table

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: None
    """

    # Generate new copy ID
    new_loan_id = f'LN-{counter}'

    # Move copy id from available to unavailable in Redis
    dependencies.redis_operations.copies.borrow_copy(
        copy_id=event['payload']['copy_id']
    )

    # Create new loan
    dependencies.redis_operations.loans.create_active_loan(
        loan_id=new_loan_id,
        copy_id=event['payload']['copy_id'],
        due_date=event['payload']['due_date']
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='copy_borrowed.sql',
        params={
            'loan_id': new_loan_id,
            'user_id': event['payload']['user_id'],
            'copy_id': event['payload']['copy_id'],

            'borrow_date': event['timestamp'],
            'due_date': event['payload']['due_date'],
            'return_date': None,

            'renewal_count': 0,
            'status': 'ACTIVE', # "ACTIVE | RETURNED"
            'loan_processed_by':  event['payload']['librarian_id']
        }
    )

    # If the event was triggered for fulfilling a reservation
    # then update the reservations table with the new loan ID
    if event.get('trigger') == EventTrigger.RESERVATION_FULFILLMENT:

        # Execute the query
        execute_handler_query(
            connection=dependencies.connection,
            event_category_dir=CIRCULATION_SQL_DIR,
            sql_filename='reservation_fulfillment.sql',
            params={
                'fulfillment_loan_id': new_loan_id,
                'reservation_id': event['payload']['fulfilled_reservation_id']
            }
        )

def fulfill_copy_reservation_on_return(
        dependencies: HandlerDependencies,
        copy_id: str,
        event: dict,
) -> None:
    """
    Updates the 'reservations' table in the database and emits a new borrow event for
    the user that had reserved the returned copy

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param copy_id: str, the returned copy's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Remove and fetch reservation data from the copy's reservation queue
    item = dependencies.redis_operations.reservations.pop_next(
        copy_id=copy_id
    )

    # Load reservation data
    reservation_data = json.loads(item)

    # Unpack reservation ID and user ID
    reservation_id = reservation_data['reservation_id']
    reservation_user_id = reservation_data['user_id']

    # Generate data for the new borrow event
    new_borrow_event_data = borrow_available_copy(
        redis_client=dependencies.redis_operations.client,
        user_id=reservation_user_id,
        copy_id=copy_id,
        fulfilled_reservation_id=reservation_id,
    )

    # Create event envelope
    new_borrow_event = create_event(
        event_type=EventType.COPY_BORROWED,
        timestamp=datetime.fromisoformat(event['timestamp']),
        payload=new_borrow_event_data,
        trigger=EventTrigger.RESERVATION_FULFILLMENT
    )

    # Move reservation id from redis active reservations to fulfilled ids
    dependencies.redis_operations.reservations.fulfill(
        reservation_id=reservation_id
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='fulfill_copy_reservation_on_return.sql',
        params={
            'fulfilled_at': event['timestamp'],
            'reservation_id': reservation_id,
        }
    )

    # Finally emit new borrow event from user that reserved the copy
    emit_event(
        producer=dependencies.chain_event_producer,
        topic=TOPIC,
        event=new_borrow_event
    )

def issue_fine_on_overdue_return(
        dependencies: HandlerDependencies,
        overdue_days_count: int,
        event: dict,
) -> None:
    """
    Emits a new fine issued event for an overdue returned copy.

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param overdue_days_count: int, number of days the returned copy was overdue
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Generate data for the new issued fine event
    new_fine_issued_event_data = issue_fine(
        loan_id=event['payload']['loan_id'],
        overdue_days=overdue_days_count,
    )

    # Create event envelope
    new_fine_issued_event = create_event(
        event_type=EventType.FINE_ISSUED,
        timestamp=datetime.fromisoformat(event['timestamp']),
        payload=new_fine_issued_event_data,
        trigger=EventTrigger.OVERDUE_LOAN_RETURN
    )

    # Finally emit new fine issued event
    emit_event(
        producer=dependencies.chain_event_producer,
        topic=TOPIC,
        event=new_fine_issued_event
    )


def handle_return_borrowed_copy(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Updates the loan's and the respective copy's status in the database

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Fetch the loan it from the even
    loan_id = event['payload']['loan_id']

    # Fetch the copy from the loan's Redis hash
    copy_id = dependencies.redis_operations.loans.get_copy_id(
        loan_id=loan_id
    )

    # Move loan ID from active loans to returned loans set
    dependencies.redis_operations.loans.return_loan(
        loan_id=loan_id
    )

    # Calculate overdue days on return
    due_date = dependencies.redis_operations.loans.get_due_date(loan_id=loan_id)
    return_date = event['timestamp']
    overdue_days_count = overdue_days(due_date, return_date)

    # Check if the return is overdue
    if overdue_days_count > 0:

        # Emit new fine issued event to be handled later on
        issue_fine_on_overdue_return(
            dependencies=dependencies,
            overdue_days_count=overdue_days_count,
            event=event
        )

    # Check if the copy was reserved
    copy_is_reserved = dependencies.redis_operations.copies.has_copy_reservations(
        copy_id=copy_id
    )

    if copy_is_reserved:

        # Update reservations table and emit new borrow event for the user
        # that had reserved the returned copy
        fulfill_copy_reservation_on_return(
            dependencies=dependencies,
            copy_id=copy_id,
            event=event,
        )

        # Have to update that the reservation was fulfilled
        # The current status of the copy
        copy_status = 'UNAVAILABLE'

    else:
        # Move copy id from unavailable to available in Redis
        dependencies.redis_operations.copies.return_copy(
            copy_id=copy_id
        )

        # The current status of the copy
        copy_status = 'AVAILABLE'

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='return_borrowed_copy.sql',
        params={
            'loan_id': loan_id,
            'copy_id': copy_id,
            'return_date': return_date,
            'librarian_id': event['payload']['librarian_id'],
            'status': copy_status
        }
    )

def handle_renewal_of_borrowed_copy(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Updates the loans due date and renewal count in 'loans' table

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Fetch the loan it from the even
    loan_id = event['payload']['loan_id']

    # Add new due date to loan's hash
    new_due_date = dependencies.redis_operations.loans.renew_loan(
        loan_id=loan_id
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='renewal_of_borrowed_copy.sql',
        params={
            'loan_id': loan_id,
            'new_due_date': new_due_date,
        }
    )

def handle_fine_issued(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Creates a new unpaid fine and stores it in the 'fines' table.

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """
    # Generate new fine ID
    new_fine_id = f'FN-{counter}'

    # Create new unpaid fine in redis
    dependencies.redis_operations.fines.issue(
        fine_id=new_fine_id
    )

    # Calculate fine
    fine_amount = event['payload']['overdue_days'] * 0.50

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='fine_issued.sql',
        params={
            'fine_id': new_fine_id,
            'loan_id': event['payload']['loan_id'],
            'overdue_days': event['payload']['overdue_days'],
            'amount': fine_amount,
            'issued_at': event['timestamp'],
            'status': 'UNPAID'
        }
    )

def handle_fine_paid(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Updates the fine in the 'fines' table as paid.

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Move fine from unpaid redis set to paid fines redis set
    dependencies.redis_operations.fines.pay(
        fine_id=event['payload']['fine_id']
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=CIRCULATION_SQL_DIR,
        sql_filename='fine_paid.sql',
        params={
            'fine_id': event['payload']['fine_id'],
            'paid_at': event['timestamp'],
            'status': 'PAID'
        }
    )