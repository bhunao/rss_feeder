import logging, datetime

from typing import Optional, List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.database import get_session, SQLModel
from src.core.config import templates
from src.core.model import DatabaseModel
from src.core.service import Service
from src.models import ExampleModel, ExampleModelSchema


NAME = "example_model"
PREFIX = f"/{NAME}"
TAGS = [NAME]

router = APIRouter(prefix=PREFIX, tags=TAGS)
logger = logging.getLogger(__name__)



@router.get("/health_check")
async def home():
    return True

@router.post("/", response_model=ExampleModel)
async def create(record: ExampleModelSchema, session: Session = Depends(get_session)):
    result = Service(ExampleModel, session).create(record)
    return result

@router.get("/", response_model=ExampleModel)
async def read(id: int, session: Session = Depends(get_session)):
    result = Service(ExampleModel, session).read(id)
    return result

@router.post("/update", response_model=ExampleModel)
async def update(record: ExampleModel, session: Session = Depends(get_session)):
    result = Service(ExampleModel, session).update(record)
    return result

@router.delete("/", response_model=ExampleModel)
async def delete(id: int, session: Session = Depends(get_session)):
    result = Service(ExampleModel, session).delete(id)
    return result

@router.get("/all", response_model=List[ExampleModel])
async def read_all(
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
        ):
    result = Service(ExampleModel, session).read_all(skip, limit)
    return result
