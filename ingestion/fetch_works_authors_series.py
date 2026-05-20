"""
STEP 3: Use OpenLibraryClient.get_many to extract via keys all WORKS_ENRICHED, AUTHORS, SERIES

DETAILS:
1. WORKS_ENRICHED contains enriched data not returned from SEARCH in STEP 1
2. The queries used for each object is:
    2.1 WORKS_ENRICHED: WORKS @ API_info/base_urls
    2.2 AUTHORS:        AUTHORS @ API_info/base_urls
    2.3 SERIES:         SERIES @ API_info/base_urls
3. The results are saved as JSON files @ :
    3.1 WORKS_ENRICHED: data/raw_pages/romance_fiction/works_enriched
    3.2 AUTHORS:        data/raw_pages/romance_fiction/authors
    3.3 SERIES:         data/raw_pages/romance_fiction/series
"""
import os
import re
from config.paths import KEYS_DIR, WORKS_DIR, AUTHORS_DIR, SERIES_DIR
from config.api import GENRE
from utilities.rate_limit import wait
from open_library import Client
from utilities.io import load_json, save_json
from utilities.batching import make_batches
from utilities.logging import set_logger

logger = set_logger('FETCH_WORKS_AUTHORS_SERIES')

def run():

    logger.info(
        f'Starting extraction of all work, author and series keys via WORKS_ENRICHED, AUTHORS and SERIES queries'
    )

    # Setting up thw Open Library client for querying the API
    client = Client()

    # The regex used for later extracting the type of keys in the JSON
    # keys files extracted from export_keys.py
    key_type_pattern = r'.+_(work|author|series)_.+\.json$'

    # Connecting the type of keys with their respective saved directories
    dirs = {
        'work': WORKS_DIR,
        'author': AUTHORS_DIR,
        'series': SERIES_DIR
    }

    # For each key file the API will be queried in batches using as batch size
    # client.LIMIT and the results will be saved in JSON files
    for key_file_name in os.listdir(KEYS_DIR):

        # The file path of the current key file
        key_file_path = os.path.join(KEYS_DIR, key_file_name)

        # Finding if there is the key type in the name of the file
        key_type_match = re.search(key_type_pattern, key_file_name)

        # If a match is not made a ValueError is raised
        if not key_type_match:
            logger.info(f'Key type was not found in filename: {key_file_name}')
            continue

        # Extracting the key type from the file name
        key_file_type = key_type_match.group(1)

        # Loading the current key list
        keys_list = load_json(key_file_path)

        # Setting the batch size for querying
        batch_size = client.LIMIT

        # Creating the batches from the key list
        key_batches = make_batches(keys_list, batch_size)

        # For each batch the API is queried and the results are saved
        for i, key_batch in enumerate(key_batches):

            # Querying the API for the current batch
            records = client.get_many(key_batch)

            # If no records are returned a ValueError is returned
            if not records['result']:
                raise ValueError(f'No results were returned from {client.last_url}')

            # The file name for the current batch
            batch_filename = f'{key_file_type.upper()}_p{i+1}.json'

            # Finding the current key type directory to save the records
            key_type_dir = dirs[key_file_type]

            # The file path for the current batch
            batch_filepath = os.path.join(key_type_dir, batch_filename)

            # Saving the current batch
            save_json(records, batch_filepath)

            # Setting up the progress message for each key types
            # New line when the type changes, same row for batches in the same key type
            # if i + 1 == len(key_batches):
            #     end_str = '\n'
            # else:
            #     end_str = '\r'

            # Progress message
            # print(f'({i+1}/{len(key_batches)}) Extracting {GENRE} {key_file_type}\'s metadata...', end=end_str)

            logger.info(f'({i+1}/{len(key_batches)}) Extracted {GENRE} {key_file_type}\'s metadata')

            wait(3)

    # Success message
    # print(f'Finished extracting {GENRE} works\', authors\' and series\' metadata.')

    logger.info(f'Finished extracting {GENRE} works\', authors\' and series\' metadata.')