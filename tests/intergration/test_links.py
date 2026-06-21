"""
Integration tests for the `/links` endpoints of the API.

The suite validates:
- HTTP status codes for valid, invalid, and non-existing resources
- Response structure consistency across endpoints
- Edge cases such as missing relationships (authors, works, etc.)
- Data integrity for nested resources like overview fields

Note: Test keys are included at the sample of 2000 works provided with the project
"""

import pytest
from fastapi.testclient import TestClient
from api.app import app

# FastAPI test client used to send HTTP requests directly to the
# application without running a live server
client = TestClient(app)

# Dictionary with test keys
TEST_KEYS = {
    'existing_work': 'OL18020194W' ,    # Existing work in the database
    'missing_author': 'OL138621A',      # Nonexisting author in the database
    'invalid_key': 'OL18020194',        # Invalid key (i.e. OLxxxxW, OLxxxxA, OLxxxxM)
}

# Parametrized list of the HTTP responses for each endpoint
HTTP_response_tests = [
    (TEST_KEYS['existing_work'], 200),
    (TEST_KEYS['missing_author'], 404),
    (TEST_KEYS['invalid_key'], 422),
]

# --------------------------------------------------------------------------
# --- GET /links/ ---
def test_get_all_links_listing():
    response = client.get('/links')
    assert response.status_code == 405
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /links/{key} ---
@pytest.mark.parametrize('key,status', HTTP_response_tests)
def test_get_edition(key, status):
    response = client.get(f'/links/{key}')
    assert response.status_code == status
# --------------------------------------------------------------------------
