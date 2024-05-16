import logging
from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Field, Session, select

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

    @classmethod
    def create(cls, session: Session, record: SQLModel) -> DatabaseModel:
        query = select(cls.__class__).filter(
                Article.title == record.title,
                Article.source_id == record.source_id,
                )
        result = session.exec(query).all()
        logging.warning(f"algo = {record}")
        if len(result) == 0:
            return cls()
        return super(Article, cls).create(session, record)
        print("=====================================")
        logging.warning(f"record created: {new_record}")
