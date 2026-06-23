"""
Transformation utilities for formatting database batch query results
"""

from typing import TypeVar, Type
from pydantic import BaseModel

from api.response_builders.entities import _format_records
from api.schemas.links import PaginationLinks
from api.schemas.metadata import BatchMeta
from api.schemas.responses import BatchResponse

T = TypeVar('T', bound=BaseModel)

def format_response_batch(
        records: list,
        column_names: list[str],
        meta: dict,
        links: dict,
        model: Type[T],
) -> BatchResponse[T]:
    """
    Formats the API's final batch response

    :param records: list, list of records containing values
    :param column_names: list[str], list of column names corresponding to each value in a record
    :param meta: dict, dictionary with the metadata for the relationship query (has 'total', 'limit' ,'offset')
    :param links: dict, dictionary with the pagination links for the query (has 'self', 'next' ,'prev')
    :param model: Type[T], pydantic model class used to transform each record into a typed object

    :return: dict, dictionary mapping the API's response
    """

    return BatchResponse(

        data = _format_records(
            records=records,
            fields=column_names,
            model=model
        ),

        meta = BatchMeta(**meta),
        links = PaginationLinks(**links)
    )