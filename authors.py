from time import sleep
import math

import pandas as pd
import requests

GENRE = 'romance'
LIMIT = 100

# Source: https://openlibrary.org/dev/docs/api/search
base_url = f'https://openlibrary.org/search/authors.json'

initial_request_params = {'q': GENRE, 'limit': 0}
response = requests.get(base_url, params=initial_request_params)

result = response.json()

total_authors = result['numFound']
total_pages = math.ceil(total_authors / LIMIT)

AUTHOR_FIELDS = (
    "key", "name", "alternate_names", "birth_date", "death_date",
    "top_subjects", "top_work", "work_count",
    "ratings_average", "ratings_sortable",
    "ratings_count",
    "ratings_count_1",
    "ratings_count_2",
    "ratings_count_3",
    "ratings_count_4",
    "ratings_count_5",
    "want_to_read_count",
    "already_read_count",
    "currently_reading_count",
    "readinglog_count"
)

author_data = []

for page in range(1, total_pages+1):
    request_params = {'q': GENRE, 'page': page, 'limit': LIMIT}
    response = requests.get(base_url, params=request_params)

    result = response.json()

    author_data += result['docs']
    print(f'{page}/{total_pages} author pages done!')
    sleep(0.5)

author_data = pd.DataFrame(author_data).loc[:, AUTHOR_FIELDS]