"""Authentication and authorization services."""

from fastapi import Header, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from typing import Optional
from uuid import uuid4
import logging

from config import settings
from models.context import APIMContext, UserContext

logger = logging.getLogger(__name__)

# Security schemes
api_key_header = APIKeyHeader(
    name="Ocp-Apim-Subscription-Key",
    auto_error=False,
    description="APIM subscription key"
)


async def get_apim_context(
    # Standard APIM headers
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
    ocp_apim_subscription_key: Optional[str] = Header(None, alias="Ocp-Apim-Subscription-Key"),
    ocp_apim_trace: Optional[str] = Header(None, alias="Ocp-Apim-Trace"),

    # Custom headers from APIM policies
    x_subscription_id: Optional[str] = Header(None, alias="X-Subscription-Id"),
    x_product_name: Optional[str] = Header(None, alias="X-Product-Name"),
    x_forwarded_for: Optional[str] = Header(None, alias="X-Forwarded-For"),
) -> APIMContext:
    """
    Extract APIM context from request headers.

    These headers are set by APIM gateway and forwarded to the backend.
    """
    # Get or generate correlation ID
    correlation_id = x_correlation_id or x_request_id or str(uuid4())

    # Parse client IP from X-Forwarded-For
    client_ip = None
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()

    return APIMContext(
        request_id=x_request_id,
        correlation_id=correlation_id,
        subscription_id=x_subscription_id,
        subscription_key=ocp_apim_subscription_key,
        product_name=x_product_name,
        client_ip=client_ip,
        trace_enabled=ocp_apim_trace == "true",
    )


async def validate_subscription_key(
    api_key: Optional[str] = Security(api_key_header),
) -> str:
    """
    Validate APIM subscription key.

    Note: APIM typically validates this at the gateway level.
    This provides defense-in-depth for direct backend access.
    """
    if settings.validate_subscription_key:
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="Subscription key required",
                headers={"WWW-Authenticate": "ApiKey"}
            )
    return api_key or ""


async def get_user_context(
    # User identity headers forwarded from APIM JWT validation
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_user_name: Optional[str] = Header(None, alias="X-User-Name"),
    x_user_roles: Optional[str] = Header(None, alias="X-User-Roles"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-Id"),
    x_user_scopes: Optional[str] = Header(None, alias="X-User-Scopes"),
) -> UserContext:
    """
    Extract user context from APIM-forwarded JWT claims.

    APIM validates the JWT and forwards claims via headers.
    This function extracts those claims into a UserContext object.
    """
    if not x_user_id:
        raise HTTPException(
            status_code=401,
            detail="User context not provided. Authentication required.",
        )

    return UserContext(
        user_id=x_user_id,
        email=x_user_email,
        name=x_user_name,
        roles=x_user_roles.split(",") if x_user_roles else [],
        tenant_id=x_tenant_id,
        scopes=x_user_scopes.split(" ") if x_user_scopes else [],
    )


def require_roles(*required_roles: str):
    """
    Dependency factory for role-based access control.

    Usage:
        @router.get("/admin")
        async def admin_endpoint(user: UserContext = Depends(require_roles("Admin"))):
            ...
    """
    async def check_roles(user: UserContext = Depends(get_user_context)) -> UserContext:
        if not user.has_role(*required_roles):
            logger.warning(
                f"Access denied: user {user.user_id} lacks required roles {required_roles}",
                extra={"user_id": user.user_id, "user_roles": user.roles}
            )
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required roles: {', '.join(required_roles)}"
            )
        return user
    return check_roles


def require_scopes(*required_scopes: str):
    """
    Dependency factory for scope-based access control.

    Usage:
        @router.get("/data")
        async def data_endpoint(user: UserContext = Depends(require_scopes("data.read"))):
            ...
    """
    async def check_scopes(user: UserContext = Depends(get_user_context)) -> UserContext:
        if not user.has_scope(*required_scopes):
            logger.warning(
                f"Access denied: user {user.user_id} lacks required scopes {required_scopes}",
                extra={"user_id": user.user_id, "user_scopes": user.scopes}
            )
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required scopes: {', '.join(required_scopes)}"
            )
        return user
    return check_scopes
