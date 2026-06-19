"""
Module for the type definitions of API errors

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from enum import Enum
from pydantic import BaseModel
from typing import TypeVar, Optional

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Error responses
# --------------------------------------------------------------------

# - ERROR CODES ENUMERATION -
class ErrorCode(str, Enum):
    LISTING_NOT_SUPPORTED = 'LISTING_NOT_SUPPORTED'
    INVALID_INPUT = 'INVALID_INPUT' # for empty keys or later parameters
    WORK_NOT_FOUND = 'WORK_NOT_FOUND'
    INVALID_WORK_KEY = 'INVALID_WORK_KEY'
    AUTHOR_NOT_FOUND = 'AUTHOR_NOT_FOUND'
    INVALID_AUTHOR_KEY = 'INVALID_AUTHOR_KEY'
    EDITION_NOT_FOUND = 'EDITION_NOT_FOUND'
    INVALID_EDITION_KEY = 'INVALID_EDITION_KEY'
    INVALID_QUERY_COMBINATION = 'INVALID_QUERY_COMBINATION' # for search queries when q is used with other fields

# - BASIC API ERROR RESPONSE -
class APIError(BaseModel):
    error_code: ErrorCode
    message: str
    query: Optional[str] = None
