# Example: REST API Endpoint Generation

This example demonstrates how the Code Generator subagent creates a REST API endpoint.

## User Request

```
Generate a REST API endpoint for user registration with email validation.
Language: Python/FastAPI
Include: input validation, error handling, and password hashing
```

## Expected Response Pattern

The Code Generator will produce:

### 1. Pydantic Models

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)
```

### 2. Endpoint Implementation

```python
from fastapi import APIRouter, HTTPException, status
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # Check if user exists
    if await user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = bcrypt.hash(user.password)

    # Create user
    new_user = await create_user(
        email=user.email,
        password_hash=hashed_password,
        name=user.name
    )

    return {"id": new_user.id, "email": new_user.email}
```

### 3. Dependencies Note

```
# requirements.txt additions
passlib[bcrypt]>=1.7.4
email-validator>=2.0.0
```

## Configuration Used

```json
{
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.3,
  "max_tokens": 4096
}
```

The low temperature (0.3) ensures consistent, predictable code generation.
