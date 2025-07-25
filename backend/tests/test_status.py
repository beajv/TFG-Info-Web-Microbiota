from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "API funcionando", "version": "1.0"}

client = TestClient(app)

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "API funcionando"
    assert data["version"] == "1.0"
