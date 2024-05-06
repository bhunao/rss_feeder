from datetime import datetime

from sqlmodel import Field, SQLModel, Session



class News(SQLModel, table=True):
    __tablename__ = "news"

    id: int = Field(default=None, primary_key=True)
    source_id: int | None = Field(default=None, foreign_key="news_sources.id")
    # tags: # TODO
    link: str
    title: str
    summary: str
    published: datetime


class NewsSchema(SQLModel):
    source_id: int | None = Field(default=None, foreign_key="news_sources.id")
    link: str
    title: str
    summary: str
    published: datetime
