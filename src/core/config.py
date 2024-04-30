from starlette.config import Config
from jinja2_fragments.fastapi import Jinja2Blocks

config = Config(".env")
templates = Jinja2Blocks(directory="src/template/")
