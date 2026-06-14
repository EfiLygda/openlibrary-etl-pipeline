"""
Editions Router

This module defines API endpoints related to "editions", including retrieval of
edition records and associated metadata such as detailed information, contents,
publishing data, and contributors.

Endpoints:
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

from api.dependencies import DB_DEPENDENCY
import api.repository.editions as editions_repo
from api.service import format_response
from api.schemas import (
    Edition,
    EditionDetails,
    EditionContents,
    EditionsPublishing,
    EditionsContributors,
    APIResponse,
)

# Defining the works router
router = APIRouter(
    prefix="/editions",
    tags=["Editions"]
)

@router.get("/{edition_key}", response_model=APIResponse[Edition])
async def get_author(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[Edition]:
    """
    Retrieve an edition's records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = editions_repo.get_edition_by_edition_key(connection, edition_key)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        endpoint=f'/editions/{edition_key}',
        method='GET',
        records=data,
        column_names=column_names,
        model=Edition
    )

@router.get("/{edition_key}/details", response_model=APIResponse[EditionDetails])
async def get_editions_details(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionDetails]:
    """
    Retrieve an edition's details records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = editions_repo.get_details_by_edition_key(connection, edition_key)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        endpoint=f'/editions/{edition_key}/details',
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionDetails
    )

@router.get("/{edition_key}/contents", response_model=APIResponse[EditionContents])
async def get_editions_details(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionContents]:
    """
    Retrieve an edition's contents records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = editions_repo.get_contents_by_edition_key(connection, edition_key)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        endpoint=f'/editions/{edition_key}/contents',
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionContents
    )

@router.get("/{edition_key}/publishing", response_model=APIResponse[EditionsPublishing])
async def get_editions_publishing(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionsPublishing]:
    """
    Retrieve an edition's publishing records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = editions_repo.get_publishing_by_edition_key(connection, edition_key)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        endpoint=f'/editions/{edition_key}/publishing',
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionsPublishing
    )

@router.get("/{edition_key}/contributors", response_model=APIResponse[EditionsContributors])
async def get_editions_contributors(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionsContributors]:
    """
    Retrieve an edition's publishing records by **edition_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided edition_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = editions_repo.get_contributors_by_edition_key(connection, edition_key)

    # Format and return consistent API response structure
    return format_response(
        query=edition_key,
        endpoint=f'/editions/{edition_key}/contributors',
        method='GET',
        records=data,
        column_names=column_names,
        model=EditionsContributors
    )