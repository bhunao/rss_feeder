import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src import routers
from src.core.config import templates
from src.core.dependencies import lifespan


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="src/static/"), name="static")

for name in dir(routers):
    if name.startswith("__") or name == "database_test":
        continue
    _router = getattr(routers, name)
    app.include_router(_router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> str:
    return templates.TemplateResponse(
        "base.html", {"request": request}, block_name=None
    )
