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

from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from utilities.database import db_connection

# Load variables from the .env file to the environment
load_dotenv()
DB_NAME = os.getenv("DB_NAME")

# ---
app = FastAPI()

def get_db_connection():
    """
    FastAPI dependency that provides a PostgreSQL database connection per request.

    :return: generator, yields psycopg2.extensions.connection (active DB connection)
    """

    # Set up connection object
    connection = None

    # Try to make the connection with the database and return it as a generator
    # Source: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-session-dependency
    try:

        # Make the connectio and return it as a generator
        connection = db_connection(database=DB_NAME)
        yield connection

    finally:

        # If the connection was made is not used anymore then close it
        if connection:
            connection.close()

def format_records(records: list, fields: list[str]):

    if not records:
        return []

    results = []

    for record in records:

        if len(record) != len(fields):
            return []

        results.append(zip(fields, record))

    return results

@app.get("/works/{work_key}")
async def read_work(work_key: str, connection = Depends(get_db_connection)):

    with connection.cursor() as cursor:

        cursor.execute(
            f"""
            SELECT * FROM works WHERE work_key = %s;
            """,
            (work_key,)
        )

        data = cursor.fetchall()
        column_names = [d[0] for d in cursor.description] if cursor.description else []

        return {
            'query': work_key,
            'endpoint': f'/works/{work_key}',
            'method': 'GET',

            'found': True if len(data) > 0 else False,
            'count': len(data),

            'records': format_records(data, column_names)
        }



