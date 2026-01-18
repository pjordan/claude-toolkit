# JWT Authentication Policy Example

An example session using the Azure APIM + FastAPI Developer subagent to create APIM policies for Azure AD JWT validation.

## User Request

```
Create an APIM policy that:
- Validates JWT tokens from Azure AD (Entra ID)
- Requires the "API.Read" or "API.Write" role claim
- Extracts user ID, email, and roles from the token
- Forwards them to the backend as X-User-Id, X-User-Email, and X-User-Roles headers
- Rate limits to 100 requests per minute per user
- Returns structured error responses with correlation IDs
```

## Expected Response

Here's a complete APIM policy with JWT validation, claim extraction, and rate limiting:

### Complete Policy

```xml
<policies>
    <inbound>
        <base />

        <!-- Generate correlation ID if not present -->
        <set-header name="X-Correlation-ID" exists-action="skip">
            <value>@(Guid.NewGuid().ToString())</value>
        </set-header>

        <!-- Store correlation ID for error responses -->
        <set-variable name="correlationId" value="@(context.Request.Headers.GetValueOrDefault("X-Correlation-ID", Guid.NewGuid().ToString()))" />

        <!-- Validate JWT from Azure AD -->
        <validate-jwt
            header-name="Authorization"
            failed-validation-httpcode="401"
            failed-validation-error-message="Unauthorized. Valid Azure AD token required."
            require-expiration-time="true"
            require-signed-tokens="true">

            <!-- Azure AD OpenID configuration -->
            <openid-config url="https://login.microsoftonline.com/{{azure-tenant-id}}/v2.0/.well-known/openid-configuration" />

            <!-- Expected audience (your API's app registration) -->
            <audiences>
                <audience>api://{{azure-api-client-id}}</audience>
                <audience>{{azure-api-client-id}}</audience>
            </audiences>

            <!-- Expected issuer -->
            <issuers>
                <issuer>https://login.microsoftonline.com/{{azure-tenant-id}}/v2.0</issuer>
                <issuer>https://sts.windows.net/{{azure-tenant-id}}/</issuer>
            </issuers>

            <!-- Require specific roles -->
            <required-claims>
                <claim name="roles" match="any">
                    <value>API.Read</value>
                    <value>API.Write</value>
                </claim>
            </required-claims>
        </validate-jwt>

        <!-- Extract claims and set as variables -->
        <set-variable name="userId" value="@{
            var authHeader = context.Request.Headers.GetValueOrDefault("Authorization", "");
            if (authHeader.StartsWith("Bearer ")) {
                var token = authHeader.Substring(7);
                var jwt = token.AsJwt();
                return jwt?.Claims.GetValueOrDefault("oid", "") ?? "";
            }
            return "";
        }" />

        <set-variable name="userEmail" value="@{
            var authHeader = context.Request.Headers.GetValueOrDefault("Authorization", "");
            if (authHeader.StartsWith("Bearer ")) {
                var token = authHeader.Substring(7);
                var jwt = token.AsJwt();
                // Try preferred_username first, then email, then upn
                return jwt?.Claims.GetValueOrDefault("preferred_username",
                    jwt?.Claims.GetValueOrDefault("email",
                        jwt?.Claims.GetValueOrDefault("upn", ""))) ?? "";
            }
            return "";
        }" />

        <set-variable name="userRoles" value="@{
            var authHeader = context.Request.Headers.GetValueOrDefault("Authorization", "");
            if (authHeader.StartsWith("Bearer ")) {
                var token = authHeader.Substring(7);
                var jwt = token.AsJwt();
                var roles = jwt?.Claims.Where(c => c.Key == "roles").Select(c => c.Value);
                return roles != null ? string.Join(",", roles) : "";
            }
            return "";
        }" />

        <!-- Forward claims to backend -->
        <set-header name="X-User-Id" exists-action="override">
            <value>@((string)context.Variables["userId"])</value>
        </set-header>

        <set-header name="X-User-Email" exists-action="override">
            <value>@((string)context.Variables["userEmail"])</value>
        </set-header>

        <set-header name="X-User-Roles" exists-action="override">
            <value>@((string)context.Variables["userRoles"])</value>
        </set-header>

        <!-- Rate limit per user: 100 requests per minute -->
        <rate-limit-by-key
            calls="100"
            renewal-period="60"
            counter-key="@((string)context.Variables["userId"])"
            increment-condition="@(context.Response.StatusCode >= 200 && context.Response.StatusCode < 400)"
            retry-after-header-name="Retry-After" />

        <!-- Remove Authorization header before forwarding (backend trusts X-User-* headers) -->
        <set-header name="Authorization" exists-action="delete" />

    </inbound>

    <backend>
        <base />
    </backend>

    <outbound>
        <base />

        <!-- Remove internal headers from response -->
        <set-header name="X-Powered-By" exists-action="delete" />
        <set-header name="Server" exists-action="delete" />

        <!-- Add correlation ID to response -->
        <set-header name="X-Correlation-ID" exists-action="override">
            <value>@((string)context.Variables["correlationId"])</value>
        </set-header>

        <!-- Add rate limit headers -->
        <set-header name="X-RateLimit-Limit" exists-action="override">
            <value>100</value>
        </set-header>
    </outbound>

    <on-error>
        <base />

        <!-- Structured error response -->
        <set-header name="Content-Type" exists-action="override">
            <value>application/json</value>
        </set-header>

        <set-header name="X-Correlation-ID" exists-action="override">
            <value>@((string)context.Variables.GetValueOrDefault("correlationId", context.RequestId.ToString()))</value>
        </set-header>

        <set-body>@{
            var correlationId = (string)context.Variables.GetValueOrDefault("correlationId", context.RequestId.ToString());

            string errorCode;
            string errorMessage;

            switch (context.Response.StatusCode) {
                case 401:
                    errorCode = "UNAUTHORIZED";
                    errorMessage = "Authentication required. Please provide a valid Azure AD token.";
                    break;
                case 403:
                    errorCode = "FORBIDDEN";
                    errorMessage = "Access denied. You don't have the required permissions.";
                    break;
                case 429:
                    errorCode = "RATE_LIMITED";
                    errorMessage = "Too many requests. Please wait before retrying.";
                    break;
                default:
                    errorCode = "INTERNAL_ERROR";
                    errorMessage = context.LastError?.Message ?? "An unexpected error occurred.";
                    break;
            }

            return new JObject(
                new JProperty("error", new JObject(
                    new JProperty("code", errorCode),
                    new JProperty("message", errorMessage),
                    new JProperty("status", context.Response.StatusCode),
                    new JProperty("correlation_id", correlationId),
                    new JProperty("timestamp", DateTime.UtcNow.ToString("o"))
                ))
            ).ToString();
        }</set-body>
    </on-error>
</policies>
```

