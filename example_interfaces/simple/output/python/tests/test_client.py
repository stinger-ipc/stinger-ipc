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
        discovered_instance=mock_discovery,
    )
    return client


class TestClientInit:
    """Tests for client initialization."""

    def test_client_initializes(self, client):
        """Test that client initializes successfully."""
        assert client is not None, "Client failed to initialize"
        assert client.service_id == "test_instance", "Client service_id does not match expected value"
