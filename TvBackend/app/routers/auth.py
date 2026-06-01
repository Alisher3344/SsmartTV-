from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.auth import LoginIn, RegisterIn, UserOut
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session_cookie(response: Response, session_id: str) -> None:
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_id,
        max_age=settings.SESSION_TTL_SECONDS,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite="lax",
        path="/",
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterIn,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await auth_service.register_user(db, data)
    session_id = await auth_service.start_session(
        user.id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    _set_session_cookie(response, session_id)
    return user


@router.post("/login", response_model=UserOut)
async def login(
    data: LoginIn,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await auth_service.authenticate(db, data)
    session_id = await auth_service.start_session(
        user.id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    _set_session_cookie(response, session_id)
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if session_id:
        await auth_service.end_session(session_id)
    response.delete_cookie(settings.SESSION_COOKIE_NAME, path="/")


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return user
