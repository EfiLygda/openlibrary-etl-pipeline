import os
import psycopg2
from dotenv import load_dotenv

# ---------------------------------------------------------------------------------------
# --- Load Environment Variables ---

# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Establish Connection ---

# Establish a connection to the PostgreSQL server
connection = psycopg2.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Use autocommit in order to be able to create tables inside a transaction block
connection.autocommit = True

# Create a cursor object
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