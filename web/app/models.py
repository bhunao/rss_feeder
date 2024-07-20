from sqlmodel import SQLModel


class NewSourceSchema(SQLModel):
    name: str = "duckgogo"
    link: str = "www.duckgogo.com"


class SourceSchema(SQLModel):
    title: str
    subtitle: str
    url: str
    language: str | None = None


class ArticleSchema(SQLModel):
    source: str
    title: str
    summary: str
    date_published: str
    image_url: str
