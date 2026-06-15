"""
Authors Router

This module defines API endpoints related to "authors", including retrieval of
author details and associated data such as works, editions, statistics, and
alternative names

The router acts as an orchestration layer that retrieves and aggregates author
data from multiple related tables while keeping endpoints focused and consistent

Endpoints:

- GET /authors/
  Retrieve all authors' related metadata (Not Supported)

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

import psycopg2

from fastapi import APIRouter

from open_library import KeyHandler

from api.dependencies import DB_DEPENDENCY
import api.repository.authors as authors_repo
from api.service import format_response

from api.schemas.responses import APIResponse
from api.schemas.entities.core import Author

from api.schemas.entities.relationships import (
    AuthorsWorks,
    AuthorsEditions,
    AuthorsStatistics,
    AuthorsAlternativeNames
)

from api.exceptions import (
    LISTING_NOT_SUPPORTED,
    INVALID_AUTHOR_KEY_ERROR,
    AUTHOR_NOT_FOUND_ERROR
)

from api.responses import (
    LISTING_NOT_SUPPORTED_RESPONSE,
    AUTHOR_NOT_FOUND_RESPONSE,
    INVALID_AUTHOR_KEY_RESPONSE
)

# --- Defining the authors router ---
router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

# --- Defining all endpoints ---
@router.get("/",  responses={'405': LISTING_NOT_SUPPORTED_RESPONSE})
async def authors_root() -> None:
    """
    Root endpoint for the authors collection

    This endpoint is intentionally not supported for listing operations

    It exists to explicitly reject requests made to `/authors/` without a
    valid `author_key`, and returns a standardized error response
    """
    raise LISTING_NOT_SUPPORTED(query="/authors/")

@router.get(
    path="/{author_key}",
    response_model=APIResponse[Author],
    responses={
        '404': AUTHOR_NOT_FOUND_RESPONSE,
        '422': INVALID_AUTHOR_KEY_RESPONSE
    }
)
async def get_author(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[Author]:
    """
    Retrieve an author's records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/authors/{author_key}'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(author_key) != 'author':
        raise INVALID_AUTHOR_KEY_ERROR(query, author_key)

    # Fetch data
    data, column_names = authors_repo.get_author_by_author_key(connection, author_key)

    # If no data is returned then error is raised
    if not data:
        raise AUTHOR_NOT_FOUND_ERROR(query)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=Author
    )

@router.get(
    path="/{author_key}/works",
    response_model=APIResponse[AuthorsWorks],
    responses={
        '404': AUTHOR_NOT_FOUND_RESPONSE,
        '422': INVALID_AUTHOR_KEY_RESPONSE
    }
)
async def get_authors_works(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[AuthorsWorks]:
    """
    Retrieve an author's work records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/authors/{author_key}/works'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(author_key) != 'author':
        raise INVALID_AUTHOR_KEY_ERROR(query, author_key)

    # Fetch data
    data, column_names = authors_repo.get_works_by_author_key(connection, author_key)

    # If no data is returned then error is raised
    if not data:
        raise AUTHOR_NOT_FOUND_ERROR(query)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=AuthorsWorks
    )

@router.get(
    path="/{author_key}/editions",
    response_model=APIResponse[AuthorsEditions],
    responses={
        '404': AUTHOR_NOT_FOUND_RESPONSE,
        '422': INVALID_AUTHOR_KEY_RESPONSE
    }
)
async def get_authors_editions(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[AuthorsEditions]:
    """
    Retrieve an author's edition records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/authors/{author_key}/editions'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(author_key) != 'author':
        raise INVALID_AUTHOR_KEY_ERROR(query, author_key)

    # Fetch data
    data, column_names = authors_repo.get_editions_by_author_key(connection, author_key)

    # If no data is returned then error is raised
    if not data:
        raise AUTHOR_NOT_FOUND_ERROR(query)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=AuthorsEditions
    )

@router.get(
    path="/{author_key}/statistics",
    response_model=APIResponse[AuthorsStatistics],
    responses={
        '404': AUTHOR_NOT_FOUND_RESPONSE,
        '422': INVALID_AUTHOR_KEY_RESPONSE
    }
)
async def get_authors_statistics(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[AuthorsStatistics]:
    """
    Retrieve an author's statistic records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/authors/{author_key}/statistics'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(author_key) != 'author':
        raise INVALID_AUTHOR_KEY_ERROR(query, author_key)

    # Fetch data
    data, column_names = authors_repo.get_author_statistics_by_author_key(connection, author_key)

    # If no data is returned then error is raised
    if not data:
        raise AUTHOR_NOT_FOUND_ERROR(query)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=AuthorsStatistics
    )

@router.get(
    path="/{author_key}/alternative_names",
    response_model=APIResponse[AuthorsAlternativeNames],
    responses={
        '404': AUTHOR_NOT_FOUND_RESPONSE,
        '422': INVALID_AUTHOR_KEY_RESPONSE
    }
)
async def get_authors_alternative_names(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[AuthorsAlternativeNames]:
    """
    Retrieve an author's alternative name records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Current query
    query = f'/authors/{author_key}/alternative_names'

    # Validate if the key is a valid work key
    if KeyHandler.detect_key(author_key) != 'author':
        raise INVALID_AUTHOR_KEY_ERROR(query, author_key)

    # Fetch data
    data, column_names = authors_repo.get_author_alternative_names_by_author_key(connection, author_key)

    # If no data is returned then error is raised
    if not data:
        raise AUTHOR_NOT_FOUND_ERROR(query)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=query,
        method='GET',
        records=data,
        column_names=column_names,
        model=AuthorsAlternativeNames
    )
