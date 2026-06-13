"""
/works router
"""
import psycopg2

from fastapi import APIRouter

from api.dependencies import DB_DEPENDENCY
from api.schemas import (
    Work,
    WorkAuthors,
    WorkEditions,
    APIResponse,
    WorkSeries,
    WorkAvailability
)
from api.repository.works import (
    get_works_by_work_key,
    get_authors_by_work_key,
    get_editions_by_work_key,
    get_series_by_work_key, get_availability_by_work_key
)
from api.service import format_response


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
    data, column_names = get_works_by_work_key(connection, work_key)

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

    """
    # Fetch data
    data, column_names = get_authors_by_work_key(connection, work_key)

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

    """
    # Fetch data
    data, column_names = get_editions_by_work_key(connection, work_key)

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

    """
    # Fetch data
    data, column_names = get_series_by_work_key(connection, work_key)

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

    """
    # Fetch data
    data, column_names = get_availability_by_work_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}/availability',
        method='GET',
        records=data,
        column_names=column_names,
        model=WorkAvailability
    )

#
# @router.get("/{work_key}/subjects")
# async def get_work_availability(
#         work_key: str,
#         connection: psycopg2.extensions.connection = DB_DEPENDENCY
# ):
#
#     pass
#
#
# @router.get("/{work_key}/people")
# async def get_work_availability(
#         work_key: str,
#         connection: psycopg2.extensions.connection = DB_DEPENDENCY
# ):
#     pass
#
#
# @router.get("/{work_key}/places")
# async def get_work_availability(
#         work_key: str,
#         connection: psycopg2.extensions.connection = DB_DEPENDENCY
# ):
#     pass
#
#
# @router.get("/{work_key}/time_periods")
# async def get_work_availability(
#         work_key: str,
#         connection: psycopg2.extensions.connection = DB_DEPENDENCY
# ):
#     pass
#
# @router.get("/{work_key}/facets")
# async def get_work_availability(
#         work_key: str,
#         connection: psycopg2.extensions.connection = DB_DEPENDENCY
# ):
#     # Add subjects, people,... to the same
#     pass