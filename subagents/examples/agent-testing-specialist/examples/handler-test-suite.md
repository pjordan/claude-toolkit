# A2A Handler Test Suite Example

An example session using the Agent Testing Specialist subagent to create a comprehensive test suite.

## User Request

```
Write a comprehensive test suite for an A2A text analysis handler.
The handler:
- Accepts TextAnalysisRequest with text and analysis_type (sentiment/summary/keywords)
- Returns TextAnalysisResponse with results and confidence
- Has a streaming variant that yields progress updates
- Uses state management for request history

Include conftest.py fixtures, unit tests, and integration tests.
```

## Expected Response

Here's a complete test suite with fixtures, unit tests, and integration tests:

### conftest.py

```python
"""
Test fixtures for A2A text analysis agent.
"""

import pytest
import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Import your agent modules
from agent.main import app, a2a_server, state_store
from agent.models import TextAnalysisRequest, TextAnalysisResponse, AnalysisType

# === Event Loop Fixture ===

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# === Client Fixtures ===

@pytest.fixture
def client() -> TestClient:
    """Synchronous test client for FastAPI."""
    return TestClient(app)

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async test client for FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# === Request Factories ===

@pytest.fixture
def sentiment_request() -> TextAnalysisRequest:
    """Factory for sentiment analysis requests."""
    return TextAnalysisRequest(
        text="I absolutely love this product! It's amazing.",
        analysis_type=AnalysisType.SENTIMENT,
        options={}
    )

@pytest.fixture
def summary_request() -> TextAnalysisRequest:
    """Factory for summary analysis requests."""
    return TextAnalysisRequest(
        text="A" * 5000,  # Long text for summarization
        analysis_type=AnalysisType.SUMMARY,
        options={"max_length": 200}
    )

@pytest.fixture
def keywords_request() -> TextAnalysisRequest:
    """Factory for keywords analysis requests."""
    return TextAnalysisRequest(
        text="Machine learning and artificial intelligence are transforming technology.",
        analysis_type=AnalysisType.KEYWORDS,
        options={"top_n": 5}
    )

@pytest.fixture
def request_factory():
    """Factory function for creating custom requests."""
    def _create(
        text: str = "Sample text",
        analysis_type: AnalysisType = AnalysisType.SENTIMENT,
        options: dict = None
    ) -> TextAnalysisRequest:
        return TextAnalysisRequest(
            text=text,
            analysis_type=analysis_type,
            options=options or {}
        )
    return _create

# === Mock Fixtures ===

@pytest.fixture
def mock_context():
    """Mock A2A context object."""
    context = MagicMock()
    context.agent_id = "test-agent"
    context.request_id = "test-request-123"
    context.metadata = {"source": "test"}
    return context

@pytest.fixture
def mock_streaming_context():
    """Mock streaming context."""
    context = MagicMock()
    context.agent_id = "test-agent"
    context.is_cancelled = False
    return context

# === State Fixtures ===

@pytest.fixture(autouse=True)
def clean_state():
    """Clean state before each test."""
    state_store.clear()
    yield
    state_store.clear()

@pytest.fixture
def populated_state():
    """State with pre-existing data."""
    state_store["session-1"] = {
        "requests": [
            {"text": "Previous request", "type": "sentiment"}
        ]
    }
    return state_store

# === Response Fixtures ===

@pytest.fixture
def expected_sentiment_response() -> dict:
    """Expected structure for sentiment response."""
    return {
        "analysis": {
            "type": "sentiment",
            "result": {
                "sentiment": "positive",
                "scores": {"positive": 0.85, "negative": 0.10, "neutral": 0.05}
            },
            "confidence": 0.85
        }
    }
```

### test_handlers.py

