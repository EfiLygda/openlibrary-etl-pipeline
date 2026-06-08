"""
STEP 5: Extract all editions' keys associated with a work

DETAILS:
1. Data are saved in a JSON file @ data/keys
"""
import os

import open_library

from config.paths import KEYS_DIR, BOOKS_DIR
from config.api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.batching import make_batches
from utilities.rate_limit import wait
from utilities.retry import retry
from utilities.logging import set_logger, log_result

logger = set_logger('FETCH_BOOKS_VIA_WORK_KEY')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def fetch_editions_via_work_key(
        client: open_library.Client,
        work_key: str
) -> dict:
    """
    Fetch all edition records associated with a given OpenLibrary work key.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    The OpenLibrary API returns a limited number of edition records per request
    (typically 50), so this function automatically paginates through all
    available results using the offset parameter and aggregates them into a
    single dataset.

    :param client: open_library.Client, OpenLibrary API client
    :param work_key: str, work key

    :return: dict, containing total_editions and aggregated edition data
    """

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

    return {
        'total_editions': total_editions,
        'data': data
    }

def run():

    logger.info('Starting extraction of edition keys and data for each general work')

    # Setting up thw Open Library client for querying the API
    client = open_library.Client()

    # Loading the file containing the general work keys
    work_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_work_keys.json')
    work_keys = load_json(work_keys_filepath)

    # Make batches of keys
    work_keys_batches = make_batches(work_keys, batch_size=1000)

    # Setting up the dictionary that will contain the work keys and book keys
    work_books_keys = dict()

    # Counter for works
    work_counter = 0

    # For each work keys batch fetch all editions/book data
    for i, work_keys_batch in enumerate(work_keys_batches):

        # Setting up the dictionary that will contain the book data for current batch
        books_data_batch = dict()

        # Setting up current work key batch's filepath
        work_batch_filename = f'BOOKS_p{i+1}.json'
        work_batch_filepath = os.path.join(BOOKS_DIR, work_batch_filename)

        # For each work key in the current batch
        # all book keys that are associated with it and data are extracted
        for work_key in work_keys_batch:

            # Add to work counter
            work_counter += 1

            # Fetch all editions via work key with built-in retries in case of errors
            results = fetch_editions_via_work_key(
                client=client,
                work_key=work_key
            )

            # Success flag
            is_successful = results['success']

            # Check for successful extraction and in any case return the total editions
            if is_successful:
                total_editions = results['results']['total_editions']
            else:
                total_editions = 'no_data'

            # Log messages to be used
            success_msg = (
                f'SEARCH_EDITIONS_VIA_WORK_KEY_SUCCESS work={work_counter}/{len(work_keys)} '
                f'total_editions={total_editions} '
                f'batch_file={work_batch_filename} '
                f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
                f'duration={results['duration']:.2f}s'
            )

            error_msg = (
                f'SEARCH_EDITIONS_VIA_WORK_KEY_FAILED work={work_counter}/{len(work_keys)} '
                f'error_type={results['error']} '
                f'total_editions={total_editions} '
                f'batch_file={work_batch_filename} '
                f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
                f'duration={results['duration']:.2f}s'
            )

            # Log the result using the proper message and level
            log_result(
                logger=logger,
                is_successful=is_successful,
                success_msg=success_msg,
                error_msg=error_msg
            )

            # Move to next work if there was no success in fetching the editions
            if not is_successful:
                continue

            # Get only data from results
            data = results['results']['data']

            # Extract the book entries from the result of the query
            books = data['entries']

            # Set up the list that will contain all book keys for the current work
            current_works_book_keys = []

            # For each edition add book key to list and data to batch dict
            for book in books:
                # Add all book keys to the list
                current_works_book_keys.append(book['key'])

                # Add edition data to current batch's dictionary
                books_data_batch[book['key']] = book

            # Add the list to dictionary
            work_books_keys[work_key] = current_works_book_keys

            # Logging possible missing data
            if total_editions != len(data['entries']):
                logger.warning(f'EDITIONS_FAILED work={work_counter}/{len(work_keys)} '
                               f'not all edition keys were extracted for work \'{work_key}\'')

            # Politely wait more than 1 seconds for each request
            wait()

        # Save the result as a JSON file
        save_json(books_data_batch, work_batch_filepath)


    # Setting up the work and book keys' filepath
    work_book_keys_filename = f'{GENRE_facet}_works_books_keys.json'
    work_book_keys_filepath = os.path.join(KEYS_DIR, work_book_keys_filename)

    # Save the result as a JSON file
    save_json(work_books_keys, work_book_keys_filepath)

    logger.info('Finished extraction of edition keys and data for each general work')
