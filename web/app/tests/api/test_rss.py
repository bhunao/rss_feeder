from fastapi.testclient import TestClient


def test_rss_link(client: TestClient) -> None:
    LINK = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"
    response = client.post(
        "/rss/parse_xml",
        json=LINK
    )
    assert response.status_code == 200
    assert response.json()
