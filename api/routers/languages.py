"""
Languages Router

This module defines API endpoints related to "languages"

Note: ISO 693-2 codes: https://www.loc.gov/standards/iso639-2/php/code_list.php

Endpoints:
- GET /languages
  Retrieve all languages metadata

- GET /languages?lang=eng,deu,...
  Retrieve predetermined languages metadata via their ISO 693-2 codes
"""

import os
from dotenv import load_dotenv

from fastapi import APIRouter, Request

from api.errors import BaseErrors
from api.schemas.responses import LanguagesResponse
from api.service.languages import language_service


# -----------------------------------------------------------------------------
# --- Load API LIMIT from environment variables ---
# Load variables from the .env file to the environment
load_dotenv()

# --- Setting up parameters ---
API_LIMIT = int(os.getenv("API_LIMIT"))
OFFSET = 0
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining the works router ---
router = APIRouter(
    prefix="/languages",
    tags=["Languages"]
)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Defining all endpoints ---
@router.get(
    path="",
    response_model=LanguagesResponse,
    responses={
        '404': BaseErrors.NotFound.response,
    }
)
async def get_languages(
        request: Request,
        lang: str | None = None,
        limit: int = API_LIMIT,
        offset: int = OFFSET,
) -> LanguagesResponse:
    """
    Retrieve languages batch records by their ISO 693-2 **codes**.

    Returns a standardized response dictionary containing:

    - **data**: the languages
    - **meta**: metadata for the query
    - **links**: current link used
    """

    return language_service(
        request=request,
        lang=lang,
        limit=limit,
        offset=offset
    )
# ----------------------------------------------------------------------------------
