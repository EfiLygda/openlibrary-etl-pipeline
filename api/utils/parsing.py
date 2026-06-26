"""
Utilities for parsing entity key query parameters.
"""

def parse_comma_separated_text(comma_separated_text: str | None) -> list[str]:
    """
    Parse a comma-separated string of entity keys

    Leading and trailing whitespace is removed from each key and
    empty values are discarded

    :param comma_separated_text: str, comma-separated keys or None

    :returns: list[str], list of normalized keys
    """
    if not comma_separated_text:
        return []

    # Make list of striped keys
    normalized_text = [
        key.strip()
        for key in comma_separated_text.split(',')
        if key.strip()
    ]

    # Remove duplicates by keeping original order
    removed_duplicates = list(dict.fromkeys(normalized_text))

    return removed_duplicates