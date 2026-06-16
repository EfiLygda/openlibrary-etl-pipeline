"""
Transformation utilities for formatting database entity search query results
"""

from typing import TypeVar, Type
from pydantic import BaseModel

from api.schemas.entities.core import EntityType
from api.schemas.responses import APIResponse, LinksResponse

T = TypeVar('T', bound=BaseModel)

# -------------------------------------------------------------------
# Search API Response
# -------------------------------------------------------------------

