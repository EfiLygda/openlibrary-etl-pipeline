"""

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from api.schemas.entities.core import EntityType

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
    meta: dict[str, EntityType]
    links: dict[str, str]

# --- Relationship Response ---
class RelationshipResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: dict[str, int]
    links: dict[str, Optional[str]]
