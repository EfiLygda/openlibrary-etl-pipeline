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

- GET /editions/{edition_key}/details
  Retrieve detailed edition metadata by edition_key, including structured descriptive fields

- GET /editions/{edition_key}/contents
  Retrieve edition contents by edition_key, such as table of contents or structured content data

- GET /editions/{edition_key}/publishing
  Retrieve publishing information for an edition, including publication metadata and related records

- GET /editions/{edition_key}/contributors
  Retrieve contributors associated with an edition, such as authors, editors, and other collaborators
"""

import psycopg2

from fastapi import APIRouter

from open_library import KeyHandler

from api.dependencies import DB_DEPENDENCY
import api.repository.editions as editions_repo
from api.service import format_response

from api.errors import BaseErrors, EditionsErrors
from api.schemas.responses import APIResponse
from api.schemas.entities.core import Edition
from api.schemas.entities.relationships import (
    EditionsDetails,
    EditionsContents,
    EditionsPublishing,
    EditionsContributors
)

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
    response_model=APIResponse[Edition],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_edition(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[Edition]:
    """
    Retrieve an edition's records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **self**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/editions/{edition_key}'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(edition_key) != 'edition':
        raise EditionsErrors.InvalidKey(query)

    # Fetch data
    data, column_names = editions_repo.get_edition_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if not data:
        raise EditionsErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        self=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=Edition
    )

@router.get(
    path="/{edition_key}/details",
    response_model=APIResponse[EditionsDetails],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_details(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionsDetails]:
    """
    Retrieve an edition's details records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **self**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/editions/{edition_key}/details'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(edition_key) != 'edition':
        raise EditionsErrors.InvalidKey(query)

    # Fetch data
    data, column_names = editions_repo.get_details_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if not data:
        raise EditionsErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        self=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionsDetails
    )

@router.get(
    path="/{edition_key}/contents",
    response_model=APIResponse[EditionsContents],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_contents(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionsContents]:
    """
    Retrieve an edition's contents records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **self**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/editions/{edition_key}/contents'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(edition_key) != 'edition':
        raise EditionsErrors.InvalidKey(query)

    # Fetch data
    data, column_names = editions_repo.get_contents_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if not data:
        raise EditionsErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        self=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionsContents
    )

@router.get(
    path="/{edition_key}/publishing",
    response_model=APIResponse[EditionsPublishing],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_publishing(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionsPublishing]:
    """
    Retrieve an edition's publishing records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **self**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/editions/{edition_key}/publishing'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(edition_key) != 'edition':
        raise EditionsErrors.InvalidKey(query)

    # Fetch data
    data, column_names = editions_repo.get_publishing_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if not data:
        raise EditionsErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        self=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionsPublishing
    )

@router.get(
    path="/{edition_key}/contributors",
    response_model=APIResponse[EditionsContributors],
    responses={
        '404': EditionsErrors.NotFound.response,
        '422': EditionsErrors.InvalidKey.response
    }
)
async def get_editions_contributors(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionsContributors]:
    """
    Retrieve an edition's publishing records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **self**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/editions/{edition_key}/contributors'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(edition_key) != 'edition':
        raise EditionsErrors.InvalidKey(query)

    # Fetch data
    data, column_names = editions_repo.get_contributors_by_edition_key(connection, edition_key)

    # If no data is returned then error is raised
    if not data:
        raise EditionsErrors.NotFound(query)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        self=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionsContributors
    )