"""Logging configuration for Azure Monitor integration."""

import logging
import json
from datetime import datetime
from typing import Any

from config import settings


class AzureMonitorFormatter(logging.Formatter):
    """
    JSON formatter compatible with Azure Monitor / Application Insights.

    Produces structured JSON logs that can be queried in Azure Log Analytics.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add correlation ID if available
        if hasattr(record, 'correlation_id'):
            log_obj["correlationId"] = record.correlation_id

        # Add extra fields from record
        extra_fields = {
            k: v for k, v in record.__dict__.items()
            if k not in (
                'name', 'msg', 'args', 'created', 'filename',
                'funcName', 'levelname', 'levelno', 'lineno',
                'module', 'msecs', 'pathname', 'process',
                'processName', 'relativeCreated', 'stack_info',
                'thread', 'threadName', 'exc_info', 'exc_text',
                'correlation_id', 'message', 'taskName'
            )
        }
        if extra_fields:
            log_obj["properties"] = extra_fields

        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "stackTrace": self.formatException(record.exc_info),
            }

        return json.dumps(log_obj, default=str)


class TextFormatter(logging.Formatter):
    """Human-readable formatter for local development."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        correlation_id = getattr(record, 'correlation_id', '-')

        base = f"[{timestamp}] {record.levelname:8} [{correlation_id[:8]}] {record.name}: {record.getMessage()}"

        if record.exc_info:
            base += f"\n{self.formatException(record.exc_info)}"

        return base


def configure_logging():
    """
    Configure logging based on settings.

    Uses JSON format for production (Azure Monitor compatible)
    and text format for local development.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Remove existing handlers
    root_logger.handlers = []

    # Create handler with appropriate formatter
    handler = logging.StreamHandler()

    if settings.log_format == "json" or settings.environment == "production":
        handler.setFormatter(AzureMonitorFormatter())
    else:
        handler.setFormatter(TextFormatter())

    root_logger.addHandler(handler)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
