"""
Module responsible for dispatching events to their corresponding handlers
"""

from library.core.registry import EVENTS
from library.consumer.handlers.dependencies import HandlerDependencies

def handle_event(
        dependencies: HandlerDependencies,
        event: dict,
) -> None:
    """
    Function for handling all events regardless of type, by inserting new records

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Save event type
    event_type = event['event_type']

    # Fetch event spec
    event_spec = EVENTS[event_type]

    # Get the current event's counter name and its key (if the counter is in a hash)
    # for Redis
    counter_name = event_spec.counter_name
    counter_hash_key = event_spec.get_counter_hash_key(event)

    # Increment event counter
    counter = dependencies.redis_operations.client.counters.increment(
        name=counter_name,
        key=counter_hash_key
    )

    return event_spec.handler(
        dependencies=dependencies,
        counter=counter,
        event=event,
    )
