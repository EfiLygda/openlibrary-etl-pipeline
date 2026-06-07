"""
STEP 1: Fetch and extract general works under the GERNE via Open Library API's SEARCH

DETAILS:
1. Not all works are extracted, config.LIMIT, config.MAX_PAGES are used as to not overload the API
2. GERNE refers to config.api.GENRE
3. The query uses the SEARCH basic url (See example SEARCH @ etl/extract/docs/entrypoints.md)
4. All pages of records are saved as JSON files @ data/raw_pages/{GERNE}/works
"""

import os

import open_library

from utilities.rate_limit import wait
from utilities.logging import set_logger, log_result
from utilities.retry import retry

from config.paths import SEARCH_DIR
from config.api import LIMIT, MAX_PAGES, GENRE_facet, MAX_ATTEMPTS

logger = set_logger('FETCH_WORKS')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def save_search_page(
        client: open_library.Client,
        filepath: str,
        page: int
) -> None:
    """
    Save a single search page to a JSON file.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    :param client: open_library.Client, OpenLibrary API client
    :param filepath: str, file path for JSON output
    :param page: int, page number of search results to fetch

    :return: None
    """
    # Save the current page's data in JSON format
    client.save_search(filename=filepath, subject=GENRE_facet, page=page)


def run():
    # ----------------------------------------------------------------------------------
    # --- Querying Open Library API ---

    logger.info(f'Starting extraction of first {MAX_PAGES} pages via SEARCH query')

    # Setting up an Open Library Client for querying the API
    client = open_library.Client()

    # Setting the page limit
    client.LIMIT = LIMIT

    # For each page in the results save the records in JSON format
    for page in range(1, MAX_PAGES+1):

        # Set up the file name for saving the response
        filename = f'SEARCH_p{page}.json'
        filepath = os.path.join(SEARCH_DIR, filename)

        # Save current page with built-in retries in case of errors
        results = save_search_page(client, filepath, page)

        # Log messages to be used
        success_msg = (
            f'SEARCH_SUCCESS page={page}/{MAX_PAGES} '
            f'file={filename} '
            f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
            f'duration={results['duration']:.2f}s'
        )

        error_msg = (
            f'SEARCH_FAILED page={page}/{MAX_PAGES} '
            f'error_type={results['error']} '
            f'file={filename} '
            f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
            f'duration={results['duration']:.2f}s'
        )

        # Success flag
        is_successful = results['success']

        # Log the result using the proper message and level
        log_result(
            logger=logger,
            is_successful=is_successful,
            success_msg=success_msg,
            error_msg=error_msg
        )

        # Politely wait more than 1 seconds for each request
        wait()

    logger.info('Finished extraction of all pages via SEARCH query')
    # ----------------------------------------------------------------------------------
