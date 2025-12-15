"""
Tests for Simple server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from simpleipc.server import SimpleServer
from simpleipc.property import SimpleInitialPropertyValues
from simpleipc.interface_types import *
from pyqttier.mock import MockConnection
import json


@pytest.fixture
def initial_property_values():
    initial_property_values = SimpleInitialPropertyValues(
        school="apples",
    )
    return initial_property_values


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(mock_connection, initial_property_values):
    server = SimpleServer(mock_connection, "test_instance", initial_property_values)
    yield server
    server.shutdown(timeout=0.1)


class TestServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestServerProperties:

    def test_server_school_property_initialization(self, server, initial_property_values):
        """Test that the school server property is initialized correctly."""
        assert hasattr(server, "school"), "Server missing property 'school'"
        assert server.school is not None, "Property 'school' not initialized properly"
        assert server.school == initial_property_values.school, "Property 'school' value does not match expected value"
