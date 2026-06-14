"""
Module containing all HTTP exceptions that can be raised from the API

HTTP status codes sources:
https://fastapi.tiangolo.com/tutorial/response-status-code/?h=http+stat#about-http-status-codes
https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

- 400 Bad Request
- 404 Not Found
- 405 Method Not Allowed
- 422 Unprocessable Content
"""

from fastapi.exceptions import HTTPException

# ---------------------------------------------------------------
# Define Errors
# ---------------------------------------------------------------

# --- Base Error ---
LISTING_NOT_SUPPORTED = lambda query: HTTPException(
    status_code=405,
    detail={
        'error_code': 'LISTING_NOT_SUPPORTED',
        'message': 'Listing all records is not supported',
        'query': query
    }
)

INVALID_INPUT_ERROR = lambda query: HTTPException(
    status_code=400,
    detail={
        'error_code': 'INVALID_INPUT',
        'message': 'Request contains invalid or missing input',
        'query': query
    }
)

# --- Works Errors ---
WORK_NOT_FOUND_ERROR = lambda query: HTTPException(
    status_code=404,
    detail={
        'error_code': 'WORK_NOT_FOUND',
        'message': 'Work not found error',
        'query': query
    }
)

INVALID_WORK_KEY_ERROR = lambda query, work_key: HTTPException(
    status_code=422,
    detail={
        'error_code': 'INVALID_WORK_KEY',
        'message': f'Work key \'{work_key}\' is invalid',
        'query': query
    }
)

# --- Author Errors ---
AUTHOR_NOT_FOUND_ERROR = lambda query: HTTPException(
    status_code=404,
    detail={
        'error_code': 'AUTHOR_NOT_FOUND',
        'message': 'Author not found error',
        'query': query
    }
)

INVALID_AUTHOR_KEY_ERROR = lambda query, author_key: HTTPException(
    status_code=422,
    detail={
        'error_code': 'INVALID_AUTHOR_KEY',
        'message': f'Author key \'{author_key}\' is invalid',
        'query': query
    }
)

# --- Editions Errors ---
EDITION_NOT_FOUND_ERROR = lambda query: HTTPException(
    status_code=404,
    detail={
        'error_code': 'EDITION_NOT_FOUND',
        'message': 'Edition not found error',
        'query': query
    }
)

INVALID_EDITION_KEY_ERROR = lambda query, edition_key: HTTPException(
    status_code=422,
    detail={
        'error_code': 'INVALID_EDITION_KEY',
        'message': f'Edition key \'{edition_key}\' is invalid',
        'query': query
    }
)

# ---------------------------------------------------------------
# HTTP Codes Grouping
# ---------------------------------------------------------------

HTTP_CODES = {
    400: [
        'INVALID_INPUT_ERROR',
    ],

    404: [
        'WORK_NOT_FOUND_ERROR',
        'AUTHOR_NOT_FOUND_ERROR',
        'EDITION_NOT_FOUND_ERROR',
    ],

    405: [
        'LISTING_NOT_SUPPORTED',
    ],

    422: [
        'INVALID_WORK_KEY_ERROR',
        'INVALID_AUTHOR_KEY_ERROR',
        'INVALID_EDITION_KEY_ERROR',
    ]
}
