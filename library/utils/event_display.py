"""
Module for displaying events
"""

import json

def print_event(
        source: str,
        event: dict,
        indent: int = 4,
) -> None:
    """
    Pretty-prints an event to the console.

    The event is displayed in JSON format together with the name of the
    component that produced the output (for example, the producer or the
    consumer).

    :param source: str, the name of the component printing the event
    :param event: dict, the event to display
    :param indent: int, the indentation level used for JSON formatting

    :return: None
    """
    print(100*'=')
    print(f"[{source}] {event['event_type']}")
    print(json.dumps(event, indent=indent))
