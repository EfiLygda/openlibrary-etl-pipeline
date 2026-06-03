"""
STEP 6: Extract all editions' data

DETAILS:
1. Data are saved in a JSON file @ data/raw_pages/{GENRE_facet}/books
"""
import os
import requests

from open_library import Client

from config.paths import KEYS_DIR, BOOKS_DIR
from config.api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.batching import make_batches
from utilities.rate_limit import  wait
from utilities.logging import set_logger

logger = set_logger('FETCH_BOOKS')

def run():

    logger.info('Starting extraction of books \'editions\' data')

    # Setting up thw Open Library client for querying the API
    client = Client()

    # Loading the general work keys and book keys file
    work_book_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_works_books_keys.json')
    work_book_keys = load_json(work_book_keys_filepath)

    # Extracting all book keys from the file
    book_keys = [
        book_key
        for book_keys in work_book_keys.values()
        for book_key in book_keys
    ]

    # Setting up the limit of querying to 100 keys by page
    client.LIMIT = 100

    # Make batches of keys
    key_batches = make_batches(book_keys, client.LIMIT)

    # For each key batch fetch all book data
    for i, key_batch in enumerate(key_batches):

        # Progress message
        # print(f'({i+1}/{len(key_batches)}) Extracting books\'/editions\' data...', end='\r')
        logger.info(f'({i+1}/{len(key_batches)}) Extracting books editions\' data')

        for _ in range(MAX_ATTEMPTS):

            # Try to extract the data during these attempts
            # Possible errors:
            # 1. connection errors: requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout
            # 2. no data available: requests.exceptions.HTTPError
            try:

                # Fetch the book data
                books = client.get_many(key_batch)

                # Setting up the path for the file that will contain the data
                filename = f'BOOKS_p{i+1}.json'
                filepath = os.path.join(BOOKS_DIR, filename)

                # Save the book data
                save_json(books, filepath)

                break

            except (
                requests.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout
            ) as e:

                # In case of an error print a message
                # print(f'\nDid not connect or found data for \'{author_name}\'. Trying again...', end='\n')
                logger.error(f'Did not connect or found data for \'{author_name}\'. Trying again...')

                # Politely wait more than 5 seconds, especially of a connection error
                wait(5)

        # Politely wait more than 5 seconds for each request
        wait(5)

    logger.info('Finished extraction of books\'/editions\' data')
