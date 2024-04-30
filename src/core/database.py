import logging

from typing import Generator

from sqlmodel import SQLModel
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

from sqlmodel import create_engine
from sqlmodel import Session


config = Config(".env")
logging.basicConfig(
    format="[%(asctime)s | %(levelname)s | %(name)s.%(funcName)s]: %(message)s"
)

POSTGRES_USER = config("POSTGRES_USER", default="USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="default_db")
DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
)

postgre_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(postgre_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
