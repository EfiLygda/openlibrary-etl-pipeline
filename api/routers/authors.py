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
import api.repository.authors as authors_repo

from api.schemas.entities.core import Author
from api.schemas.entities.summaries import WorkSummary, EditionSummary
from api.schemas.entities.extensions import AuthorStatistics, AuthorAlternativeNames
from api.schemas.responses import EntityResponse, RelationshipResponse, BatchResponse

from api.utils.query import build_query
from api.utils.validation import validate_key
from api.utils.links import build_entity_links, build_pagination_links
from api.utils.metadata import build_entity_meta, build_relationship_meta, build_batch_meta
from api.utils.parsing import parse_entity_keys

from api.errors import BaseErrors, AuthorsErrors

from api.response_builders.entities import format_response_entity, format_response_relationship
from api.response_builders.batches import format_response_batch

# --- Load API LIMIT from environment variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
API_LIMIT = int(os.getenv("API_LIMIT"))

# --- Defining the authors router ---
router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

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
async def get_batch_works(
        request: Request,
        keys: str | None = None,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> BatchResponse[Author]:
    """
    Retrieve works records by their **work_keys**.

    Returns a standardized response dictionary containing:

    - **data**: the works
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Intentionally not supported for listing operations
    if keys is None:
        raise BaseErrors.ListingNotSupported(query)

    # Split and strip key string
    author_keys = parse_entity_keys(keys=keys)

    # For each key validate key type
    for author_key in author_keys:

        # Validate if any of the keys is an invalid work key
        validate_key(
            key=author_key,
            entity='author',
            query=query
        )

    # Fetch data
    results = authors_repo.get_authors_by_author_key(
        connection=connection,
        author_key=author_keys,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise AuthorsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_authors'],
        limit=limit,
        offset=offset
    )

    # Build metadata
    meta = build_batch_meta(
        entity_type='author',
        keys=author_keys,
        total=results['total_authors'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_batch(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=Author
    )

# ----------------------------------------------------------------------------------
# --- DEPRECATED ---
# @router.get("/",  responses={'405': BaseErrors.ListingNotSupported.response})
# async def authors_root() -> None:
#     """
#     Root endpoint for the authors collection
#
#     This endpoint is intentionally not supported for listing operations
#
#     It exists to explicitly reject requests made to `/authors/` without a
#     valid `author_key`, and returns a standardized error response
#     """
#     raise BaseErrors.ListingNotSupported(query="/authors/")
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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Author]:
    """
    Retrieve an author's records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the author returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid author key
    validate_key(
        key=author_key,
        entity='author',
        query=query
    )

    # Fetch data
    results = authors_repo.get_authors_by_author_key(
        connection=connection,
        author_key=author_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise AuthorsErrors.NotFound(query)

    # Build links
    links = build_entity_links(self=query)

    # Build metadata
    meta = build_entity_meta(entity_type='author')

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=Author
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[WorkSummary]:
    """
    Retrieve an author's work records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the works returned ranked by ascending work key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid author key
    validate_key(
        key=author_key,
        entity='author',
        query=query
    )

    # Fetch data
    results = authors_repo.get_works_by_author_key(
        connection=connection,
        author_key=author_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_authors'] == 0:
        raise AuthorsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_works'],
        limit=limit,
        offset=offset
    )

    # Build metadata
    meta = build_relationship_meta(
        parent_type='author',
        parent_key=author_key,
        child_type='work',
        total_children=results['total_works'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=WorkSummary,
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionSummary]:
    """
    Retrieve an author's edition records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid author key
    validate_key(
        key=author_key,
        entity='author',
        query=query
    )

    # Fetch data
    results = authors_repo.get_editions_by_author_key(
        connection=connection,
        author_key=author_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_authors'] == 0:
        raise AuthorsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_editions'],
        limit=limit,
        offset=offset
    )

    # Build metadata
    meta = build_relationship_meta(
        parent_type='author',
        parent_key=author_key,
        child_type='edition',
        total_children=results['total_editions'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=EditionSummary,
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[AuthorStatistics]:
    """
    Retrieve an author's statistic records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: the statistics returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid author key
    validate_key(
        key=author_key,
        entity='author',
        query=query
    )

    # Fetch data
    results = authors_repo.get_author_statistics_by_author_key(
        connection=connection,
        author_key=author_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise AuthorsErrors.NotFound(query)

    # Build links
    links = links = build_entity_links(self=query)

    # Build meta
    meta = build_entity_meta(entity_type='author')

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=AuthorStatistics
    )

@router.get(
    path="/{author_key}/alternative_names",
    response_model=EntityResponse[AuthorAlternativeNames],
    responses={
        '404': AuthorsErrors.NotFound.response,
        '422': AuthorsErrors.InvalidKey.response
    }
)
async def get_authors_alternative_names(
        request: Request,
        author_key: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[AuthorAlternativeNames]:
    """
    Retrieve an author's alternative name records by **author_key**.

    Returns a standardized response dictionary containing:

    - **data**: dictionary with a list of the alternative names
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid author key
    validate_key(
        key=author_key,
        entity='author',
        query=query
    )

    # Fetch data
    results = authors_repo.get_author_alternative_names_by_author_key(
        connection=connection,
        author_key=author_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise AuthorsErrors.NotFound(query)

    # Build links
    links = build_entity_links(self=query)

    # Build meta
    meta = build_entity_meta(entity_type='author')

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=AuthorAlternativeNames
    )
