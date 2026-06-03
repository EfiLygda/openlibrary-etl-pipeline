"""
Centralized project paths
"""

import os
from config.api import GENRE_facet

# Project directory
ROOT_DIR = os.path.abspath('./')

# Log messages directories
LOG_DIR = os.path.join(ROOT_DIR, 'logs')

# Data directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')
GENRE_DIR = os.path.join(DATA_DIR, GENRE_facet)

# Raw JSON files directory root directory
RAW_PAGES_DIR = os.path.join(GENRE_DIR, 'raw')
KEYS_DIR = os.path.join(GENRE_DIR, 'staging', 'keys')
CSV_DIR = os.path.join(GENRE_DIR, 'processed')

# Raw JSON files directories
SEARCH_DIR = os.path.join(RAW_PAGES_DIR, 'works')
WORKS_DIR = os.path.join(RAW_PAGES_DIR, 'works_enriched')
AUTHORS_DIR = os.path.join(RAW_PAGES_DIR, 'authors')
SERIES_DIR = os.path.join(RAW_PAGES_DIR, 'series')
BOOKS_DIR = os.path.join(RAW_PAGES_DIR, 'books')
# PUBLISHERS_DIR = os.path.join(KEYS_DIR, 'publishers')
# SUBJECTS_DIR = os.path.join(KEYS_DIR, 'subjects')
AUTHORS_STATISTICS_DIR = os.path.join(RAW_PAGES_DIR, 'authors_statistics')
WORKS_RATINGS_DIR = os.path.join(RAW_PAGES_DIR, 'works_ratings')

# Schema directory
SCHEMA_DIR = os.path.join(ROOT_DIR, 'database', 'schema')
