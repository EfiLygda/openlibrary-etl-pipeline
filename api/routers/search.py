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

from urllib.parse import urlparse, parse_qs

from fastapi import APIRouter
from fastapi import Request

from api.dependencies import DB_DEPENDENCY
import api.repository.search as search_repo
from api.errors import SearchErrors

from api.schemas.search import SearchWork
from api.schemas.responses import SearchResponse

from api.utils.links import build_pagination_links
from api.utils.metadata import build_search_meta

from api.response_builders.search import format_response_search

# ----------------------------------------------------------------------------------
# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
GENRE = os.getenv("API_LIMIT")
API_LIMIT = int(os.getenv("API_LIMIT"))
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Defining the works router ---
router = APIRouter(
    prefix="/search",
    tags=["Search"]
)
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Defining search fields ---
SEARCH_FEILDS = [
    'q',
    'year',
    'lang',
    'published_by',
    'limit',
    'offset',
]
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Defining all endpoints ---
@router.get(
    path="",
    response_model=SearchResponse[SearchWork],
    responses={
        '404': SearchErrors.NotFound.response,
        '422': SearchErrors.QueryConflict.response
    }
)
async def search(
        request: Request,
        q: str,
        year: int | None = None,
        lang: str | None = None,
        published_by: str | None = None,
        limit: int = API_LIMIT,
        offset: int = 0,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
) -> SearchResponse[SearchWork]:
    """
    Retrieve works via a **query**.

    Returns a standardized response dictionary containing:

    - **data**: the works returned ranked by descending text relevance score
    - **meta**: pagination metadata for the query (total results, limit and offset)
    - **links**: pagination links for navigation
    """

    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    # Check if other params were given except 'q', 'limit', 'offset'
    # Parse url to components (here we need 'query' for parameters)
    url_parts = urlparse(str(request.url))

    # Convert parameters to dictionary like {'q' = ['...'], 'limit' = ['20'], 'offset' = ['0']}
    current_query = parse_qs(url_parts.query)

    if not all([param_name in SEARCH_FEILDS for param_name in current_query.keys()]):
        raise SearchErrors.QueryConflict(query)

    # Fetch data
    results = search_repo.search(
        connection=connection,
        q=q,
        year=year,
        lang=lang,
        published_by=published_by,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    if results['total_results'] == 0:
        raise SearchErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_results'],
        limit=limit,
        offset=offset
    )

    # Build metadata
    meta = build_search_meta(
        total=results['total_results'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_search(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=SearchWork,
    )
# ----------------------------------------------------------------------------------
