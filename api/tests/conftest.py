"""Shared pytest parts for api app."""
from __future__ import annotations
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app import app, get_producer

@pytest.fixture 
def fake_producer() -> MagicMock:
    # Stand in for Kafka producer - initalise the object at the start of the test.
    # Record calls to send() and flush ().
    return MagicMock()

@pytest.fixture
def client(fake_producer: MagicMock):
    # Test HTTP client with the real Kafka producer swapped out
    app.dependency_overrides[get_producer] = lambda: fake_producer
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()