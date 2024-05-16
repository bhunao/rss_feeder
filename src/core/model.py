from __future__ import annotations

import logging

from typing import Generic, List, TypeVar, Union, Any

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel, Session, select

from src.core.database import get_session
from src.core.dependencies import handle_database_errors


logger = logging.getLogger(__name__)
ITEM_NOT_FOUND = HTTPException(status_code=404, detail="Item not found")


class DatabaseModel(SQLModel):
    __router__ = None
    __schema__ = None

    def __new__(cls, *args: Any, **kwargs: Any) -> DatabaseModel:
        cls.__router__ = APIRouter(
                prefix=f"/{cls.__tablename__}",
                tags=[cls.__tablename__]
                )
        new_object = super().__new__(cls)
        return new_object

    def _update_model(self, model: SQLModel, values: SQLModel) -> None:
        for key, val in values:
            if key.startswith("_"):
                continue
            model.__setattr__(key, val)

    @handle_database_errors
    def create(cls, session: Session, record: SQLModel) -> DatabaseModel:
        _new_record = cls.from_orm(record)
        session.add(_new_record)
        session.commit()
        session.refresh(_new_record)
        logger.debug(f"new entry added to {cls.__name__}")
        return _new_record

    @handle_database_errors
    def read(self, session: Session, id: Union[int, str]) -> DatabaseModel:
        record = session.get(self.__class__, id)
        if record is None:
            raise ITEM_NOT_FOUND
        self._validate_not_empty(record)
        logger.debug(f"found {self.__name__} with id {record.id}")
        return record

    @handle_database_errors
    def read_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[DatabaseModel]:
        query = select(self.__class__).offset(skip).limit(limit)
        result = session.exec(query).all()
        logger.debug(f"read {len(result)} lines from {skip} to {skip+limit}")
        return result

    @handle_database_errors
    def update(self, session: Session, updated_record: SQLModel) -> DatabaseModel:
        record = session.get(self.__class__, updated_record.id)
        self._validate_not_empty(record)
        logger.info(f"{self.__name__} record found {record}")
        self._update_model(model=record, values=updated_record)
        session.add(record)
        session.commit()
        session.refresh(record)
        logger.debug(f"{self.__name__} with id {id} updated")
        return record

    @handle_database_errors
    def delete(self, session: Session, id: int) -> SQLModel:
        logger.warning(f"class == {self.__class__}")
        record = session.get(self.__class__, id)
        logger.warning(f"alguma coisa aconteceu aqui {id=}")
        if record is None:
            logger.warning(f"alguma coisa aconteceu aqui {id=}")
            logger.info(f"No row with id '{id}' found in {self.__class__}")
            raise HTTPException(status_code=404, detail="Item not found")
        self._validate_not_empty(record)
        session.delete(record)
        session.commit()
        logger.debug(f"{self.__name__} with id {id} deleted")
        return record

    @handle_database_errors
    def search(self, session: Session, *where: BinaryExpression) -> List[DatabaseModel]:
        query = select(self.__class__).where(*where)
        result = session.exec(query).all()
        logger.debug(f"search found {len(result)} lines")
        return result

    def _validate_not_empty(self, record):
        if record is None:
            logger.debug(f"{self.__name__} not found")
            raise HTTPException(
                status_code=404, detail=f"{self.__name__} not found"
            )
