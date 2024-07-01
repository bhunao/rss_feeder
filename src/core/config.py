import logging

from databases import DatabaseURL
from jinja2_fragments.fastapi import Jinja2Blocks
from starlette.config import Config
from starlette.datastructures import Secret


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s | %(levelname)s | %(name)s.%(funcName)s]: %(message)s"
)
config = Config(".env")
templates = Jinja2Blocks(directory="src/template/")

SECRET_KEY = config("SECRET_KEY", default="DEFAULT_KEY")
ALGORITHM = config("ALGORITHM", cast=str, default="HS256")


POSTGRES_USER = config("POSTGRES_USER", default="USER", cast=str)
POSTGRES_PASSWORD = config(
    "POSTGRES_PASSWORD", default="PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="default_db")
DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
)
