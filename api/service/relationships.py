"""
Relationship service implementations

This module provides reusable service-layer functionality for relationship-based
endpoints that return child resources associated with a parent entity key
"""

import psycopg2
from fastapi import Request

import api.repository.works as works_repo
import api.repository.authors as authors_repo
import api.repository.editions as editions_repo

from api.utils.links import build_pagination_links
from api.utils.metadata import build_relationship_meta
from api.utils.query import build_query
from api.utils.validation import validate_key, validate_parent_existance

from api.service.base import ServiceConfig

from api.schemas.entities.summaries import AuthorSummary, EditionSummary, WorkSummary
from api.schemas.entities.relationships import (
    WorkSeries,
    AuthorAlternativeNames,
    EditionDetails,
    EditionContents,
    EditionPublishing,
    EditionContributor
)

from api.response_builders.entities import format_response_relationship

# Define configurations for batch services
# --- WORKS ---
WORKS_AUTHORS = ServiceConfig(
    repository_function=works_repo.get_authors_by_work_key,
    response_base_model=AuthorSummary,
    router_entity_type='work',
    endpoint_child_type='author',
)

WORKS_EDITIONS = ServiceConfig(
    repository_function=works_repo.get_editions_by_work_key,
    response_base_model=EditionSummary,
    router_entity_type='work',
    endpoint_child_type='edition',
)

WORKS_SERIES = ServiceConfig(
    repository_function=works_repo.get_series_by_work_key,
    response_base_model=WorkSeries,
    router_entity_type='work',
    endpoint_child_type='series',
)

# --- AUTHORS ---
AUTHORS_WORKS = ServiceConfig(
    repository_function=authors_repo.get_works_by_author_key,
    response_base_model=WorkSummary,
    router_entity_type='author',
    endpoint_child_type='work',
)

AUTHORS_EDITIONS = ServiceConfig(
    repository_function=authors_repo.get_editions_by_author_key,
    response_base_model=EditionSummary,
    router_entity_type='author',
    endpoint_child_type='edition',
)

AUTHORS_ALTERNATIVE_NAMES = ServiceConfig(
    repository_function=authors_repo.get_author_alternative_names_by_author_key,
    response_base_model=AuthorAlternativeNames,
    router_entity_type='author',
    endpoint_child_type='alternative_name',
)

# --- EDITIONS ---
EDITIONS_WORK = ServiceConfig(
    repository_function=editions_repo.get_works_by_edition_key,
    response_base_model=WorkSummary,
    router_entity_type='edition',
    endpoint_child_type='work',
)

EDITIONS_DETAILS = ServiceConfig(
    repository_function=editions_repo.get_details_by_edition_key,
    response_base_model=EditionDetails,
    router_entity_type='edition',
    endpoint_child_type='detail',
)

EDITIONS_CONTENTS = ServiceConfig(
    repository_function=editions_repo.get_contents_by_edition_key,
    response_base_model=EditionContents,
    router_entity_type='edition',
    endpoint_child_type='content',
)

EDITIONS_PUBLISHING = ServiceConfig(
    repository_function=editions_repo.get_publishing_by_edition_key,
    response_base_model=EditionPublishing,
    router_entity_type='edition',
    endpoint_child_type='publishing',
)

EDITIONS_CONTRIBUTORS = ServiceConfig(
    repository_function=editions_repo.get_contributors_by_edition_key,
    response_base_model=EditionContributor,
    router_entity_type='edition',
    endpoint_child_type='contributor',
)

# Dictionary with all batch configurations
RELATIONSHIP_CONFIGS = {
    'works_authors': WORKS_AUTHORS,
    'works_editions': WORKS_EDITIONS,
    'works_series': WORKS_SERIES,

    'authors_works': AUTHORS_WORKS,
    'authors_editions': AUTHORS_EDITIONS,
    'authors_alternative_names': AUTHORS_ALTERNATIVE_NAMES,

    'editions_work': EDITIONS_WORK,
    'editions_details': EDITIONS_DETAILS,
    'editions_contents': EDITIONS_CONTENTS,
    'editions_publishing': EDITIONS_PUBLISHING,
    'editions_contributors': EDITIONS_CONTRIBUTORS,
}

def relationship_service(
        connection: psycopg2.extensions.connection,
        request: Request,
        configuration: str,
        key: str,
        limit: int,
        offset: int,
):
    """
    Execute a standardized relationship retrieval workflow

    This service is used by relationship endpoints that retrieve
    child resources associated with a validated parent entity key

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param request: Request, current FastAPI request object used for query and link generation
    :param configuration: str, relationship configuration to use
    :param key: str, parent entity key used for validation and filtering
    :param limit: int, maximum number of child records returned
    :param offset: int, number of child records skipped before returning results

    :returns: RelationshipResponse[T], standardized relationship response containing 'data', 'meta', and 'links'
    """

    # Current batch configuration
    resource_config = RELATIONSHIP_CONFIGS[configuration]

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
    links = build_pagination_links(
        url=query,
        total=results['total_children'],
        limit=limit,
        offset=offset
    )

    # Build metadata
    meta = build_relationship_meta(
        parent_type=resource_config.router_entity_type,
        parent_key=key,
        child_type=resource_config.endpoint_child_type,
        total_children=results['total_children'],
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_relationship(
        records=results['data'],
        column_names=results['column_names'],
        meta=meta,
        links=links,
        model=resource_config.response_base_model,
    )