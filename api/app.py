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
from dotenv import load_dotenv

import psycopg2
from fastapi import FastAPI, Depends

from utilities.database import database_dependency

# Load variables from the .env file to the environment
load_dotenv()
DB_NAME = os.getenv("DB_NAME")

def format_records(records: list, fields: list[str]):

    if not records:
        return []

    results = []

    for record in records:

        if len(record) != len(fields):
            return []

        results.append(zip(fields, record))

    return results

DB_DEPENDENCY = Depends(database_dependency)

app = FastAPI()

@app.get("/works/{work_key}")
async def read_work(
        work_key: str,
        connection: psycopg2.extensions.connection = DB_DEPENDENCY
):

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



