"""
Module for the type definitions of metadata in entity and relationship
`meta` (metadata) fields
"""

from pydantic import BaseModel
from typing import TypeVar

from api.schemas.entities.core import EntityType

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --- Entity Response Metadata ---
class EntityMeta(BaseModel):
    type: EntityType

# --- Relationship Response Metadata ---
class RelationshipMeta(BaseModel):
    total: int = 0
    limit: int = 0
    offset: int = 0
