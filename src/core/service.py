from typing import Tuple, TypeVar, List
from src.core.database import get_session
from sqlmodel import Session, select, SQLModel

MODEL_TYPE = TypeVar("MODEL_TYPE", bound=SQLModel)


class Service:
    def __init__(self, model: MODEL_TYPE, session: Session):
        self.model: MODEL_TYPE = model
        self.session: Session = session

    def mo_ses(self) -> Tuple[SQLModel, Session]:
        return self.model, self.session

    def create(self, rec: SQLModel):
        model, session = self.mo_ses()

        db_rec = model.model_validate(rec, from_attributes=True)
        session.add(db_rec)
        session.commit()
        session.refresh(db_rec)
        return db_rec
    
    def read(self, id: int) -> MODEL_TYPE | None:
        model, session = self.mo_ses()
        db_rec = session.get(model, id)
        return db_rec

    def read_all(self, skip: int = 0, limit: int = 100) -> List[MODEL_TYPE]:
        model, session = self.mo_ses()
        query = select(model).offset(skip).limit(limit)
        result = session.exec(query).all()
        return result

    def update(self, rec: SQLModel) -> MODEL_TYPE | None:
        model, session = self.mo_ses()
        db_rec = session.get(model, rec.id)
        if db_rec is None:
            return None
        db_rec.sqlmodel_update(rec)
        session.add(db_rec)
        session.commit()
        session.refresh(db_rec)
        return db_rec

    def delete(self, id: int) -> MODEL_TYPE | None:
        model, session = self.mo_ses()
        db_rec = session.get(model, id)
        if db_rec is None:
            return None
        session.delete(db_rec)
        session.commit()
        return db_rec
