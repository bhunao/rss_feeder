from datetime import timezone, datetime, timedelta
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from src.core.config import templates, config
from src.core.database import get_session
from src.database import Database
from src.database import get_current_user
from src.models import User


NAME = "User"
PREFIX = "/user"
TAGS = ["user"]
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default="30"
)
router = APIRouter(prefix=PREFIX, tags=TAGS)


@router.get("/signup", response_model=User)
async def signup(
    request: Request,
    current_user: str = Depends(get_current_user),
):
    html_page = "pages/me.html" if current_user else "pages/signup.html"
    template = templates.TemplateResponse(
        html_page,
        {"request": request, "user": current_user},
        block_name=None,
    )
    return template


@router.post("/signup")
async def signup_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    db = Database(session)
    new_user = User(
        username=username,
        email=email,
        password=password,
    )
    new_user = db.create_user(new_user)
    return new_user


@router.get("/login", response_model=User)
async def login(
    request: Request,
    current_user: str = Depends(get_current_user),
):
    html_page = "pages/me.html" if current_user else "pages/login.html"
    template = templates.TemplateResponse(
        html_page,
        {"request": request, "user": current_user},
        block_name=None,
    )
    return template


@router.post("/login")
async def login_form(
    request: Request,
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    db = Database(session)
    user = db.authenticate_user(form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Database.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    template = templates.TemplateResponse(
        "pages/me.html",
        {"request": request, "user": user, "response": response},
        block_name="content",
    )
    template.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        expires=datetime.now(timezone.utc) + access_token_expires,
    )
    return template


@router.post("/logout")
async def logout(
    request: Request,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    headers = {"HX-Redirect": "/user/login"} if current_user else None
    template = templates.TemplateResponse(
        "pages/me.html",
        {"request": request, "user": current_user},
        headers=headers,
        block_name="content",
    )
    template.delete_cookie(key="access_token")
    return template


@ router.get("/me/")
async def read_users_me(
    request: Request,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not current_user:
        return RedirectResponse("/user/login")

    return templates.TemplateResponse(
        "pages/me.html",
        {"request": request, "user": current_user},
        block_name=None,
    )
