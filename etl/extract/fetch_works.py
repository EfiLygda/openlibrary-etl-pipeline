"""
STEP 1: Fetch and extract general works under the GERNE via Open Library API's SEARCH

DETAILS:
1. Not all works are extracted, config.LIMIT, config.MAX_PAGES are used as to not overload the API
2. GERNE refers to config.api.GENRE
3. The query uses the SEARCH basic url (See example SEARCH @ etl/extract/docs/entrypoints.md)
4. All pages of records are saved as JSON files @ data/raw_pages/{GERNE}/works
"""

import os
import requests

from open_library import Client

from utilities.rate_limit import wait
from utilities.logging import set_logger

from config.paths import SEARCH_DIR
from config.api import LIMIT, MAX_PAGES, GENRE, GENRE_facet, MAX_ATTEMPTS

logger = set_logger('FETCH_WORKS')

def run():
    # ----------------------------------------------------------------------------------
    # --- Querying Open Library API ---

    logger.info(f'Starting extraction of first {MAX_PAGES} pages via SEARCH query')

    # Setting up an Open Library Client for querying the API
    client = Client()

    # Setting the page limit
    client.LIMIT = LIMIT

    # For each page in the results save the records in JSON format
    for page in range(1, MAX_PAGES+1):

        # Print a message to show progress
        # print(f'({page}/{MAX_PAGES}) Extracting {GENRE} works\' metadata...', end='\r')

        # Set up the file name for saving the response
        filename = f'SEARCH_p{page}.json'
        filepath = os.path.join(SEARCH_DIR, filename)

        for _ in range(MAX_ATTEMPTS):

            # Try to extract the data during these attempts
            # Possible errors:
            # 1. connection errors: requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout
            # 2. no data available: requests.exceptions.HTTPError
            try:

                # Save the response as a JSON file
                client.save_search(filename=filepath, subject=GENRE_facet, page=page)

                break

            except (
                requests.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout
            ) as e:

                # In case of an error print a message
                # print(f'\nDid not connect or found data for \'{author_name}\'. Trying again...', end='\n')
                logger.error(f'Did not connect or found data for page \'{page}\'. Trying again...')

                # Politely wait more than 5 seconds, especially of a connection error
                wait(5)

        # Politely wait more than 3 seconds for each request
        # Adding a random seconds between 0 and 1.5 to the 3, in order to simulate human behavior
        wait(3)

        logger.info(f'Finished extraction of page {page}/{MAX_PAGES} to file {filename}')

    logger.info('Finished extraction of all pages via SEARCH query')
    # ----------------------------------------------------------------------------------
