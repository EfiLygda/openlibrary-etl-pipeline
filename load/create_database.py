"""

"""

from utilities.database import db_connection

# ---------------------------------------------------------------------------------------
# --- Set up Connection to Database ---

# Establish connection
connection = db_connection()

# Set up cursor
cursor = connection.cursor()
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Create Database (if it does not exist) ---

# Check if database already exists and then create
# Source: https://stackoverflow.com/a/44512503
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'romance_fiction';")
exists = cursor.fetchone()
if not exists:
    cursor.execute('CREATE DATABASE romance_fiction;')

# Close the connection
connection.close()
# ---------------------------------------------------------------------------------------