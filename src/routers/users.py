from datetime import timezone, datetime, timedelta
from typing import Annotated, Optional

from fastapi import (
    Depends,
    APIRouter,
    Request,
    Form,
    Response,
    HTTPException,
    status,
    Cookie,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from src.core.config import templates, config
from src.core.database import get_session
from src.database import (
    UserDatabase,
)
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
    session: Session = Depends(get_session),
):
    return templates.TemplateResponse(
        "pages/signup.html",
        {"request": request},
        block_name=None,
    )


@router.post("/signup")
async def signup_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    db = UserDatabase(session)
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
    session: Session = Depends(get_session),
):
    return templates.TemplateResponse(
        "pages/login.html",
        {"request": request},
        block_name=None,
    )


@router.post("/login")
async def login_form(
    request: Request,
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    db = UserDatabase(session)
    user = db.authenticate_user(form.username, form.password)
    print("================")
    print(f"{user=}", type(user))
    print("================")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserDatabase.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        expires=datetime.now(timezone.utc) + access_token_expires,
    )
    return templates.TemplateResponse(
        "pages/me.html",
        {"request": request, "user": user},
        block_name="content",
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

    db = UserDatabase(session)
    user = db.get_current_user_from_cookie(access_token)
    if not user:
        return {"msg": "you're not logged in."}

    response.delete_cookie(key="access_token")
    return {"msg": f"logged out as {user.username}"}


@router.get("/me/")
async def read_users_me(
    request: Request,
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    db = UserDatabase(session)
    print("========-------------======")
    print(access_token)
    if not access_token:
        return RedirectResponse("/user/login")

    current_user = db.get_current_user_from_cookie(access_token)
    return templates.TemplateResponse(
        "pages/me.html",
        {"request": request, "user": current_user},
        block_name=None,
    )


# @router.get("/cookie/")
# async def get_cookie(
# access_token: Optional[str] = Cookie(None), session: Session = Depends(get_session)
# ):
# assert access_token is not None
# user = UserService.get_current_user_from_cookie(access_token, session)
# return {"user": user.username}
# return
