"""
Contains all base urls for quering Open Library API
"""

import requests

# ---------------------------------------------------------------------------------------------------------
# --- Open Library API - IDs small explanation ---
# Work ID    -> OLxxxxW (the abstract work, e.g. Pride and Prejudice)
# Edition ID -> OLxxxxM (specific edition)
# Author ID  -> OLxxxxA (specific author)
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
# --- Parameters for quering the API ---
# Limiting to 100 records per page and maximum 20 pages
LIMIT = 100

# Setting the connection and reading timeouts
CONNECT_TIMEOUT = 15
READ_TIMEOUT = 15
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def request_wrapper(
        base_url: str,
        request_params: dict,
        connect_timeout: float = CONNECT_TIMEOUT,
        read_timeout: float = READ_TIMEOUT
) -> dict | None :
    """
    Basic wrapper for requests with error handling

    :param base_url : str, the base url for the request
    :param request_params: dict, dictionary containing the parameters of the request
    :param connect_timeout: float, connection timeout
    :param read_timeout: float, reading timeout
    :return: dict | None, returns JSON response or None in case there was an error
    """

    try:
        # Querying the API
        response = requests.get(
            base_url,
            params=request_params,
            timeout=(connect_timeout, read_timeout)
        )

        # If the URL is invalid or returns a 4xx/5xx status code, it raises an HTTPError.
        response.raise_for_status()

        # Returns the JSON response as a dictionary
        return response.json()

    except requests.exceptions.RequestException as e:
        # Print error message and return None
        print(f"Request failed: {e}")
        return None
# ---------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------
# --- Search  ---

# Example: https://openlibrary.org/search.json?subject={SUBJECT}&page={PAGE}&limit={LIMIT}
#          This returns records in JSON format with a certain subject,
#          limiting to certain number of records by page and in a specified page of the results

# Source for more fields: https://openlibrary.org/dev/docs/api/search
SEARCH_BASE_URL = 'https://openlibrary.org/search.json'

def search_OL(limit: int = LIMIT, **kwargs) -> dict | None:
    """
    Function for quering Open Library API to retrieve book data
    :param limit: int, maximum number of records by page
    :param kwargs:  dict, dictionary containing additional parameters for the query (Read more: https://openlibrary.org/dev/docs/api/search)
    :return: dict | None, returns JSON response or None in case there was an error
    """

    # Set up the parameters for the query
    request_params = {'limit': limit}

    # Add the new parameters as passed
    request_params.update(kwargs)

    # Request and return the JSON response
    return request_wrapper(SEARCH_BASE_URL, request_params)
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
# TODO: https://openlibrary.org/books/OL45650119M.json
#       OL45650119M is the edition_key and it returns info

# TODO: https://openlibrary.org/search/authors.json?q=romance&limit=1
#       this searches for romance authors

# TODO: https://openlibrary.org/authors/OL7412785A.json
#       this searches for specific author data

# TODO: https://openlibrary.org/api/get_many?keys=%5B%22/authors/OL7412785A%22,%22/authors/OL7300387A%22%5D
#       this returns many authors or books