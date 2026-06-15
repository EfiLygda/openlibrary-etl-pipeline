"""

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from enum import Enum
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, TypeAlias

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

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
    work: Optional[str]