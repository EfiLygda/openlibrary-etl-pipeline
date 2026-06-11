"""


"""

import psycopg2

def get_work_by_key(
        connection: psycopg2.extensions.connection,
        work_key: str
) -> tuple:
    """

    """

    # Query the database
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM works WHERE work_key = %s;
            """,
            (work_key,)
        )

        # Fetch all records as returned
        records = cursor.fetchall()

        # Fetch column names as returned
        column_names = [d[0] for d in cursor.description] if cursor.description else []

        return records, column_names