"""
Editions Router
"""

import psycopg2

from fastapi import APIRouter

from api.dependencies import DB_DEPENDENCY
import api.repository.editions as editions_repo
from api.service import format_response
from api.schemas import (
    Edition,

    APIResponse, EditionDetails, EditionContents, EditionsPublishing, EditionPublishing,
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
    Retrieve edition records by **edition_key**.

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
    Retrieve edition details records by **edition_key**.

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
    Retrieve edition contents records by **edition_key**.

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

@router.get("/{edition_key}/publishing", response_model=APIResponse[EditionPublishing])
async def get_editions_publishing(
        edition_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[EditionPublishing]:
    """
    Retrieve edition publishing records by **edition_key**.

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
        model=EditionPublishing
    )