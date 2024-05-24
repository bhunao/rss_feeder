from sqlmodel import SQLModel, Session, select
from src.core.service import Service
from src.models import Article


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
