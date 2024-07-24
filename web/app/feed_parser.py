# import logging
import feedparser

from collections.abc import Generator
from sqlmodel import SQLModel
from typing import Any, BinaryIO  # pyright: ignore[reportAny]

from app.models import SourceSchema, ArticleSchema


GEN_DICT = Generator[dict[str, Any], None, None]
DICT = dict[str, Any]

URL_XML_FILE = str | bytes | BinaryIO


class RssSchema(SQLModel):
    source: SourceSchema
    articles: list[ArticleSchema]

    @staticmethod
    def parse_source(parsed_rss: DICT, url: str = "") -> SourceSchema:
        assert parsed_rss.get("feed"), "RSS has no feed key in dict."

        feed: DICT = parsed_rss["feed"]
        title: str = feed.get("title", "NO_TITLE")
        subtitle: str = feed.get("subtitle", "")
        language: str = feed.get("language", "")

        record = SourceSchema(
            title=title,
            subtitle=subtitle,
            language=language,
            url=url,
        )
        return record

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
    def rss_dict_from(url_or_xml: URL_XML_FILE) -> DICT:
        parsed: DICT = feedparser.parse(url_or_xml)
        assert isinstance(parsed, dict)
        return parsed

    @classmethod
    def parse_feed(cls, url_or_xml: URL_XML_FILE):
        rss_dict = cls.rss_dict_from(url_or_xml)
        source = cls.parse_source(rss_dict)
        articles = cls.parse_articles(rss_dict)
        return cls(
            source=source,
            articles=articles
        )
