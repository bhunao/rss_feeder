from pprint import pprint as print
import requests

from fastapi.testclient import TestClient

from app.feed_parser import RssSchema

LINKS = [
    "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss",
    "https://ge.globo.com/ESP/Noticia/Rss/0,,AS0-4433,00.xml"
]

LINK = LINKS[1]


def test_rss_link(client: TestClient) -> None:
    response = client.post(
        "/rss/parse_from/url",
        json=LINK
    )
    assert response.status_code == 200
    print("\n\n")
    json = response.json()
    assert isinstance(json, dict)
    print(json["source"])


def test_feedparser_params() -> None:
    """Test to see if the feedparser libary under the function accept
    diferent parameter types"""
    rss_schema = RssSchema.parse_feed(LINK)
    assert isinstance(rss_schema, RssSchema)

    xml = requests.get(LINK).content
    rss_schema = RssSchema.parse_feed(xml)
    assert isinstance(rss_schema, RssSchema)
