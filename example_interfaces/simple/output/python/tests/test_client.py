"""
Tests for Simple client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from simpleipc.client import SimpleClient, DiscoveredInstance
from simpleipc.property import SimpleInitialPropertyValues
from simpleipc.interface_types import *
from pyqttier.mock import MockConnection
import json


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def client(mock_connection):
    """Fixture providing a Simple client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=SimpleInitialPropertyValues(
            school="apples",
        ),
    )
    client = SimpleClient(
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

    def test_client_properties_initialization(self, client):
        """Test that client properties are initialized correctly."""

        assert hasattr(client, "school"), "Client missing property 'school'"

        assert client.school is not None, "Property 'school' not initialized properly"

    def test_trade_numbers_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "your_number": 42,
        }
        client.trade_numbers(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'trade_numbers' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/tradeNumbers"), "Incorrect topic for 'trade_numbers' method call: {message.topic}"
        payload = json.loads(message.payload.decode())
        assert payload["your_number"] == kwargs["your_number"], "Payload argument 'your_number' does not match expected value"
