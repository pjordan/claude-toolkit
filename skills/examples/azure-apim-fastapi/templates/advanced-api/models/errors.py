"""Error response models and exception handlers."""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional, Any
import logging

from middleware.correlation import get_correlation_id

logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str
    message: str
    correlation_id: Optional[str] = None
    details: Optional[Any] = None


def setup_exception_handlers(app: FastAPI):
    """Configure exception handlers for the application."""

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions."""
        correlation_id = get_correlation_id()

        logger.exception(
            "Unhandled exception",
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method,
            }
        )

        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="internal_error",
                message="An unexpected error occurred",
                correlation_id=correlation_id,
            ).model_dump()
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions with consistent format."""
        correlation_id = get_correlation_id()

        # Map common status codes to error types
        error_types = {
            400: "bad_request",
            401: "unauthorized",
            403: "forbidden",
            404: "not_found",
            409: "conflict",
            422: "validation_error",
            429: "rate_limit_exceeded",
            500: "internal_error",
            502: "bad_gateway",
            503: "service_unavailable",
        }

        error_type = error_types.get(exc.status_code, "error")

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=error_type,
                message=str(exc.detail),
                correlation_id=correlation_id,
            ).model_dump(),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        correlation_id = get_correlation_id()

        # Format validation errors
        errors = []
        for error in exc.errors():
            loc = ".".join(str(l) for l in error["loc"])
            errors.append({
                "field": loc,
                "message": error["msg"],
                "type": error["type"],
            })

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error="validation_error",
                message="Request validation failed",
                correlation_id=correlation_id,
                details={"errors": errors},
            ).model_dump()
        )
