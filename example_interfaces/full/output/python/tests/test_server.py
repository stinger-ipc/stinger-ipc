"""
Tests for Full server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from fullipc.server import FullServer
from fullipc.property import FullInitialPropertyValues
from fullipc.interface_types import *
from pyqttier.mock import MockConnection
import json


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(mock_connection):

    initial_property_values = FullInitialPropertyValues(
        favorite_number=42,
        favorite_foods=FullFavoriteFoodsProperty(
            drink="apples",
            slices_of_pizza=42,
            breakfast="apples",
        ),
        lunch_menu=FullLunchMenuProperty(
            monday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
            tuesday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
        ),
        family_name="apples",
        last_breakfast_time=datetime.now(UTC),
        last_birthdays=FullLastBirthdaysProperty(
            mom=datetime.now(UTC),
            dad=datetime.now(UTC),
            sister=datetime.now(UTC),
            brothers_age=42,
        ),
    )

    server = FullServer(mock_connection, "test_instance", initial_property_values)
    return server


class TestServer:
    """Tests for server initialization."""

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"

    def test_server_properties_initialization(self, server):
        """Test that server properties are initialized correctly."""

        assert hasattr(server, "favorite_number"), "Server missing property 'favorite_number'"

        assert server.favorite_number is not None, "Property 'favorite_number' not initialized properly"

        assert hasattr(server, "favorite_foods"), "Server missing property 'favorite_foods'"

        assert server.favorite_foods is not None, "Property 'favorite_foods' not initialized properly"

        assert hasattr(server, "lunch_menu"), "Server missing property 'lunch_menu'"

        assert server.lunch_menu is not None, "Property 'lunch_menu' not initialized properly"

        assert hasattr(server, "family_name"), "Server missing property 'family_name'"

        assert server.family_name is not None, "Property 'family_name' not initialized properly"

        assert hasattr(server, "last_breakfast_time"), "Server missing property 'last_breakfast_time'"

        assert server.last_breakfast_time is not None, "Property 'last_breakfast_time' not initialized properly"

        assert hasattr(server, "last_birthdays"), "Server missing property 'last_birthdays'"

        assert server.last_birthdays is not None, "Property 'last_birthdays' not initialized properly"
