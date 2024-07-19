from collections.abc import Generator
import logging

from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import rss


def lifespan(app: FastAPI) -> Generator[None, None, None]:
    logging.info("Starting application lifespan...")
    assert app
    yield
    logging.info("Finishing application lifespan...")


app = FastAPI(
    title=settings.APP_TITLE,
    # lifespan=lifespan
)
app.include_router(rss.router)


@app.get("/")
async def health_check():
    return True
