from fastapi import APIRouter, UploadFile

from app.feed_parser import RssSchema


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss"


@router.post("/parse_from/url")
async def parse_from_url(url: str = EX_URL):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.parse_feed(url)
    return rss


@router.post("/parse_from/xml")
async def parse_from_xml(xml: str):
    """Transform a RSS xml feed to json (xml -> json)"""
    # TODO: create test for this (current test client don't accept xml only json)
    rss = RssSchema.parse_feed(xml)
    return rss


@router.post("/parse_from/file")
async def parse_from_file(file: UploadFile):
    rss = RssSchema.parse_feed(file.file)
    return rss.source
