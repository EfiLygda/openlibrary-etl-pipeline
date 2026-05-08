import os

ROOT_DIR = './'
DATA_DIR = os.path.join(ROOT_DIR, 'data')

CSV_DIR = os.path.join(DATA_DIR, 'csv')
RAW_PAGES_DIR = os.path.join(DATA_DIR, 'raw_pages')

NEW_DIRS = [DATA_DIR, CSV_DIR, RAW_PAGES_DIR]

for dir in NEW_DIRS:
    if not os.path.exists(dir):
        os.makedirs(dir)