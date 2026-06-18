"""
Works Router

This module defines API endpoints related to "works", including retrieval of
work details and associated data such as authors, editions, series, availability,
overview, and ratings

Endpoints:
- GET /works/
  Retrieve all work's related metadata (Not Supported)

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

from fastapi import APIRouter
from fastapi import Request

from open_library import KeyHandler

from api.dependencies import DB_DEPENDENCY
import api.repository.works as works_repo

from api.utils.pagination import build_pagination_links
from api.errors import BaseErrors, WorksErrors

from api.schemas.entities.core import Work
from api.schemas.entities.summaries import AuthorSummary, EditionSummary
from api.schemas.entities.extensions import WorkSeries, WorkAvailability, WorkRatings, WorkOverview
from api.schemas.responses import EntityResponse, RelationshipResponse

from api.response_builders.entities import format_response_entity, format_response_relationship

# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
GENRE = os.getenv("API_LIMIT")
API_LIMIT = int(os.getenv("API_LIMIT"))

# --- Defining the works router ---
router = APIRouter(
    prefix="/works",
    tags=["Works"]
)

# --- Defining all endpoints ---
@router.get("/",  responses={'405': BaseErrors.ListingNotSupported.response})
async def works_root() -> None:
    """
    Root endpoint for the works collection

    This endpoint is intentionally not supported for listing operations

    It exists to explicitly reject requests made to `/works/` without a
    valid `work_key`, and returns a standardized error response
    """
    raise BaseErrors.ListingNotSupported(query="/works/")

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
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> EntityResponse[Work]:
    """
    Retrieve a work's records by **work_key**.

    Returns a standardized response dictionary containing:

    - **data**: the work
    - **meta**: metadata for the query (entity type)
    - **links**: current link used
    """

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    results = works_repo.get_works_by_work_key(
        connection=connection,
        work_key=work_key
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

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

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
            'total': results['total_authors'],
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

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

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
            'total': results['total_editions'],
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

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

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
            'total': results['total_series'],
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

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

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

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

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

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

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
