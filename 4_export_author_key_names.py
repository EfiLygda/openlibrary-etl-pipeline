"""
STEP 4:

DETAILS:
1.
"""

import os
import json
from config import GENRE_facet, AUTHORS_DIR, KEYS_DIR
from OpenLibrary import OpenLibraryClient

client = OpenLibraryClient()

author_key_names = dict()

for filename in os.listdir(AUTHORS_DIR):

    filepath = os.path.join(AUTHORS_DIR, filename)

    with open(filepath, mode='r', encoding='utf-8') as j:
        data = json.load(j)

    records = data['result']

    for key, record in records.items():

        if client.is_redirect(record):
            record = client.get_redirected_record(record)

        new_name = record['name']

        if key in author_key_names:
            old_name = author_key_names[key]['name']
            if old_name != new_name:
                raise ValueError(
                    f'Two different names \'{old_name}\' and \'{new_name}\' for author key \'{key}\'.'
                )

        author_key_names[key] = new_name

result_filename = f'{GENRE_facet}_authors_key_name.json'
result_filepath = os.path.join(KEYS_DIR, result_filename)

client.save_json(author_key_names, result_filepath)
