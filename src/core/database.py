import logging

from typing import Generator, TypeVar, List

from sqlmodel import SQLModel, select
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

from sqlmodel import create_engine
from sqlmodel import Session

from src.core.config import config


logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s | %(levelname)s | %(name)s.%(funcName)s]: %(message)s"
        )

POSTGRES_USER = config("POSTGRES_USER", default="USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="default_db")
DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
)

postgre_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(postgre_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


class Database:
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, record: SQLModel, table: SQLModel = None) -> SQLModel:
        table = table if table else record.__class__

        new_record = table.model_validate(record, from_attributes=True)
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        return new_record

    def read(self, table: SQLModel, id: int) -> SQLModel | None:
        db_record = self.session.get(table, id)
        return db_record

    def read_all(self, table: SQLModel = None, skip: int = 0, limit: int = 100) -> List[SQLModel]:
        query = select(table).offset(skip).limit(limit)
        result = self.session.exec(query).all()
        return result

    def update(self, record: SQLModel, table: SQLModel = None) -> SQLModel | None:
        table = table if table else record.__class__
        db_record = self.session.get(table, record.id)
        if db_record is None:
            return None
        db_record.sqlmodel_update(record)
        self.session.add(db_record)
        self.session.commit()
        self.session.refresh(db_record)
        return db_record

    def delete(self, table: SQLModel, id: int) -> SQLModel | None:
        db_record = self.session.get(table, id)
        if db_record is None:
            return None
        self.session.delete(db_record)
        self.session.commit()
        return db_record
