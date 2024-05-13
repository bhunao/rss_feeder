import logging

from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Field, Session

from src.core.base_service import BaseService
from src.core.database import get_session
from src.core.config import templates
from src.models.articles import Article, ArticleSchema

MODEL = Article
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/articles", tags=["articles"])


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
async def create(post: ArticleSchema, session: Session = Depends(get_session)):
    result = BaseService(MODEL, session).create(post)
    return result
