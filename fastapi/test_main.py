from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_procesos():
    response = client.get("/procesos/", headers={"Authorization": "Bearer admin"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Asegúrate de que devuelve una lista

def test_authentication():
    # Test incorrect login
    response = client.post("/token", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 400

    # Test correct login
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()