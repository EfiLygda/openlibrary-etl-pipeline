"""

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from typing import Generic, TypeVar, Optional, TypeAlias
from pydantic import BaseModel

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Primary Entities
# --------------------------------------------------------------------

# --- LEVEL 1: Entities (Works, Authors, Editions) ---
class Work(BaseModel):
    work_key: str
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    first_sentence: Optional[str] = None
    edition_count: Optional[int] = None
    first_publish_year: Optional[int] = None
    first_publish_date: Optional[str] = None

class Author(BaseModel):
    pass

class Edition(BaseModel):
    pass

# --- LEVEL 2: Extensions ---

# - WORKS -
class WorksSeries(BaseModel):
    series_key: Optional[str] = None
    series_position: Optional[int] = None
    series_name: Optional[str] = None

class WorksAvailability(BaseModel):
    ebook_access: Optional[str] = None
    has_fulltext: Optional[bool] = None
    has_public_scan: Optional[bool] = None


# --------------------------------------------------------------------
# Grouped Results
# --------------------------------------------------------------------
class WorkGroup(BaseModel, Generic[T]):
    work_key: str
    record_count: int
    records: list[T]

# --------------------------------------------------------------------
# Entity Summaries
# --------------------------------------------------------------------
class AuthorSummary(BaseModel):
    author_key: str
    author_name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

class EditionSummary(BaseModel):
    edition_key: str
    title: str
    subtitle: Optional[str] = None
    name: Optional[str] = None

# --------------------------------------------------------------------
# Final API response
# --------------------------------------------------------------------
class APIResponse(BaseModel, Generic[T]):
    query: str
    endpoint: str
    method: str
    count: int
    results: list[T]


# --------------------------------------------------------------------
# Aliasing Types
# --------------------------------------------------------------------
# Note: Avoid nesting in routers
WorkAuthors: TypeAlias = WorkGroup[AuthorSummary]
WorkEditions: TypeAlias = WorkGroup[EditionSummary]
WorkSeries: TypeAlias = WorkGroup[WorksSeries]
WorkAvailability: TypeAlias = WorkGroup[WorksAvailability]

