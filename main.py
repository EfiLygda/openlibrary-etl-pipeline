from time import sleep
import math
import requests

GENRE = 'romance'
LIMIT = 100
TIMEOUT = 5
# Source: https://openlibrary.org/dev/docs/api/search
base_url = 'https://openlibrary.org/search.json'

initial_request_params = {'subject': GENRE, 'limit': 0}
response = requests.get(base_url, params=initial_request_params, timeout=TIMEOUT)

result = response.json()

total_books = result['numFound']
total_pages = math.ceil(total_books / LIMIT)

for page in range(total_pages):
    request_params = {'subject': GENRE, 'page': page, 'limit': LIMIT}
    response = requests.get(base_url, params=request_params, timeout=TIMEOUT)

    result = response.json()

    data = result['docs']

    sleep(0.5)