### Named Values Required

Create these named values in APIM before applying the policy:

```bash
# Azure tenant ID
az apim nv create \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --named-value-id azure-tenant-id \
  --display-name "Azure Tenant ID" \
  --value "your-tenant-id-here"

# API client ID (from app registration)
az apim nv create \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --named-value-id azure-api-client-id \
  --display-name "Azure API Client ID" \
  --value "your-api-client-id-here"
```

### FastAPI Backend Handler

The backend receives validated claims via headers:

```python
from fastapi import Header, Depends, HTTPException
from typing import Optional
from dataclasses import dataclass


@dataclass
class UserContext:
    """Validated user context from APIM."""
    user_id: str
    email: str
    roles: list[str]

    @property
    def can_read(self) -> bool:
        return "API.Read" in self.roles or "API.Write" in self.roles

    @property
    def can_write(self) -> bool:
        return "API.Write" in self.roles


async def get_user_context(
    x_user_id: str = Header(..., alias="X-User-Id"),
    x_user_email: str = Header("", alias="X-User-Email"),
    x_user_roles: str = Header("", alias="X-User-Roles"),
) -> UserContext:
    """
    Extract user context from APIM-forwarded headers.

    APIM has already validated the JWT - we trust these headers.
    """
    if not x_user_id:
        raise HTTPException(status_code=401, detail="User context missing")

    return UserContext(
        user_id=x_user_id,
        email=x_user_email,
        roles=x_user_roles.split(",") if x_user_roles else [],
    )


@app.get("/api/v1/protected")
async def protected_endpoint(user: UserContext = Depends(get_user_context)):
    """Endpoint that receives validated user context."""
    return {
        "message": f"Hello {user.email}",
        "user_id": user.user_id,
        "roles": user.roles,
        "can_write": user.can_write,
    }


@app.post("/api/v1/admin")
async def admin_endpoint(user: UserContext = Depends(get_user_context)):
    """Endpoint requiring write permission."""
    if not user.can_write:
        raise HTTPException(
            status_code=403,
            detail="API.Write role required for this operation"
        )
    return {"message": "Admin action completed", "user_id": user.user_id}
```

## Key Design Decisions

1. **Dual Audience**: Accepts both `api://client-id` and bare `client-id` formats
2. **Dual Issuer**: Supports both v2.0 and v1.0 Azure AD token formats
3. **Multiple Email Claims**: Tries `preferred_username`, `email`, and `upn` in order
4. **User-Based Rate Limiting**: Limits per user ID, not per subscription
5. **Header Deletion**: Removes Authorization before forwarding (backend trusts X-User-* headers)
6. **Structured Errors**: Consistent JSON error format with correlation IDs

## Testing the Policy

```bash
# Get a token from Azure AD
TOKEN=$(az account get-access-token \
  --resource api://your-api-client-id \
  --query accessToken -o tsv)

# Call the API through APIM
curl -X GET https://your-apim.azure-api.net/api/v1/protected \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Correlation-ID: test-correlation-123"

# Expected response headers:
# X-Correlation-ID: test-correlation-123
# X-RateLimit-Limit: 100
```

## Error Response Examples

**401 Unauthorized (missing or invalid token):**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Please provide a valid Azure AD token.",
    "status": 401,
    "correlation_id": "abc-123-def",
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

**429 Rate Limited:**
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please wait before retrying.",
    "status": 429,
    "correlation_id": "abc-123-def",
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```
