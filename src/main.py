from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.core.config import templates
from src.core.dependencies import lifespan
from src.routers import news, news_source, users


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static/"), name="static")
app.include_router(news)
app.include_router(news_source)
app.include_router(users)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> str:
    print("algo6")
    return templates.TemplateResponse(
        "base.html", {"request": request}, block_name=None
    )
