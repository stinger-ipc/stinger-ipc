"""
Tests for SignalOnly client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from signal_onlyipc.client import SignalOnlyClient, DiscoveredInstance
from signal_onlyipc.interface_types import *
from pyqttier.mock import MockConnection
import json


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

    def test_client_properties_initialization(self, client):
        """Test that client properties are initialized correctly."""
