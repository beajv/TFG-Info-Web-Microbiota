# backend/tests/test_api.py
from fastapi.testclient import TestClient
from myapp.main_test import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
