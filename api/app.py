"""
A RESTful API for querying romance fiction metadata derived from Open Library data

The Romance Fiction API is a RESTful API built with FastAPI that provides
structured access to works, authors, editions, ratings, availability,
and related metadata stored in a relational database derived from Open Library

Run:
uvicorn api.app:app --reload
"""
import os
from dotenv import load_dotenv

from fastapi import FastAPI

from api.dependencies import DB_DEPENDENCY
from api.routers import (
    links,
    works,
    authors,
    editions,
    search
)

# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
GENRE = str(os.getenv("GENRE"))
API_VERSION = str(os.getenv("API_VERSION"))

# API description
API_description = ('A FastAPI-based API for searching and retrieving '
                   'structured book metadata stored in a relational '
                   'database derived from Open Library data.')

# API license
api_license = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }

# Main FastAPI application instance
app = FastAPI(
    dependencies=[DB_DEPENDENCY],
    title=f'{GENRE.title()} API',
    summary=API_description,
    version=API_VERSION,
    docs_url='/docs',
    license_info=api_license,
)

# Include routers as defined in api.routers
app.include_router(search.router)
app.include_router(works.router)
app.include_router(authors.router)
app.include_router(editions.router)
app.include_router(links.router)
