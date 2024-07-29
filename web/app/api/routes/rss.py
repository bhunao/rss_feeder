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


html_template = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body class="container align-content-center p-5">
        <h1>This is a heading</h1>
        <p>This is a paragraph.</p>
        <h3 class="display-3">{content}</h3>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>\
""".format


@router.get("/tst",
            responses={
                200: {
                    "content": {"text/html": {}},
                    "description": "Return the JSON item or HTML.",
                }
            })
async def tst(a: str = "empty"):
    if len(a) < 5:
        html = html_template(content=a)
        return HTMLResponse(html)
    else:
        return JSONResponse({"algo": a})
