"""
Module for the type definitions of basic entities (works, authors and editions)

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from enum import Enum
from pydantic import BaseModel
from typing import TypeVar, Optional

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Primary Entities
# --------------------------------------------------------------------

# --- Entity Types ---
class EntityType(str, Enum):
    work = 'work'
    author = 'author'
    edition = 'edition'
    # series = 'series'

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
