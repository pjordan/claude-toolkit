# Azure APIM Policy Patterns

Comprehensive reference for Azure API Management policies when working with FastAPI backends.

## Policy Structure

```xml
<policies>
    <inbound>
        <!-- Policies applied before request is forwarded to backend -->
        <base />
    </inbound>
    <backend>
        <!-- Policies applied when forwarding to backend -->
        <base />
    </backend>
    <outbound>
        <!-- Policies applied to response before sending to client -->
        <base />
    </outbound>
    <on-error>
        <!-- Policies applied when an error occurs -->
        <base />
    </on-error>
</policies>
```

## Authentication Policies

### Subscription Key Validation

```xml
<!-- Require subscription key (default behavior) -->
<inbound>
    <base />
    <!-- Key can be in header or query parameter -->
    <!-- Header: Ocp-Apim-Subscription-Key -->
    <!-- Query: subscription-key -->
</inbound>
```

### JWT Validation (Azure AD / Entra ID)

```xml
<inbound>
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="Unauthorized">
        <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration" />
        <audiences>
            <audience>api://my-api-client-id</audience>
        </audiences>
        <issuers>
            <issuer>https://login.microsoftonline.com/{tenant-id}/v2.0</issuer>
            <issuer>https://sts.windows.net/{tenant-id}/</issuer>
        </issuers>
        <required-claims>
            <claim name="roles" match="any">
                <value>API.Read</value>
                <value>API.ReadWrite</value>
            </claim>
        </required-claims>
    </validate-jwt>
</inbound>
```

### Extract and Forward JWT Claims

```xml
<inbound>
    <validate-jwt header-name="Authorization" output-token-variable-name="jwt">
        <!-- validation config -->
    </validate-jwt>

    <!-- Forward claims to backend -->
    <set-header name="X-User-Id" exists-action="override">
        <value>@(((Jwt)context.Variables["jwt"]).Claims.GetValueOrDefault("oid", ""))</value>
    </set-header>
    <set-header name="X-User-Email" exists-action="override">
        <value>@(((Jwt)context.Variables["jwt"]).Claims.GetValueOrDefault("email", ""))</value>
    </set-header>
    <set-header name="X-User-Roles" exists-action="override">
        <value>@(string.Join(",", ((Jwt)context.Variables["jwt"]).Claims.GetValueOrDefault("roles", new string[0])))</value>
    </set-header>
</inbound>
```

### Client Certificate (mTLS)

```xml
<inbound>
    <choose>
        <when condition="@(context.Request.Certificate == null)">
            <return-response>
                <set-status code="403" reason="Client certificate required" />
                <set-body>{"error": "Client certificate is required"}</set-body>
            </return-response>
        </when>
        <when condition="@(!context.Request.Certificate.Verify())">
            <return-response>
                <set-status code="403" reason="Invalid certificate" />
                <set-body>{"error": "Client certificate validation failed"}</set-body>
            </return-response>
        </when>
        <when condition="@(!context.Deployment.Certificates.Any(c => c.Value.Thumbprint == context.Request.Certificate.Thumbprint))">
            <return-response>
                <set-status code="403" reason="Unknown certificate" />
                <set-body>{"error": "Client certificate not recognized"}</set-body>
            </return-response>
        </when>
    </choose>

    <!-- Forward certificate info -->
    <set-header name="X-Client-Cert-Thumbprint" exists-action="override">
        <value>@(context.Request.Certificate.Thumbprint)</value>
    </set-header>
    <set-header name="X-Client-Cert-Subject" exists-action="override">
        <value>@(context.Request.Certificate.Subject)</value>
    </set-header>
</inbound>
```

### Basic Authentication

```xml
<inbound>
    <authentication-basic username="{{backend-username}}" password="{{backend-password}}" />
</inbound>
```

### Managed Identity Authentication (to Azure services)

```xml
<inbound>
    <!-- Get token for Azure Resource using managed identity -->
    <authentication-managed-identity resource="https://management.azure.com/" output-token-variable-name="msi-token" />
    <set-header name="Authorization" exists-action="override">
        <value>@("Bearer " + (string)context.Variables["msi-token"])</value>
    </set-header>
</inbound>
```

## Rate Limiting Policies

### Rate Limit by Subscription

```xml
<inbound>
    <rate-limit-by-key
        calls="100"
        renewal-period="60"
        counter-key="@(context.Subscription.Id)"
        increment-condition="@(context.Response.StatusCode >= 200 && context.Response.StatusCode < 400)" />
</inbound>
```

### Rate Limit by IP Address

```xml
<inbound>
    <rate-limit-by-key
        calls="20"
        renewal-period="60"
        counter-key="@(context.Request.IpAddress)" />
</inbound>
```

### Rate Limit by User (from JWT)

```xml
<inbound>
    <rate-limit-by-key
        calls="50"
        renewal-period="60"
        counter-key="@(context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()?.Claims.GetValueOrDefault("oid", context.Request.IpAddress))" />
</inbound>
```

### Quota by Subscription

```xml
<inbound>
    <quota-by-key
        calls="10000"
        bandwidth="50000000"
        renewal-period="2592000"
        counter-key="@(context.Subscription.Id)" />
</inbound>
```

