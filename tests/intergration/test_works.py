"""
Integration tests for the `/works` endpoints of the API.

The suite validates:
- HTTP status codes for valid, invalid, and non-existing resources
- Response structure consistency across endpoints
- Edge cases such as missing relationships (authors, editions, series, etc.)
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
TEST_WORK_KEYS = {
    'existing': 'OL18020194W' ,             # Existing work in the database
    'missing': 'OL1800194W',                # Nonexisting work in the database
    'invalid': 'OL1800194',                 # Invalid work key (i.e. OLxxxxW)
    'no_authors': 'OL3467482W',             # Existing work with no authors
    'no_editions': 'OL3467482W',            # Existing work with no editions
    'no_series': 'OL35223328W',             # Existing work with no series
    'no_overview': 'OL3467482W',            # Existing work with no subjects, people, places or time periods
    'only_subjects': 'OL21487810W',         # Existing work with subjects but no people, places or time periods
    'only_subjects_people': 'OL27245843W',  # Existing work with subjects, people but no places or time periods
    'only_no_time_periods': 'OL27733867W',  # Existing work with subjects, people, places but no time periods
    'existing_batch': 'OL18020194W,OL24390422W',
    'missing_batch': 'OL1020194W,OL1800194W',
    'invalid_batch': 'OL18020194W,OL1800194'
}

# Parametrized list of the HTTP responses for each endpoint
HTTP_response_tests = [
    (TEST_WORK_KEYS['existing'], 200),
    (TEST_WORK_KEYS['missing'], 404),
    (TEST_WORK_KEYS['invalid'], 422),
]

HTTP_batch_response_tests = [
    (TEST_WORK_KEYS['existing_batch'], 200),
    (TEST_WORK_KEYS['missing_batch'], 404),
    (TEST_WORK_KEYS['invalid_batch'], 422),
]

# --------------------------------------------------------------------------
# --- GET /works/ ---
def test_get_all_works_listing():
    response = client.get('/works')
    assert response.status_code == 405

@pytest.mark.parametrize('keys,status', HTTP_batch_response_tests)
def test_get_batch_work(keys, status):
    response = client.get(f'/works?keys={keys}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key} ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work(work_key, status):
    response = client.get(f'/works/{work_key}')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key}/authors ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work_authors(work_key, status):
    response = client.get(f'/works/{work_key}/authors')
    assert response.status_code == status

def test_get_work_nonexisting_authors():
    response = client.get(f'/works/{TEST_WORK_KEYS['no_authors']}/authors')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key}/editions ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work_editions(work_key, status):
    response = client.get(f'/works/{work_key}/editions')
    assert response.status_code == status

def test_get_work_nonexisting_editions():
    response = client.get(f'/works/{TEST_WORK_KEYS['no_editions']}/editions')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key}/series ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work_series(work_key, status):
    response = client.get(f'/works/{work_key}/series')
    assert response.status_code == status

def test_get_work_nonexisting_series():
    response = client.get(f'/works/{TEST_WORK_KEYS['no_series']}/series')
    assert response.json()['data'] == []
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key}/availability ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work_availability(work_key, status):
    response = client.get(f'/works/{work_key}/availability')
    assert response.status_code == status
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key}/overview ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work_overview(work_key, status):
    response = client.get(f'/works/{work_key}/overview')
    assert response.status_code == status

def test_get_work_nonexisting_all_overview():
    response = client.get(f'/works/{TEST_WORK_KEYS['no_overview']}/overview')
    assert response.json()['data'][0]['subjects'] is None
    assert response.json()['data'][0]['people'] is None
    assert response.json()['data'][0]['places'] is None
    assert response.json()['data'][0]['time_periods'] is None

def test_get_work_only_existing_subjects_overview():
    response = client.get(f'/works/{TEST_WORK_KEYS['only_subjects']}/overview')
    assert response.json()['data'][0]['subjects'] is not None
    assert response.json()['data'][0]['people'] is None
    assert response.json()['data'][0]['places'] is None
    assert response.json()['data'][0]['time_periods'] is None

def test_get_work_only_existing_subjects_places_overview():
    response = client.get(f'/works/{TEST_WORK_KEYS['only_subjects_people']}/overview')
    assert response.json()['data'][0]['subjects'] is not None
    assert response.json()['data'][0]['people'] is not None
    assert response.json()['data'][0]['places'] is None
    assert response.json()['data'][0]['time_periods'] is None

def test_get_work_only_existing_subjects_places_people_overview():
    response = client.get(f'/works/{TEST_WORK_KEYS['only_no_time_periods']}/overview')
    assert response.json()['data'][0]['subjects'] is not None
    assert response.json()['data'][0]['people'] is not None
    assert response.json()['data'][0]['places'] is not None
    assert response.json()['data'][0]['time_periods'] is None
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /works/{work_key}/ratings ---
@pytest.mark.parametrize('work_key,status', HTTP_response_tests)
def test_get_work_ratings(work_key, status):
    response = client.get(f'/works/{work_key}/ratings')
    assert response.status_code == status
# --------------------------------------------------------------------------
