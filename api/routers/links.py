"""
Navigation Router

Endpoints:

"""

import psycopg2

from fastapi import APIRouter

from open_library import KeyHandler

from api.dependencies import DB_DEPENDENCY
import api.repository.navigation as navigation_repo
from api.response_builders.links import format_response
from api.errors import BaseErrors, LinksErrors
from api.schemas.entities.core import EntityType
from api.schemas.links import Link
from api.schemas.responses import LinksResponse

# --- Defining the editions router ---
router = APIRouter(
    prefix="/links",
    tags=["Links"]
)

# --- Defining all endpoints ---
@router.get("/",  responses={'405': BaseErrors.ListingNotSupported.response})
async def links_root() -> None:
    """
    Root endpoint for the links collection

    This endpoint is intentionally not supported for listing operations

    It exists to explicitly reject requests made to `/links/` without a
    valid `key`, and returns a standardized error response
    """
    raise BaseErrors.ListingNotSupported(query="/links/")


@router.get(
    path="/{key}",
    response_model=LinksResponse[Link],
    responses={
        '404': LinksErrors.NotFound.response,
        '422': LinksErrors.InvalidKey.response
    }
)
async def get_links_by_key(
        key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> LinksResponse[Link]:
    """
    Retrieve a record's links by **key**.

    Returns a standardized response dictionary containing:

    - **key**: the provided key
    - **type**: the provided key's entity (work, author or edition)
    - **links**: dictionary with the records API's navigation links
    """

    # Current query
    query = f'/{key}'

    # Find the current key's type
    raw_key_type = KeyHandler.detect_key(key)

    # Attempt to convert raw input into a valid EntityType enum member
    # This ensures the value is one of the allowed types (work, author, edition)
    # Else raises Invalid Key Error
    try:
        key_type = EntityType(raw_key_type)
    except ValueError as e:
        raise LinksErrors.InvalidKey(query) from e

    # Check if key exists in its entity table
    key_exists = navigation_repo.exists_with_filter_key_by_entity_type(connection, key, key_type)

    # If key does not exist in its entity table then error is raised
    if not key_exists:
        raise LinksErrors.NotFound(query)

    # Format and return consistent Links response structure
    return format_response(
        key=key,
        key_type=key_type
    )
