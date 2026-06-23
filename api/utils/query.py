"""
Module for building request query strings
"""

from fastapi import Request

def build_query(request: Request) -> str:
    """
    Build the current endpoint's request path and query string

    :param request: fastapi.Request, incoming FastAPI request
    :returns: str, the request path, including query parameters when present
    """
    # Fetch current request's path and parameters query
    path_url = request.url.path
    query_url = request.url.query

    # Current query
    query = f'{path_url}?{query_url}' if query_url else path_url

    return query
