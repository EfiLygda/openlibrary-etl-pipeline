"""
Setting up the directories
"""

import os
from config.api import GENRE_facet

# Project directory
ROOT_DIR = os.path.abspath('./')

# Data directory
# DATA_ROOT_DIR = os.path.abspath('../')
# DATA_DIR = os.path.join(DATA_ROOT_DIR, 'data')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

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

# Log messages directories
LOG_DIR = os.path.join(ROOT_DIR, 'logs')

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
    LOG_DIR
]

# Creating new directories, if they do not already exist
for directory in NEW_DIRS:
    if not os.path.exists(directory):
        os.makedirs(directory)