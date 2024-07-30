import logging
from typing import Annotated, Union
from fastapi import APIRouter, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import SQLModel

from app.models import RssSchema
from app.errors import S400_INVALID_URL
from app.core.config import settings


templates = settings.TEMPLATES


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://techcrunch.com/feed/"


class UrlSchema(SQLModel):
    url: str = EX_URL


@ router.post("/parse_from/url")
async def parse_from_url(url: str = EX_URL):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url)
    if isinstance(rss, Exception):
        raise S400_INVALID_URL
    return rss

multi_responses = {
    200: {
        "content": {"application/json": {}},
        "description": "Return the JSON item or HTML.",
    }
}


@ router.get("/tst", response_class=HTMLResponse, responses=multi_responses)
async def tst(request: Request, a: str = "empty"):
    logging.warning("".center(30, "="))
    accept_value = request.headers.get("accept", None)
    assert accept_value
    if "application/json" in accept_value:
        return JSONResponse({"a": a})
    return templates.TemplateResponse(request, "index.html", context={"a": a})
