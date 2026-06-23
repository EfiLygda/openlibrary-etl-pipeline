"""
Editions Router

This module defines API endpoints related to "editions", including retrieval of
edition records and associated metadata such as detailed information, contents,
publishing data, and contributors.

Endpoints:
- GET /editions/
  Retrieve all editions' related metadata (Not Supported)

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
import api.repository.editions as editions_repo

from api.schemas.entities.core import Edition
from api.schemas.entities.summaries import WorkSummary
from api.schemas.entities.extensions import EditionDetails, EditionContents, EditionPublishing, EditionContributor
from api.schemas.responses import EntityResponse, RelationshipResponse

from api.utils.query import build_query
from api.utils.validation import validate_key
from api.utils.pagination import build_pagination_links
from api.utils.parsing import parse_entity_keys

from api.errors import BaseErrors, EditionsErrors

from api.response_builders.entities import format_response_entity, format_response_relationship

# --- Load API LIMIT from environment variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
API_LIMIT = int(os.getenv("API_LIMIT"))

# --- Defining the editions router ---
router = APIRouter(
    prefix="/editions",
    tags=["Editions"]
)

# --- Defining all endpoints ---
@router.get("/",  responses={'405': BaseErrors.ListingNotSupported.response})
async def editions_root() -> None:
    """
    Root endpoint for the editions collection

    This endpoint is intentionally not supported for listing operations

    It exists to explicitly reject requests made to `/editions/` without a
    valid `edition_key`, and returns a standardized error response
    """
    raise BaseErrors.ListingNotSupported(query="/editions/")

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
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Edition]:
    """
    Retrieve an edition's records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **data**: the edition returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid edition key
    validate_key(
        key=edition_key,
        entity='edition',
        query=query
    )

    # Fetch data
    results = editions_repo.get_edition_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise EditionsErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta={'type': 'edition'},
        links={'self': query},
        model=Edition
    )

@router.get(
    path="/{edition_key}/works",
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

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid edition key
    validate_key(
        key=edition_key,
        entity='edition',
        query=query
    )

    # Fetch data
    results = editions_repo.get_works_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if results['total_editions'] == 0:
        raise EditionsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_works'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'total': results['total_works'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=WorkSummary,
    )

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

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid edition key
    validate_key(
        key=edition_key,
        entity='edition',
        query=query
    )

    # Fetch data
    results = editions_repo.get_details_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if results['total_editions'] == 0:
        raise EditionsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_details'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'total': results['total_details'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=EditionDetails,
    )

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

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid edition key
    validate_key(
        key=edition_key,
        entity='edition',
        query=query
    )

    # Fetch data
    results = editions_repo.get_contents_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if results['total_editions'] == 0:
        raise EditionsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_contents'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'total': results['total_contents'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=EditionContents,
    )

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

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid edition key
    validate_key(
        key=edition_key,
        entity='edition',
        query=query
    )

    # Fetch data
    results = editions_repo.get_publishing_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if results['total_editions'] == 0:
        raise EditionsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_publishing'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'total': results['total_publishing'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=EditionPublishing,
    )

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

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if any of the keys is an invalid edition key
    validate_key(
        key=edition_key,
        entity='edition',
        query=query
    )

    # Fetch data
    results = editions_repo.get_contributors_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if results['total_editions'] == 0:
        raise EditionsErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_contributors'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'total': results['total_contributors'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=EditionContributor,
    )