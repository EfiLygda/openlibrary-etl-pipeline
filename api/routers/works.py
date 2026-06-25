"""
Works Router

This module defines API endpoints related to "works", including retrieval of
work details and associated data such as authors, editions, series, availability,
overview, and ratings

Endpoints:
- GET /works?keys=OLxxxW,OLxxxW,...
  Retrieve all work's related metadata via their work key

- GET /works/{work_key}
  Retrieve full work details and all related metadata

- GET /works/{work_key}/authors
  Retrieve summarized authors' data associated with a work

- GET /works/{work_key}/editions
  Retrieve available editions summarized data of a work

- GET /works/{work_key}/series
  Retrieve series information for a work

- GET /works/{work_key}/availability
  Retrieve availability information for a work

- GET /works/{work_key}/overview
  Retrieve a high-level overview of a work (subjects, people, places and time periods asociated with the work)

- GET /works/{work_key}/ratings
  Retrieve 5-star ratings counts for a work

"""
import os
from dotenv import load_dotenv

import psycopg2

from fastapi import APIRouter, Request

from api.dependencies import DB_DEPENDENCY

from api.errors import BaseErrors, WorksErrors

from api.schemas.entities.core import Work
from api.schemas.entities.summaries import AuthorSummary, EditionSummary
from api.schemas.entities.relationships import WorkSeries, WorkAvailability, WorkRatings, WorkOverview
from api.schemas.responses import EntityResponse, RelationshipResponse, BatchResponse
from api.service.batches import batch_service
from api.service.entities import entity_service
from api.service.relationships import relationship_service

# -----------------------------------------------------------------------------
# --- Load API LIMIT from environment variables ---
# Load variables from the .env file to the environment
load_dotenv()

# --- Setting up parameters ---
LIMIT = int(os.getenv("API_LIMIT"))
OFFSET = 0
ENTITY_TYPE = 'work'
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining the works router ---
router = APIRouter(
    prefix="/works",
    tags=["Works"]
)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining all endpoints ---
@router.get(
    path="",
    response_model=BatchResponse[Work],
    responses={
        '404': WorksErrors.NotFound.response,
        '405': BaseErrors.ListingNotSupported.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_batch_works(
        request: Request,
        keys: str | None = None,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> BatchResponse[Work]:
    """
    Retrieve works batch records by their **work_keys**.

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
    path="/{work_key}",
    response_model=EntityResponse[Work],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Work]:
    """
    Retrieve a work's records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the work
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='works',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{work_key}/authors",
    response_model=RelationshipResponse[AuthorSummary],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_authors(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[AuthorSummary]:
    """
    Retrieve a work's authors' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the authors returned ranked by ascending work key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='works_authors',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{work_key}/editions",
    response_model=RelationshipResponse[EditionSummary],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_editions(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionSummary]:
    """
    Retrieve a work's editions' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='works_editions',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{work_key}/series",
    response_model=RelationshipResponse[WorkSeries],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_series(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[WorkSeries]:
    """
    Retrieve a work's series records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the series returned ranked by ascending series key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='works_series',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{work_key}/availability",
    response_model=EntityResponse[WorkAvailability],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_availability(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[WorkAvailability]:
    """
    Retrieve a work's availability records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the availability returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='works_availability',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{work_key}/ratings",
    response_model=EntityResponse[WorkRatings],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_ratings(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[WorkRatings]:
    """
    Retrieve a work's ratings records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the ratings returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='works_ratings',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{work_key}/overview",
    response_model=EntityResponse[WorkOverview],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_overview(
        request: Request,
        work_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[WorkOverview]:
    """
    Retrieve a work's overview records (subjects, people, places, time periods) by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: dictionary of lists for subjects, people, places and time periods for the work
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='works_overview',
        key=work_key,
        limit=limit,
        offset=offset,
    )
# -----------------------------------------------------------------------------
