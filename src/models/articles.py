from datetime import datetime

from sqlmodel import Field, SQLModel, Session



class Article(SQLModel, table=True):
    __tablename__ = "articles"

    id: int = Field(default=None, primary_key=True)
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str


class ArticleSchema(SQLModel):
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str
