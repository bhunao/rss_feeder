import logging

from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import UJSONResponse
from sqlmodel import Session, SQLModel

from src.core.database import get_session
from src.core.config import templates


logger = logging.getLogger(__name__)

def create_base_api_routes(
        router: APIRouter,
        Model: SQLModel,
        Schema: Optional[SQLModel] = None
        ) -> None:

    if Schema is None:
        Schema = Model

    @router.post("/")
    async def create(record: Schema, session: Session = Depends(get_session)):
        result = Model().create(session, record)
        return result

    @router.get("/")
    async def get(id: int, session: Session = Depends(get_session)):
        result = Model().get(session, id)
        return result

    @router.delete("/")
    async def delete(id: int, session: Session = Depends(get_session)):
        result = Model().delete(session, id)
        return result

