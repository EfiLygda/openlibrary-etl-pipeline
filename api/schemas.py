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
    author_key: str
    author_name: str
    bio: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

class Edition(BaseModel):
    edition_key: str
    work_key: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    edition_name: Optional[str] = None

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

class WorksRatings(BaseModel):
    ratings_count_1: Optional[int]
    ratings_count_2: Optional[int]
    ratings_count_3: Optional[int]
    ratings_count_4: Optional[int]
    ratings_count_5: Optional[int]

class WorksOverview(BaseModel):
    subjects: Optional[list[str]]
    people: Optional[list[str]]
    places: Optional[list[str]]
    time_periods: Optional[list[str]]

# - AUTHORS -
class AuthorsStatistics(BaseModel):
    top_work: Optional[str] = None
    work_count: int

    ratings_count_1: int
    ratings_count_2: int
    ratings_count_3: int
    ratings_count_4: int
    ratings_count_5: int

    readinglog_count: int
    want_to_read_count: int
    currently_reading_count: int
    already_read_count: int

# - EDITIONS -
class EditionDetails(BaseModel):
    edition_key: str
    number_of_pages: Optional[int] = None
    physical_format: Optional[str] = None
    physical_dimensions: Optional[str] = None
    weight: Optional[str] = None
    language: Optional[str] = None

class EditionContents(BaseModel):
    edition_key: str
    description: Optional[str] = None
    notes: Optional[str] = None
    first_sentence: Optional[str] = None

class EditionsPublishing(BaseModel):
    publish_date: Optional[str] = None
    publish_year: Optional[int] = None
    publisher: Optional[str] = None
    publish_place: Optional[str] = None
    publish_country: Optional[str] = None
    series_title: Optional[str] = None

# class EditionContributor(BaseModel):
#     edition_key: str
#     contributor_name: str
#     contributor_role: str
#     by_statement: Optional[str] = None
#     translated_from: Optional[str] = None
#     translation_of: Optional[str] = None

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

# --------------------------------------------------------------------
# Entity Summaries
# --------------------------------------------------------------------

class WorkSummary(BaseModel):
    work_key: str
    title: str
    subtitle: Optional[str] = None
    edition_count: Optional[int] = None
    first_publish_year: Optional[int] = None

class AuthorSummary(BaseModel):
    author_key: str
    author_name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

class EditionSummary(BaseModel):
    edition_key: str
    title: str
    subtitle: Optional[str] = None
    edition_name: Optional[str] = None

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

# - WORKS -
WorkAuthors: TypeAlias = WorkGroup[AuthorSummary]
WorkEditions: TypeAlias = WorkGroup[EditionSummary]
WorkSeries: TypeAlias = WorkGroup[WorksSeries]
WorkAvailability: TypeAlias = WorkGroup[WorksAvailability]
WorkOverview: TypeAlias = WorkGroup[WorksOverview]
WorkRatings: TypeAlias = WorkGroup[WorksRatings]

# - AUTHORS -
AuthorWorks: TypeAlias = AuthorGroup[WorkSummary]
AuthorStatistics: TypeAlias = AuthorGroup[AuthorsStatistics]
AuthorAlternativeNames: TypeAlias = AuthorGroup[str]
AuthorEditions: TypeAlias = AuthorGroup[EditionSummary]

# - EDITIONS -
EditionPublishing: TypeAlias = EditionGroup[EditionsPublishing]
