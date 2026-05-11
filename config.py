import os

# Setting up the genre
GENRE = 'romance fiction'

# A normalized version of the genre used for filenames and directories
GENRE_facet = GENRE.replace(' ', '_')

# Setting up the directories
ROOT_DIR = './'
DATA_DIR = os.path.join(ROOT_DIR, 'data')
CSV_DIR = os.path.join(DATA_DIR, 'csv')
RAW_PAGES_DIR = os.path.join(DATA_DIR, 'raw_pages')
GENRE_DIR = os.path.join(RAW_PAGES_DIR, GENRE_facet)
WORKS_DIR = os.path.join(GENRE_DIR, 'works')
KEYS_DIR = os.path.join(DATA_DIR, 'keys')

# List containing all new directories
NEW_DIRS = [
    DATA_DIR,
    CSV_DIR,
    RAW_PAGES_DIR,
    GENRE_DIR,
    WORKS_DIR,
    KEYS_DIR
]

# Creating new directories, if they do not already exist
for directory in NEW_DIRS:
    if not os.path.exists(directory):
        os.makedirs(directory)
