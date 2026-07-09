"""
Centralized project paths
"""

import os
from config.openlibrary_api import GENRE_facet

# ------------------------------------------------------------------------------------
# Project directory
ROOT_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Log messages directories
LOG_DIR = os.path.join(ROOT_DIR, 'logs')

# Data directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# --- Book dataset ---
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

# Indexes directory
INDEXES_DIR = os.path.join(ROOT_DIR, 'database', 'indexes')
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# --- Library dataset ---

# Library Root directory
LIBRARY_ROOT = os.path.join(ROOT_DIR, 'library')

# Library data directory
LIBRARY_DIR = os.path.join(DATA_DIR, 'library')

# Raw library data directory (json)
LIBRARY_RAW = os.path.join(LIBRARY_DIR, 'raw')

# Library tables directory (csv)
LIBRARY_TABLES = os.path.join(LIBRARY_DIR, 'tables')

# Library tables directory (csv)
LIBRARY_SCHEMA = os.path.join(ROOT_DIR, 'library',  'database', 'schema')

# Directory with the consumer's SQL commands used by the handlers
PRODUCER_SQL_DIR = os.path.join(LIBRARY_ROOT, 'producer', 'sql')

# Directory with the consumer's SQL commands used by the handlers
CONSUMER_SQL_DIR = os.path.join(LIBRARY_ROOT, 'consumer', 'sql')
# ------------------------------------------------------------------------------------
