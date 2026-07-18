"""
STEP 9: Fetch all general works' ratings from Open Library

DETAILS:
1. Data are saved in a JSON file @ data/raw_pages/{GENRE_facet}/works_ratings
"""
import os

from data_pipeline import open_library

from config.paths import KEYS_DIR, WORKS_RATINGS_DIR
from config.openlibrary_api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.rate_limit import wait
from utilities.retry import retry
from utilities.logging import set_logger, log_result

logger = set_logger('FETCH_WORKS_RATINGS')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def fetch_work_ratings(
        client: open_library.Client,
        work_key: str,
) -> dict | None:
    """
    Fetch rating data for a given OpenLibrary work.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    The function retrieves rating information associated with a work key
    and returns the raw API response. If no rating data is available, the
    function may return None.

    :param client: open_library.Client, OpenLibrary API client
    :param work_key: str, OpenLibrary work identifier (e.g. "/works/OLxxxxW")

    :return: dict | None containing rating data for the work
    """
    # Fetch all editions associated with the current work key
    data = client.get_work(work_key, ratings=True)

    return data

def run():

    logger.info('STAGE_START')

    # Setting up thw Open Library client for querying the API
    client = open_library.Client()

    # Loading the file containing the general work keys
    work_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_work_keys.json')
    work_keys = load_json(work_keys_filepath)

    # Setting up the result's filepath
    result_filename = f'{GENRE_facet}_works_ratings.json'
    result_filepath = os.path.join(WORKS_RATINGS_DIR, result_filename)

    # Setting up the dictionary that will contain the work keys and book keys
    works_ratings = dict()

    # For each work key all book keys that are associated with it are extracted
    for i, work_key in enumerate(work_keys):

        # Fetch current work ratings with built-in retries in case of errors
        results = fetch_work_ratings(client, work_key)

        # Get only the data
        data = results['results']

        # Log messages to be used
        success_msg = (
            f'WORKS_RATINGS_SUCCESS work={i+1}/{len(work_keys)} '
            f'file={result_filename} '
            f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
            f'duration={results['duration']:.2f}s'
        )

        error_msg = (
            f'WORKS_RATINGS_SUCCESS work={i+1}/{len(work_keys)} '
            f'error_type={results['error']} '
            f'file={result_filename} '
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

        # Move to next work in case of no data
        if not is_successful:
            continue

        # Ratings' counts for current general work
        ratings = data['counts']

        # Normalize the work key
        normalized_work_key = open_library.KeyHandler.normalize_key(work_key)

        # Add ratings to final result dictionary
        works_ratings[normalized_work_key] = ratings

        # Politely wait more than 1 seconds for each request
        wait()

    # Save the result as a JSON file
    save_json(works_ratings, result_filepath)

    logger.info('STAGE_COMPLETE')
