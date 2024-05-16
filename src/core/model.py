from __future__ import annotations

import logging

from typing import Generic, List, TypeVar, Union, Any

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import Session, select

from src.core.database import get_session, SQLModel
from src.core.dependencies import handle_database_errors
from src.core.errors import HTTP404_ITEM_NOT_FOUND


logger = logging.getLogger(__name__)


class DatabaseModel(SQLModel):
    __router__ = None
    __schema__ = None

    @classmethod
    def create_router(cls) -> APIRouter:
        cls.__router__ = APIRouter(
                prefix=f"/{cls.__tablename__}",
                tags=[cls.__tablename__]
                )
        return cls.__router__

    def __new__(cls, *args: Any, **kwargs: Any) -> DatabaseModel:
        cls.__router__ = APIRouter(
                prefix=f"/{cls.__tablename__}",
                tags=[cls.__tablename__]
                )
        new_object = super().__new__(cls)
        return new_object

    @staticmethod
    def _update_model(model: SQLModel, values: SQLModel) -> None:
        for key, val in values:
            if key.startswith("_"):
                continue
            model.__setattr__(key, val)

    @classmethod
    @handle_database_errors
    def create(cls, session: Session, record: SQLModel) -> DatabaseModel:
        _new_record = cls.from_orm(record)
        session.add(_new_record)
        session.commit()
        session.refresh(_new_record)
        logger.debug(f"new entry added to {cls.__name__}")
        return _new_record

    @classmethod
    @handle_database_errors
    def read(cls, session: Session, id: Union[int, str]) -> DatabaseModel:
        record = session.get(cls, id)
        if record is None:
            raise HTTP04_ITEM_NOT_FOUND
        logger.debug(f"found {cls.__name__} with id {record.id}")
        return record

    @classmethod
    @handle_database_errors
    def read_all(cls, session: Session, skip: int = 0, limit: int = 100) -> List[DatabaseModel]:
        query = select(cls).offset(skip).limit(limit)
        result = session.exec(query).all()
        logger.debug(f"read {len(result)} lines from {skip} to {skip+limit}")
        return result

    @classmethod
    @handle_database_errors
    def update(cls, session: Session, updated_record: SQLModel) -> DatabaseModel:
        record = session.get(cls, updated_record.id)
        if record is None:
            raise HTTP04_ITEM_NOT_FOUND
        logger.info(f"{cls.__name__} record found {record}")
        cls._update_model(model=record, values=updated_record)
        session.add(record)
        session.commit()
        session.refresh(record)
        logger.debug(f"{cls.__name__} with id {id} updated")
        return record

    @classmethod
    @handle_database_errors
    def delete(cls, session: Session, id: int) -> SQLModel:
        logger.warning(f"class == {cls}")
        record = session.get(cls, id)
        logger.warning(f"alguma coisa aconteceu aqui {id=}")
        if record is None:
            logger.warning(f"alguma coisa aconteceu aqui {id=}")
            logger.info(f"No row with id '{id}' found in {cls}")
            raise HTTP04_ITEM_NOT_FOUND
        session.delete(record)
        session.commit()
        logger.debug(f"{cls.__name__} with id {id} deleted")
        return record

    @classmethod
    @handle_database_errors
    def search(cls, session: Session, *where: BinaryExpression) -> List[DatabaseModel]:
        ...
        # === *where is not working properly, is returning no result if more than 1 BinaryExpression
        # query = select(cls).filter(*where)
        # for be in where:
        #     logger.warning(f"====== {be=}")
        # result = session.exec(query).all()
        # logger.debug(f"search found {len(result)} lines")
        # return result
