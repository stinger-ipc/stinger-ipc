"""
Tests for SignalOnly server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from signal_onlyipc.server import SignalOnlyServer
from signal_onlyipc.interface_types import *
from pyqttier.mock import MockConnection
import json


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(mock_connection):

    server = SignalOnlyServer(mock_connection, "test_instance")
    return server


class TestServer:
    """Tests for server initialization."""

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"

    def test_server_properties_initialization(self, server):
        """Test that server properties are initialized correctly."""
