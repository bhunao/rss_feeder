import logging


from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel


class Source(SQLModel, table=True):
    __tablename__ = "sources"

    id: int = Field(default=None, primary_key=True)
    title: str
    subtitle: str
    url: str
    language: str


class SourceSchema(SQLModel):
    title: str
    subtitle: str
    url: str
    language: str

