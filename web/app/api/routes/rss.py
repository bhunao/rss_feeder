from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from sqlmodel import SQLModel

from app.models import RssSchema
from app.errors import S400_INVALID_URL
from app.core.config import settings


templates = settings.TEMPLATES


router = APIRouter(
    prefix="/rss",
    tags=["rss"],
)

EX_URL = "https://techcrunch.com/feed/"


class UrlSchema(SQLModel):
    url: str = EX_URL


multi_responses = {
    200: {
        "content": {"text/html": {}},
        "description": "Returns the JSON or HTML.",
    }
}


def multi_response_type(request: Request, model_or_schema: SQLModel | Exception) -> Response | SQLModel:
    accept_values = request.headers.get("accept", None)
    if isinstance(accept_values, str) and "application/json" in accept_values:
        if isinstance(model_or_schema, Exception):
            raise S400_INVALID_URL
        else:
            return model_or_schema

    if isinstance(model_or_schema, Exception):
        context = {"error": model_or_schema}
    else:
        context = {"rss": model_or_schema}

    return templates.TemplateResponse(request, "index.html", context=context)


@ router.get("/parse_from", responses=multi_responses)
async def parse_from_url(request: Request, url: str = EX_URL):
    """Returns a parsed dict(json) from a RSS url (url -> json)"""
    rss = RssSchema.from_url(url)

    return multi_response_type(request, rss)

    context = {"rss": rss}
    accept_values = request.headers.get("accept", None)
    assert accept_values
    if "application/json" in accept_values:
        if isinstance(rss, Exception):
            raise S400_INVALID_URL
        return rss

    if isinstance(rss, Exception):
        del context["rss"]
        context["error"] = rss
    return templates.TemplateResponse(request, "index.html", context=context)
