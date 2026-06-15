"""

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

from .entities.core import EntityType

# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')

# --------------------------------------------------------------------
# Final API responses
# --------------------------------------------------------------------

# --- Basic API response ---
class APIResponse(BaseModel, Generic[T]):
    query: str
    endpoint: str
    method: str
    entity_count: int
    results: list[T]

# --- Navigation API response ---
class LinksResponse(BaseModel):
    key: str
    type: Optional[EntityType]
    links: Optional[dict[str, str]]