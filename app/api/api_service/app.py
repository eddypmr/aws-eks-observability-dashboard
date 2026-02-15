"""FastAPI application wiring."""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from api_service.core.errors import add_error_handlers
from api_service.core.logging import configure_logging
from api_service.routers.health import router as health_router
from api_service.routers.status import router as status_router
from api_service.routers.version import router as version_router


def create_app() -> FastAPI:
    configure_logging()
    logger = logging.getLogger("api_service")

    application = FastAPI(title="EKS Observability API")

    @application.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "%s %s -> unhandled exception (%.2f ms)",
                request.method,
                request.url.path,
                duration_ms,
            )
            raise
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    add_error_handlers(application)

    application.include_router(health_router, prefix="/api", tags=["health"])
    application.include_router(version_router, prefix="/api", tags=["version"])
    application.include_router(status_router, prefix="/api", tags=["status"])

    return application


app = create_app()
