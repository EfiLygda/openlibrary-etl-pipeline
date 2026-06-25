"""
Integration tests for the `/editions` endpoints of the API.

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
TEST_EDITION_KEYS = {
    'existing': 'OL37490633M' ,             # Existing edition in the database
    'missing': 'OL5864068M',                # Nonexisting edition in the database
    'invalid': 'OL5864068',                 # Invalid edition key (i.e. OLxxxxM)
    'no_details': 'OL7502900M',             # Existing edition with no details
    'no_contents': 'OL58640668M',           # Existing edition with no contents
    'no_publishing': 'OL43136091M',         # Existing edition with no publishing
    'no_contributors': 'OL37986988M',       # Existing edition with no contributors
    'existing_batch': 'OL37490633M,OL7502900M',
    'missing_batch': 'OL3790633M,OL752900M',
    'invalid_batch': 'OL37490633M,OL7502900'
}

# Parametrized list of the HTTP responses for each endpoint
HTTP_response_tests = [
    (TEST_EDITION_KEYS['existing'], 200),
    (TEST_EDITION_KEYS['missing'], 404),
    (TEST_EDITION_KEYS['invalid'], 422),
]

HTTP_batch_response_tests = [
    (TEST_EDITION_KEYS['existing_batch'], 200),
    (TEST_EDITION_KEYS['missing_batch'], 404),
    (TEST_EDITION_KEYS['invalid_batch'], 422),
]


# --------------------------------------------------------------------------
# --- GET /editions/ ---
def test_get_all_editions_listing():
    response = client.get('/editions')
    assert response.status_code == 405

@pytest.mark.parametrize('keys,status', HTTP_batch_response_tests)
def test_get_batch_editions(keys, status):
    response = client.get(f'/editions?keys={keys}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /editions/{editions_key} ---
@pytest.mark.parametrize('editions_key,status', HTTP_response_tests)
def test_get_edition(editions_key, status):
    response = client.get(f'/editions/{editions_key}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /editions/{editions_key}/work ---
@pytest.mark.parametrize('editions_key,status', HTTP_response_tests)
def test_get_edition_work(editions_key, status):
    response = client.get(f'/editions/{editions_key}/work')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /editions/{editions_key}/details ---
@pytest.mark.parametrize('editions_key,status', HTTP_response_tests)
def test_get_edition_details(editions_key, status):
    response = client.get(f'/editions/{editions_key}/details')
    assert response.status_code == status

def test_get_edition_nonexisting_details():
    response = client.get(f'/editions/{TEST_EDITION_KEYS['no_details']}/details')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /editions/{editions_key}/contents ---
@pytest.mark.parametrize('editions_key,status', HTTP_response_tests)
def test_get_edition_contents(editions_key, status):
    response = client.get(f'/editions/{editions_key}/contents')
    assert response.status_code == status

def test_get_edition_nonexisting_contents():
    response = client.get(f'/editions/{TEST_EDITION_KEYS['no_contents']}/contents')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /editions/{editions_key}/publishing ---
@pytest.mark.parametrize('editions_key,status', HTTP_response_tests)
def test_get_edition_publishing(editions_key, status):
    response = client.get(f'/editions/{editions_key}/publishing')
    assert response.status_code == status

def test_get_edition_nonexisting_publishing():
    response = client.get(f'/editions/{TEST_EDITION_KEYS['no_publishing']}/publishing')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /editions/{editions_key}/contributors ---
@pytest.mark.parametrize('editions_key,status', HTTP_response_tests)
def test_get_edition_contributors(editions_key, status):
    response = client.get(f'/editions/{editions_key}/contributors')
    assert response.status_code == status

def test_get_edition_nonexisting_contributors():
    response = client.get(f'/editions/{TEST_EDITION_KEYS['no_contributors']}/contributors')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------
