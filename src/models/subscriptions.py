import logging

from typing import Optional

from sqlmodel import Field

from src.core.database import SQLModel
from src.core.model import DatabaseModel


class SubscriptionSchema(SQLModel):
    user_id: int
    source_id: int


class Subscription(DatabaseModel, table=True):
    __name__ = "subscriptions"
    __tablename__ = __name__
    __schema__ = SubscriptionSchema

    id: Optional[int] = Field(nullable=False, primary_key=True)
    user_id: int
    source_id: int

