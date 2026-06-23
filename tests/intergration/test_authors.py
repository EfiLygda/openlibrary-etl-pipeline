"""
Integration tests for the `/authors` endpoints of the API.

The suite validates:
- HTTP status codes for valid, invalid, and non-existing resources
- Response structure consistency across endpoints
- Edge cases such as missing relationships (works, editions, etc.)
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
TEST_AUTHOR_KEYS = {
    'existing': 'OL1386221A' ,              # Existing author in the database
    'missing': 'OL138221A',                 # Nonexisting author in the database
    'invalid': 'OL1386221',                 # Invalid author key (i.e. OLxxxxA)
    'no_works': 'OL1393290A',               # Existing author with no works
    'no_statistics': 'OL12903718A',         # Existing author with no statistics
    'no_alternative_names': 'OL6216069A',   # Existing author with no alternative names
    'existing_batch': 'OL1386221A,OL1393290A',
    'missing_batch': 'OL138621A,OL13320A',
    'invalid_batch': 'OL1386221A,OL1393290'
}

# Parametrized list of the HTTP responses for each endpoint
HTTP_response_tests = [
    (TEST_AUTHOR_KEYS['existing'], 200),
    (TEST_AUTHOR_KEYS['missing'], 404),
    (TEST_AUTHOR_KEYS['invalid'], 422),
]

HTTP_batch_response_tests = [
    (TEST_AUTHOR_KEYS['existing_batch'], 200),
    (TEST_AUTHOR_KEYS['missing_batch'], 404),
    (TEST_AUTHOR_KEYS['invalid_batch'], 422),
]

# --------------------------------------------------------------------------
# --- GET /authors/ ---
def test_get_all_authors_listing():
    response = client.get('/authors')
    assert response.status_code == 405

@pytest.mark.parametrize('keys,status', HTTP_batch_response_tests)
def test_get_batch_author(keys, status):
    response = client.get(f'/authors?keys={keys}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /authors/{author_key} ---
@pytest.mark.parametrize('author_key,status', HTTP_response_tests)
def test_get_author(author_key, status):
    response = client.get(f'/authors/{author_key}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /authors/{author_key}/works ---
@pytest.mark.parametrize('author_key,status', HTTP_response_tests)
def test_get_authors_works(author_key, status):
    response = client.get(f'/authors/{author_key}/works')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /authors/{author_key}/editions ---
@pytest.mark.parametrize('author_key,status', HTTP_response_tests)
def test_get_author_editions(author_key, status):
    response = client.get(f'/authors/{author_key}/editions')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /authors/{author_key}/statistics ---
@pytest.mark.parametrize('author_key,status', HTTP_response_tests)
def test_get_author_statistics(author_key, status):
    response = client.get(f'/authors/{author_key}/statistics')
    assert response.status_code == status

def test_get_author_nonexisting_statistics():
    response = client.get(f'/authors/{TEST_AUTHOR_KEYS['no_statistics']}/statistics')
    assert all(field is None for field in response.json()['data'][0].values())
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /authors/{author_key}/alternative_names ---
@pytest.mark.parametrize('author_key,status', HTTP_response_tests)
def test_get_author_alternative_names(author_key, status):
    response = client.get(f'/authors/{author_key}/alternative_names')
    assert response.status_code == status

def test_get_author_nonexisting_alternative_names():
    response = client.get(f'/authors/{TEST_AUTHOR_KEYS['no_alternative_names']}/alternative_names')
    assert response.json()['data'][0]['alternative_names'] == []
# --------------------------------------------------------------------------
