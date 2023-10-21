from dateutil import parser
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from feedparser import parse
from jinja2_fragments.fastapi import Jinja2Blocks


app = FastAPI()
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Blocks(directory="template/")

youtube = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
primetime = youtube.format("UCUyeluBRhGPCW4rPe_UvBZQ")
tiojoao = youtube.format("UC7-Pp09PJX_SYP9oyMzUAtg")
crunchy_anime = "https://feeds.feedburner.com/crunchyroll/rss/anime"
anime_news = "https://www.animenewsnetwork.com/all/rss.xml?ann-edition=us"
blind_tech = "https://www.teamblind.com/rss/Tech/rss"


def get_youtube_feed(url: str):
    feed = parse(url)
    return feed


@app.get("/", response_class=HTMLResponse)
async def get_all_notes(request: Request):
    coiso = get_youtube_feed(blind_tech)
    coiso['entries'] += get_youtube_feed(primetime)["entries"]
    coiso['entries'] += get_youtube_feed(tiojoao)["entries"]
    coiso['entries'] += get_youtube_feed(anime_news)["entries"]

    for c in coiso['entries']:
        v = c['published_parsed']
        treco = f"{v.tm_year}-{v.tm_mon}-{v.tm_mday}-{v.tm_hour}-{v.tm_min}-{v.tm_sec}"
        c['published_parsed'] = treco

    coiso['entries'].sort(key=lambda x: x['published_parsed'], reverse=True)

    print(coiso['entries'][0]['published_parsed'])
    print(type(coiso['entries'][0]['published_parsed']))
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "feed": coiso
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
