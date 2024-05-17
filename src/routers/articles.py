import logging

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Field, Session

from src.core.base_service import BaseService
from src.core.config import templates
from src.core.database import get_session
from src.core.config import templates
from src.models.articles import Article, ArticleSchema


logger = logging.getLogger(__name__)
router = Article.create_router()

@router.get("/trena", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_session)) -> str:
    result = Article.read_all(session)
    return templates.TemplateResponse(
            "cards/list.html", {"request": request, "items": result}, block_name=None
    )

@router.post("/")
async def create(record: ArticleSchema, session: Session = Depends(get_session)):
    result = Article.create(session, record)
    return result

@router.get("/")
async def read(id: int, session: Session = Depends(get_session)):
    result = Article.read(session, id)
    return result

@router.post("/update")
async def update(record: Article, session: Session = Depends(get_session)):
    result = Article.update(session, record)
    return result

@router.delete("/")
async def delete(id: int, session: Session = Depends(get_session)):
    result = Article.delete(session, id)
    return result

@router.get("/all", response_model=List[Article])
async def read_all(
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
        ):
    result = Article.read_all(session, skip, limit)
    return result
