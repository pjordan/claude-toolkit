"""
Test suite for advanced A2A agent
"""
import pytest
from fastapi.testclient import TestClient
from main import app, state_store


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def clean_state():
    """Clean state before each test."""
    state_store.data.clear()
    yield
    state_store.data.clear()


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["agent"] == "advanced-agent"


def test_analyze_handler(client):
    """Test text analysis handler."""
    request_data = {
        "text": "This is a great and excellent day!",
        "options": {}
    }

    response = client.post("/a2a/analyze", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["word_count"] == 7
    assert data["sentiment"] == "positive"
    assert "processing_time" in data


def test_analyze_negative_sentiment(client):
    """Test negative sentiment detection."""
    request_data = {
        "text": "This is a terrible and awful situation.",
        "options": {}
    }

    response = client.post("/a2a/analyze", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["sentiment"] == "negative"


def test_state_set_and_get(client, clean_state):
    """Test state management."""
    # Set state
    set_request = {
        "key": "test_key",
        "value": "test_value"
    }

    response = client.post("/a2a/state", json=set_request)
    assert response.status_code == 200
    assert response.json()["action"] == "set"
    assert response.json()["success"] is True

    # Get state
    get_request = {
        "key": "test_key"
    }

    response = client.post("/a2a/state", json=get_request)
    assert response.status_code == 200
    assert response.json()["action"] == "get"
    assert response.json()["data"]["value"] == "test_value"


def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "agent" in response.json()
    assert response.json()["agent"] == "advanced-agent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
