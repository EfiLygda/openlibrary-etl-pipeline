"""
API configuration and request settings
"""

# Setting up the genre
GENRE = 'romance fiction'

# A normalized version of the genre used for filenames and directories
GENRE_facet = GENRE.replace(' ', '_')

# Maximum number of records for every query
LIMIT = 100

# Maximum number of pages to extract from search queries
MAX_PAGES = 20

# Maximum number of retries for a query
MAX_ATTEMPTS = 5
