import os
import math
import pandas as pd
import requests
from time import sleep
from dataset_initilize import DATA_DIR

# Genre as 'romance' is too broad and returns noise
# 'romance fiction' doesn't return all authors
# Result: Will have to extract romance works first -> find authors -> then extract their metadata

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

    print(f'({page}/{total_pages}) Extracting {GENRE} authors\' data...', end='\r')

    request_params = {'q': GENRE, 'page': page, 'limit': LIMIT}
    response = requests.get(base_url, params=request_params)

    result = response.json()

    author_data += result['docs']
    sleep(0.5)

df = pd.DataFrame(author_data).loc[:, AUTHOR_FIELDS]

filename = 'authors.csv'

df.to_csv(os.path.join(DATA_DIR, filename), index=False)

print(f'Exported {GENRE} authors\' data!')