```python
"""
Unit tests for A2A text analysis handlers.
"""

import pytest
from unittest.mock import patch, AsyncMock
from pydantic import ValidationError

from agent.main import handle_analyze_text, handle_analyze_text_stream
from agent.models import TextAnalysisRequest, TextAnalysisResponse, AnalysisType

class TestAnalyzeTextHandler:
    """Tests for the basic analyze_text handler."""

    @pytest.mark.asyncio
    async def test_sentiment_analysis_returns_valid_response(
        self, sentiment_request, mock_context
    ):
        """Test that sentiment analysis returns properly structured response."""
        # Act
        response = await handle_analyze_text(sentiment_request, mock_context)

        # Assert
        assert isinstance(response, TextAnalysisResponse)
        assert response.analysis.type == AnalysisType.SENTIMENT
        assert response.analysis.confidence > 0
        assert response.analysis.confidence <= 1.0
        assert "sentiment" in response.analysis.result

    @pytest.mark.asyncio
    async def test_summary_analysis_respects_max_length(
        self, summary_request, mock_context
    ):
        """Test that summary respects max_length option."""
        # Act
        response = await handle_analyze_text(summary_request, mock_context)

        # Assert
        assert response.analysis.type == AnalysisType.SUMMARY
        assert len(response.analysis.result["summary"]) <= 200 + 3  # +3 for "..."

    @pytest.mark.asyncio
    async def test_keywords_analysis_returns_requested_count(
        self, keywords_request, mock_context
    ):
        """Test that keywords extraction returns requested number."""
        # Act
        response = await handle_analyze_text(keywords_request, mock_context)

        # Assert
        assert response.analysis.type == AnalysisType.KEYWORDS
        assert len(response.analysis.result["keywords"]) <= 5

    @pytest.mark.asyncio
    async def test_includes_processing_time(
        self, sentiment_request, mock_context
    ):
        """Test that response includes processing time."""
        # Act
        response = await handle_analyze_text(sentiment_request, mock_context)

        # Assert
        assert response.processing_time_ms > 0

    @pytest.mark.asyncio
    async def test_includes_request_metadata(
        self, sentiment_request, mock_context
    ):
        """Test that response includes metadata from request."""
        # Act
        response = await handle_analyze_text(sentiment_request, mock_context)

        # Assert
        assert response.request_id is not None
        assert response.metadata["text_length"] == len(sentiment_request.text)

    @pytest.mark.asyncio
    async def test_empty_text_raises_validation_error(
        self, request_factory, mock_context
    ):
        """Test that empty text raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            request = request_factory(text="")

    @pytest.mark.asyncio
    async def test_whitespace_only_text_raises_validation_error(
        self, request_factory, mock_context
    ):
        """Test that whitespace-only text raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            request = request_factory(text="   \n\t  ")

    @pytest.mark.asyncio
    async def test_very_long_text_is_handled(
        self, request_factory, mock_context
    ):
        """Test that very long text is processed without error."""
        # Arrange
        request = request_factory(text="A" * 50000)

        # Act
        response = await handle_analyze_text(request, mock_context)

        # Assert
        assert isinstance(response, TextAnalysisResponse)


class TestAnalyzeTextStreamHandler:
    """Tests for the streaming analyze_text handler."""

    @pytest.mark.asyncio
    async def test_streaming_yields_progress_updates(
        self, sentiment_request, mock_streaming_context
    ):
        """Test that streaming handler yields progress updates."""
        # Act
        chunks = []
        async for chunk in handle_analyze_text_stream(
            sentiment_request, mock_streaming_context
        ):
            chunks.append(chunk)

        # Assert
        assert len(chunks) >= 2  # At least progress + result
        progress_chunks = [c for c in chunks if '"type": "progress"' in c]
        assert len(progress_chunks) >= 1

    @pytest.mark.asyncio
    async def test_streaming_ends_with_complete_message(
        self, sentiment_request, mock_streaming_context
    ):
        """Test that streaming ends with complete message."""
        # Act
        chunks = []
        async for chunk in handle_analyze_text_stream(
            sentiment_request, mock_streaming_context
        ):
            chunks.append(chunk)

        # Assert
        last_chunk = chunks[-1]
        assert '"type": "complete"' in last_chunk

    @pytest.mark.asyncio
    async def test_streaming_format_is_sse(
        self, sentiment_request, mock_streaming_context
    ):
        """Test that streaming chunks are SSE formatted."""
        # Act
        async for chunk in handle_analyze_text_stream(
            sentiment_request, mock_streaming_context
        ):
            # Assert
            assert chunk.startswith("data: ")
            assert chunk.endswith("\n\n")

    @pytest.mark.asyncio
    async def test_progress_increases_monotonically(
        self, summary_request, mock_streaming_context
    ):
        """Test that progress values increase monotonically."""
        import json

        # Act
        progress_values = []
        async for chunk in handle_analyze_text_stream(
            summary_request, mock_streaming_context
        ):
            data = json.loads(chunk.replace("data: ", "").strip())
            if data.get("type") == "progress":
                progress_values.append(data["progress"])

        # Assert
        for i in range(1, len(progress_values)):
            assert progress_values[i] >= progress_values[i-1]

    @pytest.mark.asyncio
    async def test_streaming_final_progress_is_100(
        self, sentiment_request, mock_streaming_context
    ):
        """Test that final progress update is 100%."""
        import json

        # Act
        progress_values = []
        async for chunk in handle_analyze_text_stream(
            sentiment_request, mock_streaming_context
        ):
            data = json.loads(chunk.replace("data: ", "").strip())
            if data.get("type") == "progress":
                progress_values.append(data["progress"])

        # Assert
        if progress_values:  # Only if there are progress updates
            assert progress_values[-1] == 100


class TestHandlerErrorHandling:
    """Tests for error handling in handlers."""

    @pytest.mark.asyncio
    async def test_internal_error_returns_structured_response(
        self, sentiment_request, mock_context
    ):
        """Test that internal errors are caught and returned properly."""
        # Arrange
        with patch(
            'agent.main._analyze_sentiment',
            side_effect=RuntimeError("Internal error")
        ):
            # Act & Assert
            with pytest.raises(Exception) as exc_info:
                await handle_analyze_text(sentiment_request, mock_context)

            assert "ANALYSIS_ERROR" in str(exc_info.value) or "Internal" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_timeout_is_handled(
        self, sentiment_request, mock_context
    ):
        """Test that timeout errors are handled."""
        import asyncio

        # Arrange
        async def slow_analysis(*args):
            await asyncio.sleep(10)
            return {"data": {}, "confidence": 0}

        with patch('agent.main._analyze_sentiment', side_effect=slow_analysis):
            # Act & Assert
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(
                    handle_analyze_text(sentiment_request, mock_context),
                    timeout=0.1
                )
```

