# import logging
import feedparser

from collections.abc import Generator
from sqlmodel import SQLModel
from typing import Any  # pyright: ignore[reportAny]

from app.models import SourceSchema, ArticleSchema


GEN_DICT = Generator[dict[str, Any], None, None]
DICT = dict[str, Any]


class RssSchema(SQLModel):
    source: SourceSchema
    articles: list[ArticleSchema]

    @staticmethod
    def parse_source(parsed_rss: DICT, url: str = "") -> SourceSchema:
        assert parsed_rss.get("feed"), "RSS has no feed key in dict."

        feed: DICT = parsed_rss["feed"]
        match feed:
            case {"title": title, "subtitle": subtitle, "language": lang}:
                title: str
                subtitle: str
                lang: str
                record = SourceSchema(
                    title=title,
                    subtitle=subtitle,
                    language=lang,
                    url=url,
                )
                return record
            case _:
                raise KeyError("missing something or wawhetversdasdver")

    @ staticmethod
    def parse_articles(parsed_rss: DICT) -> list[ArticleSchema]:
        articles: list[ArticleSchema] = []
        for entry in parsed_rss["entries"]:
            entry: dict[str, Any]

            source: str = entry.get("source", "")
            title: str = entry.get("title", "")
            summary: str = entry.get("summary", "")
            date_published: str = entry.get("date_published", "")
            image_url: str = entry.get("image_url", "")

            _article = ArticleSchema(
                source=source,
                title=title,
                summary=summary,
                date_published=date_published,
                image_url=image_url,
            )
            articles.append(_article)
        return articles

    @staticmethod
    def rss_dict_from(url: str) -> DICT:
        parsed: DICT = feedparser.parse(url)
        assert isinstance(parsed, dict)
        return parsed

    @classmethod
    def from_url(cls, url: str):
        rss_dict = cls.rss_dict_from(url)
        source = cls.parse_source(rss_dict, url)
        articles = cls.parse_articles(rss_dict)
        return cls(
            source=source,
            articles=articles
        )

    @classmethod
    def parse_feed(cls, url: str):
        rss_dict = cls.rss_dict_from(url)
        source = cls.parse_source(rss_dict, url)
        articles = cls.parse_articles(rss_dict)
        return cls(
            source=source,
            articles=articles
        )
