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
from itertools import count

import psycopg2

from dotenv import load_dotenv
from fastapi import FastAPI, Depends

from utilities.database import database_dependency
from api.service import format_response
from api.repository.works import get_work_by_key

# Load variables from the .env file to the environment
load_dotenv()
DB_NAME = os.getenv("DB_NAME")

# FastAPI dependency for obtaining a database connection
DB_DEPENDENCY = Depends(database_dependency)

# Main FastAPI application instance.
app = FastAPI()

@app.get("/works/{work_key}")
async def read_work(
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




