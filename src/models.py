from datetime import date
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.core.database import MODEL


class SourceSchema(MODEL):
    title: str
    subtitle: str
    url: str
    language: str


class Source(MODEL, table=True):
    __tablename__ = "sources"

    id: int = Field(default=None, primary_key=True)
    title: str
    subtitle: str
    url: str = Field(sa_column=Column("url", String, unique=True))
    language: str
    date_created: datetime = Field(default_factory=datetime.now)
    articles: list["Article"] = Relationship(back_populates="source")


class ExampleModelSchema(MODEL):
    name: str
    favorite_number: int
    date: date


class ExampleModel(MODEL, table=True):
    __tablename__ = "example_model"

    id: Optional[int] = Field(nullable=False, primary_key=True)
    name: str
    favorite_number: int
    date: date


class ArticleSchema(MODEL):
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str


class Article(MODEL, table=True):
    __tablename__ = "articles"

    id: int = Field(default=None, primary_key=True)
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str

    source: Source | None = Relationship(back_populates="articles")


class SubscriptionSchema(MODEL):
    user_id: int
    source_id: int


class Subscription(MODEL, table=True):
    __tablename__ = "subscriptions"

    id: Optional[int] = Field(nullable=False, primary_key=True)
    user_id: int
    source_id: int


class User(MODEL, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False


class Token(MODEL):
    access_token: str
    token_type: str


class TokenData(MODEL):
    username: Optional[str] = None
