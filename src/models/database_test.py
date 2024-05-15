import logging

from typing import Optional
from datetime import date

from sqlmodel import Field

from src.core.database import SQLModel
from src.core.model import DatabaseModel


class ExampleModelSchema(SQLModel):
    name: str
    favorite_number: int
    date: date


class ExampleModel(DatabaseModel, table=True):
    __name__ = "example_model"
    __tablename__ = __name__
    __schema__ = ExampleModelSchema

    id: Optional[int] = Field(nullable=False, primary_key=True)
    name: str
    favorite_number: int
    date: date

