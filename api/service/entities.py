"""
Entity service implementations

This module provides reusable service-layer functionality for entity-based
endpoints that return a single resource associated with a parent entity key
"""

import psycopg2
from fastapi import Request

import api.repository.works as works_repo
import api.repository.authors as authors_repo
import api.repository.editions as editions_repo

from api.response_builders.entities import format_response_entity
from api.schemas.entities.core import Work, Author, Edition
from api.schemas.entities.relationships import WorkRatings, WorkAvailability, WorkOverview, AuthorStatistics

from api.utils.links import build_pagination_links, build_entity_links
from api.utils.metadata import build_batch_meta, build_entity_meta
from api.utils.parsing import parse_entity_keys
from api.utils.query import build_query
from api.utils.validation import validate_key, validate_parent_existance

from api.service.base import ServiceConfig

from api.response_builders.batches import format_response_batch

# Define configurations for batch services
# --- WORKS ---
WORKS = ServiceConfig(
    router_entity_type='work',
    repository_function=works_repo.get_works_by_work_key,
    response_base_model=Work,
)

WORKS_AVAILABILITY = ServiceConfig(
    router_entity_type='work',
    repository_function=works_repo.get_availability_by_work_key,
    response_base_model=WorkAvailability
)

WORKS_RATINGS = ServiceConfig(
    router_entity_type='work',
    repository_function=works_repo.get_ratings_by_work_key,
    response_base_model=WorkRatings
)

WORKS_OVERVIEW = ServiceConfig(
    router_entity_type='work',
    repository_function=works_repo.get_overview_by_work_key,
    response_base_model=WorkOverview
)

# --- AUTHORS ---
AUTHORS = ServiceConfig(
    router_entity_type='author',
    repository_function=authors_repo.get_authors_by_author_key,
    response_base_model=Author,
)

AUTHORS_STATISTICS = ServiceConfig(
    router_entity_type='author',
    repository_function=authors_repo.get_author_statistics_by_author_key,
    response_base_model=AuthorStatistics,
)

# --- EDITIONS ---
EDITIONS = ServiceConfig(
    router_entity_type='edition',
    repository_function=editions_repo.get_editions_by_edition_key,
    response_base_model=Edition,
)

# Dictionary with all batch configurations
ENTITY_CONFIGS = {
    'works': WORKS,
    'works_availability': WORKS_AVAILABILITY,
    'works_ratings': WORKS_RATINGS,
    'works_overview': WORKS_OVERVIEW,

    'authors': AUTHORS,
    'authors_statistics': AUTHORS_STATISTICS,

    'editions': EDITIONS,
}

def entity_service(
        connection: psycopg2.extensions.connection,
        request: Request,
        configuration: str,
        key: str,
        limit: int,
        offset: int,
):
    """
    Execute a standardized entity retrieval workflow

    This service is used by entity endpoints that retrieve a single
    resource associated with a validated Open Library key

    The service performs request validation, repository execution,
    metadata generation, link generation, and response formatting,
    returning a consistent API response structure across entity types

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param request: Request, current FastAPI request object used for query and link generation
    :param configuration: str, resource configuration to use
    :param key: str, entity key used for validation and filtering
    :param limit: int, maximum number of records returned
    :param offset: int, number of records skipped before returning results

    :returns: EntityResponse[T], standardized entity response containing 'data', 'meta' and 'links'
    """

    # Current batch configuration
    resource_config = ENTITY_CONFIGS[configuration]

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Validate if the key is a valid work key
    validate_key(
        key=key,
        entity_type=resource_config.router_entity_type,
        query=query
    )

    # Fetch data
    results = resource_config.repository_function(
        connection=connection,
        key=key,
        limit=limit,
        offset=offset
    )

    # If no data is returned then error is raised
    validate_parent_existance(
        total_parents=results['total_parents'],
        entity_type=resource_config.router_entity_type,
        query=query
    )

    # Build links
    links = build_entity_links(self=query)

    # Build metadata
    meta = build_entity_meta(entity_type=resource_config.router_entity_type)

    # Format and return consistent API response structure
    return format_response_entity(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=resource_config.response_base_model
    )