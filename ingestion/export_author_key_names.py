"""
STEP 4: Export author key and name pairs.

DETAILS:
1. Data are saved in a JSON file @ data/keys
2. Some records that were returned from STEP 1 were redirecting to another records.
   In such cases OpenLibraryClient.get_redirected_record is used to find the right record and
   the final data were added to the final data. As such no data is lost.
"""

import os
from config.paths import AUTHORS_DIR, KEYS_DIR
from config.api import GENRE_facet
from open_library import Client
from utilities.io import load_json, save_json
from utilities.logging import set_logger

logger = set_logger('EXPORT_AUTHOR_KEY_NAMES')

def run():
    logger.info(f'Starting exporting of all authors\' keys and names')

    # Setting up thw Open Library client for querying the API
    client = Client()

    # Setting up the dictionary that will contain the final author key, name pairs
    author_key_names = dict()

    # Count how many redirected records will be
    redirected_records = 0

    # For each raw pages that were returned for authors all author key and names
    # are extracted
    for filename in os.listdir(AUTHORS_DIR):

        # Find the current author page's file path
        filepath = os.path.join(AUTHORS_DIR, filename)

        # Opening the current JSON file
        data = load_json(filepath)

        # Extracting the author records
        records = data['result']

        # For each record, a check is done in case it is not an author's record
        # but a redirect instead
        for key, record in records.items():

            # If the record is a redirect then the author's right record is fetched
            if client.is_redirect(record):

                # Add to redirected records counter
                redirected_records += 1

                # Fetch the record that the original redirects to
                record = client.get_redirected_record(record)

                # Export it to the right format
                record_to_export = {'result': {record['key']: record}}
                save_json(
                    record_to_export,
                    os.path.join(AUTHORS_DIR, f'redirected_{redirected_records}.json')
                )

                # print(
                #     f'Key \'{key}\' redirects to \'{record['key']}\'. Added new raw page but original stays as is.'
                # )
                logger.info(
                    f'Key \'{key}\' redirects to \'{record['key']}\'. Added new raw page but original stays as is.'
                )

            # The current record's author name is extracted
            new_name = record['name']

            # A check is done in case alternative names for the same author key
            # are found
            if key in author_key_names:

                # Save the original name that was saved in a previous iteration
                old_name = author_key_names[key]['name']

                # In case the previous name and the current new are different
                # a ValueError is raised
                if old_name != new_name:
                    raise ValueError(
                        f'Two different names \'{old_name}\' and \'{new_name}\' for author key \'{key}\'.'
                    )

            # Add the author's key, name pair to the dictionary
            author_key_names[key] = new_name

    # Setting up the final JSON file's name and path
    result_filename = f'{GENRE_facet}_authors_key_name.json'
    result_filepath = os.path.join(KEYS_DIR, result_filename)

    # Save the final JSON file with the pairs
    save_json(author_key_names, result_filepath)

    logger.info(f'Finished exporting all authors\' keys and names')
