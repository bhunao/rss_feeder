import logging

import feedparser
import requests

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlmodel import Field, SQLModel, Session

from src.core.base_service import BaseService
from src.core.database import get_session
from src.core.config import templates
from src.routers.news.models import News, NewsSchema


class NewsSource(SQLModel, table=True):
    __tablename__ = "news_sources"

    id: int = Field(default=None, primary_key=True)
    link: str
    name: str
    subtitle: str
    rights: Optional[str] = None
    image: Optional[str] = None


class NewsSourceSchema(SQLModel):
    link: str
    name: str
    subtitle: str
    rights: Optional[str] = None
    image: Optional[str] = None

def create_news_from_source(news_source: NewsSource, link, session) -> [NewsSchema]:
    response = requests.get(link)
    parsed = feedparser.parse(response.content)
    news_service = BaseService(News, session)
    for entry in parsed["entries"]:
        logger.info(f"creating record: {entry}")
        published = datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %z")
        exists = news_service.search(
                News.title == entry["title"],
                News.published == published,
                News.source_id == news_source.id
                )
        if exists:
            continue
        news_rec = NewsSchema(
                source_id=news_source.id,
                link=entry["link"],
                title=entry["title"],
                summary=entry["summary"],
                published=published
                )
        news_service.create(news_rec)
        logger.info("record created")


MODEL = NewsSource
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news_source", tags=["news_source"])


@router.get("/", response_class=HTMLResponse)
async def read_all(
    request: Request,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 15,
):
    result = BaseService(MODEL, session).read_all(skip=skip, limit=limit)
    return templates.TemplateResponse(
        "cards/list.html", {"request": request, "items": result}, block_name=None
    )


@router.post("/")
async def create(record: NewsSourceSchema, bg_task: BackgroundTasks, session: Session = Depends(get_session)):
    new_record = BaseService(MODEL, session).create(record)
    bg_task.add_task(create_news_from_source, new_record, record.link, session)
    return new_record

@router.get("/reload/{source_id}")
async def reload(source_id: int, bg_task: BackgroundTasks, session: Session = Depends(get_session)):
    record = BaseService(MODEL, session).read(source_id)
    bg_task.add_task(create_news_from_source, record, record.link, session)
    return True
