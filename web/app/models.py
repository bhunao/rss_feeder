from __future__ import annotations
import logging
import feedparser  # pyright: ignore[reportMissingTypeStubs]

from collections.abc import Generator
from sqlmodel import SQLModel
from typing import Any  # pyright: ignore[reportAny]


logger = logging.getLogger(__name__)


GEN_DICT = Generator[dict[str, Any], None, None]
DICT = dict[str, Any]


class SourceSchema(SQLModel):
    title: str
    url: str
    subtitle: str | None = None
    language: str | None = None
    link: str | None = None

    @classmethod
    def from_rss(cls, parsed_rss: DICT, url: str = "") -> SourceSchema | Exception:
        """Creates a new instance of the class `SourceSchema` with the data
        from the parsed rss dictionary."""
        assert parsed_rss.get("feed"), "RSS has no feed key in dict."

        feed: DICT = parsed_rss["feed"]
        title: str = feed.get("title", "")
        subtitle: str = feed.get("subtitle", "")
        language: str = feed.get("language", "")
        link: str = feed.get("link", "")

        if not title:
            NO_TITLE_SOURCE = AttributeError(
                "Source has no title and can not be created.")
            logger.error(NO_TITLE_SOURCE)
            return NO_TITLE_SOURCE

        record = cls(
            title=title,
            subtitle=subtitle,
            language=language,
            url=url,
            link=link,
        )
        return record


class ArticleSchema(SQLModel):
    source: str
    title: str
    summary: str
    date_published: str
    image_url: str

    @classmethod
    def from_rss(cls, parsed_rss: DICT) -> list[ArticleSchema]:
        """Get the articles from the `rss_dict` and create an `ArticleSchema`
        for each one of the valid articles.

        The articles often come with missing fields so all fields must be
        checked if exists and if its valid before trying to acess and save that
        data into the `ArticleSchema` object."""
        articles: list[ArticleSchema] = []
        for entry in parsed_rss["entries"]:
            entry: dict[str, Any]

            source: str = entry.get("source", "")
            title: str = entry.get("title", "")
            summary: str = entry.get("summary", "")
            date_published: str = entry.get("date_published", "")
            image_url: str = entry.get("image_url", "")

            _article = cls(
                source=source,
                title=title,
                summary=summary,
                date_published=date_published,
                image_url=image_url,
            )
            articles.append(_article)
        return articles


class RssSchema(SQLModel):
    source: SourceSchema
    articles: list[ArticleSchema]

    @staticmethod
    def rss_dict_from(url: str) -> DICT | Exception:
        """Parses an RSS feed from a given URL and returns the parsed content.

        This method fetches and parses an RSS feed from the provided URL using
        the `feedparser` library. If the parsing results
        returns an exception inside the dictionary then the method will return
        the error as a value.

        The `feedparser.parse` can accept multiple type of arguments.
        - url
        - file
        - stream
        - xml as string
        """
        parsed: DICT = feedparser.parse(url)
        assert isinstance(parsed, dict)
        exception: Exception | None = parsed.get("bozo_exception")
        if exception:
            return exception
        return parsed

    @classmethod
    def from_url(cls, url: str) -> RssSchema | Exception:
        """Creates a new instance of the class `RssSchema` from the parsed
        results of the given url.

        This method parses everything needed for the `RssSchema` to be
        created, if any data necessary for the creation of the `RssSchema`
        is invalid or not present the method returns the error as a value."""
        rss_dict = cls.rss_dict_from(url)
        if isinstance(rss_dict, Exception):
            return rss_dict
        source = SourceSchema.from_rss(rss_dict, url)
        assert isinstance(source, SourceSchema), "Error creating SourceSchema."
        articles = ArticleSchema.from_rss(rss_dict)
        return cls(
            source=source,
            articles=articles
        )
