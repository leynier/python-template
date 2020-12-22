from fastapi.testclient import TestClient

from template.main import app

client = TestClient(app)


def test_redirections():
    response_home = client.get("/")
    response_api = client.get("/api")
    response_api_v1 = client.get("/api/v1")
    assert response_home.status_code == 200
    assert response_api.status_code == 200
    assert response_api_v1.status_code == 200
    assert response_home.url == response_api.url
    assert response_api.url == response_api_v1.url


def test_hello_world():
    response = client.get("/api/v1/hello-world")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
