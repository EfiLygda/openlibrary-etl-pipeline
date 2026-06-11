"""
API configuration and request settings
"""
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Setting up the genre
GENRE = os.getenv("GENRE")

# A normalized version of the genre used for filenames and directories
GENRE_facet = GENRE.replace(' ', '_')

# Maximum number of records for every query
LIMIT = int(os.getenv("LIMIT"))

# Maximum number of pages to extract from search queries
MAX_PAGES = int(os.getenv("MAX_PAGES"))

# Maximum number of retries for a query
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS"))

# Connection and reading request times
CONNECT_TIMEOUT = float(os.getenv("CONNECT_TIMEOUT"))
READ_TIMEOUT = float(os.getenv("READ_TIMEOUT"))
