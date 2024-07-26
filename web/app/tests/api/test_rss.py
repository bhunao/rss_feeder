from pprint import pprint as print

from fastapi.testclient import TestClient

from app.errors import S400_INVALID_URL
from app.feed_parser import RssSchema

LINKS = [
    "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss",
    "https://ge.globo.com/ESP/Noticia/Rss/0,,AS0-4433,00.xml",
    "https://www.apartmenttherapy.com/main.rss",
    "https://techcrunch.com/feed/",
    "http://www.billboard.com/feed",
    "https://gizmodo.com/rss",
]
INVALID_LINK = "https://duckgogo.com.br"

LINK = LINKS[1]


def test_rss_link(client: TestClient) -> None:
    data = {"url": LINK}
    response = client.post(
        "/rss/parse_from/url",
        json=data
    )
    assert response.status_code == 200
    json: dict[str, str] = response.json()
    assert isinstance(json, dict)


def test_rss_invalid_link(client: TestClient) -> None:
    data = {"url": INVALID_LINK}
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

    all_keys: set[str] = set()
    missing_in: set[str] = set()
    always_keys: set[str] = set()
    for _link in LINKS:
        rss_schema = RssSchema.rss_dict_from(_link)
        assert isinstance(rss_schema, dict)
        # assert rss_schema["status"] == 200
        # assert isinstance(rss_schema, RssSchema)
        # print(rss_schema.keys())
        # print(["bozo", rss_schema["bozo"]])
        # print(["feed", rss_schema["feed"].keys()])
        # print(rss_schema["source"])

        #  articles
        for entry in rss_schema["entries"]:
            entry: dict[str, str | list[dict[str, str]]]
            keys = list(entry.keys())
            _all = [all_keys.add(name) for name in keys]
            _missing = {missing_in.add(name)
                        for name in all_keys if name not in keys}
            # print("")
            # print("S".center(100, "="))
            print(len(all_keys))
            # assert entry["authors"]
            match entry:
                case {
                    # "tags": [{"term": tags}],
                    # "title": title,
                    # "title_detail": title_detail,
                    # "summary": summary,
                    # "summary_detail": summary_detail,
                    # "links": links,
                    # "link": link,
                    # "published": published,
                    # "published_parsed": published_parsed
                }:
                    # assert tags
                    # assert title
                    # assert title_detail
                    # assert summary_detail
                    # assert summary
                    # assert links
                    # assert link
                    # assert published
                    # assert published_parsed
                    ...
                case _:
                    e = list(entry.keys())
                    # assert False, f"Invalid Key inside the `entries`: {e}"

            # source
            feed = rss_schema["feed"]
            feed: dict[str, str]
            match feed:
                case {
                    "title": title,
                    "title_detail": title_detail,
                    "link": link,
                    "links": links,
                    "subtitle": subtitle,
                    "language": language,
                    "rights": rights,
                    "rights_detail": rights_detail,
                    "image": image
                }:
                    assert title
                    assert title_detail
                    assert link
                    assert links
                    assert subtitle
                    assert language
                    assert rights
                    assert rights_detail
                    assert image
                case _:
                    e = list(entry.keys())
                    # assert False, f"Invalid Key inside the `feed`: {e}"

            # rss feed
            match rss_schema:
                case {
                    "etag": etag,
                    "href": href,
                    "namespaces": namespaces,
                    "version": version,
                    "status": status,
                    "updated": updated,
                    "updated_parsed": updated_parsed,
                    "encoding": encoding
                }:
                    assert etag is not None
                    assert href is not None
                    assert namespaces is not None
                    assert version is not None
                    assert status is not None
                    assert updated is not None
                    assert updated_parsed is not None
                    assert encoding is not None
                case _:
                    e = list(entry.keys())
                    # assert False, f"Invalid Key inside `rss dictionary`: {e}"

            # print(rss_schema.keys())
            # print(rss_schema["etag"])
            # print("")
            # print(rss_schema["updated"])
            # print("")
            # print(rss_schema["href"])
            # print("")
            # print(rss_schema["namespaces"])
            # print("")
            # print(rss_schema["version"])
            # print("")
            # print(rss_schema["status"])
            # print("")
            # print(rss_schema["updated"])
            # print("")
            # print(rss_schema["updated_parsed"])
            # print(type(rss_schema["updated_parsed"]))
            # print("")
            # print(rss_schema["encoding"])

    print("")
    print(f"{all_keys =}")
    print("")
    print(f"{missing_in =}")
    print("")
    always_keys = {name for name in all_keys if name not in missing_in}
    print(f"{always_keys =}")


def test_parse_feed_invalid_link() -> None:
    """Test to see if the feedparser libary under the function accept
    diferent parameter types"""
    # xml = requests.get(LINK).content
    rss_schema = RssSchema.rss_dict_from(INVALID_LINK)
    assert isinstance(rss_schema, Exception)
