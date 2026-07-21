"""
Module for displaying events
"""

from rich.json import JSON
from rich.console import Console

# Set up a rich console for using colours
RICH_CONSOLE = Console(force_terminal=True)

# Dictionary with the colours used for each displayed event
CONSOLE_COLOURS = {
    "PRODUCER": "green",
    "SYSTEM_CONSUMER": "cyan",
    "REJECTED": "red",
    "SYSTEM_CONSUMER_PROCESSING_ERROR": "red",
}

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

    # Fetch the colour to use or use white as default
    color = CONSOLE_COLOURS.get(source, "white")

    # Print event header
    RICH_CONSOLE.print(f"[bold {color}][{source}] {event['event_type']} [/bold {color}]")

    # Print event using rich's JSON predetermined format
    RICH_CONSOLE.print(
        JSON.from_data(
            data=event,
            indent=indent,
        )
    )

    # Print final new line
    RICH_CONSOLE.print()

