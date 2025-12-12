"""
Tests for testable client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from testableipc.client import TestableClient, DiscoveredInstance
from testableipc.property import TestableInitialPropertyValues
from testableipc.interface_types import *
from pyqttier.mock import MockConnection


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def client(mock_connection):
    """Fixture providing a testable client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=TestableInitialPropertyValues(
            read_write_integer=42,
            read_only_integer=42,
            read_write_optional_integer=42,
            read_write_two_integers=TestableReadWriteTwoIntegersProperty(
                first=42,
                second=42,
            ),
            read_only_string="apples",
            read_write_string="apples",
            read_write_optional_string="apples",
            read_write_two_strings=TestableReadWriteTwoStringsProperty(
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
            read_write_two_structs=TestableReadWriteTwoStructsProperty(
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
            read_write_two_enums=TestableReadWriteTwoEnumsProperty(
                first=Numbers.ONE,
                second=Numbers.ONE,
            ),
            read_write_datetime=datetime.now(UTC),
            read_write_optional_datetime=None,
            read_write_two_datetimes=TestableReadWriteTwoDatetimesProperty(
                first=datetime.now(UTC),
                second=datetime.now(UTC),
            ),
            read_write_duration=timedelta(seconds=3536),
            read_write_optional_duration=None,
            read_write_two_durations=TestableReadWriteTwoDurationsProperty(
                first=timedelta(seconds=3536),
                second=None,
            ),
            read_write_binary=b"example binary data",
            read_write_optional_binary=b"example binary data",
            read_write_two_binaries=TestableReadWriteTwoBinariesProperty(
                first=b"example binary data",
                second=b"example binary data",
            ),
            read_write_list_of_strings=["apples", "foo"],
            read_write_lists=TestableReadWriteListsProperty(
                the_list=[Numbers.ONE, Numbers.ONE],
                optional_list=[datetime.now(UTC), datetime.now(UTC)],
            ),
        ),
    )
    client = TestableClient(
        connection=mock_connection,
        discovered_instance=mock_discovery,
    )
    return client


class TestClientInit:
    """Tests for client initialization."""

    def test_client_initializes(self, client):
        """Test that client initializes successfully."""
        assert client is not None, "Client failed to initialize"
        assert client.service_id == "test_instance", "Client service_id does not match expected value"
