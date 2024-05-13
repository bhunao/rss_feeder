from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.core.config import templates
from src.core.dependencies import lifespan
from src.routers import routers_list


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static/"), name="static")

for router in routers_list:
    app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> str:
    return templates.TemplateResponse(
        "base.html", {"request": request}, block_name=None
    )
