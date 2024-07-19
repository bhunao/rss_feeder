from sqlmodel import SQLModel
from fastapi import APIRouter


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)


class NewRss(SQLModel):
    name: str = "duckgogo"
    link: str = "www.duckgogo.com"


@router.post("/")
async def create(record: NewRss) -> NewRss:
    return record
