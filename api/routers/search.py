"""
Search Router

This module defines API endpoints for performing a simple text-based search
across works and related metadata fields such as authors, subjects, people,
places, time periods, editions, and series.

The search uses basic pattern matching (ILIKE) across multiple fields and
returns a paginated list of matching works with minimal display data.

Endpoint:
- GET /search/
  Returns a list of works matching the search query across multiple fields
  (works, authors, subjects, etc.), including basic metadata such as
  work_key, title, and authors.

"""
import os
from dotenv import load_dotenv

import psycopg2

from fastapi import APIRouter
from fastapi import Request

from api.dependencies import DB_DEPENDENCY
import api.repository.search as search_repo
from api.errors import WorksErrors

from api.schemas.search import SearchWork
from api.schemas.responses import RelationshipResponse

from api.utils.pagination import build_pagination_links
from api.response_builders.entities import format_response_relationship

# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
GENRE = os.getenv("API_LIMIT")
API_LIMIT = int(os.getenv("API_LIMIT"))

# --- Defining the works router ---
router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

# --- Defining all endpoints ---
@router.get(
    path="",
    response_model=RelationshipResponse[SearchWork],
    responses={
        '404': WorksErrors.NotFound.response,
        # '422': WorksErrors.InvalidKey.response
    }
)
async def search(
        request: Request,
        q: str,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> RelationshipResponse[SearchWork]:
    """
    Retrieve a work's records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **self**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Fetch data
    results = search_repo.search(
        connection=connection,
        q=q,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_results'] == 0:
        raise WorksErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_results'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta={
            'total': results['total_results'],
            'limit': limit,
            'offset': offset
        },
        links=links,
        model=SearchWork,
    )