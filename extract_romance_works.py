import os
import json
import requests
from time import sleep
from dataset_initilize import RAW_PAGES_DIR
from random import uniform

GENRE = 'romance fiction'
GENRE_facet = GENRE.replace(' ', '_') # A normalized version of the genre
GENRE_DIR = os.path.join(RAW_PAGES_DIR, GENRE_facet)
if not os.path.exists(GENRE_DIR):
    os.makedirs(GENRE_DIR)

LIMIT = 100
MAX_PAGES = 20

CONNECT_TIMEOUT = 15
READ_TIMEOUT = 15

# Source: https://openlibrary.org/dev/docs/api/search
base_url = 'https://openlibrary.org/search.json'


for page in range(1, MAX_PAGES+1):
    print(f'({page}/{MAX_PAGES}) Extracting {GENRE} works\' metadata...', end='\r')

    request_params = {'subject': GENRE, 'page': page, 'limit': LIMIT}

    try:
        response = requests.get(base_url, params=request_params, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
    except Exception as e:
        print(e)

    result = response.json()

    filename = f'works_p{page}.json'
    with open(os.path.join(GENRE_DIR, filename), mode='w') as j:
        json.dump(result, j, indent=4)

    sleep(3 + uniform(0, 1.5))