### Rate Limit Headers in Response

```xml
<outbound>
    <set-header name="X-RateLimit-Limit" exists-action="override">
        <value>100</value>
    </set-header>
    <set-header name="X-RateLimit-Remaining" exists-action="override">
        <value>@{
            var remaining = context.Variables.GetValueOrDefault<int>("remainingCalls", 0);
            return remaining.ToString();
        }</value>
    </set-header>
    <set-header name="X-RateLimit-Reset" exists-action="override">
        <value>@{
            var reset = DateTime.UtcNow.AddMinutes(1);
            return ((DateTimeOffset)reset).ToUnixTimeSeconds().ToString();
        }</value>
    </set-header>
</outbound>
```

## Caching Policies

### Response Caching

```xml
<inbound>
    <cache-lookup vary-by-developer="false" vary-by-developer-groups="false" downstream-caching-type="none">
        <vary-by-header>Accept</vary-by-header>
        <vary-by-header>Accept-Language</vary-by-header>
        <vary-by-query-parameter>version</vary-by-query-parameter>
        <vary-by-query-parameter>format</vary-by-query-parameter>
    </cache-lookup>
</inbound>

<outbound>
    <cache-store duration="300" />
</outbound>
```

### Conditional Caching

```xml
<outbound>
    <choose>
        <when condition="@(context.Response.StatusCode == 200)">
            <cache-store duration="300" />
        </when>
    </choose>
</outbound>
```

### Cache Value Lookup

```xml
<inbound>
    <cache-lookup-value key="@("config-" + context.Api.Id)" variable-name="cached-config" />
    <choose>
        <when condition="@(!context.Variables.ContainsKey("cached-config"))">
            <!-- Fetch and cache config -->
            <send-request mode="new" response-variable-name="config-response">
                <set-url>https://config-service/api/config</set-url>
            </send-request>
            <set-variable name="cached-config" value="@(((IResponse)context.Variables["config-response"]).Body.As<string>())" />
            <cache-store-value key="@("config-" + context.Api.Id)" value="@((string)context.Variables["cached-config"])" duration="3600" />
        </when>
    </choose>
</inbound>
```

## Transformation Policies

### Request Body Transformation

```xml
<inbound>
    <set-body>@{
        var body = context.Request.Body.As<JObject>();
        body["timestamp"] = DateTime.UtcNow.ToString("o");
        body["requestId"] = context.RequestId;
        body["source"] = "apim";
        return body.ToString();
    }</set-body>
</inbound>
```

### Response Body Transformation

```xml
<outbound>
    <set-body>@{
        var body = context.Response.Body.As<JObject>();

        // Remove sensitive fields
        body.Remove("internalId");
        body.Remove("debugInfo");

        // Add metadata
        body["apiVersion"] = "1.0";
        body["processedAt"] = DateTime.UtcNow.ToString("o");

        return body.ToString();
    }</set-body>
</outbound>
```

### XML to JSON Conversion

```xml
<outbound>
    <xml-to-json kind="direct" apply="always" consider-accept-header="true" />
</outbound>
```

### JSON to XML Conversion

```xml
<inbound>
    <json-to-xml apply="always" consider-accept-header="true" />
</inbound>
```

### URL Rewrite

```xml
<inbound>
    <rewrite-uri template="/api/v2/{path}" />
</inbound>
```

### Header Manipulation

```xml
<inbound>
    <!-- Add headers -->
    <set-header name="X-Correlation-ID" exists-action="skip">
        <value>@(Guid.NewGuid().ToString())</value>
    </set-header>

    <!-- Forward original host -->
    <set-header name="X-Forwarded-Host" exists-action="override">
        <value>@(context.Request.OriginalUrl.Host)</value>
    </set-header>
</inbound>

<outbound>
    <!-- Remove sensitive headers -->
    <set-header name="X-Powered-By" exists-action="delete" />
    <set-header name="Server" exists-action="delete" />
    <set-header name="X-AspNet-Version" exists-action="delete" />
</outbound>
```

## Backend Policies

### Backend Selection

```xml
<backend>
    <choose>
        <when condition="@(context.Request.Headers.GetValueOrDefault("X-Region", "") == "eu")">
            <set-backend-service base-url="https://api-eu.example.com" />
        </when>
        <when condition="@(context.Request.Headers.GetValueOrDefault("X-Region", "") == "us")">
            <set-backend-service base-url="https://api-us.example.com" />
        </when>
        <otherwise>
            <set-backend-service base-url="https://api-default.example.com" />
        </otherwise>
    </choose>
</backend>
```

### Circuit Breaker

```xml
<backend>
    <circuit-breaker
        rule-name="backend-circuit"
        max-failures="5"
        reset-timeout="30"
        trip-duration="60" />
</backend>
```

### Retry Policy

```xml
<backend>
    <retry condition="@(context.Response.StatusCode == 503 || context.Response.StatusCode == 502)"
           count="3"
           interval="1"
           delta="1"
           max-interval="10"
           first-fast-retry="true">
        <forward-request buffer-request-body="true" />
    </retry>
</backend>
```

