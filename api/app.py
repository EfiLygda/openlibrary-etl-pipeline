"""
Rub:
uvicorn api.app:app --reload

 each of the HTTP methods is called an "operation":
POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data.
"""
import os

import psycopg2

from dotenv import load_dotenv
from fastapi import FastAPI

from api.dependencies import DB_DEPENDENCY
from api.service import format_response
from api.repository.works import get_work_by_key

# TODO: add parameters when needed

# Load variables from the .env file to the environment
load_dotenv()
DB_NAME = os.getenv("DB_NAME")

# Main FastAPI application instance.
app = FastAPI()

# ---------------------------------------------------------------------------------
# Works Endpoints
# ---------------------------------------------------------------------------------

@app.get("/works/{work_key}")
async def get_work(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
):
    """
    Retrieve work records by **work_key**.

    Returns a standardized response dictionary containing:

    - **query**: the provided work_key
    - **endpoint**: API endpoint called
    - **method**: HTTP method used
    - **count**: number of records found
    - **records**: formatted database rows
    """

    # Fetch raw data from repository layer
    data, column_names = get_work_by_key(connection, work_key)

    # Format and return consistent API response structure
    return format_response(
        query=work_key,
        endpoint=f'/works/{work_key}',
        method='GET',
        records=data,
        column_names=column_names
    )


@app.get("/works/{work_key}/editions")
async def get_work_editions(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
):

    pass

# ---------------------------------------------------------------------------------
# Authors Endpoints TODO
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# Editions Endpoints TODO
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# Search Endpoints TODO
# ---------------------------------------------------------------------------------
