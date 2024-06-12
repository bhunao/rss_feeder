import logging

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.config import templates
from src.core.database import get_session
from src.core.config import templates
from src.models import Article, ArticleSchema, Source
from src.database import ServiceDatabase


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

    db = ServiceDatabase(session)
    for s in db.read_all_sources():
        logger.debug(f"created background task: REFRESH_SOURCE: '{s.title}'")
        bg_tasks.add_task(db.refresh_articles, s.id)

    result = ServiceDatabase(session).get_lasts()
    return templates.TemplateResponse(
            "pages/articles_by_date.html", {"request": request, "items": result}, block_name=None
    )

@router.get("/by_source")
async def articles_by_source(
        request: Request,
        bg_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
        ) -> str:
    db = ServiceDatabase(session)
    for s in db.read_all_sources():
        logger.debug(f"created background task: REFRESH_SOURCE: '{s.title}'")
        bg_tasks.add_task(db.refresh_articles, s.id)

    result_dict: Dict[str, Article] = dict()
    for source in db.read_all(Source):
        tup = source.id, source.title, source.subtitle
        result_dict[tup] = db.get_by_source(source)

    return templates.TemplateResponse(
            "pages/articles_by_source.html", {"request": request, "items": result_dict}, block_name=None
    )
