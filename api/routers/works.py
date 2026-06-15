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

import psycopg2

from fastapi import APIRouter

from open_library import KeyHandler

from api.dependencies import DB_DEPENDENCY
import api.repository.works as works_repo
from api.service import format_response

from api.errors import BaseErrors, WorksErrors
from api.schemas.responses import APIResponse
from api.schemas.entities.core import Work
from api.schemas.entities.relationships import (
    WorksAuthors,
    WorksEditions,
    WorksSeries,
    WorksAvailability,
    WorksOverview,
    WorksRatings
)

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
    response_model=APIResponse[Work],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[Work]:
    """
    Retrieve a work's records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """
    # Current query
    query = f'/works/{work_key}'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_works_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=Work
    )

@router.get(
    path="/{work_key}/authors",
    response_model=APIResponse[WorksAuthors],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_authors(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorksAuthors]:
    """
    Retrieve a work's authors' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/works/{work_key}/authors'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_authors_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=WorksAuthors
    )

@router.get(
    path="/{work_key}/editions",
    response_model=APIResponse[WorksEditions],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_editions(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorksEditions]:
    """
    Retrieve a work's editions' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/works/{work_key}/editions'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_editions_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=WorksEditions
    )

@router.get(
    path="/{work_key}/series",
    response_model=APIResponse[WorksSeries],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_series(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorksSeries]:
    """
    Retrieve a work's series records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/works/{work_key}/series'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_series_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=WorksSeries
    )

@router.get(
    path="/{work_key}/availability",
    response_model=APIResponse[WorksAvailability],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_availability(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorksAvailability]:
    """
    Retrieve a work's availability records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """
    # Current query
    query = f'/works/{work_key}/availability'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_availability_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=WorksAvailability
    )

@router.get(
    path="/{work_key}/ratings",
    response_model=APIResponse[WorksRatings],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_ratings(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorksRatings]:
    """
    Retrieve a work's ratings records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/works/{work_key}/ratings'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_ratings_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=WorksRatings
    )

@router.get(
    path="/{work_key}/overview",
    response_model=APIResponse[WorksOverview],
    responses={
        '404': WorksErrors.NotFound.response,
        '422': WorksErrors.InvalidKey.response
    }
)
async def get_work_overview(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorksOverview]:
    """
    Retrieve a work's overview records (subjects, people, places, time periods) by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/works/{work_key}/overview'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(work_key) != 'work':
        raise WorksErrors.InvalidKey(query)

    # Fetch data
    data, column_names = works_repo.get_overview_by_work_key(connection, work_key)

    # If no data is returned then error is raised
    if not data:
        raise WorksErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=WorksOverview
    )
