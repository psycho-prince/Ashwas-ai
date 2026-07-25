from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_trigger_validation():
    # Test with empty situation (should fail validation)
    response = client.post("/trigger", json={"situation": ""})
    assert response.status_code == 422
