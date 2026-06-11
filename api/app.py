"""
Run:
uvicorn api.app:app --reload
"""

from fastapi import FastAPI

from api.dependencies import DB_DEPENDENCY
from api.routers import works

# TODO: add parameters when needed

# Main FastAPI application instance.
app = FastAPI(
    dependencies=[DB_DEPENDENCY]
)

# Include routers as defined in api.routers
app.include_router(works.router)

