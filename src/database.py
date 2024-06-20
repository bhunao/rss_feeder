import logging
import feedparser
import requests

from datetime import datetime, timezone, timedelta
from time import mktime
from typing import List, Optional, Annotated

from jose import JWTError, jwt
from sqlmodel import SQLModel, select, or_, and_, Session
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer

from src.core.database import Database, get_session
from src.core.errors import HTTP401_INVALID_CREDENTIALS
from src.models import Source, Article, User, TokenData
from src.core.config import SECRET_KEY, ALGORITHM


logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def get_rss(url: str) -> dict:
    response = requests.get(url)
    parsed = feedparser.parse(response.content)
    return parsed


class ServiceDatabase(Database):
    def create_source(self, rec: SQLModel) -> Source | None:
        session = self.session

        query = select(Source).where(
            or_(
                Source.url == rec.url.strip(),
                and_(
                    Source.title == rec.title.strip(),
                    Source.subtitle == rec.subtitle.strip(),
                    Source.language == rec.language.strip(),
                ),
            )
        )
        result = session.exec(query).all()
        if len(result) > 0:
            return None
        re = self.create(rec)
        return re

    def source_from_rss(self, url: str, parsed_rss: dict) -> Source:
        record = Source(
            title=parsed_rss.get("title", "NO_TITLE"),
            subtitle=parsed_rss.get("subtitle", ""),
            url=url,
            language=parsed_rss["language"],
        )
        created_record = self.create_source(record)
        return created_record

    def read_all_sources(
        self, order_by=Source.date_created, skip: int = 0, limit: int = 100
    ) -> List[SQLModel]:
        query = select(Source).order_by(
            order_by.desc()).offset(skip).limit(limit)
        result = self.session.exec(query).all()
        return result

    def create_article(self, rec: SQLModel) -> Article | None:
        session = self.session
        query = select(Article).where(
            Article.title == rec.title,
            Article.source_id == rec.source_id,
        )
        result = session.exec(query).all()
        if len(result) > 0:
            return None
        return super().create(rec)

    def get_lasts(self, limit=100) -> List[Article]:
        query = select(Article).order_by(
            Article.date_published.desc()).limit(limit)
        result = self.session.exec(query).all()
        return result

    def get_by_source(self, source: Source, limit=100) -> List[Article]:
        query = (
            select(Article)
            .where(Article.source_id == source.id)
            .order_by(Article.date_published.desc())
            .limit(limit)
        )
        result = self.session.exec(query).all()
        return result

    def refresh_articles(self, source_id: int, entries: dict = None):
        if not entries:
            source = self.read(Source, source_id)
            rss = get_rss(source.url)
            entries = rss["entries"]

        for entry in entries:
            if entry.get("published_parsed", None) is None:
                published = datetime.now()
            else:
                date = mktime(entry["published_parsed"])
                published = datetime.fromtimestamp(date)

            new_record = Article(
                source_id=source_id,
                title=entry.get("title", ""),
                summary=entry.get("summary", ""),
                date_published=published,
                image_url="",
            )
            record = self.create_article(new_record)
            if record:
                logger.warning(
                    f"new article sucessfully created with id '{record.id}' and title '{record.title}'"
                )

    def get_user(self, username: Optional[str] = None):
        query = select(User).where(User.username == username)
        user = self.session.exec(query).one_or_none()
        user.password = ""
        return user

    def create_user(self, rec: User) -> User:
        if self.get_user(rec.username):
            return None
        rec.password = pwd_context.hash(rec.password)
        return self.create(rec)

    def authenticate_user(self, username: str, password: str):
        query = select(User).where(User.username == username)
        user = self.session.exec(query).one_or_none()
        if user and pwd_context.verify(password, user.password):
            return user
        return None

    # ==================================================

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_user_from_cookie(self, access_token: str):
        try:
            payload = jwt.decode(access_token, SECRET_KEY,
                                 algorithms=[ALGORITHM])
            username = payload.get("sub")
            assert isinstance(username, str)
            if username is None:
                raise HTTP401_INVALID_CREDENTIALS
            token_data = TokenData(username=username)
        except JWTError as e:
            logger.error(e)
            raise HTTP401_INVALID_CREDENTIALS

        user = self.get_user(token_data.username)
        if not user:
            raise HTTP401_INVALID_CREDENTIALS
        return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
    access_token: str = Cookie(None),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        assert isinstance(username, str)
        if username is None:
            raise HTTP401_INVALID_CREDENTIALS
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTP401_INVALID_CREDENTIALS

    user = UserDatabase(session).get_user(token_data.username)
    if not user:
        raise HTTP401_INVALID_CREDENTIALS
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
