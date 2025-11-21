import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def payload():
    return {
        "source_system": "SAP_CLOUD",
        "transaction_id": "TX-99",
        "total_amount": 500.00,
        "currency_code": "USD"
    }

@patch("app.services.ingest_service.IngestService.process_async")
# Test successful ingestion
def test_ingest_returns_202(mock_process, payload, client):
    response = client.post("/api/ingest", json=payload)

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
    assert response.json()["rule_applied"] == "FINANCE_PARTNER_X"

    # Ensure the background task was enqueued
    assert mock_process.called is True
