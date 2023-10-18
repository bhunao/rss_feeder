from feedparser import parse
from fastapi.responses import HTMLResponse
from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Blocks(directory="template/")

youtube = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
primetime = youtube.format("UCUyeluBRhGPCW4rPe_UvBZQ")
tiojoao = youtube.format("UC7-Pp09PJX_SYP9oyMzUAtg")
crunchy_anime = "https://feeds.feedburner.com/crunchyroll/rss/anime"
anime_news = "https://www.animenewsnetwork.com/all/rss.xml?ann-edition=us"


def get_youtube_feed(url: str):
    feed = parse(url)
    print(feed.keys())
    print(feed['entries'][0].keys())
    return feed


@app.get("/", response_class=HTMLResponse)
async def get_all_notes(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "feed": get_youtube_feed(crunchy_anime)
        },
        block_name=None
    )


@app.get("/explorer", response_class=HTMLResponse)
async def explorer(request: Request):
    return templates.TemplateResponse(
        "explorer.html",
        {
            "request": request,
            "feed": get_youtube_feed(crunchy_anime)
        },
        block_name=None
    )
