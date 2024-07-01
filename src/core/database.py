import logging
from typing import TypeVar

from typing import Generator

from sqlmodel import SQLModel as MODEL
from sqlmodel import select

from sqlmodel import create_engine
from sqlmodel import Session

from src.core.config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_DB,
    POSTGRES_PORT,
)


logger = logging.getLogger(__name__)

postgre_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(postgre_url, echo=False)


def create_db_and_tables():
    MODEL.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


MODEL_T = TypeVar("MODEL_T", bound=MODEL)


class BaseDatabase:
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, record: MODEL, table: MODEL = None) -> MODEL:
        table = table if table else record.__class__

        new_record = table.model_validate(record, from_attributes=True)
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        logger.debug(
            f"Record {table.__name__}(id={new_record.id}) created.")
        return new_record

    def read(self, table: MODEL_T, id: int) -> MODEL_T | None:
        db_record = self.session.get(table, id)
        return db_record

    def read_all(
            self,
            table: MODEL = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[MODEL]:
        query = select(table).offset(skip).limit(limit)
        result = self.session.exec(query).all()
        return result

    def update(self, record: MODEL, table: MODEL = None) -> MODEL | None:
        table = table if table else record.__class__
        db_record = self.session.get(table, record.id)
        if db_record is None:
            return None
        db_record.sqlmodel_update(record)
        self.session.add(db_record)
        self.session.commit()
        self.session.refresh(db_record)
        return db_record

    def delete(self, table: MODEL, id: int) -> MODEL | None:
        db_record = self.session.get(table, id)
        if db_record is None:
            return None
        self.session.delete(db_record)
        self.session.commit()
        logger.debug(
            f"Record {table.__name__}(id={db_record.id}) deleted.")
        return db_record
