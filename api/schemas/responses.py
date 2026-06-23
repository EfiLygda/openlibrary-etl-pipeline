"""
Module for the type definitions of API responses

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
    2. APIResponse is deprecated
"""

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from api.schemas.entities.core import EntityType
from api.schemas.links import SelfLink, PaginationLinks
from api.schemas.metadata import EntityMeta, RelationshipMeta, SearchMeta, BatchMeta

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Final API responses
# --------------------------------------------------------------------

# --- Search Response ---
class SearchResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: SearchMeta
    links: PaginationLinks

# --- Entity Response ---
class EntityResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: EntityMeta
    links: SelfLink

# --- Relationship Response ---
class RelationshipResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: RelationshipMeta
    links: PaginationLinks

# --- Batch Response ---
class BatchResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: BatchMeta
    links: PaginationLinks

# --- Links API response ---
class LinksResponse(BaseModel, Generic[T]):
    key: str
    type: Optional[EntityType] = None
    links: Optional[T] = None
