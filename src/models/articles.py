from datetime import datetime

from sqlmodel import Field

from src.core.database import SQLModel
from src.core.model import DatabaseModel


class ArticleSchema(SQLModel):
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str


class Article(DatabaseModel, table=True):
    __name__ = "articles"
    __tablename__ = __name__
    __schema__ = ArticleSchema

    id: int = Field(default=None, primary_key=True)
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str
