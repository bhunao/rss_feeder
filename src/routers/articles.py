import logging

from fastapi import APIRouter, Depends, Request
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
async def home(request: Request, session: Session = Depends(get_session)) -> str:
    result = ServiceDatabase(session).get_lasts()
    return templates.TemplateResponse(
            "pages/articles_by_date.html", {"request": request, "items": result}, block_name=None
    )

@router.get("/by_source")
async def articles_by_source(request: Request, session: Session = Depends(get_session)) -> str:
    database = ServiceDatabase(session)
    result_dict: Dict[str, Article] = dict()
    for source in database.read_all(Source):
        tup = source.id, source.title, source.subtitle
        result_dict[tup] = database.get_by_source(source)

    return templates.TemplateResponse(
            "pages/articles_by_source.html", {"request": request, "items": result_dict}, block_name=None
    )
