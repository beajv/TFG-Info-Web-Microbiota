from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ok"}

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
