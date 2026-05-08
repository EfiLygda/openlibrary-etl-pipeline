import os
import math
import json
import pandas as pd
import requests
from time import sleep
from dataset_initilize import CSV_DIR, RAW_PAGES_DIR
from langdetect import detect
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

FIELDS = [
    # Identity
    "key",
    "ia", # Internet Archive ID

    # Work
    "title",
    "subtitle",
    "alternative_title",
    "alternative_subtitle",
    "first_publish_year",

    # Edition
    "edition_key",
    "format",

    # Editions
    "edition_count",
    "number_of_pages_median",
    "publish_date",
    "publish_year",
    "language",
    "isbn",

    # Series
    "series_key",
    "series_name",
    "series_position",

    # Author
    "author_key",
    "author_name",
    "author_facet", # A normalized version of author names used for filtering
    "author_alternative_name",
    "contributor",

    # Publisher
    "publisher",
    "publisher_facet", # A normalized version of publisher names used for filtering
    "publish_place",

    # Content metadata
    "subject", "subject_key",
    "person", "person_key",
    "place", "place_key",
    "time", "time_key",

    # Accessibility
    "ebook_access",
    "has_fulltext",
    "ia_count", # number of Internet Archive items associated with that work
    "public_scan_b", # at least one publicly available scanned copy in the Internet Archive

    # Statistics
    "ratings_count", # Number of ratings
    "readinglog_count", # Total reading log entries
    "want_to_read_count", # Users who want to read it
    "currently_reading_count", # Users currently reading it
    "already_read_count", # Users who finished it

]

# Source: https://openlibrary.org/dev/docs/api/search
base_url = 'https://openlibrary.org/search.json'

# initial_request_params = {'subject': GENRE, 'limit': 0}
# response = requests.get(base_url, params=initial_request_params, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
#
# result = response.json()

# total_books = result['numFound']
# total_pages = math.ceil(total_books / LIMIT)

# works_authors_fields = ['author_key', 'key', 'role_guess', 'confidence', 'signals']
# works_authors = pd.DataFrame(columns=works_authors_fields)

# works_data = []

# TODO: Dump the json results and keep them maybe in a different py file do the dataset

for page in range(1, MAX_PAGES+1):
    print(f'({page}/{MAX_PAGES}) Extracting {GENRE} works\' metadata...', end='\r')

    request_params = {'subject': GENRE, 'page': page, 'limit': LIMIT}

    while True:
        try:
            response = requests.get(base_url, params=request_params, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
            break

        except Exception as e:
            print(e)
            sleep(3 + uniform(0, 1.5))
            continue

    result = response.json()

    filename = f'works_p{page}.json'
    with open(os.path.join(GENRE_DIR, filename), mode='w') as j:
        json.dump(result, j, indent=4)

    # data = result['docs']
    # works_data += result['docs']


    sleep(3 + uniform(0, 1.5))

# df = pd.DataFrame(works_data)
#
# filename = f'{GENRE}_works.parquet'
#
# df.to_parquet(os.path.join(DATA_DIR, filename), index=False)
#
# print(f'Exported {GENRE} works\' metadata!')