from fastapi.testclient import TestClient
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de entrada para simular datos
class Numeros(BaseModel):
    a: int
    b: int

@app.post("/suma")
def sumar(numeros: Numeros):
    return {"resultado": numeros.a + numeros.b}

client = TestClient(app)

def test_suma():
    payload = {"a": 7, "b": 5}
    response = client.post("/suma", json=payload)
    assert response.status_code == 200
    assert response.json()["resultado"] == 12
