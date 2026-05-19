import os

# Setting up the genre
GENRE = 'romance fiction'

# A normalized version of the genre used for filenames and directories
GENRE_facet = GENRE.replace(' ', '_')

# Maximum number of records for every query
LIMIT = 100

# Maximum number of pages to extract from search queries
MAX_PAGES = 20

# --- Setting up the directories ---
# Project directory
ROOT_DIR = os.path.abspath('../../')

# Data directory
# DATA_ROOT_DIR = os.path.abspath('../')
# DATA_DIR = os.path.join(DATA_ROOT_DIR, 'data')
DATA_DIR = os.path.join(ROOT_DIR, '../../data')

# Raw JSON files directory root directory
RAW_PAGES_DIR = os.path.join(DATA_DIR, 'raw_pages')
GENRE_DIR = os.path.join(RAW_PAGES_DIR, GENRE_facet)

# Raw JSON files directories
SEARCH_DIR = os.path.join(GENRE_DIR, 'works')
KEYS_DIR = os.path.join(DATA_DIR, 'keys')
WORKS_DIR = os.path.join(GENRE_DIR, 'works_enriched')
AUTHORS_DIR = os.path.join(GENRE_DIR, 'authors')
SERIES_DIR = os.path.join(GENRE_DIR, 'series')
BOOKS_DIR = os.path.join(GENRE_DIR, 'books')
# PUBLISHERS_DIR = os.path.join(KEYS_DIR, 'publishers')
# SUBJECTS_DIR = os.path.join(KEYS_DIR, 'subjects')
AUTHORS_STATISTICS_DIR = os.path.join(GENRE_DIR, 'author_statistics')

# Processed CSV files directory
CSV_DIR = os.path.join(DATA_DIR, 'csv')

# List containing all new directories
NEW_DIRS = [
    DATA_DIR,
    CSV_DIR,
    RAW_PAGES_DIR,
    GENRE_DIR,
    SEARCH_DIR,
    KEYS_DIR,
    WORKS_DIR,
    AUTHORS_DIR,
    SERIES_DIR,
    BOOKS_DIR,
    # PUBLISHERS_DIR,
    # SUBJECTS_DIR,
    AUTHORS_STATISTICS_DIR,
]

# Creating new directories, if they do not already exist
for directory in NEW_DIRS:
    if not os.path.exists(directory):
        os.makedirs(directory)
