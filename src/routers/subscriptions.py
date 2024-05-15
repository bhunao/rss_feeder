import logging

from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, SQLModel, Field

from src.models.subscriptions import Subscription, SubscriptionSchema
from src.core.database import get_session
from src.core.config import templates


logger = logging.getLogger(__name__)
router = Subscription().__router__

Schema = SubscriptionSchema
Model = Subscription

@router.get("/health_check")
async def home():
    return True

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
