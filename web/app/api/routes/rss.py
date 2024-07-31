from fastapi import APIRouter, Request
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


multi_responses = {
    200: {
        "content": {"text/html": {}},
        "description": "Returns the JSON or HTML.",
    }
}


@ router.get("/parse_from", responses=multi_responses)
async def parse_from_url(request: Request, url: str = EX_URL):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url)
    context = {"rss": rss}
    accept_values = request.headers.get("accept", None)
    assert accept_values
    if "application/json" in accept_values:
        if isinstance(rss, Exception):
            raise S400_INVALID_URL
        return rss

    assert not isinstance(
        rss, Exception), "Rss is not RssSchema, is an exception."
    return templates.TemplateResponse(request, "index.html", context=context)
