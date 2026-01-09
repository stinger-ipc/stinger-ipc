"""
Tests for SignalOnly client.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

from signalonlyipc.client import SignalOnlyClient, DiscoveredInstance
from signalonlyipc.interface_types import *
from pyqttier.mock import MockConnection
import json
from typing import Dict, Any


def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def client(mock_connection):
    """Fixture providing a SignalOnly client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
    )
    client = SignalOnlyClient(
        connection=mock_connection,
        instance_info=mock_discovery,
    )
    return client


class TestClient:
    """Tests for client initialization."""

    def test_client_initializes(self, client):
        """Test that client initializes successfully."""
        assert client is not None, "Client failed to initialize"
        assert client.service_id == "test_instance", "Client service_id does not match expected value"
