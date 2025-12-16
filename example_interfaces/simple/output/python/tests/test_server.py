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
from pyqttier.message import Message
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

    def test_school_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'school' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_school_value()

        published_list = mock_connection.find_published("simple/{}/property/school/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'school'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "simple/{}/property/school/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = SchoolProperty.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_dict.get("name") == initial_property_values.school, f"Payload 'name' does not match expected value of '{ initial_property_values.school }'"

    def test_school_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'school' updates the server property and calls callbacks."""
        received_data = None

        def callback(name):
            nonlocal received_data
            received_data = {
                "name": name,
            }

        server.on_school_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "name": "example",
        }
        prop_obj = SchoolProperty(**prop_data)
        incoming_msg = Message(
            topic="simple/{}/property/school/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json().encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_school.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is not None, "Callback for property 'school' was not called"


class TestServerSignals:

    def test_server_emit_person_entered(self, server, mock_connection):
        """Test that the server can emit the 'person_entered' signal."""
        signal_data = {
            "person": Person(name="apples", gender=Gender.MALE),
        }
        server.emit_person_entered(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("simple/{}/signal/personEntered".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'person_entered'"

        msg = published_list[0]
        expected_topic = "simple/{}/signal/personEntered".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = PersonEnteredSignalPayload.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_obj.person == signal_data["person"], f"Payload 'person' does not match expected struct value of '{ signal_data["person"]}'"
