import logging


from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from src.core.database import get_session, SQLModel
from src.core.config import templates
from src.core.model import DatabaseModel
from src.models.database_test import ExampleModel, ExampleModelSchema


logger = logging.getLogger(__name__)
router = ExampleModel().__router__

@router.get("/health_check")
async def home():
    return True

@router.post("/")
async def create(record: ExampleModelSchema, session: Session = Depends(get_session)):
    result = ExampleModel().create(session, record)
    return result

@router.get("/")
async def get(id: int, session: Session = Depends(get_session)):
    result = ExampleModel().get(session, id)
    return result

@router.post("/update")
async def delete(record: ExampleModel, session: Session = Depends(get_session)):
    result = ExampleModel().update(session, record)
    return result


@router.delete("/")
async def delete(id: int, session: Session = Depends(get_session)):
    result = ExampleModel().delete(session, id)
    return result

