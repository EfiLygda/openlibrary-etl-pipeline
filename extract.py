"""
Extract General Works, Editions and Authors' data using the OpenLibrary API to JSON files

Note: Refer to API_info/base_urls for keywords SEARCH, WORKS, AUTHORS, SERIES,
      SEARCH_EDITIONS_VIA_WORK_KEY, SEARCH_AUTHORS

Pipeline:
STEP 1: Extract first 2000 works under the genre via SEARCH
STEP 2: Extract all work keys, author keys, series keys,
STEP 3: Use OpenLibraryClient.get_many to extract via keys all WORKS, AUTHORS, SERIES
STEP 4: From author data extract author key, name pairs. This is done to use author's main name and
        remove pen names or other versions
STEP 5: Use SEARCH_EDITIONS_VIA_WORK_KEY to find and extract all editions in a work
STEP 6: Use OpenLibraryClient.get_many to extract via keys all BOOKS
Step 7: Extract all publishers, subjects, subject_people and subject_times via SEARCH_EDITIONS_VIA_WORK_KEY
Step 8: Extract all SEARCH_AUTHORS fields from SEARCH_AUTHORS
"""

import os
from config.paths import ROOT_DIR
from utilities.pipeline import run_pipeline

# Set up directory containing the pipeline py files
tasks_dir = os.path.join(ROOT_DIR, 'ingestion')

# The pipeline's py filenames for extracting JSON files via the API
tasks = [
    'fetch_works.py',
    'export_keys.py',
    'fetch_works_authors_series.py',
    'export_author_key_names.py',
    'fetch_books_keys_via_work_key.py',
    'fetch_books.py',
    'export_publishers_subjects_people_times.py',
    'fetch_author_statistics.py',
]

# Run the pipeline
run_pipeline(
    tasks_dir=tasks_dir,
    tasks=tasks
)
