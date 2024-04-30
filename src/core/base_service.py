from sqlalchemy.exc import OperationalError
import logging

from functools import wraps
from typing import Generic, List, TypeVar, Union, Callable

from fastapi import HTTPException
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel, Session, select


logger = logging.getLogger(__name__)

M = TypeVar("M", bound=SQLModel)


def handle_database_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as ex:
            logger.error(f"database connection error {ex}")
            return []

    return wrapper


class BaseService(Generic[M]):
    def __init__(self, model: M, session: Session) -> None:
        self.model: M = model
        self.session = session
        logger.info(f"BaseModule created with model {model.__name__}")

    def _update_model(self, model: M, update: M) -> None:
        for key, val in update:
            model.__setattr__(key, val)

    @handle_database_errors
    def create(self, new_entry: M) -> M:
        db_entry = self.model.from_orm(new_entry)
        self._update_model(db_entry, new_entry)
        self.session.add(db_entry)
        self.session.commit()
        self.session.refresh(db_entry)
        logger.debug(f"new entry added to {self.model.__name__}")
        return db_entry

    @handle_database_errors
    def read(self, id: Union[int, str]) -> M:
        db_entry = self.session.get(self.model, id)
        if db_entry is None:
            raise HTTPException(status_code=404, detail="Item not found")
        self._validate_not_empty(db_entry)
        logger.debug(f"found {self.model.__name__} with id {db_entry.id}")
        return db_entry

    @handle_database_errors
    def read_all(self, skip: int = 0, limit: int = 100) -> List[M]:
        query = select(self.model).offset(skip).limit(limit)
        result = self.session.exec(query).all()
        logger.debug(f"read {len(result)} lines from {skip} to {skip+limit}")
        return result

    @handle_database_errors
    def update(self, id: int, schema: M) -> M:
        db_entry = self.session.get(self.model, id)
        self._validate_not_empty(db_entry)
        self._update_model(db_entry, schema)
        self.session.add(db_entry)
        self.session.commit()
        self.session.refresh(db_entry)
        logger.debug(f"{self.model.__name__} with id {id} updated")
        return db_entry

    @handle_database_errors
    def delete(self, id: int) -> bool:
        db_entry = self.session.get(self.model, id)
        self._validate_not_empty(db_entry)
        self.session.delete(db_entry)
        self.session.commit()
        logger.debug(f"{self.model.__name__} with id {id} deleted")
        return True

    @handle_database_errors
    def search(self, *where: BinaryExpression) -> List[M]:
        query = select(self.model).where(*where)
        result = self.session.exec(query).all()
        logger.debug(f"search found {len(result)} lines")
        return result

    def _validate_not_empty(self, db_entry):
        if db_entry is None:
            logger.debug(f"{self.model.__name__} not found")
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found"
            )
