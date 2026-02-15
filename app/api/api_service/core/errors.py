"""Global API error handlers."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _http_error_payload(status_code: int, detail: Any) -> dict[str, dict[str, Any]]:
    if isinstance(detail, str):
        message = detail
    else:
        message = "HTTP error"
    return {"error": {"message": message, "status_code": status_code}}


def add_error_handlers(app: FastAPI) -> None:
    """Register HTTP and generic exception handlers."""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_http_error_payload(exc.status_code, exc.detail),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception while processing request %s", request.url.path)
        return JSONResponse(
            status_code=500,
            content={"error": {"message": "Internal Server Error", "status_code": 500}},
        )

