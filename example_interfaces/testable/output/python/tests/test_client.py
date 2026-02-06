"""
Tests for testable client.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC

from testableipc.client import TestableClient, DiscoveredInstance
from testableipc.property import TestableInitialPropertyValues
from testableipc.interface_types import *
from pyqttier.mock import MockConnection
import json
from typing import Dict, Any


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
            second=datetime.now(UTC),
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
def client(mock_connection, initial_property_values):
    """Fixture providing a testable client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=initial_property_values,
    )
    client = TestableClient(
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

        assert hasattr(client, "read_write_integer"), "Client missing property 'read_write_integer'"
        assert client.read_write_integer is not None, "Property 'read_write_integer' not initialized properly"
        assert client.read_write_integer == initial_property_values.read_write_integer, "Property 'read_write_integer' value does not match expected value"

        assert hasattr(client, "read_only_integer"), "Client missing property 'read_only_integer'"
        assert client.read_only_integer is not None, "Property 'read_only_integer' not initialized properly"
        assert client.read_only_integer == initial_property_values.read_only_integer, "Property 'read_only_integer' value does not match expected value"

        assert hasattr(client, "read_write_optional_integer"), "Client missing property 'read_write_optional_integer'"
        assert client.read_write_optional_integer == initial_property_values.read_write_optional_integer, "Property 'read_write_optional_integer' value does not match expected value"

        assert hasattr(client, "read_write_two_integers"), "Client missing property 'read_write_two_integers'"
        assert client.read_write_two_integers is not None, "Property 'read_write_two_integers' not initialized properly"
        assert client.read_write_two_integers == initial_property_values.read_write_two_integers, "Property 'read_write_two_integers' value does not match expected value"

        assert hasattr(client, "read_only_string"), "Client missing property 'read_only_string'"
        assert client.read_only_string is not None, "Property 'read_only_string' not initialized properly"
        assert client.read_only_string == initial_property_values.read_only_string, "Property 'read_only_string' value does not match expected value"

        assert hasattr(client, "read_write_string"), "Client missing property 'read_write_string'"
        assert client.read_write_string is not None, "Property 'read_write_string' not initialized properly"
        assert client.read_write_string == initial_property_values.read_write_string, "Property 'read_write_string' value does not match expected value"

        assert hasattr(client, "read_write_optional_string"), "Client missing property 'read_write_optional_string'"
        assert client.read_write_optional_string == initial_property_values.read_write_optional_string, "Property 'read_write_optional_string' value does not match expected value"

        assert hasattr(client, "read_write_two_strings"), "Client missing property 'read_write_two_strings'"
        assert client.read_write_two_strings is not None, "Property 'read_write_two_strings' not initialized properly"
        assert client.read_write_two_strings == initial_property_values.read_write_two_strings, "Property 'read_write_two_strings' value does not match expected value"

        assert hasattr(client, "read_write_struct"), "Client missing property 'read_write_struct'"
        assert client.read_write_struct is not None, "Property 'read_write_struct' not initialized properly"
        assert client.read_write_struct == initial_property_values.read_write_struct, "Property 'read_write_struct' value does not match expected value"

        assert hasattr(client, "read_write_optional_struct"), "Client missing property 'read_write_optional_struct'"
        assert client.read_write_optional_struct == initial_property_values.read_write_optional_struct, "Property 'read_write_optional_struct' value does not match expected value"

        assert hasattr(client, "read_write_two_structs"), "Client missing property 'read_write_two_structs'"
        assert client.read_write_two_structs is not None, "Property 'read_write_two_structs' not initialized properly"
        assert client.read_write_two_structs == initial_property_values.read_write_two_structs, "Property 'read_write_two_structs' value does not match expected value"

        assert hasattr(client, "read_only_enum"), "Client missing property 'read_only_enum'"
        assert client.read_only_enum is not None, "Property 'read_only_enum' not initialized properly"
        assert client.read_only_enum == initial_property_values.read_only_enum, "Property 'read_only_enum' value does not match expected value"

        assert hasattr(client, "read_write_enum"), "Client missing property 'read_write_enum'"
        assert client.read_write_enum is not None, "Property 'read_write_enum' not initialized properly"
        assert client.read_write_enum == initial_property_values.read_write_enum, "Property 'read_write_enum' value does not match expected value"

        assert hasattr(client, "read_write_optional_enum"), "Client missing property 'read_write_optional_enum'"
        assert client.read_write_optional_enum == initial_property_values.read_write_optional_enum, "Property 'read_write_optional_enum' value does not match expected value"

        assert hasattr(client, "read_write_two_enums"), "Client missing property 'read_write_two_enums'"
        assert client.read_write_two_enums is not None, "Property 'read_write_two_enums' not initialized properly"
        assert client.read_write_two_enums == initial_property_values.read_write_two_enums, "Property 'read_write_two_enums' value does not match expected value"

        assert hasattr(client, "read_write_datetime"), "Client missing property 'read_write_datetime'"
        assert client.read_write_datetime is not None, "Property 'read_write_datetime' not initialized properly"
        assert client.read_write_datetime == initial_property_values.read_write_datetime, "Property 'read_write_datetime' value does not match expected value"

        assert hasattr(client, "read_write_optional_datetime"), "Client missing property 'read_write_optional_datetime'"
        assert client.read_write_optional_datetime == initial_property_values.read_write_optional_datetime, "Property 'read_write_optional_datetime' value does not match expected value"

        assert hasattr(client, "read_write_two_datetimes"), "Client missing property 'read_write_two_datetimes'"
        assert client.read_write_two_datetimes is not None, "Property 'read_write_two_datetimes' not initialized properly"
        assert client.read_write_two_datetimes == initial_property_values.read_write_two_datetimes, "Property 'read_write_two_datetimes' value does not match expected value"

        assert hasattr(client, "read_write_duration"), "Client missing property 'read_write_duration'"
        assert client.read_write_duration is not None, "Property 'read_write_duration' not initialized properly"
        assert client.read_write_duration == initial_property_values.read_write_duration, "Property 'read_write_duration' value does not match expected value"

        assert hasattr(client, "read_write_optional_duration"), "Client missing property 'read_write_optional_duration'"
        assert client.read_write_optional_duration == initial_property_values.read_write_optional_duration, "Property 'read_write_optional_duration' value does not match expected value"

        assert hasattr(client, "read_write_two_durations"), "Client missing property 'read_write_two_durations'"
        assert client.read_write_two_durations is not None, "Property 'read_write_two_durations' not initialized properly"
        assert client.read_write_two_durations == initial_property_values.read_write_two_durations, "Property 'read_write_two_durations' value does not match expected value"

        assert hasattr(client, "read_write_binary"), "Client missing property 'read_write_binary'"
        assert client.read_write_binary is not None, "Property 'read_write_binary' not initialized properly"
        assert client.read_write_binary == initial_property_values.read_write_binary, "Property 'read_write_binary' value does not match expected value"

        assert hasattr(client, "read_write_optional_binary"), "Client missing property 'read_write_optional_binary'"
        assert client.read_write_optional_binary == initial_property_values.read_write_optional_binary, "Property 'read_write_optional_binary' value does not match expected value"

        assert hasattr(client, "read_write_two_binaries"), "Client missing property 'read_write_two_binaries'"
        assert client.read_write_two_binaries is not None, "Property 'read_write_two_binaries' not initialized properly"
        assert client.read_write_two_binaries == initial_property_values.read_write_two_binaries, "Property 'read_write_two_binaries' value does not match expected value"

        assert hasattr(client, "read_write_list_of_strings"), "Client missing property 'read_write_list_of_strings'"
        assert client.read_write_list_of_strings is not None, "Property 'read_write_list_of_strings' not initialized properly"
        assert client.read_write_list_of_strings == initial_property_values.read_write_list_of_strings, "Property 'read_write_list_of_strings' value does not match expected value"

        assert hasattr(client, "read_write_lists"), "Client missing property 'read_write_lists'"
        assert client.read_write_lists is not None, "Property 'read_write_lists' not initialized properly"
        assert client.read_write_lists == initial_property_values.read_write_lists, "Property 'read_write_lists' value does not match expected value"


class TestClientMethods:

    def test_call_with_nothing_method_call_sends_request(self, mock_connection, client):
        kwargs = {}  # type: Dict[str, Any]
        client.call_with_nothing(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_with_nothing' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callWithNothing"), f"Incorrect topic for 'call_with_nothing' method call: {message.topic}"

    def test_call_one_integer_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": 42,
        }  # type: Dict[str, Any]
        client.call_one_integer(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_integer' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneInteger"), f"Incorrect topic for 'call_one_integer' method call: {message.topic}"

    def test_call_optional_integer_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": 42,
        }  # type: Dict[str, Any]
        client.call_optional_integer(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_integer' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalInteger"), f"Incorrect topic for 'call_optional_integer' method call: {message.topic}"

    def test_call_three_integers_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": 42,
            "input2": 42,
            "input3": 42,
        }  # type: Dict[str, Any]
        client.call_three_integers(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_integers' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeIntegers"), f"Incorrect topic for 'call_three_integers' method call: {message.topic}"

    def test_call_one_string_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": "apples",
        }  # type: Dict[str, Any]
        client.call_one_string(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_string' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneString"), f"Incorrect topic for 'call_one_string' method call: {message.topic}"

    def test_call_optional_string_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": "apples",
        }  # type: Dict[str, Any]
        client.call_optional_string(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_string' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalString"), f"Incorrect topic for 'call_optional_string' method call: {message.topic}"

    def test_call_three_strings_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": "apples",
            "input2": "apples",
            "input3": "apples",
        }  # type: Dict[str, Any]
        client.call_three_strings(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_strings' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeStrings"), f"Incorrect topic for 'call_three_strings' method call: {message.topic}"

    def test_call_one_enum_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": Numbers.ONE,
        }  # type: Dict[str, Any]
        client.call_one_enum(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_enum' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneEnum"), f"Incorrect topic for 'call_one_enum' method call: {message.topic}"

    def test_call_optional_enum_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": Numbers.ONE,
        }  # type: Dict[str, Any]
        client.call_optional_enum(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_enum' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalEnum"), f"Incorrect topic for 'call_optional_enum' method call: {message.topic}"

    def test_call_three_enums_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": Numbers.ONE,
            "input2": Numbers.ONE,
            "input3": Numbers.ONE,
        }  # type: Dict[str, Any]
        client.call_three_enums(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_enums' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeEnums"), f"Incorrect topic for 'call_three_enums' method call: {message.topic}"

    def test_call_one_struct_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": AllTypes(
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
        }  # type: Dict[str, Any]
        client.call_one_struct(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_struct' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneStruct"), f"Incorrect topic for 'call_one_struct' method call: {message.topic}"

    def test_call_optional_struct_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": AllTypes(
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
        }  # type: Dict[str, Any]
        client.call_optional_struct(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_struct' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalStruct"), f"Incorrect topic for 'call_optional_struct' method call: {message.topic}"

    def test_call_three_structs_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": AllTypes(
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
            "input2": AllTypes(
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
            "input3": AllTypes(
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
        }  # type: Dict[str, Any]
        client.call_three_structs(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_structs' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeStructs"), f"Incorrect topic for 'call_three_structs' method call: {message.topic}"

    def test_call_one_date_time_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": datetime.now(UTC),
        }  # type: Dict[str, Any]
        client.call_one_date_time(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_date_time' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneDateTime"), f"Incorrect topic for 'call_one_date_time' method call: {message.topic}"

    def test_call_optional_date_time_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": None,
        }  # type: Dict[str, Any]
        client.call_optional_date_time(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_date_time' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalDateTime"), f"Incorrect topic for 'call_optional_date_time' method call: {message.topic}"

    def test_call_three_date_times_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": datetime.now(UTC),
            "input2": datetime.now(UTC),
            "input3": datetime.now(UTC),
        }  # type: Dict[str, Any]
        client.call_three_date_times(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_date_times' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeDateTimes"), f"Incorrect topic for 'call_three_date_times' method call: {message.topic}"

    def test_call_one_duration_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": timedelta(seconds=3536),
        }  # type: Dict[str, Any]
        client.call_one_duration(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_duration' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneDuration"), f"Incorrect topic for 'call_one_duration' method call: {message.topic}"

    def test_call_optional_duration_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": None,
        }  # type: Dict[str, Any]
        client.call_optional_duration(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_duration' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalDuration"), f"Incorrect topic for 'call_optional_duration' method call: {message.topic}"

    def test_call_three_durations_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": timedelta(seconds=3536),
            "input2": timedelta(seconds=3536),
            "input3": None,
        }  # type: Dict[str, Any]
        client.call_three_durations(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_durations' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeDurations"), f"Incorrect topic for 'call_three_durations' method call: {message.topic}"

    def test_call_one_binary_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": b"example binary data",
        }  # type: Dict[str, Any]
        client.call_one_binary(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_binary' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneBinary"), f"Incorrect topic for 'call_one_binary' method call: {message.topic}"

    def test_call_optional_binary_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": b"example binary data",
        }  # type: Dict[str, Any]
        client.call_optional_binary(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_binary' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalBinary"), f"Incorrect topic for 'call_optional_binary' method call: {message.topic}"

    def test_call_three_binaries_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": b"example binary data",
            "input2": b"example binary data",
            "input3": b"example binary data",
        }  # type: Dict[str, Any]
        client.call_three_binaries(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_three_binaries' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callThreeBinaries"), f"Incorrect topic for 'call_three_binaries' method call: {message.topic}"

    def test_call_one_list_of_integers_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": [42, 2022],
        }  # type: Dict[str, Any]
        client.call_one_list_of_integers(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_one_list_of_integers' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOneListOfIntegers"), f"Incorrect topic for 'call_one_list_of_integers' method call: {message.topic}"

    def test_call_optional_list_of_floats_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": [3.14, 1.0],
        }  # type: Dict[str, Any]
        client.call_optional_list_of_floats(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_optional_list_of_floats' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callOptionalListOfFloats"), f"Incorrect topic for 'call_optional_list_of_floats' method call: {message.topic}"

    def test_call_two_lists_method_call_sends_request(self, mock_connection, client):
        kwargs = {
            "input1": [Numbers.ONE, Numbers.ONE],
            "input2": ["apples", "foo"],
        }  # type: Dict[str, Any]
        client.call_two_lists(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'call_two_lists' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/callTwoLists"), f"Incorrect topic for 'call_two_lists' method call: {message.topic}"
