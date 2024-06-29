import logging

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.core.database import BaseDatabase as Database
from src.core.database import get_session
from src.models import ExampleModel, ExampleModelSchema


NAME = "example_model"
PREFIX = f"/{NAME}"
TAGS = [NAME]

router = APIRouter(prefix=PREFIX, tags=TAGS)
logger = logging.getLogger(__name__)


@router.get("/health_check")
async def db_test_home():
    return True


@router.post("/", response_model=ExampleModel)
async def db_test_create(record: ExampleModelSchema, session: Session = Depends(get_session)):
    result = Database(session).create(record, table=ExampleModel)
    return result


@router.get("/", response_model=ExampleModel)
async def db_test_read(id: int, session: Session = Depends(get_session)):
    result = Database(session).read(ExampleModel, id)
    return result


@router.post("/update", response_model=ExampleModel)
async def db_test_update(record: ExampleModel, session: Session = Depends(get_session)):
    result = Database(session).update(record)
    return result


@router.delete("/", response_model=ExampleModel)
async def db_test_delete(id: int, session: Session = Depends(get_session)):
    result = Database(session).delete(ExampleModel, id)
    return result


@router.get("/all", response_model=list[ExampleModel])
async def db_test_read_all(
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    result = Database(session).read_all(ExampleModel, skip, limit)
    return result


@router.post("/ioio", response_model=ExampleModel)
async def db_test_ioio(record: ExampleModelSchema, session: Session = Depends(get_session)):
    result = Database(session).create(record, table=ExampleModel)
    return result
