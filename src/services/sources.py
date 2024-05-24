from sqlmodel import SQLModel, Session, select, or_, and_
from src.core.service import Service
from src.models import Source


class SourceService(Service):
    def __init__(self, session: Session):
        super().__init__(Source, session)

    def create(self, rec: SQLModel) -> Source | None:
        model, session = self.mo_ses()

        query = select(model).where(
                or_(
                    Source.url == rec.url,
                    and_(
                        Source.title == rec.title,
                        Source.subtitle == rec.subtitle,
                        Source.language == rec.language
                        )
                    )
                )
        result = session.exec(query).all()
        if len(result) > 0:
            return None
        return super().create(rec)
