import logging, datetime

from typing import Optional, List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.database import get_session, SQLModel
from src.core.config import templates
from src.core.model import DatabaseModel
from src.models.database_test import ExampleModel, ExampleModelSchema


logger = logging.getLogger(__name__)
router = ExampleModel.create_router()

@router.get("/health_check")
async def home():
    return True

@router.post("/", response_model=ExampleModel)
async def create(record: ExampleModelSchema, session: Session = Depends(get_session)):
    result = ExampleModel.create(session, record)
    return result

@router.get("/", response_model=ExampleModel)
async def get(id: int, session: Session = Depends(get_session)):
    result = ExampleModel.read(session, id)
    return result

@router.post("/update", response_model=ExampleModel)
async def update(record: ExampleModel, session: Session = Depends(get_session)):
    result = ExampleModel.update(session, record)
    return result

@router.delete("/", response_model=ExampleModel)
async def delete(id: int, session: Session = Depends(get_session)):
    result = ExampleModel.delete(session, id)
    return result

@router.get("/all", response_model=List[ExampleModel])
async def read_all(
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
        ):
    result = ExampleModel.read_all(session, skip, limit)
    return result
