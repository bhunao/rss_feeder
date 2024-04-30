import logging

from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Field, SQLModel, Session

from src.core.base_service import BaseService
from src.core.database import get_session
from src.core.config import templates


class News(SQLModel, table=True):
    __tablename__ = "news"
    id: int = Field(default=None, primary_key=True)
    title: str
    content: Optional[str] = None


class NewsSchema(SQLModel):
    __tablename__ = "news"
    title: str
    content: Optional[str] = None


MODEL = News
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news", tags=["news"])


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
async def create(post: NewsSchema, session: Session = Depends(get_session)):
    print(post)
    result = BaseService(MODEL, session).create(post)
    return result
