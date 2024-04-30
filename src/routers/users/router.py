from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Cookie, Depends, HTTPException, Response, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from starlette.config import Config

from src.routers.users.model import Token, User, UserService, get_current_active_user
from src.core.database import get_session


config = Config(".env")
NAME = "User"
PREFIX = "/user"
TAGS = ["users"]
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default="30"
)
router = APIRouter(prefix=PREFIX, tags=TAGS)


@router.post("/signup", response_model=User)
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user_info = {
        "username": form_data.username,
        "password": form_data.password,
        "disabled": False,
    }

    new_user = User(**user_info)
    result = UserService(session).create(new_user)
    return result


@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = UserService(session).authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        expires=datetime.now(timezone.utc) + access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    response: Response,
    access_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session),
):
    if access_token is None:
        return {"msg": "you're not logged in."}
    user = UserService.get_current_user_from_cookie(access_token, session)
    if not user:
        return {"msg": "you're not logged in."}

    response.delete_cookie(key="access_token")
    return {"msg": f"logged out as {user.username}"}


@router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/cookie/")
async def get_cookie(
    access_token: Optional[str] = Cookie(None), session: Session = Depends(get_session)
):
    assert access_token is not None
    user = UserService.get_current_user_from_cookie(access_token, session)
    return {"user": user.username}
