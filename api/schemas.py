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
class WorkSeries(BaseModel):
    series_key: Optional[str] = None
    series_position: Optional[int] = None
    series_name: Optional[str] = None

class WorkAvailability(BaseModel):
    ebook_access: Optional[str] = None
    has_fulltext: Optional[bool] = None
    has_public_scan: Optional[bool] = None

class WorkRatings(BaseModel):
    ratings_count_1: Optional[int]
    ratings_count_2: Optional[int]
    ratings_count_3: Optional[int]
    ratings_count_4: Optional[int]
    ratings_count_5: Optional[int]

class WorkOverview(BaseModel):
    subjects: Optional[list[str]]
    people: Optional[list[str]]
    places: Optional[list[str]]
    time_periods: Optional[list[str]]

# - AUTHORS -
class AuthorStatistics(BaseModel):
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

class EditionPublishing(BaseModel):
    publish_date: Optional[str] = None
    publish_year: Optional[int] = None
    publisher: Optional[str] = None
    publish_place: Optional[str] = None
    publish_country: Optional[str] = None
    series_title: Optional[str] = None

class EditionContributor(BaseModel):
    contributor_name: Optional[str] = None
    contributor_role: Optional[str] = None
    by_statement: Optional[str] = None
    translated_from: Optional[str] = None
    translation_of: Optional[str] = None

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

# - BASIC API ERROR RESPONSE -
class APIError(BaseModel):
    error_code: ErrorCode
    message: str
    query: Optional[str] = None

# --------------------------------------------------------------------
# Aliasing Types
# --------------------------------------------------------------------
# Note: Avoid nesting in routers

# - WORKS -
WorksAuthors: TypeAlias = WorkGroup[AuthorSummary]
WorksEditions: TypeAlias = WorkGroup[EditionSummary]
WorksSeries: TypeAlias = WorkGroup[WorkSeries]
WorksAvailability: TypeAlias = WorkGroup[WorkAvailability]
WorksOverview: TypeAlias = WorkGroup[WorkOverview]
WorksRatings: TypeAlias = WorkGroup[WorkRatings]

# - AUTHORS -
AuthorsWorks: TypeAlias = AuthorGroup[WorkSummary]
AuthorsStatistics: TypeAlias = AuthorGroup[AuthorStatistics]
AuthorsAlternativeNames: TypeAlias = AuthorGroup[str]
AuthorsEditions: TypeAlias = AuthorGroup[EditionSummary]

# - EDITIONS -
EditionsPublishing: TypeAlias = EditionGroup[EditionPublishing]
EditionsContributors: TypeAlias = EditionGroup[EditionContributor]
