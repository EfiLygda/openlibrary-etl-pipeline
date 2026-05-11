import os
import json
from config import GENRE_facet, KEYS_DIR, WORKS_DIR, AUTHORS_DIR, SERIES_DIR
from OpenLibrary import OpenLibraryClient

client = OpenLibraryClient()

for key_file in os.listdir(KEYS_DIR):

    key_file_path = os.path.join(KEYS_DIR, key_file)

    with open(key_file_path, mode='r', encoding='utf-8') as j:
        keys_list = json.load(j)

    batch_size = client.LIMIT

    key_batches = [
        keys_list[i: i+batch_size]
        for i in range(0, len(keys_list), batch_size)
    ]

    for key_batch in key_batches:
        data = client.get_many(key_batch)
        print(data)