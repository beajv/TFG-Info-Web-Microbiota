# tests/test_api.py
from fastapi.testclient import TestClient
from myapp.main import app  # Cambia esto si tu app tiene otro nombre

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
