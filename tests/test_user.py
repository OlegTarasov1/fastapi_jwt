from fastapi.testclient import TestClient
from jwt_app.main import app

client = TestClient(app)

data = {
  "username": "asdf",
  "password": "asdf"
}

def test_create():
    response = client.post('/api/v1/add_user/', json = data)    
    assert response.status_code == 200


def test_get_user():
    response = client.get('/api/v1/get_user/36/')
    print(response.json())
    assert response.status_code == 200