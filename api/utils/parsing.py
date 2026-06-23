"""
Utilities for parsing entity key query parameters.
"""

def parse_entity_keys(keys: str | None) -> list[str]:
    """
    Parse a comma-separated string of entity keys

    Leading and trailing whitespace is removed from each key and
    empty values are discarded

    :param keys: str, comma-separated keys or None

    :returns: list[str], list of normalized keys
    """
    if not keys:
        return []

    return [
        key.strip()
        for key in keys.split(',')
        if key.strip()
    ]