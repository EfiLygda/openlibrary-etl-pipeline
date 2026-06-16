"""
Transformation utilities for formatting database entity query results
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
        self: str,
        records: list,
        column_names: list[str],
        model: Type[T],
) -> APIResponse[T]:
    """
    Formats the API's final response

    :param query: str, the query used for the API
    :param self: str, the endpoint used for quering the API
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
        self=self,
        entity_count=len(formatted_records),
        results=formatted_records
    )