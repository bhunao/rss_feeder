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


def create_news_from_source(news_source: Source, link, session) -> [SourceSchema]:
    response = requests.get(link)
    parsed = feedparser.parse(response.content)
    news_service = BaseService(News, session)
    for entry in parsed["entries"]:
        logger.info(f"creating record: {entry}")
        published = datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %z")
        exists = news_service.search(
                Article.title == entry["title"],
                Article.date_published == published,
                Article.source_id == news_source.id
                )
        if exists:
            continue
        news_rec = ArticleSchema(
                source_id=news_source.id,
                link=entry["link"],
                title=entry["title"],
                summary=entry["summary"],
                published=published
                )
        news_service.create(news_rec)
        logger.info("record created")


MODEL = Source
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_class=HTMLResponse)
async def read_all(
    request: Request,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 15,
):
    result = BaseService(MODEL).read_all(session, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "cards/list.html", {"request": request, "items": result}, block_name=None
    )


@router.post("/")
async def create(record: SourceSchema, bg_task: BackgroundTasks, session: Session = Depends(get_session)):
    new_record = BaseService(MODEL).create(session, record)
    bg_task.add_task(create_news_from_source, new_record, record.link, session)
    return new_record

@router.get("/reload/{source_id}")
async def reload(source_id: int, bg_task: BackgroundTasks, session: Session = Depends(get_session)):
    record = BaseService(MODEL).read(session, source_id)
    bg_task.add_task(create_news_from_source, record, record.link, session)
    return True
