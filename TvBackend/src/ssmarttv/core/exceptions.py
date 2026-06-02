"""Domain exceptions and a consistent JSON error envelope.

Every error response has the shape::

    {"error": {"code": "...", "message": "...", "details": ...}}

Domain code raises subclasses of :class:`AppError`; the registered handlers
translate those (plus FastAPI's HTTPException and validation errors) into the
envelope above.
"""
import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("ssmarttv.error")


class AppError(Exception):
    """Base class for expected, client-facing domain errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "bad_request"
    message: str = "Bad request"

    def __init__(
        self,
        message: str | None = None,
        *,
        details: Any | None = None,
        code: str | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details
        if code:
            self.code = code
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    message = "Resource not found"


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    message = "Resource already exists"


class AuthenticationError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthenticated"
    message = "Authentication required"


class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "permission_denied"
    message = "You do not have permission to perform this action"


class SubscriptionRequiredError(AppError):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    code = "subscription_required"
    message = "An active subscription is required to watch this content"


class RateLimitError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "rate_limited"
    message = "Too many requests, please try again later"


def _envelope(code: str, message: str, details: Any | None) -> dict[str, Any]:
    body: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        body["details"] = details
    return {"error": body}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope("http_error", str(exc.detail), None),
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope("validation_error", "Invalid request", exc.errors()),
        )

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope("internal_error", "Internal server error", None),
        )
