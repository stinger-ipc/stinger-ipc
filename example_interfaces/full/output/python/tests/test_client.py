"""
Tests for Full client.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from fullipc.client import FullClient, DiscoveredInstance
from fullipc.property import FullInitialPropertyValues
from fullipc.interface_types import *
from pyqttier.mock import MockConnection
import json
from typing import Dict, Any


def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)


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
def client(mock_connection, initial_property_values):
    """Fixture providing a Full client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=initial_property_values,
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


class TestClientProperties:

    def test_client_properties_initialization(self, client, initial_property_values):
        """Test that client properties are initialized correctly."""

        assert hasattr(client, "favorite_number"), "Client missing property 'favorite_number'"
        assert client.favorite_number is not None, "Property 'favorite_number' not initialized properly"
        assert client.favorite_number == initial_property_values.favorite_number, "Property 'favorite_number' value does not match expected value"

        assert hasattr(client, "favorite_foods"), "Client missing property 'favorite_foods'"
        assert client.favorite_foods is not None, "Property 'favorite_foods' not initialized properly"
        assert client.favorite_foods == initial_property_values.favorite_foods, "Property 'favorite_foods' value does not match expected value"

        assert hasattr(client, "lunch_menu"), "Client missing property 'lunch_menu'"
        assert client.lunch_menu is not None, "Property 'lunch_menu' not initialized properly"
        assert client.lunch_menu == initial_property_values.lunch_menu, "Property 'lunch_menu' value does not match expected value"

        assert hasattr(client, "family_name"), "Client missing property 'family_name'"
        assert client.family_name is not None, "Property 'family_name' not initialized properly"
        assert client.family_name == initial_property_values.family_name, "Property 'family_name' value does not match expected value"

        assert hasattr(client, "last_breakfast_time"), "Client missing property 'last_breakfast_time'"
        assert client.last_breakfast_time is not None, "Property 'last_breakfast_time' not initialized properly"
        assert client.last_breakfast_time == initial_property_values.last_breakfast_time, "Property 'last_breakfast_time' value does not match expected value"

        assert hasattr(client, "last_birthdays"), "Client missing property 'last_birthdays'"
        assert client.last_birthdays is not None, "Property 'last_birthdays' not initialized properly"
        assert client.last_birthdays == initial_property_values.last_birthdays, "Property 'last_birthdays' value does not match expected value"


class TestClientMethods:

    def test_add_numbers_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "first": 42,
            "second": 42,
            "third": 42,
        }  # type: Dict[str, Any]
        client.add_numbers(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'add_numbers' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/addNumbers"), f"Incorrect topic for 'add_numbers' method call: {message.topic}"

    def test_do_something_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "task_to_do": "apples",
        }  # type: Dict[str, Any]
        client.do_something(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'do_something' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/doSomething"), f"Incorrect topic for 'do_something' method call: {message.topic}"

    def test_what_time_is_it_method_call_sends_request(self, mock_connection, client):
        kwargs = {}  # type: Dict[str, Any]
        client.what_time_is_it(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'what_time_is_it' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/whatTimeIsIt"), f"Incorrect topic for 'what_time_is_it' method call: {message.topic}"

    def test_hold_temperature_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "temperature_celsius": 3.14,
        }  # type: Dict[str, Any]
        client.hold_temperature(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'hold_temperature' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/holdTemperature"), f"Incorrect topic for 'hold_temperature' method call: {message.topic}"
