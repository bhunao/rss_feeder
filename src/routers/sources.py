import logging

import validators

from fastapi import APIRouter, Depends, Request, Form, Response
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.database import get_session
from src.core.config import templates
from src.models import Source, SourceSchema
from src.models import Article, ArticleSchema
from src.core.errors import HTTP400_ALREADY_EXISTS
from src.database import ServiceDatabase, get_rss


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
    items = ServiceDatabase(session).read_all_sources()
    page_data = {
            "request": request,
            "items": items,
            "alert_type": "danger",
            "msg": ""
            }
    return templates.TemplateResponse(
            "pages/sources.html",
            {"request": request, "items": items},
            block_name=None
            )

@router.post("/new", response_model=str)
async def create(
        request: Request,
        url: str = Form(...),
        session: Session = Depends(get_session)
        ):
    if not url.startswith("http"):
        url = "http://" + url

    is_url_valid = validators.url(url)
    database = ServiceDatabase(session)
    if not is_url_valid:
        items = database.read_all_sources()
        msg = f"Invalid URL: '{is_url_valid.args[1]['value']}'"
        page_data = {
                "request": request,
                "items": items,
                "alert_type": "danger",
                "msg": msg
                }
        return templates.TemplateResponse(
                "tables/sources.html",
                page_data,
                block_name="sources_table"
                )

    parsed_rss = get_rss(url)

    record = database.source_from_rss(url, parsed_rss["feed"])
    if record is None:
        items = database.read_all_sources()
        msg = HTTP400_ALREADY_EXISTS.detail
        page_data = {
                "request": request,
                "items": items,
                "alert_type": "warning",
                "msg": msg
                }
        return templates.TemplateResponse(
                "tables/sources.html", page_data, block_name="sources_table"
                )

    database.refresh_articles(record.id, parsed_rss['entries'])
    items = database.read_all_sources()
    msg = f"'{record.title}' created as a news Source."
    page_data = {
            "request": request,
            "items": items,
            "alert_type": "info",
            "msg": msg
            }
    return templates.TemplateResponse(
            "tables/sources.html", page_data, block_name="sources_table"
            )

@router.get("/refresh")
async def refresh_source(id: int, session: Session = Depends(get_session)):
    ServiceDatabase(session).refresh_articles(source_id=id)
    return "true"

@router.delete("/")
async def delete(id: int, session: Session = Depends(get_session)):
    ServiceDatabase(session).delete(Source, id)
    return Response()
