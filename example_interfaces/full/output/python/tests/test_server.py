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
def initial_property_values():
    initial_property_values = FullInitialPropertyValues(
        favorite_number=42,
        favorite_foods=FavoriteFoodsProperty(
            drink="apples",
            slices_of_pizza=42,
            breakfast="apples",
        ),
        lunch_menu=LunchMenuProperty(
            monday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
            tuesday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
        ),
        family_name="apples",
        last_breakfast_time=datetime.now(UTC),
        last_birthdays=LastBirthdaysProperty(
            mom=datetime.now(UTC),
            dad=datetime.now(UTC),
            sister=datetime.now(UTC),
            brothers_age=42,
        ),
    )
    return initial_property_values


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(mock_connection, initial_property_values):
    server = FullServer(mock_connection, "test_instance", initial_property_values)
    yield server
    server.shutdown(timeout=0.1)


class TestServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestServerProperties:

    def test_server_favorite_number_property_initialization(self, server, initial_property_values):
        """Test that the favorite_number server property is initialized correctly."""
        assert hasattr(server, "favorite_number"), "Server missing property 'favorite_number'"
        assert server.favorite_number is not None, "Property 'favorite_number' not initialized properly"
        assert server.favorite_number == initial_property_values.favorite_number, "Property 'favorite_number' value does not match expected value"

    def test_server_favorite_foods_property_initialization(self, server, initial_property_values):
        """Test that the favorite_foods server property is initialized correctly."""
        assert hasattr(server, "favorite_foods"), "Server missing property 'favorite_foods'"
        assert server.favorite_foods is not None, "Property 'favorite_foods' not initialized properly"
        assert server.favorite_foods == initial_property_values.favorite_foods, "Property 'favorite_foods' value does not match expected value"

    def test_server_lunch_menu_property_initialization(self, server, initial_property_values):
        """Test that the lunch_menu server property is initialized correctly."""
        assert hasattr(server, "lunch_menu"), "Server missing property 'lunch_menu'"
        assert server.lunch_menu is not None, "Property 'lunch_menu' not initialized properly"
        assert server.lunch_menu == initial_property_values.lunch_menu, "Property 'lunch_menu' value does not match expected value"

    def test_server_family_name_property_initialization(self, server, initial_property_values):
        """Test that the family_name server property is initialized correctly."""
        assert hasattr(server, "family_name"), "Server missing property 'family_name'"
        assert server.family_name is not None, "Property 'family_name' not initialized properly"
        assert server.family_name == initial_property_values.family_name, "Property 'family_name' value does not match expected value"

    def test_server_last_breakfast_time_property_initialization(self, server, initial_property_values):
        """Test that the last_breakfast_time server property is initialized correctly."""
        assert hasattr(server, "last_breakfast_time"), "Server missing property 'last_breakfast_time'"
        assert server.last_breakfast_time is not None, "Property 'last_breakfast_time' not initialized properly"
        assert server.last_breakfast_time == initial_property_values.last_breakfast_time, "Property 'last_breakfast_time' value does not match expected value"

    def test_server_last_birthdays_property_initialization(self, server, initial_property_values):
        """Test that the last_birthdays server property is initialized correctly."""
        assert hasattr(server, "last_birthdays"), "Server missing property 'last_birthdays'"
        assert server.last_birthdays is not None, "Property 'last_birthdays' not initialized properly"
        assert server.last_birthdays == initial_property_values.last_birthdays, "Property 'last_birthdays' value does not match expected value"
