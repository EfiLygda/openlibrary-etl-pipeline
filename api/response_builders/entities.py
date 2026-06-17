"""
Transformation utilities for formatting database entity query results
"""

from typing import TypeVar, Type
from pydantic import BaseModel

from api.schemas.responses import EntityResponse, RelationshipResponse

T = TypeVar('T', bound=BaseModel)

# -------------------------------------------------------------------
# Basic API Response
# -------------------------------------------------------------------

def _format_records(
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

def format_response_entity(
        records: list,
        column_names: list[str],
        meta: dict,
        links: dict,
        model: Type[T],
) -> EntityResponse[T]:
    """
    Formats the API's final response

    :param records: list, list of records containing values
    :param column_names: list[str], list of column names corresponding to each value in a record
    :param meta: dict, dictionary with the metadata for the entity query (has 'type')
    :param links: dict, dictionary with the pagination links for the query (has 'self')
    :param model: Type[T], pydantic model class used to transform each record into a typed object

    :return: dict, dictionary mapping the API's response
    """

    return EntityResponse(

        data = _format_records(
            records=records,
            fields=column_names,
            model=model
        ),

        meta = meta,
        links = links
    )

def format_response_relationship(
        records: list,
        column_names: list[str],
        meta: dict,
        links: dict,
        model: Type[T],
) -> RelationshipResponse[T]:
    """
    Formats the API's final response

    :param records: list, list of records containing values
    :param column_names: list[str], list of column names corresponding to each value in a record
    :param meta: dict, dictionary with the metadata for the relationship query (has 'total', 'limit' ,'offset')
    :param links: dict, dictionary with the pagination links for the query (has 'self', 'next' ,'prev')
    :param model: Type[T], pydantic model class used to transform each record into a typed object

    :return: dict, dictionary mapping the API's response
    """

    return RelationshipResponse(

        data = _format_records(
            records=records,
            fields=column_names,
            model=model
        ),

        meta = meta,
        links = links
    )