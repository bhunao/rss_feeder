import logging

import feedparser
import requests

from typing import List
from datetime import datetime
from time import mktime

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.database import get_session
from src.core.config import templates
from src.models import Source, SourceSchema
from src.models import Article, ArticleSchema
from src.services.sources import SourceService
from src.services.articles import ArticleService
from src.core.errors import HTTP400_ALREADY_EXISTS

from src.feed_parser import parse_rss_from_url


NAME = "sources"
PREFIX = f"/{NAME}"
TAGS = [NAME]

router = APIRouter(prefix=PREFIX, tags=TAGS)
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def home(
        request: Request,
        session: Session = Depends(get_session),
        ) -> str:
    result = SourceService(session).read_all()
    return templates.TemplateResponse(
            "forms/new_source.html", {"request": request, "items": result}, block_name=None
            )

@router.post("/new")
async def create(url: str = Form(...), session: Session = Depends(get_session)):
    parsed_rss = parse_rss_from_url(url)

    source_service = SourceService(session)
    article_service = ArticleService(session)

    record = source_service.from_rss(parsed_rss["feed"])
    if record is None:
        return HTTP400_ALREADY_EXISTS.detail

    article_service.articles_from_source(record)
    return record

@router.get("/refresh")
async def refresh_source(id: int, session: Session = Depends(get_session)):
    source_service = SourceService(session)
    article_service = ArticleService(session)
    record = source_service.read(id)
    article_service.articles_from_source(record)
    return "true"
# 
# @router.get("/", response_model=Source)
# async def read(id: int, session: Session = Depends(get_session)):
    # result = SourceService(session).read(id)
    # return result
# 
# @router.post("/update", response_model=Source)
# async def update(record: Source, session: Session = Depends(get_session)):
    # result = SourceService(session).update(record)
    # return result
# 
# @router.delete("/", response_model=Source)
# async def delete(id: int, session: Session = Depends(get_session)):
    # result = SourceService(session).delete(id)
    # return result
# 
# @router.get("/all", response_model=List[Source])
# async def read_all(
        # session: Session = Depends(get_session),
        # skip: int = 0,
        # limit: int = 100
        # ):
    # result = SourceService(session).read_all(skip, limit)
    # return result
