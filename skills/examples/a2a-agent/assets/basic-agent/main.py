"""
Basic A2A Agent Template
A minimal working agent demonstrating core a2a-sdk and FastAPI patterns.
"""
from fastapi import FastAPI
from a2a import A2AServer, Context
from pydantic import BaseModel, Field
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Basic A2A Agent",
    description="A simple agent template for getting started with a2a-sdk",
    version="1.0.0"
)

# Initialize A2A server
a2a_server = A2AServer(
    app=app,
    agent_name="basic-agent",
    agent_description="A basic agent that demonstrates core A2A patterns"
)


# Define request/response models
class GreetRequest(BaseModel):
    name: str = Field(..., description="Name to greet")
    language: Optional[str] = Field("english", description="Language for greeting")


class GreetResponse(BaseModel):
    message: str = Field(..., description="Greeting message")
    agent: str = Field(..., description="Agent that generated the response")


# Register agent handler
@a2a_server.handler("greet", request_model=GreetRequest, response_model=GreetResponse)
async def handle_greet(request: GreetRequest, context: Context) -> GreetResponse:
    """Handle greeting requests with language support."""

    greetings = {
        "english": f"Hello, {request.name}!",
        "spanish": f"¡Hola, {request.name}!",
        "french": f"Bonjour, {request.name}!",
        "german": f"Guten Tag, {request.name}!"
    }

    message = greetings.get(request.language.lower(), f"Hello, {request.name}!")

    return GreetResponse(
        message=message,
        agent=context.agent_name
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "agent": "basic-agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
