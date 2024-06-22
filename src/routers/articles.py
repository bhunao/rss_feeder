import logging

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.config import templates
from src.core.database import get_session
from src.database import Database
from src.models import Source


NAME = "articles"
PREFIX = f"/{NAME}"
TAGS = [NAME]

router = APIRouter(prefix=PREFIX, tags=TAGS)
logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
async def home(
        request: Request,
        bg_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
) -> str:
    db = Database(session)
    for s in db.read_all_sources():
        logger.info(f"created background task: REFRESH_SOURCE: '{s.title}'")
        bg_tasks.add_task(db.refresh_articles, s.id)

    result = Database(session).get_lasts()
    title = "Articles Ordered by Date"
    return templates.TemplateResponse(
        "pages/articles_by_date.html",
        {"request": request, "items": result, "title": title},
        block_name=None,
    )


@router.get("/by_source")
async def articles_by_source(
        request: Request,
        bg_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
) -> str:
    db = Database(session)
    source_list = db.read_all_sources()

    return templates.TemplateResponse(
        "pages/articles_by_source.html",
        {"request": request, "items": source_list},
        block_name=None,
    )


@router.get("/{id}")
async def source_articles(
    id: int,
    request: Request,
    bg_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
) -> str:
    db = Database(session)
    source = db.read(Source, id)
    items = source.articles if source else []
    title = f"{source.title} articles"
    return templates.TemplateResponse(
        "pages/articles.html",
        {"request": request, "items": items, "title": title},
        block_name=None,
    )
