import feedparser
import requests
import validators

from datetime import datetime
from time import mktime
from typing import List
from urllib.parse import urlparse


def parse_rss_from_url(url: str) -> dict:
    response = requests.get(url)
    parsed = feedparser.parse(response.content)
    return parsed

def str_to_date(date):
    dt = datetime.fromtimestamp(mktime(date))
    return dt
