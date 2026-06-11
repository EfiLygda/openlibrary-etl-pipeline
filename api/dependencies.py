"""
API's dependencies configurations
"""

from fastapi import Depends
from utilities.database import database_dependency

# FastAPI dependency for obtaining a database connection
DB_DEPENDENCY = Depends(database_dependency)
