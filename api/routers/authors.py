"""
Authors Router

This module defines API endpoints related to "authors", including retrieval of
author details and associated data such as works, editions, statistics, and
alternative names

The router acts as an orchestration layer that retrieves and aggregates author
data from multiple related tables while keeping endpoints focused and consistent

Endpoints:

- GET /authors?keys=OLxxxA,OLxxxA,...
  Retrieve all work's related metadata via their author key

- GET /authors/{author_key}
  Retrieve full author profile including core metadata and optional enriched fields

- GET /authors/{author_key}/works
  Retrieve summarized works associated with an author

- GET /authors/{author_key}/editions
  Retrieve summarized editions associated with an author

- GET /authors/{author_key}/statistics
  Retrieve aggregated statistics for an author including ratings distribution,
  reading activity, and work counts

- GET /authors/{author_key}/alternative_names
  Retrieve alternative names, aliases, and variations for an author
"""
import os
from dotenv import load_dotenv

import psycopg2

from fastapi import APIRouter
from fastapi import Request

from api.dependencies import DB_DEPENDENCY

from api.errors import BaseErrors, AuthorsErrors

from api.schemas.entities.core import Author
from api.schemas.entities.summaries import WorkSummary, EditionSummary
from api.schemas.entities.relationships import AuthorStatistics, AuthorAlternativeNames
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
ENTITY_TYPE = 'author'
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining the authors router ---
router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining all endpoints ---
@router.get(
    path="",
    response_model=BatchResponse[Author],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '405': BaseErrors.ListingNotSupported.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_batch_authors(
        request: Request,
        keys: str | None = None,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> BatchResponse[Author]:
    """
    Retrieve authors records by their **author_keys**.

    Returns a standardized response dictionary containing:

    - **data**: the authors
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
    path="/{author_key}",
    response_model=EntityResponse[Author],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_author(
        request: Request,
        author_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Author]:
    """
    Retrieve an author's records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the author returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='authors',
        key=author_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{author_key}/works",
    response_model=RelationshipResponse[WorkSummary],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_authors_works(
        request: Request,
        author_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[WorkSummary]:
    """
    Retrieve an author's work records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the works returned ranked by ascending work key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='authors_works',
        key=author_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{author_key}/editions",
    response_model=RelationshipResponse[EditionSummary],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_authors_editions(
        request: Request,
        author_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionSummary]:
    """
    Retrieve an author's edition records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='authors_editions',
        key=author_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{author_key}/statistics",
    response_model=EntityResponse[AuthorStatistics],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_authors_statistics(
        request: Request,
        author_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[AuthorStatistics]:
    """
    Retrieve an author's statistic records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the statistics returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return entity_service(
        connection=connection,
        request=request,
        configuration='authors_statistics',
        key=author_key,
        limit=limit,
        offset=offset,
    )
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
@router.get(
    path="/{author_key}/alternative_names",
    response_model=RelationshipResponse[AuthorAlternativeNames],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_authors_alternative_names(
        request: Request,
        author_key: str,
        limit: int = LIMIT,
        offset: int = OFFSET,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[AuthorAlternativeNames]:
    """
    Retrieve an author's alternative name records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: dictionary with a list of the alternative names
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    return relationship_service(
        connection=connection,
        request=request,
        configuration='authors_alternative_names',
        key=author_key,
        limit=limit,
        offset=offset,
    )
# -----------------------------------------------------------------------------
