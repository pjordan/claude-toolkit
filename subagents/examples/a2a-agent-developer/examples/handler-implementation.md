# Handler Implementation Example

An example session using the A2A Agent Developer subagent to create a document processing handler.

## User Request

```
Create an A2A handler called "analyze_text" that:
- Accepts a TextAnalysisRequest with text content and analysis_type (sentiment, summary, or keywords)
- Performs the requested analysis
- Returns a TextAnalysisResponse with results and confidence score
- Supports streaming for long text processing
- Includes comprehensive error handling
```

## Expected Response

Here's a complete implementation of the `analyze_text` handler with streaming support:

```python
from typing import AsyncGenerator
from pydantic import BaseModel, Field, validator
from enum import Enum
from a2a_sdk import A2AServer, Context, StreamingContext

# Enums and Models
class AnalysisType(str, Enum):
    SENTIMENT = "sentiment"
    SUMMARY = "summary"
    KEYWORDS = "keywords"

class TextAnalysisRequest(BaseModel):
    """Request model for text analysis."""
    text: str = Field(..., min_length=1, max_length=100000)
    analysis_type: AnalysisType
    options: dict = Field(default_factory=dict)

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v

class AnalysisResult(BaseModel):
    """Individual analysis result."""
    type: AnalysisType
    result: dict
    confidence: float = Field(..., ge=0.0, le=1.0)

class TextAnalysisResponse(BaseModel):
    """Response model for text analysis."""
    request_id: str
    analysis: AnalysisResult
    processing_time_ms: float
    metadata: dict = Field(default_factory=dict)

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    error_code: str
    details: dict = Field(default_factory=dict)

# Initialize A2A Server
a2a_server = A2AServer(
    name="text-analyzer",
    description="Analyzes text for sentiment, summaries, and keywords"
)

# Basic handler for quick analysis
@a2a_server.handler(
    "analyze_text",
    request_model=TextAnalysisRequest,
    response_model=TextAnalysisResponse
)
async def handle_analyze_text(
    request: TextAnalysisRequest,
    context: Context
) -> TextAnalysisResponse:
    """
    Analyze text based on the specified analysis type.

    Args:
        request: The analysis request with text and type
        context: A2A context with request metadata

    Returns:
        TextAnalysisResponse with analysis results
    """
    import time
    import uuid

    start_time = time.time()
    request_id = str(uuid.uuid4())

    try:
        # Perform analysis based on type
        if request.analysis_type == AnalysisType.SENTIMENT:
            result = await _analyze_sentiment(request.text, request.options)
        elif request.analysis_type == AnalysisType.SUMMARY:
            result = await _analyze_summary(request.text, request.options)
        elif request.analysis_type == AnalysisType.KEYWORDS:
            result = await _analyze_keywords(request.text, request.options)
        else:
            raise ValueError(f"Unknown analysis type: {request.analysis_type}")

        processing_time = (time.time() - start_time) * 1000

        return TextAnalysisResponse(
            request_id=request_id,
            analysis=AnalysisResult(
                type=request.analysis_type,
                result=result["data"],
                confidence=result["confidence"]
            ),
            processing_time_ms=processing_time,
            metadata={
                "text_length": len(request.text),
                "agent_id": context.agent_id if hasattr(context, 'agent_id') else "unknown"
            }
        )

    except ValueError as e:
        raise A2AError(
            error=str(e),
            error_code="INVALID_INPUT",
            details={"field": "analysis_type"}
        )
    except Exception as e:
        raise A2AError(
            error="Analysis failed",
            error_code="ANALYSIS_ERROR",
            details={"original_error": str(e)}
        )

# Streaming handler for long text processing
@a2a_server.streaming_handler(
    "analyze_text_stream",
    request_model=TextAnalysisRequest
)
async def handle_analyze_text_stream(
    request: TextAnalysisRequest,
    context: StreamingContext
) -> AsyncGenerator[str, None]:
    """
    Stream text analysis progress for long documents.

    Yields SSE-formatted progress updates and final results.
    """
    import json
    import asyncio

    text_chunks = _chunk_text(request.text, chunk_size=1000)
    total_chunks = len(text_chunks)

    # Stream progress updates
    for i, chunk in enumerate(text_chunks):
        progress = (i + 1) / total_chunks * 100

        yield f"data: {json.dumps({'type': 'progress', 'progress': progress, 'chunk': i + 1, 'total': total_chunks})}\n\n"

        # Process chunk (simulated delay for demo)
        await asyncio.sleep(0.1)

    # Perform full analysis
    if request.analysis_type == AnalysisType.SENTIMENT:
        result = await _analyze_sentiment(request.text, request.options)
    elif request.analysis_type == AnalysisType.SUMMARY:
        result = await _analyze_summary(request.text, request.options)
    else:
        result = await _analyze_keywords(request.text, request.options)

    # Stream final result
    yield f"data: {json.dumps({'type': 'complete', 'result': result})}\n\n"

# Helper functions
async def _analyze_sentiment(text: str, options: dict) -> dict:
    """Analyze text sentiment."""
    # Implementation would use NLP library or LLM
    return {
        "data": {
            "sentiment": "positive",
            "scores": {"positive": 0.85, "negative": 0.10, "neutral": 0.05}
        },
        "confidence": 0.85
    }

async def _analyze_summary(text: str, options: dict) -> dict:
    """Generate text summary."""
    max_length = options.get("max_length", 200)
    return {
        "data": {
            "summary": text[:max_length] + "...",
            "original_length": len(text),
            "summary_length": min(len(text), max_length)
        },
        "confidence": 0.90
    }

async def _analyze_keywords(text: str, options: dict) -> dict:
    """Extract keywords from text."""
    top_n = options.get("top_n", 10)
    # Implementation would use keyword extraction algorithm
    return {
        "data": {
            "keywords": ["example", "keyword", "extraction"],
            "count": 3
        },
        "confidence": 0.78
    }

def _chunk_text(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks for streaming processing."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

class A2AError(Exception):
    """Custom A2A error with structured response."""
    def __init__(self, error: str, error_code: str, details: dict = None):
        self.error = error
        self.error_code = error_code
        self.details = details or {}
        super().__init__(error)
```

## Key Design Decisions

1. **Pydantic Models**: All inputs and outputs are validated with Pydantic
2. **Streaming Support**: Separate handler for long text with progress updates
3. **Error Handling**: Custom exception class with structured error responses
4. **Async Pattern**: All handlers are async for non-blocking operation
5. **Separation of Concerns**: Analysis logic extracted to helper functions
6. **Configurability**: Options dict allows per-request customization

## Testing This Handler

```python
import pytest
from fastapi.testclient import TestClient

def test_analyze_sentiment():
    response = client.post("/a2a/analyze_text", json={
        "text": "I love this product!",
        "analysis_type": "sentiment"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["type"] == "sentiment"
    assert data["analysis"]["confidence"] > 0
```
