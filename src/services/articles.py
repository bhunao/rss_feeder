from datetime import datetime 
from typing import List
from sqlmodel import SQLModel, Session, select
from src.core.service import Service
from src.models import Article, Source
from src.feed_parser import parse_rss_from_url, str_to_date


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


    def articles_from_source(self, source: Source):
        session = self.session
        print(1, "="*50)
        parsed_rss = parse_rss_from_url(source.url)
        print(2, "="*50)
        for entry in parsed_rss["entries"]:
            print(2.5, "="*50)
            if entry.get("published_parsed", None) is None:
                published = datetime.now()
            else:
                published = str_to_date(entry["published_parsed"])
            print(3, "="*50)
            new_record = Article(
                    source_id=source.id,
                    title=entry["title"],
                    summary=entry["summary"],
                    date_published=published,
                    image_url="",
                    )
            print(4, "="*50)
            self.create(new_record)
            print(5, "="*50)

