"""
Tests for Full client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from fullipc.client import FullClient, DiscoveredInstance
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
def client(mock_connection):
    """Fixture providing a Full client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=FullInitialPropertyValues(
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
                sister=None,
                brothers_age=42,
            ),
        ),
    )
    client = FullClient(
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

        assert hasattr(client, "favorite_number"), "Client missing property 'favorite_number'"

        assert client.favorite_number is not None, "Property 'favorite_number' not initialized properly"

        assert hasattr(client, "favorite_foods"), "Client missing property 'favorite_foods'"

        assert client.favorite_foods is not None, "Property 'favorite_foods' not initialized properly"

        assert hasattr(client, "lunch_menu"), "Client missing property 'lunch_menu'"

        assert client.lunch_menu is not None, "Property 'lunch_menu' not initialized properly"

        assert hasattr(client, "family_name"), "Client missing property 'family_name'"

        assert client.family_name is not None, "Property 'family_name' not initialized properly"

        assert hasattr(client, "last_breakfast_time"), "Client missing property 'last_breakfast_time'"

        assert client.last_breakfast_time is not None, "Property 'last_breakfast_time' not initialized properly"

        assert hasattr(client, "last_birthdays"), "Client missing property 'last_birthdays'"

        assert client.last_birthdays is not None, "Property 'last_birthdays' not initialized properly"

    def test_add_numbers_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "first": 42,
            "second": 42,
            "third": 42,
        }
        client.add_numbers(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'add_numbers' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/addNumbers"), "Incorrect topic for 'add_numbers' method call: {message.topic}"
        payload = json.loads(message.payload.decode())
        assert payload["first"] == kwargs["first"], "Payload argument 'first' does not match expected value"
        assert payload["second"] == kwargs["second"], "Payload argument 'second' does not match expected value"
        assert payload["third"] == kwargs["third"], "Payload argument 'third' does not match expected value"

    def test_do_something_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "task_to_do": "apples",
        }
        client.do_something(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'do_something' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/doSomething"), "Incorrect topic for 'do_something' method call: {message.topic}"
        payload = json.loads(message.payload.decode())
        assert payload["task_to_do"] == kwargs["task_to_do"], "Payload argument 'task_to_do' does not match expected value"

    def test_what_time_is_it_method_call_sends_request(self, mock_connection, client):
        kwargs = {}
        client.what_time_is_it(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'what_time_is_it' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/whatTimeIsIt"), "Incorrect topic for 'what_time_is_it' method call: {message.topic}"
        payload = json.loads(message.payload.decode())

    def test_hold_temperature_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "temperature_celsius": 3.14,
        }
        client.hold_temperature(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'hold_temperature' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/holdTemperature"), "Incorrect topic for 'hold_temperature' method call: {message.topic}"
        payload = json.loads(message.payload.decode())
        assert payload["temperature_celsius"] == kwargs["temperature_celsius"], "Payload argument 'temperature_celsius' does not match expected value"
