"""
Integration tests for the `/search` endpoint of the API.

The suite validates:
- HTTP status codes for valid, invalid, and non-existing resources
- Response structure consistency across endpoints

Note: Test keys are included at the sample of 2000 works provided with the project
"""

import pytest
from fastapi.testclient import TestClient
from api.app import app

# FastAPI test client used to send HTTP requests directly to the
# application without running a live server
client = TestClient(app)

# Dictionary with test keys
TEST_QUERIES = {
    'existing': 'pride prejudice',
    'not_found': 'akasjidnsvsojc',
}

# Parametrized list of the HTTP responses for each endpoint
HTTP_response_tests = [
    (TEST_QUERIES['existing'], 200),
    (TEST_QUERIES['not_found'], 404),
]

# --------------------------------------------------------------------------
# --- GET /search/ ---
def test_search_listing():
    response = client.get('/search')
    assert response.status_code == 422
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /search?q={query} ---
@pytest.mark.parametrize('query,status', HTTP_response_tests)
def test_search_query(query, status):
    response = client.get(f'/search?q={query}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /search?q={query}&title={title} ---
def test_search_query_conflict():
    response = client.get(f'/search?q=pride prejudice&author=jane austin')
    assert response.status_code == 422
# --------------------------------------------------------------------------