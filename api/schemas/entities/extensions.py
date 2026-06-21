"""
Module for the type definitions of extensions of basic entity types (i.e. a work's series -> WorkSeries)

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import TypeVar, Optional

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

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
    work_count: Optional[int]

    ratings_count_1: Optional[int]
    ratings_count_2: Optional[int]
    ratings_count_3: Optional[int]
    ratings_count_4: Optional[int]
    ratings_count_5: Optional[int]

    readinglog_count: Optional[int]
    want_to_read_count: Optional[int]
    currently_reading_count: Optional[int]
    already_read_count: Optional[int]

class AuthorAlternativeNames(BaseModel):
    author_alternative_names: Optional[list[str]]

# - EDITIONS -
class EditionDetails(BaseModel):
    number_of_pages: Optional[int] = None
    physical_format: Optional[str] = None
    physical_dimensions: Optional[str] = None
    weight: Optional[str] = None
    language: Optional[str] = None

class EditionContents(BaseModel):
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