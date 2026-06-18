"""
Pagination utilities
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def _build_url(
        url: str,
        params: dict | None = None
) -> str:
    """
    Update or add query parameters to a URL while preserving existing ones

    :param url: str, the url to be updated (used for building the new one)
    :param params: dict | None, contains existing (for updating existing) or new parameters for the new url

    :return: str, the new url
    """

    # Parse url to components (here we need 'query' for parameters)
    url_parts = urlparse(url)

    # Convert parameters to dictionary like {'q' = ['...'], 'limit' = ['20'], 'offset' = ['0']}
    query = parse_qs(url_parts.query)

    # Override existing parameters via params or add new ones, if given
    if params:
        for key, value in params.items():
            query[key] = [str(value)]

    # Join params dictionary to proper representation, like q='...'&limit=20&offset=0
    new_query = urlencode(query, doseq=True)

    # Replace exiting query with the new one
    replaced_query = url_parts._replace(query=new_query)

    # Unparse the new url -> convert it to valid url
    unparsed_new_url = urlunparse(replaced_query)

    # reconstruct full URL
    return str(unparsed_new_url)

def build_pagination_links(
        url: str,
        total: int,
        limit: int,
        offset: int,
) -> dict:
    """
    Build pagination navigation links for a paginated API response

    Generates standard REST-style pagination links including `self`
    `next`, and `prev` based on the current pagination state

    :param url: str, full current request URL including query parameters (used for `self`)
    :param total: int, total number of records available for the query
    :param limit: int, number of records per page
    :param offset: int, current pagination offset

    :return: dict, dictionary containing pagination links
    """

    # Set up the next and prev urls as None in case they are not to be used
    next_url = None
    prev_url = None

    # If there is a next url update the current url
    if offset + limit < total:

        # Update or add new limit and offset parameters
        params = {
            'limit': limit,
            'offset': offset + limit
        }

        # Build the next url
        next_url = _build_url(url, params)

    # If there is a prev url update the current url
    if offset > 0:

        # Update or add new limit and offset parameters
        params = {
            'limit': limit,
            'offset': max(offset - limit, 0)
        }

        # Build the prev url
        prev_url = _build_url(url, params)

    return {
        'self': _build_url(url),
        'next': next_url,
        'prev': prev_url
    }