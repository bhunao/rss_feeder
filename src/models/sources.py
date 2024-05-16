from sqlmodel import Field, Session, select

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

    @classmethod
    def create(cls, session: Session, record: SQLModel) -> DatabaseModel:
        query = select(cls).filter(
                Source.title == record.title,
                Source.url == record.url,
                )
        result = session.exec(query).all()
        if len(result) == 0:
            return cls()
        return super(Source, cls).create(session, record)
