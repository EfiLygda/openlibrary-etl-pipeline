"""

"""

def build_pagination_links(
        query: str,
        path_url: str,
        total: int,
        limit: int,
        offset: int,
) -> dict:
    """
    Build pagination navigation links for a paginated API response

    Generates standard REST-style pagination links including `self`
    `next`, and `prev` based on the current pagination state

    :param query: str, full current request URL including query parameters (used for `self`)
    :param path_url: str, base endpoint path without query parameters
    :param total: int, total number of records available for the query
    :param limit: int, number of records per page
    :param offset: int, current pagination offset

    :return: dict, dictionary containing pagination links
    """

    return {
        'self': query,
        'next': f'{path_url}?limit={limit}&offset={offset + limit}'
                if offset + limit < total else None,
        'prev': f'{path_url}?limit={limit}&offset={max(offset - limit, 0)}'
                if offset > 0 else None,
    }