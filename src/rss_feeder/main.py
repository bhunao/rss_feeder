from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.dependencies import lifespan
from routers.news.router import router as news
from routers.users.router import router as users


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(news)
app.include_router(users)


@app.get("/")
async def home() -> str:
    return "HOME"
