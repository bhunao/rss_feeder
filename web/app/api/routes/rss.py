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


@ router.post("/parse_from/url")
async def parse_from_url(url: UrlSchema):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url.url)
    if isinstance(rss, Exception):
        raise S400_INVALID_URL
    return rss


@ router.get("/tst",
             response_class=HTMLResponse,
             # responses={
             #     200: {
             #         "content": {"text/html": {}},
             #         "description": "Return the JSON item or HTML.",
             #     }
             # }
             )
async def tst(request: Request, a: str = "empty"):
    return templates.TemplateResponse(request, "index.html", context={"a": a})
    # if len(a) < 5:

    #     return templates.TemplateResponse(request, "index.html", context={"a": 5})
    # else:
    #     return JSONResponse({"algo": a})
