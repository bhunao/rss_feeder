from fastapi.testclient import TestClient


def test_rss_link(client: TestClient) -> None:
    LINK = "www.duckgogo.com"

    payload = {"name": "duckgogo", "link": LINK}
    response = client.post(
        "/rss",
        json=payload
    )
    assert response.status_code == 200
