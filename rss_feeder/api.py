from feedparser import parse
from fastapi.responses import HTMLResponse
from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Blocks(directory="template/")

primetime = "UCUyeluBRhGPCW4rPe_UvBZQ"
tiojoao = "UC7-Pp09PJX_SYP9oyMzUAtg"


def get_youtube_feed(channel_id: str):
    feed = parse(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    print(feed.keys())
    print(feed['entries'][0].keys())
    return feed


@app.get("/", response_class=HTMLResponse)
async def get_all_notes(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "feed": get_youtube_feed(primetime)
        },
        block_name=None
    )


@app.get("/explorer", response_class=HTMLResponse)
async def explorer(request: Request):
    return templates.TemplateResponse(
        "explorer.html",
        {
            "request": request,
            "feed": get_youtube_feed(primetime)
        },
        block_name=None
    )
