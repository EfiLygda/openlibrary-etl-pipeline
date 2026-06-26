"""
Languages service

Provides a reusable service layer for batch retrieval of API languages
identified by their ISO 693-2 codes

Note: ISO 693-2 codes: https://www.loc.gov/standards/iso639-2/php/code_list.php
"""

from fastapi import Request
from pycountry import languages

from api.errors import BaseErrors

from api.schemas.languages import Language
from api.schemas.responses import LanguagesResponse

from api.utils.links import build_pagination_links
from api.utils.metadata import build_search_meta
from api.utils.parsing import parse_comma_separated_text
from api.utils.query import build_query

from api.response_builders.languages import format_response_language

def language_service(
        request: Request,
        limit: int,
        offset: int,
        lang: str | None = None,
) -> LanguagesResponse:
    """
    Execute a standardized language retrieval workflow

    :param request: Request, current FastAPI request object used for query and link generation
    :param limit: int, maximum number of records returned
    :param offset: int, number of records skipped before returning results
    :param lang: str | None, comma-separated entity languages used for filtering

    :returns: BatchResponse[T], standardized batch response containing 'data', 'meta' and 'links'
    """

    # Build the current query
    # Like '{path_url}?{query_url}'
    query = build_query(request)

    # Build translation dictionary of languages ISO 693-2 codes
    languages_codes_translations = {
        lang.alpha_3: lang.name for lang in languages
    }

    # If 'lang' parameter is given then
    # fetch only the given codes' data
    if lang:

        # Separate languages codes in normalized
        # strings or add the lone code in a list
        langs = parse_comma_separated_text(lang)

        # Convert codes and language names to list of
        # Language models if a code is valid ISO 693-2 code
        data = [
            Language(
                code=lang,
                name=languages_codes_translations.get(lang)
            )
            for lang in langs
            if lang in languages_codes_translations.keys()
        ]

    else:

        # If no 'lang' parameter is given then list all records
        data = [
            Language(
                code=lang,
                name=languages_codes_translations.get(lang)
            )
            for lang in languages_codes_translations
        ]

    # Paginate data using given limit and offset
    results = data[offset:offset + limit]

    # If no data is returned then error is raised
    if len(results) == 0:
       raise BaseErrors.NotFound(query)

    # Build links
    links = build_pagination_links(
        url=query,
        total=len(data),
        limit=limit,
        offset=offset
    )

    # Build metadata using search metadata
    meta = build_search_meta(
        total=len(data),
        limit=limit,
        offset=offset
    )

    # Format and return consistent API response structure
    return format_response_language(
        records=results,
        meta=meta,
        links=links
    )
