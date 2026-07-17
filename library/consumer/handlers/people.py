"""
Event handlers related to people in the library system

Handles events involving users and librarians, such as:
* User registration
* Librarian hiring
"""

from library.consumer.handlers.paths import PEOPLE_SQL_DIR
from library.consumer.handlers.dependencies import HandlerDependencies
from library.database.handler_queries import execute_handler_query

def handle_librarian_hired(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Inserts new hired librarian record to the 'librarians' table

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Generate new librarian ID
    new_librarian_id = f'LB-{counter}'

    # Add new ID to Redis set to be used later
    dependencies.redis_operations.librarians.register_librarian(
        librarian_id=new_librarian_id
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
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
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Inserts new registered user record to the 'users' table

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Generate new user ID
    new_user_id = f'USR-{counter}'

    # Add new ID to Redis set to be used later
    dependencies.redis_operations.users.register_user(
        user_id=new_user_id
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
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
