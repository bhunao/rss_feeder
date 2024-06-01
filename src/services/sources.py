from fastapi import BackgroundTasks
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
                    Source.url == rec.url.strip(),
                    and_(
                        Source.title == rec.title.strip(),
                        Source.subtitle == rec.subtitle.strip(),
                        Source.language == rec.language.strip()
                        )
                    )
                )
        result = session.exec(query).all()
        if len(result) > 0:
            return None
        return super().create(rec)

    def from_rss(self, parsed_rss: dict) -> Source:
        record = Source(
                title=parsed_rss["title"],
                subtitle=parsed_rss["subtitle"],
                url=parsed_rss["link"],
                language=parsed_rss["language"]
                )
        created_record = self.create(record)
        return created_record
