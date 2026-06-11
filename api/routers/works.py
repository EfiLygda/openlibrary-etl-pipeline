"""
/works router
"""
import psycopg2

from fastapi import APIRouter

from api.dependencies import DB_DEPENDENCY
from api.service import format_response
from api.repository.works import get_work_by_key

# Defining the works router
router = APIRouter(
    prefix="/works",
    tags=["Works"]
)

@router.get("/{work_key}")
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


@router.get("/{work_key}/editions")
async def get_work_editions(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
):

    pass