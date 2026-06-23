"""
Module for the type definitions of API responses

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
    2. APIResponse is deprecated
"""

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from api.schemas.entities.core import EntityType
from api.schemas.links import EntityLinks, RelationshipLinks
from api.schemas.metadata import EntityMeta, RelationshipMeta, SearchMeta

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Final API responses
# --------------------------------------------------------------------

# --- Basic API response ---
class APIResponse(BaseModel, Generic[T]):
    query: str
    self: str
    entity_count: int
    results: list[T]

# --- Links API response ---
class LinksResponse(BaseModel, Generic[T]):
    key: str
    type: Optional[EntityType] = None
    links: Optional[T] = None

# --- Entity Response ---
class EntityResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: EntityMeta # dict[str, EntityType]
    links: EntityLinks # dict[str, str]

# --- Relationship Response ---
class RelationshipResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: RelationshipMeta # dict[str, int]
    links: RelationshipLinks # dict[str, Optional[str]]

# --- Search Response ---
class SearchResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: SearchMeta # dict[str, int]
    links: RelationshipLinks # dict[str, Optional[str]]