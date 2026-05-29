"""
STEP 8: Fetch all author statistics from Open Library

DETAILS:
1. Data are saved in a JSON file @ data/raw_pages/{GENRE_facet}/author_statistics
"""
import os
import requests

from open_library import Client, KeyHandler

from config.paths import KEYS_DIR, AUTHORS_STATISTICS_DIR
from config.api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.rate_limit import wait
from utilities.logging import set_logger

logger = set_logger('FETCH_AUTHOR_STATISTICS')

def run():

    logger.info('Started extraction of author statistics')

    # Setting up thw Open Library client for querying the API
    client = Client()

    # Loading the general work keys and book keys file
    authors = load_json(
        os.path.join(KEYS_DIR, f'{GENRE_facet}_authors_key_name.json')
    )

    # Setting up the dictionary that will contain the data
    authors_statistics = dict()

    # For each author name the data will be fetched
    for i, (author_key, author_name) in enumerate(authors.items()):

        # Progress message
        # print(f'({i+1}/{len(authors.items())}) Extracting authors\' statistics...', end='\r')
        logger.info(f'({i+1}/{len(authors.items())}) Extracting authors\' statistics')

        # Get the key from the normalized key (basically remove '\authors\' from the key)
        denormalized_key = KeyHandler.get_key(author_key)

        # Set up the maximum number of attempts to fetch the data
        for _ in range(MAX_ATTEMPTS):

            # Try to extract the data during these attempts
            # Possible errors:
            # 1. connection errors: requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout
            # 2. no data available: requests.exceptions.HTTPError
            try:

                # Fetch authors' statistics
                data = client.search(query=author_name, mode='authors')

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
                    # print(f'\nNo data was found for author \'{author_name}\' with key \'{author_key}\'.', end='\n')
                    logger.error(f'No data was found for author \'{author_name}\' with key \'{author_key}\'.')
                else:
                    # If the right record is found break the loop with the attempts to query the API
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

        # Politely wait more than 3 seconds for the next author
        wait(3)

    # Setting up the final file's path
    filename = f'{GENRE_facet}_author_statistics.json'
    filepath = os.path.join(AUTHORS_STATISTICS_DIR, filename)

    # Exporting all authors' statistics as a JSON file
    save_json(authors_statistics, filepath)

    logger.info('Finished extraction of author statistics')
