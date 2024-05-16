from sqlmodel import Field

from src.core.database import SQLModel
from src.core.model import DatabaseModel


class SourceSchema(SQLModel):
    title: str
    subtitle: str
    url: str
    language: str


class Source(DatabaseModel, table=True):
    __name__ = "sources"
    __tablename__ = __name__
    __schema__ = SourceSchema

    id: int = Field(default=None, primary_key=True)
    title: str
    subtitle: str
    url: str
    language: str
