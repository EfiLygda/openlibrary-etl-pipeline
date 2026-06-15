"""
Transformation utilities for formatting database query results
"""

from typing import TypeVar, Type
from pydantic import BaseModel

from api.schemas.entities.core import EntityType
from api.schemas.responses import APIResponse, LinksResponse

T = TypeVar('T', bound=BaseModel)

# -------------------------------------------------------------------
# Basic API Response
# -------------------------------------------------------------------

def format_records(
        records: list | None,
        fields: list[str] | None,
        model: Type[T]
) -> list[T]:
    """
    Formats list of records into a list of dictionaries

    :param records: list, list of records containing values
    :param fields: list[str], list of field names corresponding to each value in a record
    :param model: Type[T], pydantic model class used to transform each record into a typed object
    :return: list, list of dictionaries mapping field names to record values
                   Returns an empty list if the input is invalid
    """
    if not model:
        raise TypeError('\'model\' is required')

    # In case no records or fields were passed then return empty list
    if not records or not fields:
        return []

    # Set up results list
    results = []

    # For each record make a zip object of each field and value
    for record in records:

        # In case no the same amount of record values and fields are
        # given then return empty list
        if len(record) != len(fields):
            return []

        # Convert data to dictionary
        data = dict(zip(fields, record))

        # Convert the dictionary to the model and append to the list of results
        results.append(model(**data))

    # return results
    return results

def format_response(
        query: str,
        endpoint: str,
        method: str,
        records: list,
        column_names: list[str],
        model: Type[T],
) -> APIResponse[T]:
    """
    Formats the API's final response

    :param query: str, the query used for the API
    :param endpoint: str, the endpoint used for quering the API
    :param method: str, HTTP method used (GET, POST, PUT, DELETE, PATCH, OPTIONS, and HEAD)
    :param records: list, list of records containing values
    :param column_names: list[str], list of column names corresponding to each value in a record
    :param model: Type[T], pydantic model class used to transform each record into a typed object

    :return: dict, dictionary mapping the API's response
    """

    # Format the records
    formatted_records = format_records(
        records=records,
        fields=column_names,
        model=model
    )

    return APIResponse(
        query=query,
        endpoint=endpoint,
        method=method,
        entity_count=len(formatted_records),
        results=formatted_records
    )


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
    'work': f'/works/123', # TODO: Add endpoint /editions/key/work
}

def format_link_response(
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

