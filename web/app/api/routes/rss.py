from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import SQLModel

from app.models import RssSchema
from app.errors import S400_INVALID_URL


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"


class UrlSchema(SQLModel):
    url: str = EX_URL


@router.post("/parse_from/url")
async def parse_from_url(url: UrlSchema):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url.url)
    if isinstance(rss, Exception):
        raise S400_INVALID_URL
    return rss


@router.get("/tst",
            responses={
                200: {
                    "content": {"text/html": {}},
                    "description": "Return the JSON item or HTML.",
                }
            })
async def tst(a: int = 0):
    if a == 0:
        return HTMLResponse("<html><div><h1>titulo texto</h1></div></html>")
    else:
        return JSONResponse({"algo": 1})
