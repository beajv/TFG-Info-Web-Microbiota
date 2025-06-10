from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def get_health():
    return {"healthy": True}

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["healthy"] is True
