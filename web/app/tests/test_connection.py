from fastapi.testclient import TestClient


def test_test(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() is True
