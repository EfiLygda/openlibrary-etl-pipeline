"""
Integration tests for the `/languages` endpoints of the API.

The suite validates:
- HTTP status codes for valid, invalid, and non-existing resources
- Response structure consistency across endpoints

Note: 1. Test keys are included at the sample of 2000 works provided with the project
      2. ISO 693-2 codes: https://www.loc.gov/standards/iso639-2/php/code_list.php

"""

import pytest
from fastapi.testclient import TestClient
from api.app import app

# FastAPI test client used to send HTTP requests directly to the
# application without running a live server
client = TestClient(app)

# Dictionary with test keys
TEST_KEYS = {
    'existing_language_code': 'eng' ,           # Existing ISO 693-2 language code
    'missing_language_code': 'ffffff',          # Nonexisting ISO 693-2 language code
    'existing_language_code_batch': 'eng, deu', # Existing ISO 693-2 language codes
}

# Parametrized list of the HTTP responses for each endpoint
HTTP_response_tests = [
    (TEST_KEYS['existing_language_code'], 200),
    (TEST_KEYS['missing_language_code'], 400),
    (TEST_KEYS['existing_language_code'], 200),
]

# --------------------------------------------------------------------------
# --- GET /languages/ ---
def test_get_all_languages_listing():
    response = client.get('/languages')
    assert response.status_code == 200
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# --- GET /languages?{code_1},{code_2},... ---
@pytest.mark.parametrize('key,status', HTTP_response_tests)
def test_get_languages(key, status):
    response = client.get(f'/languages?lang={key}')
    assert response.status_code == status
# --------------------------------------------------------------------------
