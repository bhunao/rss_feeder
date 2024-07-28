from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import SQLModel

from app.models import RssSchema
from app.errors import S400_INVALID_URL


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://techcrunch.com/feed/"


class UrlSchema(SQLModel):
    url: str = EX_URL


@router.post("/parse_from/url")
async def parse_from_url(url: UrlSchema):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url.url)
    if isinstance(rss, Exception):
        raise S400_INVALID_URL
    return rss


html_template = "<html><div><h1>{content}</h1></div></html>".format


@router.get("/tst",
            responses={
                200: {
                    "content": {"text/html": {}},
                    "description": "Return the JSON item or HTML.",
                }
            })
async def tst(a: int = 0):
    if a == 0:
        return HTMLResponse(html_template(content=a))
    else:
        return JSONResponse({"algo": a})
