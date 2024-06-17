from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Field, Relationship
from sqlalchemy import UniqueConstraint, Column, String

from src.core.database import SQLModel

from typing import Optional
from datetime import date

from sqlmodel import Field, SQLModel


class SourceSchema(SQLModel):
    title: str
    subtitle: str
    url: str
    language: str


class Source(SQLModel, table=True):
    __tablename__  = "sources"

    id: int = Field(default=None, primary_key=True)
    title: str
    subtitle: str
    url: str = Field(sa_column=Column("url", String, unique=True))
    language: str
    date_created: datetime = Field(default_factory=datetime.now)
    articles: list["Article"] = Relationship(back_populates="source")

class ExampleModelSchema(SQLModel):
    name: str
    favorite_number: int
    date: date


class ExampleModel(SQLModel, table=True):
    __tablename__ = "example_model"

    id: Optional[int] = Field(nullable=False, primary_key=True)
    name: str
    favorite_number: int
    date: date


class ArticleSchema(SQLModel):
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str


class Article(SQLModel, table=True):
    __tablename__ = "articles"

    id: int = Field(default=None, primary_key=True)
    source_id: int | None = Field(default=None, foreign_key="sources.id")
    title: str
    date_published: datetime
    summary: str
    image_url: str

    source: Source | None = Relationship(back_populates="articles")


class SubscriptionSchema(SQLModel):
    user_id: int
    source_id: int


class Subscription(SQLModel, table=True):
    __tablename__  = "subscriptions"

    id: Optional[int] = Field(nullable=False, primary_key=True)
    user_id: int
    source_id: int


class User(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None
