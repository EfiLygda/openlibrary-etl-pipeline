"""
Transformation utilities for formatting database links query results
"""

from typing import TypeVar
from pydantic import BaseModel

from api.schemas.entities.core import EntityType
from api.schemas.responses import LinksResponse

T = TypeVar('T', bound=BaseModel)


# -------------------------------------------------------------------
# Links API Response
# -------------------------------------------------------------------

# --- Links Builder Functions ---
make_work_links = lambda key: {
    'self': f'/works/{key}',
    'authors': f'/works/{key}/authors',
    'editions': f'/works/{key}/editions',
    'series': f'/works/{key}/series',
    'ratings': f'/works/{key}/ratings',
    'overview': f'/works/{key}/overview',
    'availability': f'/works/{key}/availability',
}

make_author_links = lambda key: {
    'self': f'/authors/{key}',
    'works': f'/authors/{key}/works',
    'editions': f'/authors/{key}/editions',
    'statistics': f'/authors/{key}/statistics',
    'alternative_names': f'/authors/{key}/alternative_names',
}

make_edition_links = lambda key: {
    'self': f'/editions/{key}',
    'details': f'/editions/{key}/details',
    'contents': f'/editions/{key}/contents',
    'publishing': f'/editions/{key}/publishing',
    'contributors': f'/editions/{key}/contributors',
    'works': f'/editions/{key}/works',
}

def format_links_response(
        key: str,
        key_type: EntityType
) -> LinksResponse[T]:
    """
    Build a LinksResponse object for a given entity key and entity type

    The function selects the appropriate link builder based on the entity type,
    generates the corresponding links, and returns them wrapped in a LinksResponse.

    :param key: str, unique identifier for the entity (work, author, or edition).
    :param key_type: EntityType, type of entity used to determine which link builder to use.
    :return: LinksResponse[T], a response containing the key, entity type, and generated links.
    """

    # Ensuring key_type is a proper Enum member
    key_type = EntityType(key_type)

    # Mapping each entity type to its corresponding link builder function
    link_builders = {
        EntityType.work: make_work_links,
        EntityType.author: make_author_links,
        EntityType.edition: make_edition_links,
    }

    # Call the correct builder function based on entity type
    # If link generation fails, fallback to None
    try:
        links = link_builders[key_type](key)
    except ValueError:
        links = None

    # Construct and return the response model
    return LinksResponse(
        key=key,
        type=key_type,
        links=links
    )
