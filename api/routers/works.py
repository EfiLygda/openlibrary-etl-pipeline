"""
Works Router

This module defines API endpoints related to "works", including retrieval of
work details and associated data such as authors, editions, series, availability,
overview, and ratings

Endpoints:
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

from api.dependencies import DB_DEPENDENCY
import api.repository.works as works_repo
from api.service import format_response
from api.schemas import (
    Work,
    WorkAuthors,
    WorkEditions,
    WorkSeries,
    WorkAvailability,
    WorkOverview,
    WorkRatings,
    APIResponse,
)

# Defining the works router
router = APIRouter(
    prefix="/works",
    tags=["Works"]
)

@router.get("/{work_key}", response_model=APIResponse[Work])
async def get_work(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[Work]:
    """
    Retrieve work records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = works_repo.get_works_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}',
        method='GET',
        records=data,
        column_names=column_names,
        model=Work
    )

@router.get("/{work_key}/authors", response_model=APIResponse[WorkAuthors])
async def get_work_authors(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorkAuthors]:
    """
    Retrieve a work's authors' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = works_repo.get_authors_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/authors',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkAuthors
    )

@router.get("/{work_key}/editions", response_model=APIResponse[WorkEditions])
async def get_work_editions(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorkEditions]:
    """
    Retrieve a work's editions' summarized records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """
    # Fetch data
    data, column_names = works_repo.get_editions_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/editions',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkEditions
    )

@router.get("/{work_key}/series", response_model=APIResponse[WorkSeries])
async def get_work_series(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorkSeries]:
    """
    Retrieve a work's series records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = works_repo.get_series_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/series',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkSeries
    )

@router.get("/{work_key}/availability", response_model=APIResponse[WorkAvailability])
async def get_work_availability(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorkAvailability]:
    """
    Retrieve a work's availability records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = works_repo.get_availability_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/availability',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkAvailability
    )

@router.get("/{work_key}/ratings", response_model=APIResponse[WorkRatings])
async def get_work_subjects(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorkRatings]:
    """
    Retrieve a work's ratings records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """
    # Fetch data
    data, column_names = works_repo.get_ratings_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/ratings',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkRatings
    )

@router.get("/{work_key}/overview", response_model=APIResponse[WorkOverview])
async def get_work_overview(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[WorkOverview]:
    """
    Retrieve a work's overview records (subjects, people, places, time periods) by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = works_repo.get_overview_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/overview',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkOverview
    )
