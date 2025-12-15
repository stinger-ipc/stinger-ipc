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
import json


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
        read_write_optional_datetime=None,
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

    def test_server_read_only_integer_property_initialization(self, server, initial_property_values):
        """Test that the read_only_integer server property is initialized correctly."""
        assert hasattr(server, "read_only_integer"), "Server missing property 'read_only_integer'"
        assert server.read_only_integer is not None, "Property 'read_only_integer' not initialized properly"
        assert server.read_only_integer == initial_property_values.read_only_integer, "Property 'read_only_integer' value does not match expected value"

    def test_server_read_write_optional_integer_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_integer server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_integer"), "Server missing property 'read_write_optional_integer'"
        assert server.read_write_optional_integer == initial_property_values.read_write_optional_integer, "Property 'read_write_optional_integer' value does not match expected value"

    def test_server_read_write_two_integers_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_integers server property is initialized correctly."""
        assert hasattr(server, "read_write_two_integers"), "Server missing property 'read_write_two_integers'"
        assert server.read_write_two_integers is not None, "Property 'read_write_two_integers' not initialized properly"
        assert server.read_write_two_integers == initial_property_values.read_write_two_integers, "Property 'read_write_two_integers' value does not match expected value"

    def test_server_read_only_string_property_initialization(self, server, initial_property_values):
        """Test that the read_only_string server property is initialized correctly."""
        assert hasattr(server, "read_only_string"), "Server missing property 'read_only_string'"
        assert server.read_only_string is not None, "Property 'read_only_string' not initialized properly"
        assert server.read_only_string == initial_property_values.read_only_string, "Property 'read_only_string' value does not match expected value"

    def test_server_read_write_string_property_initialization(self, server, initial_property_values):
        """Test that the read_write_string server property is initialized correctly."""
        assert hasattr(server, "read_write_string"), "Server missing property 'read_write_string'"
        assert server.read_write_string is not None, "Property 'read_write_string' not initialized properly"
        assert server.read_write_string == initial_property_values.read_write_string, "Property 'read_write_string' value does not match expected value"

    def test_server_read_write_optional_string_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_string server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_string"), "Server missing property 'read_write_optional_string'"
        assert server.read_write_optional_string == initial_property_values.read_write_optional_string, "Property 'read_write_optional_string' value does not match expected value"

    def test_server_read_write_two_strings_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_strings server property is initialized correctly."""
        assert hasattr(server, "read_write_two_strings"), "Server missing property 'read_write_two_strings'"
        assert server.read_write_two_strings is not None, "Property 'read_write_two_strings' not initialized properly"
        assert server.read_write_two_strings == initial_property_values.read_write_two_strings, "Property 'read_write_two_strings' value does not match expected value"

    def test_server_read_write_struct_property_initialization(self, server, initial_property_values):
        """Test that the read_write_struct server property is initialized correctly."""
        assert hasattr(server, "read_write_struct"), "Server missing property 'read_write_struct'"
        assert server.read_write_struct is not None, "Property 'read_write_struct' not initialized properly"
        assert server.read_write_struct == initial_property_values.read_write_struct, "Property 'read_write_struct' value does not match expected value"

    def test_server_read_write_optional_struct_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_struct server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_struct"), "Server missing property 'read_write_optional_struct'"
        assert server.read_write_optional_struct == initial_property_values.read_write_optional_struct, "Property 'read_write_optional_struct' value does not match expected value"

    def test_server_read_write_two_structs_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_structs server property is initialized correctly."""
        assert hasattr(server, "read_write_two_structs"), "Server missing property 'read_write_two_structs'"
        assert server.read_write_two_structs is not None, "Property 'read_write_two_structs' not initialized properly"
        assert server.read_write_two_structs == initial_property_values.read_write_two_structs, "Property 'read_write_two_structs' value does not match expected value"

    def test_server_read_only_enum_property_initialization(self, server, initial_property_values):
        """Test that the read_only_enum server property is initialized correctly."""
        assert hasattr(server, "read_only_enum"), "Server missing property 'read_only_enum'"
        assert server.read_only_enum is not None, "Property 'read_only_enum' not initialized properly"
        assert server.read_only_enum == initial_property_values.read_only_enum, "Property 'read_only_enum' value does not match expected value"

    def test_server_read_write_enum_property_initialization(self, server, initial_property_values):
        """Test that the read_write_enum server property is initialized correctly."""
        assert hasattr(server, "read_write_enum"), "Server missing property 'read_write_enum'"
        assert server.read_write_enum is not None, "Property 'read_write_enum' not initialized properly"
        assert server.read_write_enum == initial_property_values.read_write_enum, "Property 'read_write_enum' value does not match expected value"

    def test_server_read_write_optional_enum_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_enum server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_enum"), "Server missing property 'read_write_optional_enum'"
        assert server.read_write_optional_enum == initial_property_values.read_write_optional_enum, "Property 'read_write_optional_enum' value does not match expected value"

    def test_server_read_write_two_enums_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_enums server property is initialized correctly."""
        assert hasattr(server, "read_write_two_enums"), "Server missing property 'read_write_two_enums'"
        assert server.read_write_two_enums is not None, "Property 'read_write_two_enums' not initialized properly"
        assert server.read_write_two_enums == initial_property_values.read_write_two_enums, "Property 'read_write_two_enums' value does not match expected value"

    def test_server_read_write_datetime_property_initialization(self, server, initial_property_values):
        """Test that the read_write_datetime server property is initialized correctly."""
        assert hasattr(server, "read_write_datetime"), "Server missing property 'read_write_datetime'"
        assert server.read_write_datetime is not None, "Property 'read_write_datetime' not initialized properly"
        assert server.read_write_datetime == initial_property_values.read_write_datetime, "Property 'read_write_datetime' value does not match expected value"

    def test_server_read_write_optional_datetime_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_datetime server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_datetime"), "Server missing property 'read_write_optional_datetime'"
        assert server.read_write_optional_datetime == initial_property_values.read_write_optional_datetime, "Property 'read_write_optional_datetime' value does not match expected value"

    def test_server_read_write_two_datetimes_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_datetimes server property is initialized correctly."""
        assert hasattr(server, "read_write_two_datetimes"), "Server missing property 'read_write_two_datetimes'"
        assert server.read_write_two_datetimes is not None, "Property 'read_write_two_datetimes' not initialized properly"
        assert server.read_write_two_datetimes == initial_property_values.read_write_two_datetimes, "Property 'read_write_two_datetimes' value does not match expected value"

    def test_server_read_write_duration_property_initialization(self, server, initial_property_values):
        """Test that the read_write_duration server property is initialized correctly."""
        assert hasattr(server, "read_write_duration"), "Server missing property 'read_write_duration'"
        assert server.read_write_duration is not None, "Property 'read_write_duration' not initialized properly"
        assert server.read_write_duration == initial_property_values.read_write_duration, "Property 'read_write_duration' value does not match expected value"

    def test_server_read_write_optional_duration_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_duration server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_duration"), "Server missing property 'read_write_optional_duration'"
        assert server.read_write_optional_duration == initial_property_values.read_write_optional_duration, "Property 'read_write_optional_duration' value does not match expected value"

    def test_server_read_write_two_durations_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_durations server property is initialized correctly."""
        assert hasattr(server, "read_write_two_durations"), "Server missing property 'read_write_two_durations'"
        assert server.read_write_two_durations is not None, "Property 'read_write_two_durations' not initialized properly"
        assert server.read_write_two_durations == initial_property_values.read_write_two_durations, "Property 'read_write_two_durations' value does not match expected value"

    def test_server_read_write_binary_property_initialization(self, server, initial_property_values):
        """Test that the read_write_binary server property is initialized correctly."""
        assert hasattr(server, "read_write_binary"), "Server missing property 'read_write_binary'"
        assert server.read_write_binary is not None, "Property 'read_write_binary' not initialized properly"
        assert server.read_write_binary == initial_property_values.read_write_binary, "Property 'read_write_binary' value does not match expected value"

    def test_server_read_write_optional_binary_property_initialization(self, server, initial_property_values):
        """Test that the read_write_optional_binary server property is initialized correctly."""
        assert hasattr(server, "read_write_optional_binary"), "Server missing property 'read_write_optional_binary'"
        assert server.read_write_optional_binary == initial_property_values.read_write_optional_binary, "Property 'read_write_optional_binary' value does not match expected value"

    def test_server_read_write_two_binaries_property_initialization(self, server, initial_property_values):
        """Test that the read_write_two_binaries server property is initialized correctly."""
        assert hasattr(server, "read_write_two_binaries"), "Server missing property 'read_write_two_binaries'"
        assert server.read_write_two_binaries is not None, "Property 'read_write_two_binaries' not initialized properly"
        assert server.read_write_two_binaries == initial_property_values.read_write_two_binaries, "Property 'read_write_two_binaries' value does not match expected value"

    def test_server_read_write_list_of_strings_property_initialization(self, server, initial_property_values):
        """Test that the read_write_list_of_strings server property is initialized correctly."""
        assert hasattr(server, "read_write_list_of_strings"), "Server missing property 'read_write_list_of_strings'"
        assert server.read_write_list_of_strings is not None, "Property 'read_write_list_of_strings' not initialized properly"
        assert server.read_write_list_of_strings == initial_property_values.read_write_list_of_strings, "Property 'read_write_list_of_strings' value does not match expected value"

    def test_server_read_write_lists_property_initialization(self, server, initial_property_values):
        """Test that the read_write_lists server property is initialized correctly."""
        assert hasattr(server, "read_write_lists"), "Server missing property 'read_write_lists'"
        assert server.read_write_lists is not None, "Property 'read_write_lists' not initialized properly"
        assert server.read_write_lists == initial_property_values.read_write_lists, "Property 'read_write_lists' value does not match expected value"
