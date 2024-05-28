from typing import List
from sqlmodel import SQLModel, Session, select
from src.core.service import Service
from src.models import Article, Source


class ArticleService(Service):
    def __init__(self, session: Session):
        super().__init__(Article, session)

    def create(self, rec: SQLModel) -> Article | None:
        model, session = self.mo_ses()

        query = select(model).where(

                Article.title == rec.title,
                Article.source_id == rec.source_id,
                )
        result = session.exec(query).all()
        if len(result) > 0:
            return None
        return super().create(rec)

    def get_lasts(self, limit=100) -> List[Article]:
        model, session = self.mo_ses()
        query = select(model).order_by(
                    Article.date_published.desc()
                ).limit(limit)
        result = session.exec(query).all()
        return result
    
    def get_by_source(self, source: Source, limit=100) -> List[Article]:
        model, session = self.mo_ses()
        query = select(model).where(
                Article.source_id == source.id
                ).order_by(Article.date_published.desc()).limit(limit)
        result = session.exec(query).all()
        return result
