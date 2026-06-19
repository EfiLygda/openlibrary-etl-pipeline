"""
Module for the type definitions of API main entity summaries

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import TypeVar, Optional

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Entity Summaries
# --------------------------------------------------------------------

class WorkSummary(BaseModel):
    work_key: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    edition_count: Optional[int] = None
    first_publish_year: Optional[int] = None

class AuthorSummary(BaseModel):
    author_key: Optional[str] = None
    author_name: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

class EditionSummary(BaseModel):
    edition_key: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    edition_name: Optional[str] = None