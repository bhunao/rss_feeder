from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from app.feed_parser import RssSchema


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"


@router.post("/parse_from/url")
async def parse_from_url(url: str = EX_URL):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url)
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
