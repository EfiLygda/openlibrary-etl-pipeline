"""
Editions Router

This module defines API endpoints related to "editions", including retrieval of
edition records and associated metadata such as detailed information, contents,
publishing data, and contributors.

Endpoints:
- GET /editions/
  Retrieve all editions' related metadata via their edition key

- GET /editions/{edition_key}
  Retrieve edition records by edition_key

- GET /editions/{edition_key}/works
  Retrieve work records by edition_key

- GET /editions/{edition_key}/details
  Retrieve detailed edition metadata by edition_key, including structured descriptive fields

- GET /editions/{edition_key}/contents
  Retrieve edition contents by edition_key, such as table of contents or structured content data

- GET /editions/{edition_key}/publishing
  Retrieve publishing information for an edition, including publication metadata and related records

- GET /editions/{edition_key}/contributors
  Retrieve contributors associated with an edition, such as authors, editors, and other collaborators
"""

import os
from dotenv import load_dotenv

import psycopg2

from fastapi import APIRouter
from fastapi import Request

from api.dependencies import DB_DEPENDENCY

from api.errors import BaseErrors, EditionsErrors

from api.schemas.entities.core import Edition
from api.schemas.entities.summaries import WorkSummary
from api.schemas.entities.relationships import EditionDetails, EditionContents, EditionPublishing, EditionContributor
from api.schemas.responses import EntityResponse, RelationshipResponse, BatchResponse

from api.service.batches import batch_service
from api.service.entities import entity_service
from api.service.relationships import relationship_service

# -----------------------------------------------------------------------------
# --- Load API LIMIT from environment variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
API_LIMIT = int(os.getenv("API_LIMIT"))
OFFSET = 0
ENTITY_TYPE = 'edition'
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining the editions router ---
router = APIRouter(
    prefix="/editions",
    tags=["Editions"]
)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining all endpoints ---
@router.get(
    path="",
    response_model=BatchResponse[Edition],
    responses={
        '404': EditionsErrors.NotFound.response,
        '405': BaseErrors.ListingNotSupported.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_batch_editions(
        request: Request,
        keys: str | None = None,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> BatchResponse[Edition]:
    """
    Retrieve edition records by their **edition_keys**.

    Returns a standardized response dictionary containing:

    - **data**: the works
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return batch_service(
        connection=connection,
        request=request,
        configuration=ENTITY_TYPE,
        limit=limit,
        offset=offset,
        key=keys
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{edition_key}",
    response_model=EntityResponse[Edition],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_edition(
        request: Request,
        edition_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Edition]:
    """
    Retrieve an edition's records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the edition returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='editions',
        key=edition_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{edition_key}/work",
    response_model=RelationshipResponse[WorkSummary],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_work(
        request: Request,
        edition_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[WorkSummary]:
    """
    Retrieve an edition's work details records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions' work returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='editions_work',
        key=edition_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{edition_key}/details",
    response_model=RelationshipResponse[EditionDetails],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_details(
        request: Request,
        edition_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionDetails]:
    """
    Retrieve an edition's details records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions' details returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='editions_details',
        key=edition_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{edition_key}/contents",
    response_model=RelationshipResponse[EditionContents],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_contents(
        request: Request,
        edition_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionContents]:
    """
    Retrieve an edition's contents records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions' contents returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='editions_contents',
        key=edition_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{edition_key}/publishing",
    response_model=RelationshipResponse[EditionPublishing],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_publishing(
        request: Request,
        edition_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionPublishing]:
    """
    Retrieve an edition's publishing records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions' publishing details returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='editions_publishing',
        key=edition_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{edition_key}/contributors",
    response_model=RelationshipResponse[EditionContributor],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_contributors(
        request: Request,
        edition_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionContributor]:
    """
    Retrieve an edition's publishing records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions' contributors returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='editions_contributors',
        key=edition_key,
        limit=limit,
        offset=offset,
    )
# -----------------------------------------------------------------------------
