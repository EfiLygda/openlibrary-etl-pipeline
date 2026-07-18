"""
STEP 6: Extract all editions' data

DETAILS:
1. Data are saved in a JSON file @ data/raw_pages/{GENRE_facet}/books
"""
import os

from data_pipeline import open_library

from config.paths import KEYS_DIR, BOOKS_DIR
from config.openlibrary_api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from data_pipeline.utils.data.batching import make_batches
from data_pipeline.utils.retry import retry
from utilities.rate_limit import  wait
from utilities.logging import set_logger, log_result

logger = set_logger('FETCH_BOOKS')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def save_edition_data(
        client: open_library.Client,
        key_batch: list[str],
        filepath: str
) -> None:
    """
    Fetch and save a batch of edition (book) records from the OpenLibrary API.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    The function retrieves multiple book records in a single request using a
    batch of OpenLibrary keys and persists the resulting data to a JSON file.

    :param client: open_library.Client, OpenLibrary API client
    :param key_batch: list[str], list of OpenLibrary edition/book keys to fetch
    :param filepath: str, file path where the JSON output will be saved

    :return: None
    """

    # Fetch the book data
    books = client.get_many(key_batch)

    # Save the book data
    save_json(books, filepath)

def run():

    logger.info('STAGE_START')

    # Setting up thw Open Library client for querying the API
    client = open_library.Client()

    # Loading the general work keys and book keys file
    work_book_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_works_books_keys.json')
    work_book_keys = load_json(work_book_keys_filepath)

    # Extracting all book keys from the file
    book_keys = [
        book_key
        for book_keys in work_book_keys.values()
        for book_key in book_keys
    ]

    # Make batches of keys
    key_batches = make_batches(book_keys, client.LIMIT)

    # For each key batch fetch all book data
    for i, key_batch in enumerate(key_batches):

        # Progress message
        logger.info(f'({i+1}/{len(key_batches)}) Extracting books editions\' data')

        # Setting up the path for the file that will contain the data
        filename = f'BOOKS_p{i + 1}.json'
        filepath = os.path.join(BOOKS_DIR, filename)

        # Save current batch's edition data with built-in retries in case of errors
        results = save_edition_data(
            client=client,
            key_batch=key_batch,
            filepath=filepath
        )

        # Log messages to be used
        success_msg = (
            f'GET_MANY_SUCCESS batch={i+1}/{len(key_batches)} '
            f'file={filename} '
            f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
            f'duration={results['duration']:.2f}s'
        )

        error_msg = (
            f'GET_MANY_FAILED batch={i+1}/{len(key_batches)} '
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

    logger.info('STAGE_COMPLETE')
