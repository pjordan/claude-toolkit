"""Request context models."""

from pydantic import BaseModel
from typing import Optional


class APIMContext(BaseModel):
    """Context extracted from APIM headers."""

    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    subscription_id: Optional[str] = None
    subscription_key: Optional[str] = None
    product_name: Optional[str] = None
    client_ip: Optional[str] = None
    trace_enabled: bool = False


class UserContext(BaseModel):
    """User context from validated JWT claims."""

    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    roles: list[str] = []
    tenant_id: Optional[str] = None
    scopes: list[str] = []

    def has_role(self, *roles: str) -> bool:
        """Check if user has any of the specified roles."""
        return any(role in self.roles for role in roles)

    def has_scope(self, *scopes: str) -> bool:
        """Check if user has any of the specified scopes."""
        return any(scope in self.scopes for scope in scopes)
