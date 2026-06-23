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
import api.repository.works as works_repo

from api.schemas.entities.core import Work
from api.schemas.entities.summaries import AuthorSummary, EditionSummary
from api.schemas.entities.extensions import WorkSeries, WorkAvailability, WorkRatings, WorkOverview
from api.schemas.responses import EntityResponse, RelationshipResponse, BatchResponse

from api.utils.query import build_query
from api.utils.validation import validate_key
from api.utils.pagination import build_pagination_links
from api.utils.parsing import parse_entity_keys

from api.errors import BaseErrors, WorksErrors

from api.response_builders.entities import format_response_entity, format_response_relationship
from api.response_builders.batches import format_response_batch

# --- Load API LIMIT from environment variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
API_LIMIT = int(os.getenv("API_LIMIT"))

# --- Defining the works router ---
router = APIRouter(
    prefix="/works",
    tags=["Works"]
)

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> BatchResponse[Work]:
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
    work_keys = parse_entity_keys(keys=keys)

    # For each key validate key type
    for work_key in work_keys:

        # Validate if any of the keys is an invalid work key
        validate_key(
            key=work_key,
            entity='work',
            query=query
        )

    # Fetch data
    results = works_repo.get_works_by_work_key(
        connection=connection,
        work_keys=work_keys,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise WorksErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_works'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_batch(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'type': 'work',
            'keys': work_keys,
            'total': results['total_works'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=Work
    )

# ----------------------------------------------------------------------------------
# --- DEPRECATED ---
# @router.get("/",  responses={'405': BaseErrors.ListingNotSupported.response})
# async def works_root() -> None:
#     """
#     Root endpoint for the works collection
#
#     This endpoint is intentionally not supported for listing operations
#
#     It exists to explicitly reject requests made to `/works/` without a
#     valid `work_key`, and returns a standardized error response
#     """
#     raise BaseErrors.ListingNotSupported(query="/works/")
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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Work]:
    """
    Retrieve a work's records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the work
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_works_by_work_key(
        connection=connection,
        work_keys=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta={'type': 'work'},
        links={'self': query},
        model=Work
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[AuthorSummary]:
    """
    Retrieve a work's authors' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the authors returned ranked by ascending work key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_authors_by_work_key(
        connection=connection,
        work_key=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_works'] == 0:
        raise WorksErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_authors'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'parent_type': 'work',
            'parent_key': work_key,
            'child_type': 'author',
            'total_children': results['total_authors'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=AuthorSummary,
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[EditionSummary]:
    """
    Retrieve a work's editions' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the editions returned ranked by ascending edition key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_editions_by_work_key(
        connection=connection,
        work_key=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_works'] == 0:
        raise WorksErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_editions'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'parent_type': 'work',
            'parent_key': work_key,
            'child_type': 'edition',
            'total_children': results['total_editions'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=EditionSummary,
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[WorkSeries]:
    """
    Retrieve a work's series records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the series returned ranked by ascending series key
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_series_by_work_key(
        connection=connection,
        work_key=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_works'] == 0:
        raise WorksErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_series'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'parent_type': 'work',
            'parent_key': work_key,
            'child_type': 'series',
            'total_children': results['total_series'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=WorkSeries,
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[WorkAvailability]:
    """
    Retrieve a work's availability records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the availability returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_availability_by_work_key(
        connection=connection,
        work_key=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta={'type': 'work'},
        links={'self': query},
        model=WorkAvailability
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[WorkRatings]:
    """
    Retrieve a work's ratings records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the ratings returned
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_ratings_by_work_key(
        connection=connection,
        work_key=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta={'type': 'work'},
        links={'self': query},
        model=WorkRatings
    )

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
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[WorkOverview]:
    """
    Retrieve a work's overview records (subjects, people, places, time periods) by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: dictionary of lists for subjects, people, places and time periods for the work
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=work_key,
        entity='work',
        query=query
    )

    # Fetch data
    results = works_repo.get_overview_by_work_key(
        connection=connection,
        work_key=work_key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if len(results['data']) == 0:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta={'type': 'work'},
        links={'self': query},
        model=WorkOverview
    )
