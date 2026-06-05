"""
STEP 5: Extract all editions' keys associated with a work

DETAILS:
1. Data are saved in a JSON file @ data/keys
"""
import os
import requests

from open_library import Client

from config.paths import KEYS_DIR
from config.api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.rate_limit import wait
from utilities.logging import set_logger

logger = set_logger('FETCH_BOOKS_KEYS_VIA_WORK_KEY')

def run():

    logger.info('Starting extraction of edition keys for each general work')

    # Setting up thw Open Library client for querying the API
    client = Client()

    # Loading the file containing the general work keys
    work_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_work_keys.json')
    work_keys = load_json(work_keys_filepath)

    # Setting up the dictionary that will contain the work keys and book keys
    work_books_keys = dict()

    # For each work key all book keys that are associated with it are extracted
    for i, work_key in enumerate(work_keys):

        # Set up the maximum number of attempts to fetch the data
        for _ in range(MAX_ATTEMPTS):

            # Try to extract the data during these attempts
            # Possible errors:
            # 1. connection errors: requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout
            # 2. no data available: requests.exceptions.HTTPError
            try:
                # Fetch all editions associated with the current work key
                data = client.get_work(work_key, editions=True)

                # Total editions for current general work
                total_editions = data['size']

                # Check if there is a next page
                # Note: The query only returns 50 records, but more can be available via the offset parameter
                has_next_page = True if total_editions > 50 else False

                # Setting up possible offset
                offset = 0

                # While there is a next page with 50 more editions extract them
                while has_next_page:

                    # Add to the offset 50 more records for next page
                    offset += 50

                    # Query the next page with next 50 editions
                    data_offset = client.get_work(work_key, editions=True, offset=offset)

                    # Add new edition data to previous records
                    data['entries'] += data_offset['entries']

                    # Check if current page has 50 more records
                    has_next_page = True if 'next' in data_offset['links'] else False

                    wait()

                break

            except (
                requests.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError
            ) as e:

                logger.error(f"Failed to fetch work {work_key}: {e}")

                wait()

        # Extract the book entries from the result of the query
        books = data['entries']

        # Set up the list that will contain all book keys for the current work
        current_works_book_keys = []

        # Add all book keys to the list
        for book in books:
            current_works_book_keys.append(book['key'])

        # Add the list to dictionary
        work_books_keys[work_key] = current_works_book_keys

        # Progress message
        # print(f'({i+1}/{len(work_keys)}) Extracting edition keys for each general work...', end='\r')
        # logger.info(f'({i+1}/{len(work_keys)}) Extracting {total_editions} edition keys for {work_key} general work')

        # Logging possible missing data
        if total_editions == len(data['entries']):
            logger.info(
                f'({i+1}/{len(work_keys)}) Total of {total_editions} edition keys were extracted for work \'{work_key}\''
            )
        else:
            logger.error(f'({i+1}/{len(work_keys)}) Not all edition keys were extracted for work \'{work_key}\'')


        # Politely wait more than 1 seconds for each request
        wait()

    # Setting up the result's filepath
    result_filename = f'{GENRE_facet}_works_books_keys.json'
    result_filepath = os.path.join(KEYS_DIR, result_filename)

    # Save the result as a JSON file
    save_json(work_books_keys, result_filepath)

    logger.info('Finished extraction of edition keys for each general work')
