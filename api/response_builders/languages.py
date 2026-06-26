"""
Transformation utilities for formatting database languages query results
"""

from api.schemas.links import PaginationLinks
from api.schemas.metadata import SearchMeta
from api.schemas.responses import LanguagesResponse

# -------------------------------------------------------------------
# Languages API Response
# -------------------------------------------------------------------

def format_response_language(
        records: list,
        meta: dict,
        links: dict,
) -> LanguagesResponse:
    """
    Formats the API's final language response

    :param records: list, list of records containing values like {'code': 'name'}
    :param meta: dict, dictionary with the metadata for the relationship query (has 'total', 'limit' ,'offset')
    :param links: dict, dictionary with the pagination links for the query (has 'self', 'next' ,'prev')

    :return: dict, dictionary mapping the API's response
    """

    return LanguagesResponse(
        data = records,
        meta = SearchMeta(**meta),
        links = PaginationLinks(**links)
    )