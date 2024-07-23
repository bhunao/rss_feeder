import requests

from fastapi.testclient import TestClient

from app.feed_parser import RssSchema

LINK = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"


def test_rss_xml(client: TestClient) -> None:
    xml_str = requests.get(LINK).content
    assert xml_str
    # TODO: TestClient doesn't accept xml, only json
    # response = client.post(
    #     "/rss/parse_from/xml",
    #     json=""
    # )
    # assert response.status_code == 200


def test_rss_link(client: TestClient) -> None:
    response = client.post(
        "/rss/parse_from/url",
        json=LINK
    )
    assert response.status_code == 200


def test_feedparser_params() -> None:
    """Test to see if the feedparser libary under the function accept
    diferent parameter types"""
    rss_schema = RssSchema.parse_feed(LINK)
    assert isinstance(rss_schema, RssSchema)

    xml = requests.get(LINK).content
    rss_schema = RssSchema.parse_feed(xml)
    assert isinstance(rss_schema, RssSchema)