### Load Balancing

```xml
<backend>
    <set-backend-service backend-id="backend-pool" />
</backend>

<!-- Backend pool defined in APIM configuration -->
```

## Error Handling

### Standard Error Response

```xml
<on-error>
    <set-header name="Content-Type" exists-action="override">
        <value>application/json</value>
    </set-header>
    <set-body>@{
        return new JObject(
            new JProperty("error", new JObject(
                new JProperty("code", context.Response.StatusCode),
                new JProperty("message", context.LastError.Message),
                new JProperty("reason", context.LastError.Reason),
                new JProperty("correlationId", context.RequestId),
                new JProperty("timestamp", DateTime.UtcNow.ToString("o"))
            ))
        ).ToString();
    }</set-body>
</on-error>
```

### Custom Error Codes

```xml
<on-error>
    <choose>
        <when condition="@(context.LastError.Source == "jwt-validation")">
            <set-status code="401" reason="Unauthorized" />
            <set-body>{"error": "Invalid or expired token"}</set-body>
        </when>
        <when condition="@(context.LastError.Source == "rate-limit")">
            <set-status code="429" reason="Too Many Requests" />
            <set-header name="Retry-After" exists-action="override">
                <value>60</value>
            </set-header>
            <set-body>{"error": "Rate limit exceeded", "retryAfter": 60}</set-body>
        </when>
        <when condition="@(context.Response.StatusCode >= 500)">
            <set-body>{"error": "Service temporarily unavailable"}</set-body>
        </when>
    </choose>
</on-error>
```

## Logging and Tracing

### Log to Event Hub

```xml
<inbound>
    <log-to-eventhub logger-id="my-event-hub">@{
        return new JObject(
            new JProperty("timestamp", DateTime.UtcNow.ToString("o")),
            new JProperty("requestId", context.RequestId),
            new JProperty("method", context.Request.Method),
            new JProperty("url", context.Request.Url.ToString()),
            new JProperty("clientIp", context.Request.IpAddress),
            new JProperty("subscriptionId", context.Subscription.Id)
        ).ToString();
    }</log-to-eventhub>
</inbound>

<outbound>
    <log-to-eventhub logger-id="my-event-hub">@{
        return new JObject(
            new JProperty("timestamp", DateTime.UtcNow.ToString("o")),
            new JProperty("requestId", context.RequestId),
            new JProperty("statusCode", context.Response.StatusCode),
            new JProperty("duration", context.Elapsed.TotalMilliseconds)
        ).ToString();
    }</log-to-eventhub>
</outbound>
```

### Application Insights Correlation

```xml
<inbound>
    <set-header name="Request-Id" exists-action="skip">
        <value>@("|" + context.RequestId + ".")</value>
    </set-header>
    <set-header name="traceparent" exists-action="skip">
        <value>@("00-" + context.RequestId.Replace("-","") + "-" + context.RequestId.Substring(0,16).Replace("-","") + "-01")</value>
    </set-header>
</inbound>
```

## CORS Policies

### Basic CORS

```xml
<inbound>
    <cors allow-credentials="true">
        <allowed-origins>
            <origin>https://app.example.com</origin>
            <origin>https://admin.example.com</origin>
        </allowed-origins>
        <allowed-methods preflight-result-max-age="300">
            <method>GET</method>
            <method>POST</method>
            <method>PUT</method>
            <method>DELETE</method>
            <method>OPTIONS</method>
        </allowed-methods>
        <allowed-headers>
            <header>Content-Type</header>
            <header>Authorization</header>
            <header>X-Correlation-ID</header>
        </allowed-headers>
        <expose-headers>
            <header>X-RateLimit-Remaining</header>
            <header>X-Correlation-ID</header>
        </expose-headers>
    </cors>
</inbound>
```

## Policy Expressions Reference

### Common Context Properties

```csharp
// Request properties
context.Request.Method           // HTTP method
context.Request.Url              // Request URL
context.Request.IpAddress        // Client IP
context.Request.Headers          // Request headers
context.Request.Body             // Request body

// Response properties
context.Response.StatusCode      // HTTP status code
context.Response.Headers         // Response headers
context.Response.Body            // Response body

// Subscription/Product
context.Subscription.Id          // Subscription ID
context.Subscription.Name        // Subscription name
context.Product.Name             // Product name

// API
context.Api.Id                   // API ID
context.Api.Name                 // API name
context.Api.Version              // API version
context.Operation.Id             // Operation ID

// Other
context.RequestId                // Unique request ID
context.Elapsed                  // Time elapsed
context.Deployment.Region        // APIM region
```

### Useful Expressions

```csharp
// Get header value
context.Request.Headers.GetValueOrDefault("X-Custom", "default")

// Parse JWT from header
context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()

// Check if query parameter exists
context.Request.Url.Query.ContainsKey("param")

// Get query parameter value
context.Request.Url.Query.GetValueOrDefault("param", "")

// Parse JSON body
context.Request.Body.As<JObject>()

// Generate GUID
Guid.NewGuid().ToString()

// Current time
DateTime.UtcNow.ToString("o")
```
