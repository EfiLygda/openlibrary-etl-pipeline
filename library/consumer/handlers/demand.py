"""
Event handlers related to library demand.

Handles events representing user intent to access unavailable resources, such as:
* Reservation requests
"""

from library.consumer.handlers.paths import DEMAND_SQL_DIR
from library.consumer.handlers.dependencies import HandlerDependencies
from library.database.handler_queries import execute_handler_query


def handle_reservation_of_unavailable_copy(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Inserts new record at 'reservations' table

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Generate new copy ID
    new_reservation_id = f'RSRV-{counter}'

    # Add to active reservations keys
    dependencies.redis_operations.reservations.create_reservation(
        reservation_id=new_reservation_id,
        copy_id=event['data']['copy_id'],
        user_id=event['data']['user_id']
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
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
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Updates reservations table after a cancellation

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Canceled reservation ID
    cancelled_reservation_id = event['data']['reservation_id']

    # Cancel the reservation in Redis
    dependencies.redis_operations.reservations.cancel(
        reservation_id=cancelled_reservation_id
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=DEMAND_SQL_DIR,
        sql_filename='cancellation_of_active_reservation.sql',
        params={
            "reservation_id": cancelled_reservation_id,
            "cancelled_at": event['timestamp'],
            "status": 'CANCELLED',
        }
    )
