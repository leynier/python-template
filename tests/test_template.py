from fastapi.testclient import TestClient

from template.main import app

client = TestClient(app)


def test_template():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
