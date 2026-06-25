"""
Batch entity service

Provides a reusable service layer for batch retrieval of API entities
identified by their Open Library keys

The service centralizes the common workflow shared across batch endpoints:

1. Validate request parameters
2. Parse and normalize entity keys
3. Validate key formats
4. Execute repository queries
5. Validate entity existence
6. Build pagination metadata and links
7. Format standardized API responses

Supported entity types:
    - works
    - authors
    - editions

Each entity type is configured through a ServiceConfig instance that
defines the repository function, entity type, and response model used
by the service
"""

import psycopg2
from fastapi import Request

import api.repository.works as works_repo
import api.repository.authors as authors_repo
import api.repository.editions as editions_repo

from api.errors import BaseErrors
from api.schemas.entities.core import Work, Author, Edition

from api.utils.links import build_pagination_links
from api.utils.metadata import build_batch_meta
from api.utils.parsing import parse_entity_keys
from api.utils.query import build_query
from api.utils.validation import validate_key, validate_parent_existance

from api.service.base import ServiceConfig

from api.response_builders.batches import format_response_batch

# Define configurations for batch services
BATCH_WORKS = ServiceConfig(
    router_entity_type='work',
    repository_function=works_repo.get_works_by_work_key,
    response_base_model=Work,
)

BATCH_AUTHORS = ServiceConfig(
    router_entity_type='author',
    repository_function=authors_repo.get_authors_by_author_key,
    response_base_model=Author,
)

BATCH_EDITIONS = ServiceConfig(
    router_entity_type='edition',
    repository_function=editions_repo.get_editions_by_edition_key,
    response_base_model=Edition,
)

# Dictionary with all batch configurations
BATCH_CONFIGS = {
    'work': BATCH_WORKS,
    'author': BATCH_AUTHORS,
    'edition': BATCH_EDITIONS
}

def batch_service(
        connection: psycopg2.extensions.connection,
        request: Request,
        configuration: str,
        limit: int,
        offset: int,
        keys: str | None = None,
):
    """
    Execute a standardized batch entity retrieval workflow

    This service is used by batch endpoints that retrieve multiple
    entities through a comma-separated list of Open Library keys

    The service performs request validation, repository execution,
    metadata generation, link generation, and response formatting,
    returning a consistent API response structure across entity types

    Supported modes:

        - `work`
        - `author`
        - `edition`

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param request: Request, current FastAPI request object used for query and link generation
    :param configuration: str, configuration to use. Must be one of 'work', 'author' or 'edition'
    :param limit: int, maximum number of records returned
    :param offset: int, number of records skipped before returning results
    :param keys: str | None, comma-separated entity keys used for filtering

    :returns: BatchResponse[T], standardized batch response containing 'data', 'meta' and 'links'
    """

    # Check mode value
    if configuration not in BATCH_CONFIGS.keys():
        raise ValueError(
            f'Argument \'mode\' must be \'work\',\'author\' or \'edition\', \'{configuration}\' was given'
        )

    # Current batch configuration
    batch_config = BATCH_CONFIGS[configuration]

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Intentionally not supported for listing operations
    if keys is None:
        raise BaseErrors.ListingNotSupported(query)

    # Split and strip key string
    normalized_keys = parse_entity_keys(keys=keys)

    # For each key validate key type
    for normalized_key in normalized_keys:

        # Validate if any of the keys is an invalid work key
        validate_key(
            key=normalized_key,
            entity_type=batch_config.router_entity_type,
            query=query
        )

    # Fetch data
    results = batch_config.repository_function(
        connection=connection,
        keys=normalized_keys,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    validate_parent_existance(
        total_parents=results['total_parents'],
        entity_type=batch_config.router_entity_type,
        query=query
    )

    # Build links
    links = build_pagination_links(
        url=query,
        total=results['total_parents'],
        limit=limit,
        offset=offset
    )

    # Build metadata
    meta = build_batch_meta(
        entity_type=batch_config.router_entity_type,
        keys=normalized_keys,
        total=results['total_parents'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_batch(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=batch_config.response_base_model
    )
