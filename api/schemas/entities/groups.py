"""
Module for the type definitions of grouped API responses (deprecated)

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import Generic, TypeVar

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Grouped Results
# --------------------------------------------------------------------
class WorkGroup(BaseModel, Generic[T]):
    work_key: str
    record_count: int
    records: list[T]

class AuthorGroup(BaseModel, Generic[T]):
    author_key: str
    record_count: int
    records: list[T]

class EditionGroup(BaseModel, Generic[T]):
    edition_key: str
    record_count: int
    records: list[T]
