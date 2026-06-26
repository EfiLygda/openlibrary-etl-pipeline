"""
Centralized API error definitions

This module defines reusable error objects used throughout the API for:

- Raising FastAPI HTTP exceptions at runtime
- Generating standardized OpenAPI response documentation

Each error definition contains the HTTP status code, application-specific
error code, and human-readable description, ensuring consistency between
runtime behavior and API documentation
"""

from fastapi.exceptions import HTTPException
from api.schemas.errors import APIError

class _APIErrorDefinition:

    def __init__(
            self,
            status_code: int,
            error_code: str,
            description: str
    ):
        """
        Initialize an API error definition

        :param status_code: int, HTTP status code returned by the API
        :param error_code: str, application-specific error identifier
        :param description: str, human-readable error message
        """

        self.status_code = status_code
        self.error_code = error_code
        self.description = description

    def __call__(self, query: str | None = None) -> HTTPException:
        """
        Create a FastAPI HTTPException from this error definition

        :param query: str, optional query value associated with the request
        :return: HTTPException, configured HTTPException instance
        """
        return HTTPException(
            status_code=self.status_code,
            detail={
                'error_code': self.error_code,
                'message': self.description,
                'self': query
            }
        )

    @property
    def response(self) -> dict:
        """
        Generate an OpenAPI response definition for this error

        Intended for use in FastAPI route `responses` declarations to
        ensure consistent error documentation across endpoints

        :return: dict, OpenAPI-compatible response specification
        """

        return {
            "model": APIError,
            "description": self.description,
            "content": {
                "application/json": {
                    "example": {
                        "error_code": self.error_code,
                        "message": self.description
                    }
                }
            }
        }

class BaseErrors:
    """
    Common API errors that are not tied to a specific entity

    These errors may be returned by multiple endpoints across the API
    """

    ListingNotSupported = _APIErrorDefinition(
        status_code=405,
        error_code='LISTING_NOT_SUPPORTED',
        description='Listing all records is not supported'
    )

    InvalidInput = _APIErrorDefinition(
        status_code=400,
        error_code='INVALID_INPUT',
        description='Request contains invalid or missing input'
    )

    NotFound = _APIErrorDefinition(
        status_code=400,
        error_code='NOT_FOUND',
        description='Record not found'
    )

class WorksErrors:
    """
    Error definitions related to work entities
    """

    NotFound = _APIErrorDefinition(
        status_code=404,
        error_code='WORK_NOT_FOUND',
        description='Work not found'
    )

    InvalidKey = _APIErrorDefinition(
        status_code=422,
        error_code='INVALID_WORK_KEY',
        description='Work key is invalid'
    )


class AuthorsErrors:
    """
    Error definitions related to author entities
    """

    NotFound = _APIErrorDefinition(
        status_code=404,
        error_code='AUTHOR_NOT_FOUND',
        description='Author not found'
    )

    InvalidKey = _APIErrorDefinition(
        status_code=422,
        error_code='INVALID_AUTHOR_KEY',
        description='Author key is invalid'
    )

class EditionsErrors:
    """
    Error definitions related to edition entities
    """

    NotFound = _APIErrorDefinition(
        status_code=404,
        error_code='EDITION_NOT_FOUND',
        description='Edition not found'
    )

    InvalidKey = _APIErrorDefinition(
        status_code=422,
        error_code='INVALID_EDITION_KEY',
        description='Edition key is invalid'
    )

class LinksErrors:
    """
    Links navigation definitions
    """

    NotFound = _APIErrorDefinition(
        status_code=404,
        error_code='ENTITY_NOT_FOUND',
        description='Entity not found'
    )

    InvalidKey = _APIErrorDefinition(
        status_code=422,
        error_code='INVALID_KEY',
        description='Key is invalid'
    )

class SearchErrors:
    """
    Search definitions
    """
    NotFound = _APIErrorDefinition(
        status_code=404,
        error_code='NOT_FOUND',
        description='No data found'
    )

    QueryConflict = _APIErrorDefinition(
        status_code=422,
        error_code='INVALID_QUERY_COMBINATION',
        description='Only fields \'q\', \'limit\','
                    ' \'offset\', \'year\', \'lang\' or \'published_by\' '
                    'can be used for search'
    )