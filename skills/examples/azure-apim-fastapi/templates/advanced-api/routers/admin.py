"""Admin API endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
import logging

from config import settings
from models.context import UserContext
from services.auth import require_roles

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])
logger = logging.getLogger(__name__)


class SystemInfo(BaseModel):
    app_name: str
    version: str
    environment: str
    debug: bool
    timestamp: str


class StatsResponse(BaseModel):
    total_requests: int
    active_users: int
    uptime_seconds: float


@router.get("/info", response_model=SystemInfo)
async def get_system_info(
    user: UserContext = Depends(require_roles("Admin")),
):
    """
    Get system information.

    Requires Admin role.
    """
    logger.info(
        "Admin accessing system info",
        extra={"user_id": user.user_id}
    )

    return SystemInfo(
        app_name=settings.app_name,
        version=settings.version,
        environment=settings.environment,
        debug=settings.debug,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    user: UserContext = Depends(require_roles("Admin", "Analyst")),
):
    """
    Get system statistics.

    Requires Admin or Analyst role.
    """
    logger.info(
        "Admin accessing stats",
        extra={"user_id": user.user_id, "roles": user.roles}
    )

    # Mock stats - replace with actual implementation
    return StatsResponse(
        total_requests=12345,
        active_users=42,
        uptime_seconds=3600.0,
    )
