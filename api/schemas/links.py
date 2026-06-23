"""
Module for the type definitions of API links fields

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import TypeVar, Optional, TypeAlias

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Response Links
# --------------------------------------------------------------------

# --- Self Response Link ---
class SelfLink(BaseModel):
    self: str

# --- Pagination Response Links ---
class PaginationLinks(BaseModel):
    self: str
    next: Optional[str]
    prev: Optional[str]

# --------------------------------------------------------------------
# Entity Navigation
# --------------------------------------------------------------------

class WorkLinks(BaseModel):
    self: str
    authors: Optional[str]
    editions: Optional[str]
    series: Optional[str] = None
    ratings: Optional[str] = None
    overview: Optional[str] = None
    availability: Optional[str] = None

class AuthorLinks(BaseModel):
    self: str
    works: Optional[str]
    editions: Optional[str]
    statistics: Optional[str]
    alternative_names: Optional[str]

class EditionLinks(BaseModel):
    self: str
    details: Optional[str]
    contents: Optional[str]
    publishing: Optional[str]
    contributors: Optional[str]
    works: Optional[str]

# --------------------------------------------------------------------
# Aliasing Types
# --------------------------------------------------------------------

Link: TypeAlias = WorkLinks | AuthorLinks | EditionLinks | None