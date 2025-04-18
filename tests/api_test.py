from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_create_user():
    response = client.post('/user', json={"name": "Sam", "amount": 100.00})
    assert response.status_code == 200
    assert response.json()["name"] == "Sam"