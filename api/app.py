"""
Run:
uvicorn api.app:app --reload
"""
import os
from dotenv import load_dotenv

from fastapi import FastAPI

from api.dependencies import DB_DEPENDENCY
from api.routers import works, authors, editions

# TODO: add parameters when needed

# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
GENRE = os.getenv("GENRE")
API_VERSION = os.getenv("API_VERSION")

# Main FastAPI application instance

API_description = ('A FastAPI-based API for searching and retrieving '
                   'structured book metadata stored in a relational '
                   'database derived from Open Library data.')

license = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }

app = FastAPI(
    dependencies=[DB_DEPENDENCY],
    title=f'{GENRE.title()} API',
    summary=API_description,
    version=API_VERSION,
    docs_url='/docs',
    license_info=license,
)

# Include routers as defined in api.routers
app.include_router(works.router)
app.include_router(authors.router)
app.include_router(editions.router)
