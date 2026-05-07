from time import sleep
import math
import requests

GENRE = 'romance'
LIMIT = 100

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

initial_request_params = {'subject': GENRE, 'limit': 0}
response = requests.get(base_url, params=initial_request_params)

result = response.json()

total_books = result['numFound']
total_pages = math.ceil(total_books / LIMIT)

for page in range(1, total_pages+1):
    print(f'({page}/{total_pages}) Extracting {GENRE} works\' metadata...', end='\r')

    request_params = {'subject': GENRE, 'page': page, 'limit': LIMIT}
    response = requests.get(base_url, params=request_params)

    result = response.json()

    data = result['docs']

    sleep(0.5)