from fastapi import APIRouter

from app.feed_parser import RSS


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"


@router.post("/parse_xml")
async def parse_xml(url: str = EX_URL):
    """Returns a parsed dict(json) from a RSS url."""
    rss = RSS(url)
    return rss.rss_dict
