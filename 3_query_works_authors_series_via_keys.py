import os
import re
import json
from config import GENRE, KEYS_DIR, WORKS_DIR, AUTHORS_DIR, SERIES_DIR
from OpenLibrary import OpenLibraryClient

client = OpenLibraryClient()

key_type_pattern = r'.+_(work|author|series)_.+\.json$'

dirs = {
    'work': WORKS_DIR,
    'author': AUTHORS_DIR,
    'series': SERIES_DIR
}

for key_file_name in os.listdir(KEYS_DIR):

    key_file_path = os.path.join(KEYS_DIR, key_file_name)

    key_type_match = re.search(key_type_pattern, key_file_name)

    if not key_type_match:
        raise ValueError(f'Key type was not found in filename: {key_file_name}')

    key_file_type = key_type_match.group(1)

    with open(key_file_path, mode='r', encoding='utf-8') as j:
        keys_list = json.load(j)

    batch_size = client.LIMIT

    key_batches = [
        keys_list[i: i+batch_size]
        for i in range(0, len(keys_list), batch_size)
    ]

    for i, key_batch in enumerate(key_batches):
        records = client.get_many(key_batch)

        if not records['result']:
            raise ValueError(f'No results were returned from {client.last_url}')

        batch_filename = f'{key_file_type.upper()}_p{i+1}.json'
        batch_filepath = os.path.join(dirs[key_file_type], batch_filename)
        client.save_json(records, batch_filepath)

        if i + 1 == len(key_batches):
            end_str = '\n'
        else:
            end_str = '\r'

        print(f'({i+1}/{len(key_batches)}) Extracting {GENRE} {key_file_type}\'s metadata...', end=end_str)

print(f'Finished extracting {GENRE} works\', authors\' and series\' metadata.')
