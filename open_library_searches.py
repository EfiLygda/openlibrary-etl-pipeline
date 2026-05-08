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
# --- Search  ---

# Example: https://openlibrary.org/search.json?subject={SUBJECT}&page={PAGE}&limit={LIMIT}
#          This returns records in JSON format with a certain subject,
#          limiting to certain number of records by page and in a specified page of the results

# Source for more fields: https://openlibrary.org/dev/docs/api/search

SEARCH_BASE_URL = 'https://openlibrary.org/search.json'

def search_open_library(request_params, **kwargs):
    response = requests.get(
        SEARCH_BASE_URL,
        params=request_params,
        timeout=(kwargs['CONNECT_TIMEOUT'], kwargs['READ_TIMEOUT'])
    )

    return response
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
# --- Specific Edition of Book ---

# Example: https://openlibrary.org/works/{edition_key}.json
#          This returns records in JSON format for a specific edition of a book

EDITION_BASE_URL = 'https://openlibrary.org/works/{edition_key}.json'