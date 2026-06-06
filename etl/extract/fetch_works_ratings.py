"""
STEP 9: Fetch all general works' ratings from Open Library

DETAILS:
1. Data are saved in a JSON file @ data/raw_pages/{GENRE_facet}/works_ratings
"""
import os
import requests

from open_library import Client, KeyHandler

from config.paths import KEYS_DIR, WORKS_RATINGS_DIR
from config.api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.rate_limit import wait
from utilities.logging import set_logger

logger = set_logger('FETCH_WORKS_RATINGS')

def run():

    logger.info('Starting extraction of ratings for each general work')

    # Setting up thw Open Library client for querying the API
    client = Client()

    # Loading the file containing the general work keys
    work_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_work_keys.json')
    work_keys = load_json(work_keys_filepath)

    # Setting up the dictionary that will contain the work keys and book keys
    works_ratings = dict()

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
                data = client.get_work(work_key, ratings=True)

                # Ratings' counts for current general work
                ratings = data['counts']

                works_ratings[KeyHandler.normalize_key(work_key)] = ratings

                break

            except (
                requests.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError
            ) as e:

                logger.error(f"Failed to fetch work {work_key}: {e}")

                wait()

        logger.info(f'({i+1}/{len(work_keys)}) Extracted \'{work_key}\' ratings')

        # Politely wait more than 1 seconds for each request
        wait()

    # Setting up the result's filepath
    result_filename = f'{GENRE_facet}_works_ratings.json'
    result_filepath = os.path.join(WORKS_RATINGS_DIR, result_filename)

    # Save the result as a JSON file
    save_json(works_ratings, result_filepath)

    logger.info('Finished extraction of ratings for each general work')
