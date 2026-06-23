"""
Module for validating Open Library entity keys
"""

from open_library import KeyHandler
from api.errors import WorksErrors, AuthorsErrors, EditionsErrors

_Errors = {
    'work': WorksErrors,
    'author': AuthorsErrors,
    'edition': EditionsErrors
}

def validate_key(
        key: str,
        entity_type: str,
        query: str
) -> None:
    """
    Validate that a key matches the expected entity type by raising appropriate entity error

    :param key: Open Library key to validate
    :param entity_type: Expected entity type (work, author or edition)
    :param query: Original request query used in error messages
    :return: None
    """
    if KeyHandler.detect_key(key) != entity_type:
        raise _Errors[entity_type].InvalidKey(query)
