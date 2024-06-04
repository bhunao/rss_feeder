import logging 

from datetime import datetime 
from typing import List
from sqlmodel import SQLModel, Session, select
from src.core.service import Service
from src.models import Article, Source
from src.feed_parser import parse_rss_from_url, str_to_date


logger = logging.getLogger(__name__)


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


    def articles_from_source(self, source: Source, entries: dict):
        session = self.session
        for entry in entries:
            if entry.get("published_parsed", None) is None:
                published = datetime.now()
            else:
                published = str_to_date(entry["published_parsed"])

            new_record = Article(
                    source_id=source.id,
                    title=entry.get("title", ""),
                    summary=entry.get("summary", ""),
                    date_published=published,
                    image_url="",
                    )
            self.create(new_record)

