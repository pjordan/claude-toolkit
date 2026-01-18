"""Correlation ID middleware for request tracing."""

from contextvars import ContextVar
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Context variable for correlation ID
correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')


def get_correlation_id() -> str:
    """Get current correlation ID from context."""
    return correlation_id_var.get()


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle correlation IDs.

    Extracts correlation ID from APIM headers or generates a new one.
    Makes it available via context variable and adds to response headers.
    """

    async def dispatch(self, request: Request, call_next):
        # Priority: X-Correlation-ID > X-Request-ID > generate new
        correlation_id = (
            request.headers.get("X-Correlation-ID")
            or request.headers.get("X-Request-ID")
            or str(uuid4())
        )

        # Set in context for use throughout request
        correlation_id_var.set(correlation_id)

        response = await call_next(request)

        # Add to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        return response
