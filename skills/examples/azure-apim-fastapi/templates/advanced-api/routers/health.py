"""Health check endpoints."""

from fastapi import APIRouter, Response
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
import asyncio
import logging

from config import settings

router = APIRouter(prefix="/health", tags=["Health"])
logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class DependencyHealth(BaseModel):
    name: str
    status: HealthStatus
    latency_ms: Optional[float] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: HealthStatus
    timestamp: str
    version: str
    environment: str
    dependencies: list[DependencyHealth]


async def check_database() -> DependencyHealth:
    """Check database connectivity."""
    # Replace with actual database health check
    try:
        # Example: await db.execute("SELECT 1")
        return DependencyHealth(
            name="database",
            status=HealthStatus.HEALTHY,
            latency_ms=1.0,
        )
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        return DependencyHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
        )


async def check_cache() -> DependencyHealth:
    """Check cache connectivity."""
    # Replace with actual cache health check
    try:
        # Example: await redis.ping()
        return DependencyHealth(
            name="cache",
            status=HealthStatus.HEALTHY,
            latency_ms=0.5,
        )
    except Exception as e:
        logger.warning(f"Cache health check failed: {e}")
        return DependencyHealth(
            name="cache",
            status=HealthStatus.DEGRADED,  # Cache failure is degraded, not critical
            message=str(e),
        )


@router.get("", response_model=HealthResponse)
async def health_check(response: Response):
    """
    Comprehensive health check for APIM and monitoring.

    Returns:
    - 200: All systems healthy
    - 200: Some systems degraded (non-critical)
    - 503: Critical systems unhealthy
    """
    # Run all health checks concurrently
    checks = await asyncio.gather(
        check_database(),
        check_cache(),
        return_exceptions=True,
    )

    dependencies = []
    for check in checks:
        if isinstance(check, Exception):
            dependencies.append(DependencyHealth(
                name="unknown",
                status=HealthStatus.UNHEALTHY,
                message=str(check),
            ))
        else:
            dependencies.append(check)

    # Determine overall status
    if any(d.status == HealthStatus.UNHEALTHY for d in dependencies):
        overall_status = HealthStatus.UNHEALTHY
        response.status_code = 503
    elif any(d.status == HealthStatus.DEGRADED for d in dependencies):
        overall_status = HealthStatus.DEGRADED
    else:
        overall_status = HealthStatus.HEALTHY

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat() + "Z",
        version=settings.version,
        environment=settings.environment,
        dependencies=dependencies,
    )


@router.get("/live")
async def liveness():
    """
    Kubernetes liveness probe.

    Returns 200 if the application process is running.
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat() + "Z"}


@router.get("/ready")
async def readiness(response: Response):
    """
    Kubernetes readiness probe.

    Returns 200 if the application is ready to receive traffic.
    """
    # Check critical dependencies only
    db_health = await check_database()

    if db_health.status == HealthStatus.UNHEALTHY:
        response.status_code = 503
        return {"status": "not_ready", "reason": "database unavailable"}

    return {"status": "ready", "timestamp": datetime.utcnow().isoformat() + "Z"}
