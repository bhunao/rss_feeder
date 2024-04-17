import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from . import database


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    assert app is not None
    yield
    print("closing")
