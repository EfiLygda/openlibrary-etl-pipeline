import os
from dataset_initilize import RAW_PAGES_DIR

# --- Setting up the genre directories ---
GENRE = 'romance fiction'

# A normalized version of the genre used for filenames and directories
GENRE_facet = GENRE.replace(' ', '_')

# Creating the raw files directory, if it does not already exists
GENRE_DIR = os.path.join(RAW_PAGES_DIR, GENRE_facet)
if not os.path.exists(GENRE_DIR):
    os.makedirs(GENRE_DIR)