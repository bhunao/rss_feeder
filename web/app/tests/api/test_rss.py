from pprint import pprint as print

from starlette.testclient import TestClient

from app.errors import S400_INVALID_URL
from app.models import RssSchema

LINKS = [
    # TODO: download the xmls and open as files so no networking calls needed
    # or at least less for testing parsing.
    "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss",
    "https://ge.globo.com/ESP/Noticia/Rss/0,,AS0-4433,00.xml",
    "https://www.apartmenttherapy.com/main.rss",
    # "https://techcrunch.com/feed/",
    # "http://www.billboard.com/feed",
    # "https://gizmodo.com/rss",
]
INVALID_LINKS = [
    "https://duckgogo.com.br",
    "https://google.com.br"
]


def test_rss_link(client: TestClient) -> None:
    for _link in LINKS:
        data = {"url": _link}
        response = client.post(
            "/rss/parse_from/url",
            json=data
        )
        assert response.status_code == 200
        json: dict[str, str] = response.json()
        assert isinstance(json, dict)
        del json["articles"]
        # print(json)


def test_rss_invalid_link(client: TestClient) -> None:
    for _link in INVALID_LINKS:
        data = {"url": _link}
        response = client.post(
            "/rss/parse_from/url",
            json=data
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
    for _link in LINKS:
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
                # "etag": etag,
                # "href": href,
                # "namespaces": namespaces,
                # "updated": updated,
                # "updated_parsed": updated_parsed,
                # "encoding": encoding
            }:
                assert status is not None
                assert version is not None
                assert bozo is not None
                # assert etag is not None
                # assert href is not None
                # assert namespaces is not None
                # assert status is not None
                # assert updated is not None
                # assert updated_parsed is not None
                # assert encoding is not None
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
                # "link": link,
                # "links": links,
                # "subtitle": subtitle,
                # "language": language,
                # "rights": rights,
                # "rights_detail": rights_detail,
                # "image": image
            }:
                assert title
                assert title_detail
                # assert link
                # assert links
                # assert subtitle
                # assert language
                # assert rights
                # assert rights_detail
                # assert image
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
                    # "tags": [{"term": tags}],
                    # "title": title,
                    # "title_detail": title_detail,
                    # "published": published,
                    # "published_parsed": published_parsed
                }:
                    assert summary_detail is not None
                    assert summary is not None
                    assert links
                    assert link
                    # assert tags
                    # assert title
                    # assert title_detail
                    # assert published
                    # assert published_parsed
                case _:
                    e = list(entry.keys())
                    assert False, f"Invalid Key inside the `entries`: {e}"
    # print(possible_fields)


def test_parse_feed_invalid_link() -> None:
    """Test to see if the feedparser libary under the function accept
    diferent parameter types"""
    rss_schema = RssSchema.rss_dict_from(INVALID_LINKS[0])
    assert isinstance(rss_schema, Exception)


def test_template_response(client: TestClient):
    response = client.get("/rss/tst",
                          params={"a": "TEST_VALUE"})
    assert response.status_code == 200
    assert response.template
    assert response.template.name == "index.html"
    assert response.context["a"] == "TEST_VALUE"
    # print(list(response.__dict__.items()))
