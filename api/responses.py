"""
Module containing constructing all the exceptions' responses objects as dictionaries:
{
    'model': api.schemas.APIError,
    'description': str,
}
and displaying the right error code in the documentation
"""

from api.schemas.errors import APIError

def error_response(description: str, code: str) -> dict:
    """
    Build a standardized FastAPI OpenAPI error response definition

    This helper is used in FastAPI route `responses` definitions to ensure
    consistent error documentation across endpoints

    :param description: str, human-readable error description used in OpenAPI docs
                        and as the example message
    :param code: str, application-specific error code

    :return: dict, response definition containing model,description, and OpenAPI example
    """

    return {
        "model": APIError,
        "description": description,
        "content": {
            "application/json": {
                "example": {
                    "error_code": code,
                    "message": description
                }
            }
        }
    }

# ---------------------------------------------------------------
# Define Responses
# ---------------------------------------------------------------

# --- Base Responses ---
LISTING_NOT_SUPPORTED_RESPONSE = error_response(
    description='Listing all records is not supported',
    code='LISTING_NOT_SUPPORTED_ERROR'
)

INVALID_INPUT_RESPONSE = error_response(
    description='Invalid or missing input',
    code='INVALID_INPUT_ERROR'
)

# --- Works Responses ---
WORK_NOT_FOUND_RESPONSE = error_response(
    description='Work not found',
    code='WORK_NOT_FOUND_ERROR'
)

INVALID_WORK_KEY_RESPONSE = error_response(
    description='Invalid work key',
    code='INVALID_WORK_KEY_ERROR'
)

# --- Authors Responses ---
AUTHOR_NOT_FOUND_RESPONSE = error_response(
    description='Author not found',
    code='AUTHOR_NOT_FOUND_ERROR'
)

INVALID_AUTHOR_KEY_RESPONSE = error_response(
    description='Invalid author key',
    code='INVALID_AUTHOR_KEY_ERROR'
)

# --- Edition Responses ---
EDITION_NOT_FOUND_RESPONSE = error_response(
    description='Edition not found',
    code='EDITION_NOT_FOUND_ERROR'
)

INVALID_EDITION_KEY_RESPONSE = error_response(
    description='Invalid edition key',
    code='INVALID_EDITION_KEY_ERROR'
)