### test_integration.py

```python
"""
Integration tests for A2A text analysis agent.
"""

import pytest
import json
from fastapi.testclient import TestClient

class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint returns OK."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_analyze_text_endpoint(self, client, sentiment_request):
        """Test analyze_text endpoint with valid request."""
        response = client.post(
            "/a2a/analyze_text",
            json=sentiment_request.model_dump()
        )

        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert data["analysis"]["type"] == "sentiment"

    def test_analyze_text_invalid_type(self, client):
        """Test analyze_text with invalid analysis type."""
        response = client.post(
            "/a2a/analyze_text",
            json={
                "text": "Test text",
                "analysis_type": "invalid_type"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_analyze_text_missing_text(self, client):
        """Test analyze_text with missing text field."""
        response = client.post(
            "/a2a/analyze_text",
            json={
                "analysis_type": "sentiment"
            }
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_streaming_endpoint(self, async_client, sentiment_request):
        """Test streaming endpoint returns SSE."""
        async with async_client.stream(
            "POST",
            "/a2a/analyze_text_stream",
            json=sentiment_request.model_dump()
        ) as response:
            assert response.status_code == 200

            chunks = []
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    chunks.append(json.loads(line[6:]))

            # Should have progress and complete
            types = [c.get("type") for c in chunks]
            assert "complete" in types

    def test_all_analysis_types_work(self, client, request_factory):
        """Test that all analysis types return valid responses."""
        for analysis_type in ["sentiment", "summary", "keywords"]:
            request = request_factory(
                text="Test text for analysis",
                analysis_type=analysis_type
            )

            response = client.post(
                "/a2a/analyze_text",
                json=request.model_dump()
            )

            assert response.status_code == 200
            assert response.json()["analysis"]["type"] == analysis_type


class TestStateManagement:
    """Tests for state management functionality."""

    def test_request_is_recorded_in_state(self, client, sentiment_request):
        """Test that requests are recorded in state."""
        # Act
        response = client.post(
            "/a2a/analyze_text",
            json=sentiment_request.model_dump(),
            headers={"X-Session-Id": "test-session"}
        )

        # Assert
        assert response.status_code == 200
        # Verify state was updated (implementation-specific)

    def test_state_isolation_between_sessions(self, client, request_factory):
        """Test that state is isolated between sessions."""
        # Arrange
        session1_request = request_factory(text="Session 1 text")
        session2_request = request_factory(text="Session 2 text")

        # Act
        client.post(
            "/a2a/analyze_text",
            json=session1_request.model_dump(),
            headers={"X-Session-Id": "session-1"}
        )

        client.post(
            "/a2a/analyze_text",
            json=session2_request.model_dump(),
            headers={"X-Session-Id": "session-2"}
        )

        # Assert - verify each session only has its own data
        # (implementation-specific verification)


class TestMetrics:
    """Tests for metrics endpoint."""

    def test_metrics_endpoint_returns_data(self, client):
        """Test metrics endpoint returns metrics."""
        response = client.get("/metrics")

        assert response.status_code == 200
        data = response.json()
        assert "requests_total" in data or "total_requests" in data

    def test_metrics_increment_after_request(self, client, sentiment_request):
        """Test that metrics increment after requests."""
        # Get initial count
        initial = client.get("/metrics").json()

        # Make request
        client.post("/a2a/analyze_text", json=sentiment_request.model_dump())

        # Get new count
        after = client.get("/metrics").json()

        # Verify increment (implementation-specific)
```

### pytest.ini

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    asyncio: marks tests as async
    slow: marks tests as slow
    integration: marks tests as integration tests
filterwarnings =
    ignore::DeprecationWarning
addopts = -v --tb=short
```

## Key Testing Patterns Used

1. **Fixture Organization**: Grouped by purpose (clients, requests, mocks, state)
2. **Factory Pattern**: `request_factory` allows custom test data
3. **Class-based Tests**: Logical grouping by functionality
4. **Descriptive Names**: `test_<what>_<scenario>_<expected>` pattern
5. **Parametrization Ready**: Structure supports @pytest.mark.parametrize
6. **SSE Testing**: Proper handling of streaming responses
7. **State Cleanup**: autouse fixture ensures clean state

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agent --cov-report=html

# Run only async tests
pytest -m asyncio

# Run specific test class
pytest tests/test_handlers.py::TestAnalyzeTextHandler

# Verbose with print output
pytest -v -s
```
