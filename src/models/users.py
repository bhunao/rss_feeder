from typing import Optional
from typing_extensions import Annotated

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, Field

from src.core.base_service import BaseService, SQLModel
from src.core.config import config
from src.core.database import get_session


class User(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False


SECRET_KEY = config("SECRET_KEY", default="DEFAULT_KEY")
ALGORITHM = config("ALGORITHM", cast=str, default="HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class UserService(BaseService):
    def __init__(self, session: Session) -> None:
        self.context = pwd_context
        super().__init__(User, session)

    def create(self, new_entry: User) -> User:
        new_entry.password = pwd_context.hash(new_entry.password)
        return super().create(new_entry)

    def authenticate_user(self, username: str, password: str):
        user = self.search(User.username == username)
        if len(user) < 1 or user is None:
            raise credentials_exception
        user = user[0]
        if not self.context.verify(password, user.password):
            return False
        return user

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

    @staticmethod
    def get_current_user_from_cookie(access_token: str, session: Session):
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            assert isinstance(username, str)
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError as e:
            print("=" * 100)
            print(e)
            raise credentials_exception

        user = UserService(session).search(User.username == token_data.username)
        if len(user) < 1 or user is None:
            raise credentials_exception
        user = user[0]
        return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        assert isinstance(username, str)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = UserService(session).search(User.username == token_data.username)
    if len(user) < 1 or user is None:
        raise credentials_exception
    user = user[0]
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
