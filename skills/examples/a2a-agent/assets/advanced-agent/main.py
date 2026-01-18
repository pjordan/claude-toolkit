"""
Advanced A2A Agent Template
Demonstrates advanced patterns: streaming, error handling, middleware, and state management.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from a2a import A2AServer, Context, StreamingContext
from pydantic import BaseModel, Field
from typing import Optional, AsyncGenerator
import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Advanced A2A Agent",
    description="Demonstrates advanced a2a-sdk patterns and best practices",
    version="1.0.0"
)

# Initialize A2A server
a2a_server = A2AServer(
    app=app,
    agent_name="advanced-agent",
    agent_description="An advanced agent with streaming, error handling, and state management"
)


# In-memory state store (use Redis/DB in production)
class StateStore:
    def __init__(self):
        self.data = {}

    async def set(self, key: str, value: any):
        self.data[key] = {"value": value, "timestamp": datetime.now().isoformat()}

    async def get(self, key: str):
        return self.data.get(key)


state_store = StateStore()


# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} (took {duration:.2f}s)")

    return response


# Request/Response Models
class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")
    options: Optional[dict] = Field(default_factory=dict, description="Analysis options")


class AnalyzeResponse(BaseModel):
    word_count: int
    char_count: int
    sentiment: str
    processing_time: float


class StreamRequest(BaseModel):
    count: int = Field(10, description="Number of items to stream")
    delay: float = Field(0.5, description="Delay between items in seconds")


class StateRequest(BaseModel):
    key: str = Field(..., description="State key")
    value: Optional[str] = Field(None, description="Value to set (omit to get)")


# Handler: Text Analysis
@a2a_server.handler("analyze", request_model=AnalyzeRequest, response_model=AnalyzeResponse)
async def handle_analyze(request: AnalyzeRequest, context: Context) -> AnalyzeResponse:
    """Analyze text and return metrics."""
    start_time = datetime.now()

    try:
        # Simple sentiment analysis
        positive_words = ["good", "great", "excellent", "happy", "love"]
        negative_words = ["bad", "terrible", "awful", "sad", "hate"]

        text_lower = request.text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            sentiment = "positive"
        elif neg_count > pos_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        processing_time = (datetime.now() - start_time).total_seconds()

        return AnalyzeResponse(
            word_count=len(request.text.split()),
            char_count=len(request.text),
            sentiment=sentiment,
            processing_time=processing_time
        )

    except Exception as e:
        logger.error(f"Error in analyze handler: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# Handler: Streaming Response
@a2a_server.streaming_handler("stream", request_model=StreamRequest)
async def handle_stream(request: StreamRequest, context: StreamingContext) -> AsyncGenerator[str, None]:
    """Stream data back to client."""
    try:
        for i in range(request.count):
            await asyncio.sleep(request.delay)
            yield f"Item {i + 1} of {request.count}\n"

        yield "Stream complete!\n"

    except Exception as e:
        logger.error(f"Error in stream handler: {str(e)}")
        yield f"Error: {str(e)}\n"


# Handler: State Management
@a2a_server.handler("state", request_model=StateRequest, response_model=dict)
async def handle_state(request: StateRequest, context: Context) -> dict:
    """Manage agent state."""
    try:
        if request.value is not None:
            # Set state
            await state_store.set(request.key, request.value)
            return {
                "action": "set",
                "key": request.key,
                "success": True
            }
        else:
            # Get state
            result = await state_store.get(request.key)
            return {
                "action": "get",
                "key": request.key,
                "data": result
            }

    except Exception as e:
        logger.error(f"Error in state handler: {str(e)}")
        raise HTTPException(status_code=500, detail=f"State operation failed: {str(e)}")


# Health check with extended info
@app.get("/health")
async def health_check():
    """Extended health check endpoint."""
    return {
        "status": "healthy",
        "agent": "advanced-agent",
        "timestamp": datetime.now().isoformat(),
        "state_keys": len(state_store.data)
    }


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Return agent metrics."""
    return {
        "agent": "advanced-agent",
        "state_entries": len(state_store.data),
        "uptime": "calculated_in_production"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
