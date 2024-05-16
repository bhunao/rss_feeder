import logging

import feedparser
import requests

from typing import List
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


logger = logging.getLogger(__name__)
router = Source.create_router()


def parse_rss_from_url(url: str) -> dict:
    response = requests.get(url)
    parsed = feedparser.parse(response.content)
    return parsed

def str_to_date(date: str):
    return datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")


def articles_from_source(session: Session, source: Source):
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
        Article().create(session, new_record)


@router.post("/")
async def create(record: SourceSchema, session: Session = Depends(get_session)):
    result = Source.create(session, record)
    articles_from_source(session, result)
    return result

@router.get("/")
async def read(id: int, session: Session = Depends(get_session)):
    result = Source.read(session, id)
    return result

@router.post("/update")
async def update(record: Source, session: Session = Depends(get_session)):
    result = Source.update(session, record)
    return result

@router.delete("/")
async def delete(id: int, session: Session = Depends(get_session)):
    result = Source.delete(session, id)
    return result

@router.get("/all", response_model=List[Source])
async def read_all(
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
        ):
    result = Source.read_all(session, skip, limit)
    return result
