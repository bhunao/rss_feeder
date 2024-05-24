import logging

import feedparser
import requests

from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.database import get_session
from src.core.config import templates
from src.models import Source, SourceSchema
from src.models import Article, ArticleSchema
from src.services.sources import SourceService
from src.services.articles import ArticleService
from src.core.errors import HTTP400_ALREADY_EXISTS


NAME = "sources"
PREFIX = f"/{NAME}"
TAGS = [NAME]

router = APIRouter(prefix=PREFIX, tags=TAGS)
logger = logging.getLogger(__name__)


def parse_rss_from_url(url: str) -> dict:
    response = requests.get(url)
    parsed = feedparser.parse(response.content)
    return parsed

def str_to_date(date: str):
    return datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")


def articles_from_source(source: Source, session: Session):
    parsed_rss = parse_rss_from_url(source.url)
    for entry in parsed_rss["entries"]:
        published = str_to_date(entry["published"])
        new_record = Article(
                source_id=source.id,
                title=entry["title"],
                summary=entry["summary"],
                date_published=published,
                image_url="",
                )
        ArticleService(session).create(new_record)


@router.get("/trena", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_session)) -> str:
    result = SourceService(session).read_all()
    return templates.TemplateResponse(
            "cards/sources.html", {"request": request, "items": result}, block_name=None
    )


@router.post("/", response_model=Source)
async def create(record: SourceSchema, session: Session = Depends(get_session)):
    new_source = SourceService(session).create(record)
    if new_source is None:
        raise HTTP400_ALREADY_EXISTS
    articles_from_source(new_source, session)
    return new_source

@router.get("/", response_model=Source)
async def read(id: int, session: Session = Depends(get_session)):
    result = SourceService(session).read(id)
    return result

@router.post("/update", response_model=Source)
async def update(record: Source, session: Session = Depends(get_session)):
    result = SourceService(session).update(record)
    return result

@router.delete("/", response_model=Source)
async def delete(id: int, session: Session = Depends(get_session)):
    result = SourceService(session).delete(id)
    return result

@router.get("/all", response_model=List[Source])
async def read_all(
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
        ):
    result = SourceService(session).read_all(skip, limit)
    return result
