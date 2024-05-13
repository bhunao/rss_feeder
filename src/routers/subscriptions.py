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
