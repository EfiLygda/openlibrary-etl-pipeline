"""
Authors Router
"""

import psycopg2

from fastapi import APIRouter

from api.dependencies import DB_DEPENDENCY
import api.repository.authors as authors_repo
from api.service import format_response
from api.schemas import (
    Author,

    APIResponse, AuthorsWorks,
)

# Defining the works router
router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.get("/{author_key}", response_model=APIResponse[Author])
async def get_author(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[Author]:
    """
    Retrieve work records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = authors_repo.get_author_by_author_key(connection, author_key)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=f'/authors/{author_key}',
        method='GET',
        records=data,
        column_names=column_names,
        model=Author
    )

@router.get("/{author_key}/works", response_model=APIResponse[AuthorsWorks])
async def get_authors_works(
        author_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> APIResponse[AuthorsWorks]:
    """
    Retrieve work records by **author_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided author_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch data
    data, column_names = authors_repo.get_works_by_author_key(connection, author_key)

    # Format and return consistent API response structure
    return format_response(
        query=author_key,
        endpoint=f'/authors/{author_key}/works',
        method='GET',
        records=data,
        column_names=column_names,
        model=AuthorsWorks
    )