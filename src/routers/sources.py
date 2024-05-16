import logging

import feedparser
import requests

from datetime import datetime

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.base_service import BaseService
from src.core.database import get_session
from src.core.config import templates
from src.models.articles import Article, ArticleSchema
from src.models.sources import Source, SourceSchema
from src.models.articles import Article, ArticleSchema


def create_news_from_source(news_source: Source, link, session) -> [SourceSchema]:
    response = requests.get(link)
    parsed = feedparser.parse(response.content)

    for entry in parsed["entries"]:
        logger.info(f"creating record: {entry}")
        published = datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %z")
        exists = Article().search(
                Article.title == entry["title"],
                Article.date_published == published,
                Article.source_id == news_source.id
                )
        if exists:
            continue
        news_rec = ArticleSchema(
                source_id=news_source.id,
                title=entry["title"],
                summary=entry["summary"],
                date_published=published,
                image_url="",
                )
        Article().create(session, news_rec)
        logger.info(f"record created: {new_rec}")


logger = logging.getLogger(__name__)
router = Source().__router__


@router.post("/")
async def create(record: SourceSchema, session: Session = Depends(get_session)):
    result = Source().create(session, record)
    create_news_from_source(result, result.url, session)
    return result

@router.get("/")
async def get(id: int, session: Session = Depends(get_session)):
    result = Source().read(session, id)
    return result

@router.post("/update")
async def update(record: Source, session: Session = Depends(get_session)):
    result = Source().update(session, record)
    return result

@router.delete("/")
async def delete(id: int, session: Session = Depends(get_session)):
    result = Source().delete(session, id)
    return result
