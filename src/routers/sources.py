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
    result = ServiceDatabase(session).read_all(Source)
    return templates.TemplateResponse(
            "pages/sources.html", {"request": request, "items": result}, block_name=None
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
    if not is_url_valid:
        msg = f"Invalid URL: '{is_url_valid.args[1]['value']}'"
        return templates.TemplateResponse(
                "components/alert.html",
                {"request": request, "alert_type": "danger", "msg": msg},
                block_name=None
                )

    parsed_rss = get_rss(url)
    database = ServiceDatabase(session)

    record = database.source_from_rss(url, parsed_rss["feed"])
    if record is None:
        msg = HTTP400_ALREADY_EXISTS.detail
        return templates.TemplateResponse(
                "components/alert.html",
                {"request": request, "alert_type": "warning", "msg": msg},
                block_name=None
                )

    database.refresh_articles(record.id, parsed_rss['entries'])
    msg = f"'{record.title}' created as a news Source."
    return templates.TemplateResponse(
            "components/alert.html",
            {"request": request, "alert_type": "info", "msg": msg},
            block_name=None
            )

@router.get("/refresh")
async def refresh_source(id: int, session: Session = Depends(get_session)):
    ServiceDatabase(session).refresh_articles(source_id=id)
    return "true"

@router.delete("/")
async def delete(id: int, session: Session = Depends(get_session)):
    ServiceDatabase(session).delete(Source, id)
    return Response()
