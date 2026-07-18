"""
STEP 8: Fetch all author statistics from Open Library

DETAILS:
1. Data are saved in a JSON file @ data/raw_pages/{GENRE_facet}/author_statistics
"""
import os

from data_pipeline import open_library

from config.paths import KEYS_DIR, AUTHORS_STATISTICS_DIR
from config.openlibrary_api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.rate_limit import wait
from data_pipeline.utils.retry import retry
from utilities.logging import set_logger, log_result

logger = set_logger('FETCH_AUTHOR_STATISTICS')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def fetch_author_stats(
        client: open_library.Client,
        author_name: str
) -> None:
    """
    Fetch author statistics from the OpenLibrary API using a search query.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    The function performs an author search using the provided author name and
    returns the raw API response containing matching author records and metadata.

    :param client: open_library.Client, OpenLibrary API client
    :param author_name: str, name of the author to search for

    :return: dict containing the API response with author search results
    """
    # Fetch authors' statistics
    data = client.search(query=author_name, mode='authors')

    return data

def run():

    logger.info('STAGE_START')

    # Setting up thw Open Library client for querying the API
    client = open_library.Client()

    # Loading the general work keys and book keys file
    authors = load_json(
        os.path.join(KEYS_DIR, f'{GENRE_facet}_authors_key_name.json')
    )

    # Setting up the final file's path
    filename = f'{GENRE_facet}_author_statistics.json'
    filepath = os.path.join(AUTHORS_STATISTICS_DIR, filename)

    # Setting up the dictionary that will contain the data
    authors_statistics = dict()

    # For each author name the data will be fetched
    for i, (author_key, author_name) in enumerate(authors.items()):

        # Get the key from the normalized key (basically remove '\authors\' from the key)
        denormalized_key = open_library.KeyHandler.get_key(author_key)

        # Fetch author statistics via author name with built-in retries in case of errors
        results = fetch_author_stats(client, author_name)

        # Log messages to be used
        success_msg = (
            f'SEARCH_AUTHORS_SUCCESS author={i + 1}/{len(authors.items())} '
            f'file={filename} '
            f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
            f'duration={results['duration']:.2f}s'
        )

        error_msg = (
            f'SEARCH_AUTHORS_FAILED author={i + 1}/{len(authors.items())} '
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

        # Move to next author if there was no success in fetching the editions
        if not is_successful:
            continue

        # Get only data from results
        data = results['results']

        # The response can contain more than one author's data, so there is a need
        # to search by key in the results, in order to keep the right record
        found_key = False

        # Search in the response, in order to find the right record for the curren author
        # via his/her respective author key
        for author in data['docs']:

            # Checking if the current record refers to the current author
            if author['key'] == denormalized_key:
                # Change fount_key to True
                found_key = True

                # Add the record to the dictionary that will contain the final data
                authors_statistics[denormalized_key] = author

                # Break the search for the right record
                break

        # If none of the records refer to the current author then a message is displayed
        if not found_key:
            logger.error(f'AUTHOR_RECORD_NOT_FOUND author_name={author_name} author_key={author_key}')

        # Politely wait more than 1 seconds for the next author
        wait()

    # Exporting all authors' statistics as a JSON file
    save_json(authors_statistics, filepath)

    logger.info('STAGE_COMPLETE')
