# import logging
import feedparser
import requests

from dataclasses import dataclass, field
from collections.abc import Callable, Generator
from typing import Any

from app.models import SourceSchema, ArticleSchema


DICT_STR_ANY = Generator[dict[str, Any], None, None]


@dataclass
class RSS:
    url: str
    rss_dict: dict[str, Any] = field(init=False)
    source: SourceSchema = field(init=False)
    articles: DICT_STR_ANY = field(init=False)

    def __post_init__(self):
        self.rss_dict = self.get_rss(self.url)
        self.source = self.parse_source(self.rss_dict, self.url)
        self.articles = self.parse_articles(self.rss_dict)

    def get_rss(self, url: str) -> dict[str, Any]:
        response = requests.get(url)
        parsed: dict[str, str] = feedparser.parse(response.content)
        assert isinstance(parsed, dict)
        entries = parsed['entries']
        assert entries
        return parsed

    def parse_source(self, parsed_rss: dict[str, str], url: str) -> SourceSchema:
        record = SourceSchema(
            title=parsed_rss.get("title", "NO_TITLE"),
            subtitle=parsed_rss.get("subtitle", ""),
            url=url,
            language=parsed_rss.get("language", ""),
        )
        return record

    @staticmethod
    def parse_articles(parsed_rss: dict[str, Any], func: Callable | None = None) -> Generator[dict[str, Any], None, None]:
        for entry in parsed_rss["entries"]:
            assert isinstance(entry, dict)
            entry: dict[str, Any]
            data = {
                "source": entry.get("source", ""),
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "date_published": entry.get("date_published", ""),
                "image_url": entry.get("image_url", ""),
            }
            yield data

            if func:
                func(data)

    @classmethod
    def generate_rss_and_articles(cls, url: str):
        rss_dict: dict[str, Any] = cls.get_rss(url)
        assert isinstance(rss_dict, dict)
        articles_list: list[ArticleSchema] = []

        article: dict[str, str]
        parsed_arts = cls.parse_articles(
            rss_dict,
            # func=print
        )
        for article in parsed_arts:
            new_article = ArticleSchema(**article)
            articles_list.append(new_article)


if __name__ == "__main__":
    URL = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"

    rss = RSS(URL)
    print(rss.url)
    print(rss.source)
