from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.dependencies import lifespan
from src.routers.news.router import router as news
from src.routers.users.router import router as users


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static/"), name="static")
app.include_router(news)
app.include_router(users)


@app.get("/")
async def home() -> str:
    print("algo3")
    return "HOME"
