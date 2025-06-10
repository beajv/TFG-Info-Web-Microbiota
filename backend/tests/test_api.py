from fastapi.testclient import TestClient
from fastapi import FastAPI

# Definimos la app (sin necesidad de PostgreSQL)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ok"}

@app.get("/status")
def get_status():
    return {"status": "API funcionando", "version": "1.0"}

# Cliente de pruebas
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "API funcionando"
    assert data["version"] == "1.0"
