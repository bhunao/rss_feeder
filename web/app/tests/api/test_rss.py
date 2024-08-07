from typing import Any
from fastapi.testclient import TestClient

from app.errors import S400_INVALID_URL
from app.models import RssSchema

VALID_URLS = [
    # TODO: download the xmls and open as files so no networking calls needed
    # or at least less for testing parsing.
    "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss",
    "https://ge.globo.com/ESP/Noticia/Rss/0,,AS0-4433,00.xml",
    "https://www.apartmenttherapy.com/main.rss",
    "https://techcrunch.com/feed/",
    # "http://www.billboard.com/feed",
    # "https://gizmodo.com/rss",
]
INVALID_URLS = [
    "https://duckgogo.com.br",
    "https://google.com.br"
]


def test_rss_link(client: TestClient) -> None:
    for _url in VALID_URLS:
        response = client.get(
            "/rss/parse_from",
            params={"url": _url},
            headers={"accept": "application/json"}
        )
        assert response.status_code == 200
        json: dict[str, str] = response.json()
        assert isinstance(json, dict)


def test_rss_invalid_link(client: TestClient) -> None:
    for _url in INVALID_URLS:
        response = client.get(
            "/rss/parse_from",
            params={"url": _url},
            headers={"accept": "application/json"}
        )
        assert response.status_code == S400_INVALID_URL.status_code
        json: dict[str, str] = response.json()
        assert isinstance(json, dict)
        assert json["detail"] == S400_INVALID_URL.detail


def test_parse_feed() -> None:
    """Test to see if the feedparser libary under the function accept
    diferent parameter types.

    Test to see all the possible data that came in the xml."""

    possible_fields: dict[str, set[str]] = {
        "rss_feed": set(),
        "source": set(),
        "articles": set()
    }
    for _link in VALID_URLS:
        rss_schema = RssSchema.rss_dict_from(_link)
        assert isinstance(rss_schema, dict)

        possible_fields["rss_feed"].update(rss_schema.keys())
        possible_fields["source"].update(rss_schema["feed"].keys())
        possible_fields["articles"].update(rss_schema["entries"][0].keys())

        # rss feed
        match rss_schema:
            case {
                "version": version,
                "bozo": bozo,
                "status": status,
            }:
                assert status is not None
                assert version is not None
                assert bozo is not None
            case _:
                e = list(rss_schema.keys())
                assert False, f"Invalid Key inside `rss dictionary`: {e}"

        # source
        feed = rss_schema["feed"]
        feed: dict[str, str]
        match feed:
            case {
                "title": title,
                "title_detail": title_detail,
            }:
                assert title
                assert title_detail
                pass
            case _:
                e = list(feed.keys())
                assert False, f"Invalid Key inside the `feed`: {e}"

        #  articles
        for entry in rss_schema["entries"]:
            entry: dict[str, str | list[dict[str, str]]]

            match entry:
                case {
                    "summary": summary,
                    "summary_detail": summary_detail,
                    "links": links,
                    "link": link,
                }:
                    assert summary_detail is not None
                    assert summary is not None
                    assert links
                    assert link
                case _:
                    e = list(entry.keys())
                    assert False, f"Invalid Key inside the `entries`: {e}"
    # print(possible_fields)


def test_parse_feed_invalid_link() -> None:
    """Test to see if the feedparser libary under the function accept
    diferent parameter types"""
    rss_schema = RssSchema.rss_dict_from(INVALID_URLS[0])
    assert isinstance(rss_schema, Exception)


def test_multi_content_type_endpoint(client: TestClient):
    """Test the same endpoint with different header value for `accept`.
    Testing the json content-type passing `application/json` in the header
    and testing the normal endpoint without the `application/json` header
    the endpoint must return an HTML template."""
    response = client.get(
        "/rss/parse_from",
        params={"url": VALID_URLS[-1]},
        headers={"accept": "application/json"}
    )
    json_response: dict[str, Any] = response.json()
    assert response.status_code == 200
    assert isinstance(json_response, dict)

    response = client.get(
        "/rss/parse_from",
        params={"url": VALID_URLS[-1]},
    )

    assert response.status_code == 200
    assert response.template
    assert response.template.name == "index.html"

    rss = response.context["rss"]
    assert isinstance(rss, RssSchema)
    assert rss.source.title == "TechCrunch"
