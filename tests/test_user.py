from fastapi.testclient import TestClient
from fastapi import HTTPException
from contextlib import nullcontext as does_not_raises
import pytest
from jwt_app.main import app


client = TestClient(app)


@pytest.fixture
def login_prereq():
  data = {
    'username': 'test_user',
    'password': 'test_password'
  }

  client.post('/api/v1/add_user/', json = data)
  jwt_token = client.post('/api/v1/login/', json = data)

  return jwt_token


@pytest.mark.parametrize(
    "username, password, expectation",
    [
      ('string', 'string', 201),
      ('string', None, 422)
    ]
)
def test_create(username, password, expectation):

  data = {
    'username': username,
    'password': password
  }

  response = client.post('/api/v1/add_user/', json = data)    
  assert response.status_code == expectation

# incorrect case
def test_login():
  data = {
      'username': 'not_existing_one',
      'password': 'another_nonexisting'
    }
  
  resp_code = client.post('/api/v1/login/', json = data).status_code
  assert resp_code == 403
  