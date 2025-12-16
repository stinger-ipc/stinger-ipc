"""
Tests for testable server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from testableipc.server import TestableServer
from testableipc.property import TestableInitialPropertyValues
from testableipc.interface_types import *
from pyqttier.mock import MockConnection
from pyqttier.message import Message
import json
from pydantic import BaseModel
from typing import Any, Dict


def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)


@pytest.fixture
def initial_property_values():
    initial_property_values = TestableInitialPropertyValues(
        read_write_integer=42,
        read_only_integer=42,
        read_write_optional_integer=42,
        read_write_two_integers=ReadWriteTwoIntegersProperty(
            first=42,
            second=42,
        ),
        read_only_string="apples",
        read_write_string="apples",
        read_write_optional_string="apples",
        read_write_two_strings=ReadWriteTwoStringsProperty(
            first="apples",
            second="apples",
        ),
        read_write_struct=AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=Numbers.ONE,
            an_entry_object=Entry(key=42, value="apples"),
            date_and_time=datetime.now(UTC),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=Numbers.ONE,
            optional_entry_object=Entry(key=42, value="apples"),
            optional_date_time=datetime.now(UTC),
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[Numbers.ONE, Numbers.ONE],
            optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
            array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
            optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
        ),
        read_write_optional_struct=AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=Numbers.ONE,
            an_entry_object=Entry(key=42, value="apples"),
            date_and_time=datetime.now(UTC),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=Numbers.ONE,
            optional_entry_object=Entry(key=42, value="apples"),
            optional_date_time=datetime.now(UTC),
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[Numbers.ONE, Numbers.ONE],
            optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
            array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
            optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
        ),
        read_write_two_structs=ReadWriteTwoStructsProperty(
            first=AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
            second=AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
        ),
        read_only_enum=Numbers.ONE,
        read_write_enum=Numbers.ONE,
        read_write_optional_enum=Numbers.ONE,
        read_write_two_enums=ReadWriteTwoEnumsProperty(
            first=Numbers.ONE,
            second=Numbers.ONE,
        ),
        read_write_datetime=datetime.now(UTC),
        read_write_optional_datetime=datetime.now(UTC),
        read_write_two_datetimes=ReadWriteTwoDatetimesProperty(
            first=datetime.now(UTC),
            second=None,
        ),
        read_write_duration=timedelta(seconds=3536),
        read_write_optional_duration=None,
        read_write_two_durations=ReadWriteTwoDurationsProperty(
            first=timedelta(seconds=3536),
            second=None,
        ),
        read_write_binary=b"example binary data",
        read_write_optional_binary=b"example binary data",
        read_write_two_binaries=ReadWriteTwoBinariesProperty(
            first=b"example binary data",
            second=b"example binary data",
        ),
        read_write_list_of_strings=["apples", "foo"],
        read_write_lists=ReadWriteListsProperty(
            the_list=[Numbers.ONE, Numbers.ONE],
            optional_list=[datetime.now(UTC), datetime.now(UTC)],
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
    server = TestableServer(mock_connection, "test_instance", initial_property_values)
    yield server
    server.shutdown(timeout=0.1)


class TestServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestServerProperties:

    def test_server_read_write_integer_property_initialization(self, server, initial_property_values):
        """Test that the read_write_integer server property is initialized correctly."""
        assert hasattr(server, "read_write_integer"), "Server missing property 'read_write_integer'"
        assert server.read_write_integer is not None, "Property 'read_write_integer' not initialized properly"
        assert server.read_write_integer == initial_property_values.read_write_integer, "Property 'read_write_integer' value does not match expected value"

    def test_read_write_integer_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_integer' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_integer_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteInteger/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_integer'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteInteger/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteIntegerProperty(value=initial_property_values.read_write_integer)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_integer_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_integer' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_integer_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": 2020,
        }
        prop_obj = ReadWriteIntegerProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteInteger/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_integer.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_integer' was not called"

    def test_server_read_only_integer_property_initialization(self, server, initial_property_values):
        """Test that the read_only_integer server property is initialized correctly."""
        assert hasattr(server, "read_only_integer"), "Server missing property 'read_only_integer'"
        assert server.read_only_integer is not None, "Property 'read_only_integer' not initialized properly"
        assert server.read_only_integer == initial_property_values.read_only_integer, "Property 'read_only_integer' value does not match expected value"

    def test_read_only_integer_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_only_integer' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_only_integer_value()

        published_list = mock_connection.find_published("testable/{}/property/readOnlyInteger/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_only_integer'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readOnlyInteger/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadOnlyIntegerProperty(value=initial_property_values.read_only_integer)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_only_integer_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_only_integer' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_only_integer_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": 2020,
        }
        prop_obj = ReadOnlyIntegerProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readOnlyInteger/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_only_integer.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'read_only_integer' should not be updated"

    def test_server_read_write_optional_integer_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_integer server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_integer"), "Server missing property 'read_write_optional_integer'"
        assert server.read_write_optional_integer == initial_property_values.read_write_optional_integer, "Property 'read_write_optional_integer' value does not match expected value"

    def test_read_write_optional_integer_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_integer' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_integer_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalInteger/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_integer'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalInteger/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalIntegerProperty(value=initial_property_values.read_write_optional_integer)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_integer_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_integer' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_integer_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": 2020,
        }
        prop_obj = ReadWriteOptionalIntegerProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalInteger/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_integer.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_integer' was not called"

    def test_server_read_write_two_integers_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_integers server property is initialized correctly."""
        assert hasattr(server, "read_write_two_integers"), "Server missing property 'read_write_two_integers'"
        assert server.read_write_two_integers is not None, "Property 'read_write_two_integers' not initialized properly"
        assert server.read_write_two_integers == initial_property_values.read_write_two_integers, "Property 'read_write_two_integers' value does not match expected value"

    def test_read_write_two_integers_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_integers' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_integers_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoIntegers/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_integers'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoIntegers/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_integers
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_integers_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_integers' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_integers_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": 2020,
            "second": 42,
        }
        prop_obj = ReadWriteTwoIntegersProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoIntegers/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_integers.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_integers' was not called"

    def test_server_read_only_string_property_initialization(self, server, initial_property_values):
        """Test that the read_only_string server property is initialized correctly."""
        assert hasattr(server, "read_only_string"), "Server missing property 'read_only_string'"
        assert server.read_only_string is not None, "Property 'read_only_string' not initialized properly"
        assert server.read_only_string == initial_property_values.read_only_string, "Property 'read_only_string' value does not match expected value"

    def test_read_only_string_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_only_string' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_only_string_value()

        published_list = mock_connection.find_published("testable/{}/property/readOnlyString/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_only_string'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readOnlyString/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadOnlyStringProperty(value=initial_property_values.read_only_string)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_only_string_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_only_string' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_only_string_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": "example",
        }
        prop_obj = ReadOnlyStringProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readOnlyString/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_only_string.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'read_only_string' should not be updated"

    def test_server_read_write_string_property_initialization(self, server, initial_property_values):
        """Test that the read_write_string server property is initialized correctly."""
        assert hasattr(server, "read_write_string"), "Server missing property 'read_write_string'"
        assert server.read_write_string is not None, "Property 'read_write_string' not initialized properly"
        assert server.read_write_string == initial_property_values.read_write_string, "Property 'read_write_string' value does not match expected value"

    def test_read_write_string_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_string' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_string_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteString/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_string'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteString/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteStringProperty(value=initial_property_values.read_write_string)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_string_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_string' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_string_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": "example",
        }
        prop_obj = ReadWriteStringProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteString/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_string.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_string' was not called"

    def test_server_read_write_optional_string_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_string server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_string"), "Server missing property 'read_write_optional_string'"
        assert server.read_write_optional_string == initial_property_values.read_write_optional_string, "Property 'read_write_optional_string' value does not match expected value"

    def test_read_write_optional_string_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_string' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_string_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalString/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_string'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalString/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalStringProperty(value=initial_property_values.read_write_optional_string)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_string_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_string' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_string_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": "example",
        }
        prop_obj = ReadWriteOptionalStringProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalString/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_string.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_string' was not called"

    def test_server_read_write_two_strings_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_strings server property is initialized correctly."""
        assert hasattr(server, "read_write_two_strings"), "Server missing property 'read_write_two_strings'"
        assert server.read_write_two_strings is not None, "Property 'read_write_two_strings' not initialized properly"
        assert server.read_write_two_strings == initial_property_values.read_write_two_strings, "Property 'read_write_two_strings' value does not match expected value"

    def test_read_write_two_strings_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_strings' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_strings_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoStrings/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_strings'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoStrings/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_strings
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_strings_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_strings' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_strings_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": "example",
            "second": "apples",
        }
        prop_obj = ReadWriteTwoStringsProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoStrings/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_strings.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_strings' was not called"

    def test_server_read_write_struct_property_initialization(self, server, initial_property_values):
        """Test that the read_write_struct server property is initialized correctly."""
        assert hasattr(server, "read_write_struct"), "Server missing property 'read_write_struct'"
        assert server.read_write_struct is not None, "Property 'read_write_struct' not initialized properly"
        assert server.read_write_struct == initial_property_values.read_write_struct, "Property 'read_write_struct' value does not match expected value"

    def test_read_write_struct_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_struct' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_struct_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteStruct/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_struct'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteStruct/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteStructProperty(value=initial_property_values.read_write_struct)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_struct_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_struct' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_struct_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": AllTypes(
                the_bool=True,
                the_int=2020,
                the_number=1.0,
                the_str="example",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=2020, value="example"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=551),
                data=b"example binary data",
                optional_integer=2020,
                optional_string="example",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=2020, value="example"),
                optional_date_time=datetime.now(UTC),
                optional_duration=timedelta(seconds=2332),
                optional_binary=b"example binary data",
                array_of_integers=[2020, 42],
                optional_array_of_integers=[2020, 42],
                array_of_strings=["example", "apples"],
                optional_array_of_strings=["example", "apples"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=551), timedelta(seconds=3536)],
                optional_array_of_durations=[timedelta(seconds=551), timedelta(seconds=3536)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=2020, value="example"), Entry(key=42, value="apples")],
                optional_array_of_entry_objects=[Entry(key=2020, value="example"), Entry(key=42, value="apples")],
            ),
        }
        prop_obj = ReadWriteStructProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteStruct/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_struct.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_struct' was not called"

    def test_server_read_write_optional_struct_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_struct server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_struct"), "Server missing property 'read_write_optional_struct'"
        assert server.read_write_optional_struct == initial_property_values.read_write_optional_struct, "Property 'read_write_optional_struct' value does not match expected value"

    def test_read_write_optional_struct_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_struct' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_struct_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalStruct/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_struct'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalStruct/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalStructProperty(value=initial_property_values.read_write_optional_struct)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_struct_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_struct' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_struct_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": AllTypes(
                the_bool=True,
                the_int=2020,
                the_number=1.0,
                the_str="example",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=2020, value="example"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=551),
                data=b"example binary data",
                optional_integer=2020,
                optional_string="example",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=2020, value="example"),
                optional_date_time=None,
                optional_duration=timedelta(seconds=2332),
                optional_binary=b"example binary data",
                array_of_integers=[2020, 42],
                optional_array_of_integers=[2020, 42],
                array_of_strings=["example", "apples"],
                optional_array_of_strings=["example", "apples"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=551), timedelta(seconds=3536)],
                optional_array_of_durations=[timedelta(seconds=551), timedelta(seconds=3536)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=2020, value="example"), Entry(key=42, value="apples")],
                optional_array_of_entry_objects=[Entry(key=2020, value="example"), Entry(key=42, value="apples")],
            ),
        }
        prop_obj = ReadWriteOptionalStructProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalStruct/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_struct.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_struct' was not called"

    def test_server_read_write_two_structs_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_structs server property is initialized correctly."""
        assert hasattr(server, "read_write_two_structs"), "Server missing property 'read_write_two_structs'"
        assert server.read_write_two_structs is not None, "Property 'read_write_two_structs' not initialized properly"
        assert server.read_write_two_structs == initial_property_values.read_write_two_structs, "Property 'read_write_two_structs' value does not match expected value"

    def test_read_write_two_structs_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_structs' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_structs_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoStructs/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_structs'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoStructs/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_structs
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_structs_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_structs' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_structs_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": AllTypes(
                the_bool=True,
                the_int=2020,
                the_number=1.0,
                the_str="example",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=2020, value="example"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=551),
                data=b"example binary data",
                optional_integer=2020,
                optional_string="example",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=2020, value="example"),
                optional_date_time=None,
                optional_duration=timedelta(seconds=2332),
                optional_binary=b"example binary data",
                array_of_integers=[2020, 42],
                optional_array_of_integers=[2020, 42],
                array_of_strings=["example", "apples"],
                optional_array_of_strings=["example", "apples"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=551), timedelta(seconds=3536)],
                optional_array_of_durations=[timedelta(seconds=551), timedelta(seconds=3536)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=2020, value="example"), Entry(key=42, value="apples")],
                optional_array_of_entry_objects=[Entry(key=2020, value="example"), Entry(key=42, value="apples")],
            ),
            "second": AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
        }
        prop_obj = ReadWriteTwoStructsProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoStructs/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_structs.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_structs' was not called"

    def test_server_read_only_enum_property_initialization(self, server, initial_property_values):
        """Test that the read_only_enum server property is initialized correctly."""
        assert hasattr(server, "read_only_enum"), "Server missing property 'read_only_enum'"
        assert server.read_only_enum is not None, "Property 'read_only_enum' not initialized properly"
        assert server.read_only_enum == initial_property_values.read_only_enum, "Property 'read_only_enum' value does not match expected value"

    def test_read_only_enum_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_only_enum' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_only_enum_value()

        published_list = mock_connection.find_published("testable/{}/property/readOnlyEnum/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_only_enum'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readOnlyEnum/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadOnlyEnumProperty(value=initial_property_values.read_only_enum)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_only_enum_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_only_enum' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_only_enum_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": Numbers.ONE,
        }
        prop_obj = ReadOnlyEnumProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readOnlyEnum/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_only_enum.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'read_only_enum' should not be updated"

    def test_server_read_write_enum_property_initialization(self, server, initial_property_values):
        """Test that the read_write_enum server property is initialized correctly."""
        assert hasattr(server, "read_write_enum"), "Server missing property 'read_write_enum'"
        assert server.read_write_enum is not None, "Property 'read_write_enum' not initialized properly"
        assert server.read_write_enum == initial_property_values.read_write_enum, "Property 'read_write_enum' value does not match expected value"

    def test_read_write_enum_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_enum' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_enum_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteEnum/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_enum'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteEnum/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteEnumProperty(value=initial_property_values.read_write_enum)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_enum_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_enum' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_enum_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": Numbers.ONE,
        }
        prop_obj = ReadWriteEnumProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteEnum/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_enum.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_enum' was not called"

    def test_server_read_write_optional_enum_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_enum server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_enum"), "Server missing property 'read_write_optional_enum'"
        assert server.read_write_optional_enum == initial_property_values.read_write_optional_enum, "Property 'read_write_optional_enum' value does not match expected value"

    def test_read_write_optional_enum_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_enum' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_enum_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalEnum/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_enum'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalEnum/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalEnumProperty(value=initial_property_values.read_write_optional_enum)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_enum_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_enum' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_enum_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": Numbers.ONE,
        }
        prop_obj = ReadWriteOptionalEnumProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalEnum/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_enum.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_enum' was not called"

    def test_server_read_write_two_enums_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_enums server property is initialized correctly."""
        assert hasattr(server, "read_write_two_enums"), "Server missing property 'read_write_two_enums'"
        assert server.read_write_two_enums is not None, "Property 'read_write_two_enums' not initialized properly"
        assert server.read_write_two_enums == initial_property_values.read_write_two_enums, "Property 'read_write_two_enums' value does not match expected value"

    def test_read_write_two_enums_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_enums' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_enums_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoEnums/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_enums'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoEnums/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_enums
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_enums_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_enums' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_enums_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": Numbers.ONE,
            "second": Numbers.ONE,
        }
        prop_obj = ReadWriteTwoEnumsProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoEnums/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_enums.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_enums' was not called"

    def test_server_read_write_datetime_property_initialization(self, server, initial_property_values):
        """Test that the read_write_datetime server property is initialized correctly."""
        assert hasattr(server, "read_write_datetime"), "Server missing property 'read_write_datetime'"
        assert server.read_write_datetime is not None, "Property 'read_write_datetime' not initialized properly"
        assert server.read_write_datetime == initial_property_values.read_write_datetime, "Property 'read_write_datetime' value does not match expected value"

    def test_read_write_datetime_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_datetime' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_datetime_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteDatetime/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_datetime'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteDatetime/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteDatetimeProperty(value=initial_property_values.read_write_datetime)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_datetime_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_datetime' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_datetime_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": datetime.now(UTC),
        }
        prop_obj = ReadWriteDatetimeProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteDatetime/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_datetime.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_datetime' was not called"

    def test_server_read_write_optional_datetime_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_datetime server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_datetime"), "Server missing property 'read_write_optional_datetime'"
        assert server.read_write_optional_datetime == initial_property_values.read_write_optional_datetime, "Property 'read_write_optional_datetime' value does not match expected value"

    def test_read_write_optional_datetime_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_datetime' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_datetime_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalDatetime/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_datetime'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalDatetime/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalDatetimeProperty(value=initial_property_values.read_write_optional_datetime)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_datetime_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_datetime' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_datetime_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": datetime.now(UTC),
        }
        prop_obj = ReadWriteOptionalDatetimeProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalDatetime/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_datetime.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_datetime' was not called"

    def test_server_read_write_two_datetimes_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_datetimes server property is initialized correctly."""
        assert hasattr(server, "read_write_two_datetimes"), "Server missing property 'read_write_two_datetimes'"
        assert server.read_write_two_datetimes is not None, "Property 'read_write_two_datetimes' not initialized properly"
        assert server.read_write_two_datetimes == initial_property_values.read_write_two_datetimes, "Property 'read_write_two_datetimes' value does not match expected value"

    def test_read_write_two_datetimes_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_datetimes' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_datetimes_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoDatetimes/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_datetimes'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoDatetimes/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_datetimes
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_datetimes_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_datetimes' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_datetimes_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": datetime.now(UTC),
            "second": None,
        }
        prop_obj = ReadWriteTwoDatetimesProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoDatetimes/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_datetimes.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_datetimes' was not called"

    def test_server_read_write_duration_property_initialization(self, server, initial_property_values):
        """Test that the read_write_duration server property is initialized correctly."""
        assert hasattr(server, "read_write_duration"), "Server missing property 'read_write_duration'"
        assert server.read_write_duration is not None, "Property 'read_write_duration' not initialized properly"
        assert server.read_write_duration == initial_property_values.read_write_duration, "Property 'read_write_duration' value does not match expected value"

    def test_read_write_duration_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_duration' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_duration_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteDuration/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_duration'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteDuration/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteDurationProperty(value=initial_property_values.read_write_duration)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_duration_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_duration' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_duration_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": timedelta(seconds=551),
        }
        prop_obj = ReadWriteDurationProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteDuration/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_duration.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_duration' was not called"

    def test_server_read_write_optional_duration_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_duration server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_duration"), "Server missing property 'read_write_optional_duration'"
        assert server.read_write_optional_duration == initial_property_values.read_write_optional_duration, "Property 'read_write_optional_duration' value does not match expected value"

    def test_read_write_optional_duration_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_duration' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_duration_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalDuration/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_duration'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalDuration/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalDurationProperty(value=initial_property_values.read_write_optional_duration)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_duration_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_duration' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_duration_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": timedelta(seconds=2332),
        }
        prop_obj = ReadWriteOptionalDurationProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalDuration/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_duration.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_duration' was not called"

    def test_server_read_write_two_durations_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_durations server property is initialized correctly."""
        assert hasattr(server, "read_write_two_durations"), "Server missing property 'read_write_two_durations'"
        assert server.read_write_two_durations is not None, "Property 'read_write_two_durations' not initialized properly"
        assert server.read_write_two_durations == initial_property_values.read_write_two_durations, "Property 'read_write_two_durations' value does not match expected value"

    def test_read_write_two_durations_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_durations' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_durations_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoDurations/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_durations'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoDurations/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_durations
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_durations_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_durations' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_durations_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": timedelta(seconds=551),
            "second": None,
        }
        prop_obj = ReadWriteTwoDurationsProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoDurations/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_durations.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_durations' was not called"

    def test_server_read_write_binary_property_initialization(self, server, initial_property_values):
        """Test that the read_write_binary server property is initialized correctly."""
        assert hasattr(server, "read_write_binary"), "Server missing property 'read_write_binary'"
        assert server.read_write_binary is not None, "Property 'read_write_binary' not initialized properly"
        assert server.read_write_binary == initial_property_values.read_write_binary, "Property 'read_write_binary' value does not match expected value"

    def test_read_write_binary_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_binary' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_binary_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteBinary/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_binary'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteBinary/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteBinaryProperty(value=initial_property_values.read_write_binary)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_binary_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_binary' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_binary_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": b"example binary data",
        }
        prop_obj = ReadWriteBinaryProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteBinary/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_binary.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_binary' was not called"

    def test_server_read_write_optional_binary_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_binary server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_binary"), "Server missing property 'read_write_optional_binary'"
        assert server.read_write_optional_binary == initial_property_values.read_write_optional_binary, "Property 'read_write_optional_binary' value does not match expected value"

    def test_read_write_optional_binary_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_optional_binary' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_optional_binary_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteOptionalBinary/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_optional_binary'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteOptionalBinary/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteOptionalBinaryProperty(value=initial_property_values.read_write_optional_binary)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_optional_binary_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_optional_binary' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_optional_binary_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": b"example binary data",
        }
        prop_obj = ReadWriteOptionalBinaryProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalBinary/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_binary.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_optional_binary' was not called"

    def test_server_read_write_two_binaries_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_binaries server property is initialized correctly."""
        assert hasattr(server, "read_write_two_binaries"), "Server missing property 'read_write_two_binaries'"
        assert server.read_write_two_binaries is not None, "Property 'read_write_two_binaries' not initialized properly"
        assert server.read_write_two_binaries == initial_property_values.read_write_two_binaries, "Property 'read_write_two_binaries' value does not match expected value"

    def test_read_write_two_binaries_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_two_binaries' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_two_binaries_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteTwoBinaries/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_two_binaries'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteTwoBinaries/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_two_binaries
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_two_binaries_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_two_binaries' updates the server property and calls callbacks."""
        received_data = None

        def callback(first, second):
            nonlocal received_data
            received_data = {
                "first": first,
                "second": second,
            }

        server.on_read_write_two_binaries_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "first": b"example binary data",
            "second": b"example binary data",
        }
        prop_obj = ReadWriteTwoBinariesProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoBinaries/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_binaries.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_two_binaries' was not called"

    def test_server_read_write_list_of_strings_property_initialization(self, server, initial_property_values):
        """Test that the read_write_list_of_strings server property is initialized correctly."""
        assert hasattr(server, "read_write_list_of_strings"), "Server missing property 'read_write_list_of_strings'"
        assert server.read_write_list_of_strings is not None, "Property 'read_write_list_of_strings' not initialized properly"
        assert server.read_write_list_of_strings == initial_property_values.read_write_list_of_strings, "Property 'read_write_list_of_strings' value does not match expected value"

    def test_read_write_list_of_strings_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_list_of_strings' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_list_of_strings_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteListOfStrings/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_list_of_strings'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteListOfStrings/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ReadWriteListOfStringsProperty(value=initial_property_values.read_write_list_of_strings)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_list_of_strings_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_list_of_strings' updates the server property and calls callbacks."""
        received_data = None

        def callback(value):
            nonlocal received_data
            received_data = {
                "value": value,
            }

        server.on_read_write_list_of_strings_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "value": ["example", "apples"],
        }
        prop_obj = ReadWriteListOfStringsProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteListOfStrings/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_list_of_strings.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_list_of_strings' was not called"

    def test_server_read_write_lists_property_initialization(self, server, initial_property_values):
        """Test that the read_write_lists server property is initialized correctly."""
        assert hasattr(server, "read_write_lists"), "Server missing property 'read_write_lists'"
        assert server.read_write_lists is not None, "Property 'read_write_lists' not initialized properly"
        assert server.read_write_lists == initial_property_values.read_write_lists, "Property 'read_write_lists' value does not match expected value"

    def test_read_write_lists_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'read_write_lists' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_read_write_lists_value()

        published_list = mock_connection.find_published("testable/{}/property/readWriteLists/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'read_write_lists'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "testable/{}/property/readWriteLists/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.read_write_lists
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_read_write_lists_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'read_write_lists' updates the server property and calls callbacks."""
        received_data = None

        def callback(the_list, optional_list):
            nonlocal received_data
            received_data = {
                "the_list": the_list,
                "optional_list": optional_list,
            }

        server.on_read_write_lists_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "the_list": [Numbers.ONE, Numbers.ONE],
            "optional_list": [datetime.now(UTC), datetime.now(UTC)],
        }
        prop_obj = ReadWriteListsProperty(**prop_data)
        incoming_msg = Message(
            topic="testable/{}/property/readWriteLists/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_lists.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated
        assert received_data is not None, "Callback for property 'read_write_lists' was not called"


class TestServerSignals:

    def test_server_emit_empty(self, server, mock_connection):
        """Test that the server can emit the 'empty' signal."""
        signal_data = {}
        server.emit_empty(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/empty".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'empty'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/empty".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = EmptySignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_int(self, server, mock_connection):
        """Test that the server can emit the 'single_int' signal."""
        signal_data = {
            "value": 42,
        }
        server.emit_single_int(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleInt".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_int'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleInt".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleIntSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_int(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_int' signal."""
        signal_data = {
            "value": 42,
        }
        server.emit_single_optional_int(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalInt".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_int'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalInt".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalIntSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_integers(self, server, mock_connection):
        """Test that the server can emit the 'three_integers' signal."""
        signal_data = {
            "first": 42,
            "second": 42,
            "third": 42,
        }
        server.emit_three_integers(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeIntegers".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_integers'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeIntegers".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeIntegersSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_string(self, server, mock_connection):
        """Test that the server can emit the 'single_string' signal."""
        signal_data = {
            "value": "apples",
        }
        server.emit_single_string(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleString".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_string'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleString".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleStringSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_string(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_string' signal."""
        signal_data = {
            "value": "apples",
        }
        server.emit_single_optional_string(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalString".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_string'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalString".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalStringSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_strings(self, server, mock_connection):
        """Test that the server can emit the 'three_strings' signal."""
        signal_data = {
            "first": "apples",
            "second": "apples",
            "third": "apples",
        }
        server.emit_three_strings(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeStrings".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_strings'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeStrings".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeStringsSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_enum(self, server, mock_connection):
        """Test that the server can emit the 'single_enum' signal."""
        signal_data = {
            "value": Numbers.ONE,
        }
        server.emit_single_enum(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleEnum".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_enum'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleEnum".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleEnumSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_enum(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_enum' signal."""
        signal_data = {
            "value": Numbers.ONE,
        }
        server.emit_single_optional_enum(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalEnum".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_enum'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalEnum".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalEnumSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_enums(self, server, mock_connection):
        """Test that the server can emit the 'three_enums' signal."""
        signal_data = {
            "first": Numbers.ONE,
            "second": Numbers.ONE,
            "third": Numbers.ONE,
        }
        server.emit_three_enums(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeEnums".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_enums'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeEnums".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeEnumsSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_struct(self, server, mock_connection):
        """Test that the server can emit the 'single_struct' signal."""
        signal_data = {
            "value": AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=None,
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
        }
        server.emit_single_struct(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleStruct".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_struct'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleStruct".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleStructSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_struct(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_struct' signal."""
        signal_data = {
            "value": AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
        }
        server.emit_single_optional_struct(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalStruct".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_struct'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalStruct".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalStructSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_structs(self, server, mock_connection):
        """Test that the server can emit the 'three_structs' signal."""
        signal_data = {
            "first": AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
            "second": AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
            "third": AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=42, value="apples"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=42, value="apples"),
                optional_date_time=datetime.now(UTC),
                optional_duration=None,
                optional_binary=b"example binary data",
                array_of_integers=[42, 2022],
                optional_array_of_integers=[42, 2022],
                array_of_strings=["apples", "foo"],
                optional_array_of_strings=["apples", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            ),
        }
        server.emit_three_structs(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeStructs".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_structs'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeStructs".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeStructsSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_date_time(self, server, mock_connection):
        """Test that the server can emit the 'single_date_time' signal."""
        signal_data = {
            "value": datetime.now(UTC),
        }
        server.emit_single_date_time(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleDateTime".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_date_time'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleDateTime".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleDateTimeSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_datetime(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_datetime' signal."""
        signal_data = {
            "value": datetime.now(UTC),
        }
        server.emit_single_optional_datetime(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalDatetime".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_datetime'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalDatetime".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalDatetimeSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_date_times(self, server, mock_connection):
        """Test that the server can emit the 'three_date_times' signal."""
        signal_data = {
            "first": datetime.now(UTC),
            "second": datetime.now(UTC),
            "third": datetime.now(UTC),
        }
        server.emit_three_date_times(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeDateTimes".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_date_times'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeDateTimes".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeDateTimesSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_duration(self, server, mock_connection):
        """Test that the server can emit the 'single_duration' signal."""
        signal_data = {
            "value": timedelta(seconds=3536),
        }
        server.emit_single_duration(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleDuration".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_duration'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleDuration".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleDurationSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_duration(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_duration' signal."""
        signal_data = {
            "value": None,
        }
        server.emit_single_optional_duration(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalDuration".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_duration'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalDuration".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalDurationSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_durations(self, server, mock_connection):
        """Test that the server can emit the 'three_durations' signal."""
        signal_data = {
            "first": timedelta(seconds=3536),
            "second": timedelta(seconds=3536),
            "third": None,
        }
        server.emit_three_durations(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeDurations".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_durations'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeDurations".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeDurationsSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_binary(self, server, mock_connection):
        """Test that the server can emit the 'single_binary' signal."""
        signal_data = {
            "value": b"example binary data",
        }
        server.emit_single_binary(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleBinary".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_binary'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleBinary".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleBinarySignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_binary(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_binary' signal."""
        signal_data = {
            "value": b"example binary data",
        }
        server.emit_single_optional_binary(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalBinary".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_binary'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalBinary".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalBinarySignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_binaries(self, server, mock_connection):
        """Test that the server can emit the 'three_binaries' signal."""
        signal_data = {
            "first": b"example binary data",
            "second": b"example binary data",
            "third": b"example binary data",
        }
        server.emit_three_binaries(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeBinaries".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_binaries'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeBinaries".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeBinariesSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_array_of_integers(self, server, mock_connection):
        """Test that the server can emit the 'single_array_of_integers' signal."""
        signal_data = {
            "values": [42, 2022],
        }
        server.emit_single_array_of_integers(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleArrayOfIntegers".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_array_of_integers'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleArrayOfIntegers".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleArrayOfIntegersSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_array_of_strings(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_array_of_strings' signal."""
        signal_data = {
            "values": ["apples", "foo"],
        }
        server.emit_single_optional_array_of_strings(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalArrayOfStrings".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_array_of_strings'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalArrayOfStrings".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalArrayOfStringsSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_array_of_every_type(self, server, mock_connection):
        """Test that the server can emit the 'array_of_every_type' signal."""
        signal_data = {
            "first_of_integers": [42, 2022],
            "second_of_floats": [3.14, 1.0],
            "third_of_strings": ["apples", "foo"],
            "fourth_of_enums": [Numbers.ONE, Numbers.ONE],
            "fifth_of_structs": [Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
            "sixth_of_datetimes": [datetime.now(UTC), datetime.now(UTC)],
            "seventh_of_durations": [timedelta(seconds=3536), timedelta(seconds=975)],
            "eighth_of_binaries": [b"example binary data", b"example binary data"],
        }
        server.emit_array_of_every_type(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/arrayOfEveryType".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'array_of_every_type'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/arrayOfEveryType".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ArrayOfEveryTypeSignalPayload(**signal_data)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"
