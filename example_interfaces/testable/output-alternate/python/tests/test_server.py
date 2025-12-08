"""
Tests for testable server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

from testableipc.server import TestableServer
from testableipc.property import TestablePropertyAccess, TestableInitialPropertyValues
from testableipc.interface_types import *
from stinger_python_utils.return_codes import MethodReturnCode
from pyqttier.mock import MockConnection
from pyqttier.message import Message
import json
from pydantic import BaseModel
from typing import Any, Dict


def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)


class TestableServerSetup:

    def __init__(self):
        self.initial_property_values = self.get_initial_property_values()

        self.read_write_integer = self.initial_property_values.read_write_integer
        self.read_only_integer = self.initial_property_values.read_only_integer
        self.read_write_optional_integer = self.initial_property_values.read_write_optional_integer
        self.read_write_two_integers = self.initial_property_values.read_write_two_integers
        self.read_only_string = self.initial_property_values.read_only_string
        self.read_write_string = self.initial_property_values.read_write_string
        self.read_write_optional_string = self.initial_property_values.read_write_optional_string
        self.read_write_two_strings = self.initial_property_values.read_write_two_strings
        self.read_write_struct = self.initial_property_values.read_write_struct
        self.read_write_optional_struct = self.initial_property_values.read_write_optional_struct
        self.read_write_two_structs = self.initial_property_values.read_write_two_structs
        self.read_only_enum = self.initial_property_values.read_only_enum
        self.read_write_enum = self.initial_property_values.read_write_enum
        self.read_write_optional_enum = self.initial_property_values.read_write_optional_enum
        self.read_write_two_enums = self.initial_property_values.read_write_two_enums
        self.read_write_datetime = self.initial_property_values.read_write_datetime
        self.read_write_optional_datetime = self.initial_property_values.read_write_optional_datetime
        self.read_write_two_datetimes = self.initial_property_values.read_write_two_datetimes
        self.read_write_duration = self.initial_property_values.read_write_duration
        self.read_write_optional_duration = self.initial_property_values.read_write_optional_duration
        self.read_write_two_durations = self.initial_property_values.read_write_two_durations
        self.read_write_binary = self.initial_property_values.read_write_binary
        self.read_write_optional_binary = self.initial_property_values.read_write_optional_binary
        self.read_write_two_binaries = self.initial_property_values.read_write_two_binaries
        self.read_write_list_of_strings = self.initial_property_values.read_write_list_of_strings
        self.read_write_lists = self.initial_property_values.read_write_lists
        self.reset_modified_flags()

    def get_initial_property_values(self) -> TestableInitialPropertyValues:
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

    def get_property_access(self) -> TestablePropertyAccess:
        property_access = TestablePropertyAccess(
            read_write_integer_getter=self.get_property_read_write_integer,
            read_write_integer_setter=self.set_property_read_write_integer,
            read_only_integer_getter=self.get_property_read_only_integer,
            read_write_optional_integer_getter=self.get_property_read_write_optional_integer,
            read_write_optional_integer_setter=self.set_property_read_write_optional_integer,
            read_write_two_integers_getter=self.get_property_read_write_two_integers,
            read_write_two_integers_setter=self.set_property_read_write_two_integers,
            read_only_string_getter=self.get_property_read_only_string,
            read_write_string_getter=self.get_property_read_write_string,
            read_write_string_setter=self.set_property_read_write_string,
            read_write_optional_string_getter=self.get_property_read_write_optional_string,
            read_write_optional_string_setter=self.set_property_read_write_optional_string,
            read_write_two_strings_getter=self.get_property_read_write_two_strings,
            read_write_two_strings_setter=self.set_property_read_write_two_strings,
            read_write_struct_getter=self.get_property_read_write_struct,
            read_write_struct_setter=self.set_property_read_write_struct,
            read_write_optional_struct_getter=self.get_property_read_write_optional_struct,
            read_write_optional_struct_setter=self.set_property_read_write_optional_struct,
            read_write_two_structs_getter=self.get_property_read_write_two_structs,
            read_write_two_structs_setter=self.set_property_read_write_two_structs,
            read_only_enum_getter=self.get_property_read_only_enum,
            read_write_enum_getter=self.get_property_read_write_enum,
            read_write_enum_setter=self.set_property_read_write_enum,
            read_write_optional_enum_getter=self.get_property_read_write_optional_enum,
            read_write_optional_enum_setter=self.set_property_read_write_optional_enum,
            read_write_two_enums_getter=self.get_property_read_write_two_enums,
            read_write_two_enums_setter=self.set_property_read_write_two_enums,
            read_write_datetime_getter=self.get_property_read_write_datetime,
            read_write_datetime_setter=self.set_property_read_write_datetime,
            read_write_optional_datetime_getter=self.get_property_read_write_optional_datetime,
            read_write_optional_datetime_setter=self.set_property_read_write_optional_datetime,
            read_write_two_datetimes_getter=self.get_property_read_write_two_datetimes,
            read_write_two_datetimes_setter=self.set_property_read_write_two_datetimes,
            read_write_duration_getter=self.get_property_read_write_duration,
            read_write_duration_setter=self.set_property_read_write_duration,
            read_write_optional_duration_getter=self.get_property_read_write_optional_duration,
            read_write_optional_duration_setter=self.set_property_read_write_optional_duration,
            read_write_two_durations_getter=self.get_property_read_write_two_durations,
            read_write_two_durations_setter=self.set_property_read_write_two_durations,
            read_write_binary_getter=self.get_property_read_write_binary,
            read_write_binary_setter=self.set_property_read_write_binary,
            read_write_optional_binary_getter=self.get_property_read_write_optional_binary,
            read_write_optional_binary_setter=self.set_property_read_write_optional_binary,
            read_write_two_binaries_getter=self.get_property_read_write_two_binaries,
            read_write_two_binaries_setter=self.set_property_read_write_two_binaries,
            read_write_list_of_strings_getter=self.get_property_read_write_list_of_strings,
            read_write_list_of_strings_setter=self.set_property_read_write_list_of_strings,
            read_write_lists_getter=self.get_property_read_write_lists,
            read_write_lists_setter=self.set_property_read_write_lists,
        )
        return property_access

    def reset_modified_flags(self):
        self.read_write_integer_modified_flag = False
        self.read_only_integer_modified_flag = False
        self.read_write_optional_integer_modified_flag = False
        self.read_write_two_integers_modified_flag = False
        self.read_only_string_modified_flag = False
        self.read_write_string_modified_flag = False
        self.read_write_optional_string_modified_flag = False
        self.read_write_two_strings_modified_flag = False
        self.read_write_struct_modified_flag = False
        self.read_write_optional_struct_modified_flag = False
        self.read_write_two_structs_modified_flag = False
        self.read_only_enum_modified_flag = False
        self.read_write_enum_modified_flag = False
        self.read_write_optional_enum_modified_flag = False
        self.read_write_two_enums_modified_flag = False
        self.read_write_datetime_modified_flag = False
        self.read_write_optional_datetime_modified_flag = False
        self.read_write_two_datetimes_modified_flag = False
        self.read_write_duration_modified_flag = False
        self.read_write_optional_duration_modified_flag = False
        self.read_write_two_durations_modified_flag = False
        self.read_write_binary_modified_flag = False
        self.read_write_optional_binary_modified_flag = False
        self.read_write_two_binaries_modified_flag = False
        self.read_write_list_of_strings_modified_flag = False
        self.read_write_lists_modified_flag = False

    def create_server(self, mock_connection) -> TestableServer:
        server = TestableServer(mock_connection, "test_instance", self.get_property_access())
        return server

    def get_property_read_write_integer(self):
        """Return the value for the 'read_write_integer' property."""
        return self.read_write_integer

    def set_property_read_write_integer(self, value: int):
        """Set the value for the 'read_write_integer' property."""
        self.read_write_integer_modified_flag = True
        self.read_write_integer = value

    def get_property_read_only_integer(self):
        """Return the value for the 'read_only_integer' property."""
        return self.read_only_integer

    def get_property_read_write_optional_integer(self):
        """Return the value for the 'read_write_optional_integer' property."""
        return self.read_write_optional_integer

    def set_property_read_write_optional_integer(self, value: Optional[int]):
        """Set the value for the 'read_write_optional_integer' property."""
        self.read_write_optional_integer_modified_flag = True
        self.read_write_optional_integer = value

    def get_property_read_write_two_integers(self):
        """Return the value for the 'read_write_two_integers' property."""
        return self.read_write_two_integers

    def set_property_read_write_two_integers(self, value: ReadWriteTwoIntegersProperty):
        """Set the value for the 'read_write_two_integers' property."""
        self.read_write_two_integers_modified_flag = True
        self.read_write_two_integers = value

    def get_property_read_only_string(self):
        """Return the value for the 'read_only_string' property."""
        return self.read_only_string

    def get_property_read_write_string(self):
        """Return the value for the 'read_write_string' property."""
        return self.read_write_string

    def set_property_read_write_string(self, value: str):
        """Set the value for the 'read_write_string' property."""
        self.read_write_string_modified_flag = True
        self.read_write_string = value

    def get_property_read_write_optional_string(self):
        """Return the value for the 'read_write_optional_string' property."""
        return self.read_write_optional_string

    def set_property_read_write_optional_string(self, value: Optional[str]):
        """Set the value for the 'read_write_optional_string' property."""
        self.read_write_optional_string_modified_flag = True
        self.read_write_optional_string = value

    def get_property_read_write_two_strings(self):
        """Return the value for the 'read_write_two_strings' property."""
        return self.read_write_two_strings

    def set_property_read_write_two_strings(self, value: ReadWriteTwoStringsProperty):
        """Set the value for the 'read_write_two_strings' property."""
        self.read_write_two_strings_modified_flag = True
        self.read_write_two_strings = value

    def get_property_read_write_struct(self):
        """Return the value for the 'read_write_struct' property."""
        return self.read_write_struct

    def set_property_read_write_struct(self, value: AllTypes):
        """Set the value for the 'read_write_struct' property."""
        self.read_write_struct_modified_flag = True
        self.read_write_struct = value

    def get_property_read_write_optional_struct(self):
        """Return the value for the 'read_write_optional_struct' property."""
        return self.read_write_optional_struct

    def set_property_read_write_optional_struct(self, value: AllTypes):
        """Set the value for the 'read_write_optional_struct' property."""
        self.read_write_optional_struct_modified_flag = True
        self.read_write_optional_struct = value

    def get_property_read_write_two_structs(self):
        """Return the value for the 'read_write_two_structs' property."""
        return self.read_write_two_structs

    def set_property_read_write_two_structs(self, value: ReadWriteTwoStructsProperty):
        """Set the value for the 'read_write_two_structs' property."""
        self.read_write_two_structs_modified_flag = True
        self.read_write_two_structs = value

    def get_property_read_only_enum(self):
        """Return the value for the 'read_only_enum' property."""
        return self.read_only_enum

    def get_property_read_write_enum(self):
        """Return the value for the 'read_write_enum' property."""
        return self.read_write_enum

    def set_property_read_write_enum(self, value: Numbers):
        """Set the value for the 'read_write_enum' property."""
        self.read_write_enum_modified_flag = True
        self.read_write_enum = value

    def get_property_read_write_optional_enum(self):
        """Return the value for the 'read_write_optional_enum' property."""
        return self.read_write_optional_enum

    def set_property_read_write_optional_enum(self, value: Optional[Numbers]):
        """Set the value for the 'read_write_optional_enum' property."""
        self.read_write_optional_enum_modified_flag = True
        self.read_write_optional_enum = value

    def get_property_read_write_two_enums(self):
        """Return the value for the 'read_write_two_enums' property."""
        return self.read_write_two_enums

    def set_property_read_write_two_enums(self, value: ReadWriteTwoEnumsProperty):
        """Set the value for the 'read_write_two_enums' property."""
        self.read_write_two_enums_modified_flag = True
        self.read_write_two_enums = value

    def get_property_read_write_datetime(self):
        """Return the value for the 'read_write_datetime' property."""
        return self.read_write_datetime

    def set_property_read_write_datetime(self, value: datetime):
        """Set the value for the 'read_write_datetime' property."""
        self.read_write_datetime_modified_flag = True
        self.read_write_datetime = value

    def get_property_read_write_optional_datetime(self):
        """Return the value for the 'read_write_optional_datetime' property."""
        return self.read_write_optional_datetime

    def set_property_read_write_optional_datetime(self, value: Optional[datetime]):
        """Set the value for the 'read_write_optional_datetime' property."""
        self.read_write_optional_datetime_modified_flag = True
        self.read_write_optional_datetime = value

    def get_property_read_write_two_datetimes(self):
        """Return the value for the 'read_write_two_datetimes' property."""
        return self.read_write_two_datetimes

    def set_property_read_write_two_datetimes(self, value: ReadWriteTwoDatetimesProperty):
        """Set the value for the 'read_write_two_datetimes' property."""
        self.read_write_two_datetimes_modified_flag = True
        self.read_write_two_datetimes = value

    def get_property_read_write_duration(self):
        """Return the value for the 'read_write_duration' property."""
        return self.read_write_duration

    def set_property_read_write_duration(self, value: timedelta):
        """Set the value for the 'read_write_duration' property."""
        self.read_write_duration_modified_flag = True
        self.read_write_duration = value

    def get_property_read_write_optional_duration(self):
        """Return the value for the 'read_write_optional_duration' property."""
        return self.read_write_optional_duration

    def set_property_read_write_optional_duration(self, value: Optional[timedelta]):
        """Set the value for the 'read_write_optional_duration' property."""
        self.read_write_optional_duration_modified_flag = True
        self.read_write_optional_duration = value

    def get_property_read_write_two_durations(self):
        """Return the value for the 'read_write_two_durations' property."""
        return self.read_write_two_durations

    def set_property_read_write_two_durations(self, value: ReadWriteTwoDurationsProperty):
        """Set the value for the 'read_write_two_durations' property."""
        self.read_write_two_durations_modified_flag = True
        self.read_write_two_durations = value

    def get_property_read_write_binary(self):
        """Return the value for the 'read_write_binary' property."""
        return self.read_write_binary

    def set_property_read_write_binary(self, value: bytes):
        """Set the value for the 'read_write_binary' property."""
        self.read_write_binary_modified_flag = True
        self.read_write_binary = value

    def get_property_read_write_optional_binary(self):
        """Return the value for the 'read_write_optional_binary' property."""
        return self.read_write_optional_binary

    def set_property_read_write_optional_binary(self, value: bytes):
        """Set the value for the 'read_write_optional_binary' property."""
        self.read_write_optional_binary_modified_flag = True
        self.read_write_optional_binary = value

    def get_property_read_write_two_binaries(self):
        """Return the value for the 'read_write_two_binaries' property."""
        return self.read_write_two_binaries

    def set_property_read_write_two_binaries(self, value: ReadWriteTwoBinariesProperty):
        """Set the value for the 'read_write_two_binaries' property."""
        self.read_write_two_binaries_modified_flag = True
        self.read_write_two_binaries = value

    def get_property_read_write_list_of_strings(self):
        """Return the value for the 'read_write_list_of_strings' property."""
        return self.read_write_list_of_strings

    def set_property_read_write_list_of_strings(self, value: List[str]):
        """Set the value for the 'read_write_list_of_strings' property."""
        self.read_write_list_of_strings_modified_flag = True
        self.read_write_list_of_strings = value

    def get_property_read_write_lists(self):
        """Return the value for the 'read_write_lists' property."""
        return self.read_write_lists

    def set_property_read_write_lists(self, value: ReadWriteListsProperty):
        """Set the value for the 'read_write_lists' property."""
        self.read_write_lists_modified_flag = True
        self.read_write_lists = value


@pytest.fixture
def server_setup():
    setup = TestableServerSetup()
    return setup


@pytest.fixture
def initial_property_values(server_setup):
    return server_setup.initial_property_values


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(server_setup, mock_connection):
    server = server_setup.create_server(mock_connection)
    yield server
    server.shutdown(timeout=0.01)


class TestTestableServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestTestableServerProperties:

    def test_get_initial_read_write_integer_property(self, server_setup, server):
        """Test that the server can get the 'read_write_integer' property."""
        assert server.read_write_integer == server_setup.read_write_integer, "Getter for property 'read_write_integer' returned incorrect value"

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

    def test_read_write_integer_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": 2020,
        }
        prop_obj = ReadWriteIntegerProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteInteger/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_integer.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_integer_modified_flag, "Setter for property 'read_write_integer' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_integer'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_only_integer_property(self, server_setup, server):
        """Test that the server can get the 'read_only_integer' property."""
        assert server.read_only_integer == server_setup.read_only_integer, "Getter for property 'read_only_integer' returned incorrect value"

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

    def test_read_only_integer_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": 2020,
        }
        prop_obj = ReadOnlyIntegerProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readOnlyInteger/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_only_integer.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_only_integer_modified_flag is not True, "Setter for property 'read_only_integer' was called on read-only property"

    def test_get_initial_read_write_optional_integer_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_integer' property."""
        assert server.read_write_optional_integer == server_setup.read_write_optional_integer, "Getter for property 'read_write_optional_integer' returned incorrect value"

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

    def test_read_write_optional_integer_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": 2020,
        }
        prop_obj = ReadWriteOptionalIntegerProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalInteger/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_integer.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_integer_modified_flag, "Setter for property 'read_write_optional_integer' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_integer'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_integers_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_integers' property."""
        assert server.read_write_two_integers == server_setup.read_write_two_integers, "Getter for property 'read_write_two_integers' returned incorrect value"

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

    def test_read_write_two_integers_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "first": 2020,
            "second": 42,
        }
        prop_obj = ReadWriteTwoIntegersProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoIntegers/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_integers.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_integers_modified_flag, "Setter for property 'read_write_two_integers' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_integers'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_only_string_property(self, server_setup, server):
        """Test that the server can get the 'read_only_string' property."""
        assert server.read_only_string == server_setup.read_only_string, "Getter for property 'read_only_string' returned incorrect value"

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

    def test_read_only_string_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": "example",
        }
        prop_obj = ReadOnlyStringProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readOnlyString/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_only_string.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_only_string_modified_flag is not True, "Setter for property 'read_only_string' was called on read-only property"

    def test_get_initial_read_write_string_property(self, server_setup, server):
        """Test that the server can get the 'read_write_string' property."""
        assert server.read_write_string == server_setup.read_write_string, "Getter for property 'read_write_string' returned incorrect value"

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

    def test_read_write_string_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": "example",
        }
        prop_obj = ReadWriteStringProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteString/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_string.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_string_modified_flag, "Setter for property 'read_write_string' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_string'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_optional_string_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_string' property."""
        assert server.read_write_optional_string == server_setup.read_write_optional_string, "Getter for property 'read_write_optional_string' returned incorrect value"

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

    def test_read_write_optional_string_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": "example",
        }
        prop_obj = ReadWriteOptionalStringProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalString/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_string.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_string_modified_flag, "Setter for property 'read_write_optional_string' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_string'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_strings_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_strings' property."""
        assert server.read_write_two_strings == server_setup.read_write_two_strings, "Getter for property 'read_write_two_strings' returned incorrect value"

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

    def test_read_write_two_strings_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "first": "example",
            "second": "apples",
        }
        prop_obj = ReadWriteTwoStringsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoStrings/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_strings.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_strings_modified_flag, "Setter for property 'read_write_two_strings' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_strings'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_struct_property(self, server_setup, server):
        """Test that the server can get the 'read_write_struct' property."""
        assert server.read_write_struct == server_setup.read_write_struct, "Getter for property 'read_write_struct' returned incorrect value"

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

    def test_read_write_struct_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

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
        prop_obj = ReadWriteStructProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteStruct/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_struct.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_struct_modified_flag, "Setter for property 'read_write_struct' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_struct'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_optional_struct_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_struct' property."""
        assert server.read_write_optional_struct == server_setup.read_write_optional_struct, "Getter for property 'read_write_optional_struct' returned incorrect value"

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

    def test_read_write_optional_struct_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

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
        prop_obj = ReadWriteOptionalStructProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalStruct/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_struct.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_struct_modified_flag, "Setter for property 'read_write_optional_struct' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_struct'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_structs_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_structs' property."""
        assert server.read_write_two_structs == server_setup.read_write_two_structs, "Getter for property 'read_write_two_structs' returned incorrect value"

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

    def test_read_write_two_structs_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

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
        prop_obj = ReadWriteTwoStructsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoStructs/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_structs.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_structs_modified_flag, "Setter for property 'read_write_two_structs' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_structs'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_only_enum_property(self, server_setup, server):
        """Test that the server can get the 'read_only_enum' property."""
        assert server.read_only_enum == server_setup.read_only_enum, "Getter for property 'read_only_enum' returned incorrect value"

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

    def test_read_only_enum_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": Numbers.ONE,
        }
        prop_obj = ReadOnlyEnumProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readOnlyEnum/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_only_enum.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_only_enum_modified_flag is not True, "Setter for property 'read_only_enum' was called on read-only property"

    def test_get_initial_read_write_enum_property(self, server_setup, server):
        """Test that the server can get the 'read_write_enum' property."""
        assert server.read_write_enum == server_setup.read_write_enum, "Getter for property 'read_write_enum' returned incorrect value"

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

    def test_read_write_enum_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": Numbers.ONE,
        }
        prop_obj = ReadWriteEnumProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteEnum/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_enum.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_enum_modified_flag, "Setter for property 'read_write_enum' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_enum'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_optional_enum_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_enum' property."""
        assert server.read_write_optional_enum == server_setup.read_write_optional_enum, "Getter for property 'read_write_optional_enum' returned incorrect value"

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

    def test_read_write_optional_enum_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": Numbers.ONE,
        }
        prop_obj = ReadWriteOptionalEnumProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalEnum/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_enum.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_enum_modified_flag, "Setter for property 'read_write_optional_enum' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_enum'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_enums_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_enums' property."""
        assert server.read_write_two_enums == server_setup.read_write_two_enums, "Getter for property 'read_write_two_enums' returned incorrect value"

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

    def test_read_write_two_enums_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "first": Numbers.ONE,
            "second": Numbers.ONE,
        }
        prop_obj = ReadWriteTwoEnumsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoEnums/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_enums.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_enums_modified_flag, "Setter for property 'read_write_two_enums' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_enums'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_datetime_property(self, server_setup, server):
        """Test that the server can get the 'read_write_datetime' property."""
        assert server.read_write_datetime == server_setup.read_write_datetime, "Getter for property 'read_write_datetime' returned incorrect value"

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

    def test_read_write_datetime_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": datetime.now(UTC),
        }
        prop_obj = ReadWriteDatetimeProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteDatetime/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_datetime.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_datetime_modified_flag, "Setter for property 'read_write_datetime' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_datetime'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_optional_datetime_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_datetime' property."""
        assert server.read_write_optional_datetime == server_setup.read_write_optional_datetime, "Getter for property 'read_write_optional_datetime' returned incorrect value"

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

    def test_read_write_optional_datetime_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": datetime.now(UTC),
        }
        prop_obj = ReadWriteOptionalDatetimeProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalDatetime/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_datetime.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_datetime_modified_flag, "Setter for property 'read_write_optional_datetime' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_datetime'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_datetimes_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_datetimes' property."""
        assert server.read_write_two_datetimes == server_setup.read_write_two_datetimes, "Getter for property 'read_write_two_datetimes' returned incorrect value"

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

    def test_read_write_two_datetimes_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "first": datetime.now(UTC),
            "second": datetime.now(UTC),
        }
        prop_obj = ReadWriteTwoDatetimesProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoDatetimes/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_datetimes.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_datetimes_modified_flag, "Setter for property 'read_write_two_datetimes' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_datetimes'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_duration_property(self, server_setup, server):
        """Test that the server can get the 'read_write_duration' property."""
        assert server.read_write_duration == server_setup.read_write_duration, "Getter for property 'read_write_duration' returned incorrect value"

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

    def test_read_write_duration_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": timedelta(seconds=551),
        }
        prop_obj = ReadWriteDurationProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteDuration/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_duration.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_duration_modified_flag, "Setter for property 'read_write_duration' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_duration'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_optional_duration_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_duration' property."""
        assert server.read_write_optional_duration == server_setup.read_write_optional_duration, "Getter for property 'read_write_optional_duration' returned incorrect value"

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

    def test_read_write_optional_duration_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": timedelta(seconds=2332),
        }
        prop_obj = ReadWriteOptionalDurationProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalDuration/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_duration.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_duration_modified_flag, "Setter for property 'read_write_optional_duration' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_duration'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_durations_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_durations' property."""
        assert server.read_write_two_durations == server_setup.read_write_two_durations, "Getter for property 'read_write_two_durations' returned incorrect value"

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

    def test_read_write_two_durations_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "first": timedelta(seconds=551),
            "second": None,
        }
        prop_obj = ReadWriteTwoDurationsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoDurations/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_durations.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_durations_modified_flag, "Setter for property 'read_write_two_durations' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_durations'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_binary_property(self, server_setup, server):
        """Test that the server can get the 'read_write_binary' property."""
        assert server.read_write_binary == server_setup.read_write_binary, "Getter for property 'read_write_binary' returned incorrect value"

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

    def test_read_write_binary_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": b"example binary data",
        }
        prop_obj = ReadWriteBinaryProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteBinary/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_binary.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_binary_modified_flag, "Setter for property 'read_write_binary' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_binary'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_optional_binary_property(self, server_setup, server):
        """Test that the server can get the 'read_write_optional_binary' property."""
        assert server.read_write_optional_binary == server_setup.read_write_optional_binary, "Getter for property 'read_write_optional_binary' returned incorrect value"

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

    def test_read_write_optional_binary_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": b"example binary data",
        }
        prop_obj = ReadWriteOptionalBinaryProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteOptionalBinary/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_optional_binary.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_optional_binary_modified_flag, "Setter for property 'read_write_optional_binary' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_optional_binary'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_two_binaries_property(self, server_setup, server):
        """Test that the server can get the 'read_write_two_binaries' property."""
        assert server.read_write_two_binaries == server_setup.read_write_two_binaries, "Getter for property 'read_write_two_binaries' returned incorrect value"

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

    def test_read_write_two_binaries_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "first": b"example binary data",
            "second": b"example binary data",
        }
        prop_obj = ReadWriteTwoBinariesProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteTwoBinaries/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_two_binaries.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_two_binaries_modified_flag, "Setter for property 'read_write_two_binaries' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_two_binaries'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_list_of_strings_property(self, server_setup, server):
        """Test that the server can get the 'read_write_list_of_strings' property."""
        assert server.read_write_list_of_strings == server_setup.read_write_list_of_strings, "Getter for property 'read_write_list_of_strings' returned incorrect value"

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

    def test_read_write_list_of_strings_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "value": ["example", "apples"],
        }
        prop_obj = ReadWriteListOfStringsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteListOfStrings/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_list_of_strings.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_list_of_strings_modified_flag, "Setter for property 'read_write_list_of_strings' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_list_of_strings'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_read_write_lists_property(self, server_setup, server):
        """Test that the server can get the 'read_write_lists' property."""
        assert server.read_write_lists == server_setup.read_write_lists, "Getter for property 'read_write_lists' returned incorrect value"

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

    def test_read_write_lists_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "the_list": [Numbers.ONE, Numbers.ONE],
            "optional_list": [datetime.now(UTC), datetime.now(UTC)],
        }
        prop_obj = ReadWriteListsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="testable/{}/property/readWriteLists/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_read_write_lists.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.read_write_lists_modified_flag, "Setter for property 'read_write_lists' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'read_write_lists'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"


class TestTestableServerSignals:

    def test_server_emit_empty(self, server, mock_connection):
        """Test that the server can emit the 'empty' signal."""
        signal_data = {}  # type: Dict[str, Any]
        server.emit_empty(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/empty".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'empty'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/empty".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = EmptySignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_int(self, server, mock_connection):
        """Test that the server can emit the 'single_int' signal."""
        signal_data = {
            "value": 42,
        }  # type: Dict[str, Any]
        server.emit_single_int(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleInt".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_int'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleInt".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleIntSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_int(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_int' signal."""
        signal_data = {
            "value": 42,
        }  # type: Dict[str, Any]
        server.emit_single_optional_int(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalInt".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_int'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalInt".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalIntSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_integers(self, server, mock_connection):
        """Test that the server can emit the 'three_integers' signal."""
        signal_data = {
            "first": 42,
            "second": 42,
            "third": 42,
        }  # type: Dict[str, Any]
        server.emit_three_integers(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeIntegers".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_integers'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeIntegers".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeIntegersSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_string(self, server, mock_connection):
        """Test that the server can emit the 'single_string' signal."""
        signal_data = {
            "value": "apples",
        }  # type: Dict[str, Any]
        server.emit_single_string(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleString".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_string'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleString".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleStringSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_string(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_string' signal."""
        signal_data = {
            "value": "apples",
        }  # type: Dict[str, Any]
        server.emit_single_optional_string(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalString".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_string'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalString".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalStringSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_strings(self, server, mock_connection):
        """Test that the server can emit the 'three_strings' signal."""
        signal_data = {
            "first": "apples",
            "second": "apples",
            "third": "apples",
        }  # type: Dict[str, Any]
        server.emit_three_strings(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeStrings".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_strings'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeStrings".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeStringsSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_enum(self, server, mock_connection):
        """Test that the server can emit the 'single_enum' signal."""
        signal_data = {
            "value": Numbers.ONE,
        }  # type: Dict[str, Any]
        server.emit_single_enum(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleEnum".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_enum'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleEnum".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleEnumSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_enum(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_enum' signal."""
        signal_data = {
            "value": Numbers.ONE,
        }  # type: Dict[str, Any]
        server.emit_single_optional_enum(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalEnum".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_enum'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalEnum".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalEnumSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_enums(self, server, mock_connection):
        """Test that the server can emit the 'three_enums' signal."""
        signal_data = {
            "first": Numbers.ONE,
            "second": Numbers.ONE,
            "third": Numbers.ONE,
        }  # type: Dict[str, Any]
        server.emit_three_enums(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeEnums".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_enums'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeEnums".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeEnumsSignalPayload(**signal_data)  # type: ignore[arg-type]
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
        server.emit_single_struct(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleStruct".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_struct'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleStruct".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleStructSignalPayload(**signal_data)  # type: ignore[arg-type]
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
        }  # type: Dict[str, Any]
        server.emit_single_optional_struct(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalStruct".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_struct'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalStruct".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalStructSignalPayload(**signal_data)  # type: ignore[arg-type]
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
        }  # type: Dict[str, Any]
        server.emit_three_structs(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeStructs".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_structs'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeStructs".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeStructsSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_date_time(self, server, mock_connection):
        """Test that the server can emit the 'single_date_time' signal."""
        signal_data = {
            "value": datetime.now(UTC),
        }  # type: Dict[str, Any]
        server.emit_single_date_time(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleDateTime".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_date_time'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleDateTime".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleDateTimeSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_datetime(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_datetime' signal."""
        signal_data = {
            "value": datetime.now(UTC),
        }  # type: Dict[str, Any]
        server.emit_single_optional_datetime(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalDatetime".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_datetime'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalDatetime".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalDatetimeSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_date_times(self, server, mock_connection):
        """Test that the server can emit the 'three_date_times' signal."""
        signal_data = {
            "first": datetime.now(UTC),
            "second": datetime.now(UTC),
            "third": datetime.now(UTC),
        }  # type: Dict[str, Any]
        server.emit_three_date_times(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeDateTimes".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_date_times'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeDateTimes".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeDateTimesSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_duration(self, server, mock_connection):
        """Test that the server can emit the 'single_duration' signal."""
        signal_data = {
            "value": timedelta(seconds=3536),
        }  # type: Dict[str, Any]
        server.emit_single_duration(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleDuration".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_duration'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleDuration".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleDurationSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_duration(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_duration' signal."""
        signal_data = {
            "value": None,
        }  # type: Dict[str, Any]
        server.emit_single_optional_duration(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalDuration".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_duration'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalDuration".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalDurationSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_durations(self, server, mock_connection):
        """Test that the server can emit the 'three_durations' signal."""
        signal_data = {
            "first": timedelta(seconds=3536),
            "second": timedelta(seconds=3536),
            "third": None,
        }  # type: Dict[str, Any]
        server.emit_three_durations(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeDurations".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_durations'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeDurations".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeDurationsSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_binary(self, server, mock_connection):
        """Test that the server can emit the 'single_binary' signal."""
        signal_data = {
            "value": b"example binary data",
        }  # type: Dict[str, Any]
        server.emit_single_binary(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleBinary".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_binary'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleBinary".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleBinarySignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_binary(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_binary' signal."""
        signal_data = {
            "value": b"example binary data",
        }  # type: Dict[str, Any]
        server.emit_single_optional_binary(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalBinary".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_binary'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalBinary".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalBinarySignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_three_binaries(self, server, mock_connection):
        """Test that the server can emit the 'three_binaries' signal."""
        signal_data = {
            "first": b"example binary data",
            "second": b"example binary data",
            "third": b"example binary data",
        }  # type: Dict[str, Any]
        server.emit_three_binaries(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/threeBinaries".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'three_binaries'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/threeBinaries".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ThreeBinariesSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_array_of_integers(self, server, mock_connection):
        """Test that the server can emit the 'single_array_of_integers' signal."""
        signal_data = {
            "values": [42, 2022],
        }  # type: Dict[str, Any]
        server.emit_single_array_of_integers(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleArrayOfIntegers".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_array_of_integers'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleArrayOfIntegers".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleArrayOfIntegersSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_single_optional_array_of_strings(self, server, mock_connection):
        """Test that the server can emit the 'single_optional_array_of_strings' signal."""
        signal_data = {
            "values": ["apples", "foo"],
        }  # type: Dict[str, Any]
        server.emit_single_optional_array_of_strings(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/singleOptionalArrayOfStrings".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'single_optional_array_of_strings'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/singleOptionalArrayOfStrings".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SingleOptionalArrayOfStringsSignalPayload(**signal_data)  # type: ignore[arg-type]
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
        }  # type: Dict[str, Any]
        server.emit_array_of_every_type(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("testable/{}/signal/arrayOfEveryType".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'array_of_every_type'"

        msg = published_list[0]
        expected_topic = "testable/{}/signal/arrayOfEveryType".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = ArrayOfEveryTypeSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"


class TestTestableServerMethods:

    def test_server_handle_call_with_nothing_method(self, server, mock_connection):
        """Test that the server can handle the 'call_with_nothing' method."""
        handler_callback_data = None
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler() -> None:
            nonlocal received_args
            received_args = {}
            return handler_callback_data

        server.handle_call_with_nothing(handler)

        # Create and simulate receiving a method call message
        method_data = {}  # type: Dict[str, Any]
        method_obj = CallWithNothingMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callWithNothing".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_with_nothing' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_with_nothing'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = {}  # type: Dict[str, Any]
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_integer_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_integer' method."""
        handler_callback_data = 42
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> int:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_integer(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": 2020,
        }  # type: Dict[str, Any]
        method_obj = CallOneIntegerMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneInteger".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_integer' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_integer'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneIntegerMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_integer_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_integer' method."""
        handler_callback_data = 42
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> Optional[int]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_integer(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": 2020,
        }  # type: Dict[str, Any]
        method_obj = CallOptionalIntegerMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalInteger".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_integer' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_integer'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalIntegerMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_integers_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_integers' method."""
        handler_callback_data = CallThreeIntegersMethodResponse(output1=42, output2=42, output3=42)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeIntegersMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_integers(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": 2020,
            "input2": 42,
            "input3": 2022,
        }  # type: Dict[str, Any]
        method_obj = CallThreeIntegersMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeIntegers".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_integers' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_integers'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_string_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_string' method."""
        handler_callback_data = "apples"
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> str:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_string(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": "example",
        }  # type: Dict[str, Any]
        method_obj = CallOneStringMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneString".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_string' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_string'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneStringMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_string_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_string' method."""
        handler_callback_data = "apples"
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> Optional[str]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_string(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": "example",
        }  # type: Dict[str, Any]
        method_obj = CallOptionalStringMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalString".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_string' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_string'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalStringMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_strings_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_strings' method."""
        handler_callback_data = CallThreeStringsMethodResponse(output1="apples", output2="apples", output3="apples")
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeStringsMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_strings(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": "example",
            "input2": "apples",
            "input3": "foo",
        }  # type: Dict[str, Any]
        method_obj = CallThreeStringsMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeStrings".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_strings' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_strings'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_enum_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_enum' method."""
        handler_callback_data = Numbers.ONE
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> Numbers:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_enum(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": Numbers.ONE,
        }  # type: Dict[str, Any]
        method_obj = CallOneEnumMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneEnum".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_enum' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_enum'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneEnumMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_enum_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_enum' method."""
        handler_callback_data = Numbers.ONE
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> Optional[Numbers]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_enum(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": Numbers.ONE,
        }  # type: Dict[str, Any]
        method_obj = CallOptionalEnumMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalEnum".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_enum' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_enum'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalEnumMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_enums_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_enums' method."""
        handler_callback_data = CallThreeEnumsMethodResponse(output1=Numbers.ONE, output2=Numbers.ONE, output3=Numbers.ONE)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeEnumsMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_enums(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": Numbers.ONE,
            "input2": Numbers.ONE,
            "input3": Numbers.ONE,
        }  # type: Dict[str, Any]
        method_obj = CallThreeEnumsMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeEnums".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_enums' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_enums'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_struct_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_struct' method."""
        handler_callback_data = AllTypes(
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
        )
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> AllTypes:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_struct(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": AllTypes(
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
        }  # type: Dict[str, Any]
        method_obj = CallOneStructMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneStruct".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_struct' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_struct'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneStructMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_struct_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_struct' method."""
        handler_callback_data = AllTypes(
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
        )
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> AllTypes:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_struct(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": AllTypes(
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
        }  # type: Dict[str, Any]
        method_obj = CallOptionalStructMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalStruct".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_struct' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_struct'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalStructMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_structs_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_structs' method."""
        handler_callback_data = CallThreeStructsMethodResponse(
            output1=AllTypes(
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
            output2=AllTypes(
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
            output3=AllTypes(
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
        )
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeStructsMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_structs(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": AllTypes(
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
            "input3": AllTypes(
                the_bool=True,
                the_int=2022,
                the_number=1.0,
                the_str="foo",
                the_enum=Numbers.ONE,
                an_entry_object=Entry(key=2022, value="foo"),
                date_and_time=datetime.now(UTC),
                time_duration=timedelta(seconds=975),
                data=b"example binary data",
                optional_integer=2022,
                optional_string="foo",
                optional_enum=Numbers.ONE,
                optional_entry_object=Entry(key=2022, value="foo"),
                optional_date_time=datetime.now(UTC),
                optional_duration=timedelta(seconds=2428),
                optional_binary=b"example binary data",
                array_of_integers=[2022, 2022],
                optional_array_of_integers=[2022, 2022],
                array_of_strings=["foo", "foo"],
                optional_array_of_strings=["foo", "foo"],
                array_of_enums=[Numbers.ONE, Numbers.ONE],
                optional_array_of_enums=[Numbers.ONE, Numbers.ONE],
                array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                optional_array_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                array_of_durations=[timedelta(seconds=975), timedelta(seconds=967)],
                optional_array_of_durations=[timedelta(seconds=975), timedelta(seconds=967)],
                array_of_binaries=[b"example binary data", b"example binary data"],
                optional_array_of_binaries=[b"example binary data", b"example binary data"],
                array_of_entry_objects=[Entry(key=2022, value="foo"), Entry(key=2022, value="foo")],
                optional_array_of_entry_objects=[Entry(key=2022, value="foo"), Entry(key=2022, value="foo")],
            ),
        }  # type: Dict[str, Any]
        method_obj = CallThreeStructsMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeStructs".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_structs' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_structs'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_date_time_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_date_time' method."""
        handler_callback_data = datetime.now(UTC)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> datetime:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_date_time(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": datetime.now(UTC),
        }  # type: Dict[str, Any]
        method_obj = CallOneDateTimeMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneDateTime".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_date_time' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_date_time'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneDateTimeMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_date_time_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_date_time' method."""
        handler_callback_data = datetime.now(UTC)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> Optional[datetime]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_date_time(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": datetime.now(UTC),
        }  # type: Dict[str, Any]
        method_obj = CallOptionalDateTimeMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalDateTime".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_date_time' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_date_time'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalDateTimeMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_date_times_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_date_times' method."""
        handler_callback_data = CallThreeDateTimesMethodResponse(output1=datetime.now(UTC), output2=datetime.now(UTC), output3=None)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeDateTimesMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_date_times(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": datetime.now(UTC),
            "input2": datetime.now(UTC),
            "input3": datetime.now(UTC),
        }  # type: Dict[str, Any]
        method_obj = CallThreeDateTimesMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeDateTimes".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_date_times' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_date_times'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_duration_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_duration' method."""
        handler_callback_data = timedelta(seconds=3536)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> timedelta:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_duration(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": timedelta(seconds=551),
        }  # type: Dict[str, Any]
        method_obj = CallOneDurationMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneDuration".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_duration' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_duration'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneDurationMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_duration_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_duration' method."""
        handler_callback_data = None
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> Optional[timedelta]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_duration(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": timedelta(seconds=2332),
        }  # type: Dict[str, Any]
        method_obj = CallOptionalDurationMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalDuration".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_duration' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_duration'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalDurationMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_durations_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_durations' method."""
        handler_callback_data = CallThreeDurationsMethodResponse(output1=timedelta(seconds=3536), output2=timedelta(seconds=3536), output3=None)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeDurationsMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_durations(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": timedelta(seconds=551),
            "input2": timedelta(seconds=3536),
            "input3": timedelta(seconds=2428),
        }  # type: Dict[str, Any]
        method_obj = CallThreeDurationsMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeDurations".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_durations' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_durations'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_binary_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_binary' method."""
        handler_callback_data = b"example binary data"
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> bytes:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_binary(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": b"example binary data",
        }  # type: Dict[str, Any]
        method_obj = CallOneBinaryMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneBinary".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_binary' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_binary'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneBinaryMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_binary_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_binary' method."""
        handler_callback_data = b"example binary data"
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> bytes:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_binary(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": b"example binary data",
        }  # type: Dict[str, Any]
        method_obj = CallOptionalBinaryMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalBinary".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_binary' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_binary'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalBinaryMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_three_binaries_method(self, server, mock_connection):
        """Test that the server can handle the 'call_three_binaries' method."""
        handler_callback_data = CallThreeBinariesMethodResponse(output1=b"example binary data", output2=b"example binary data", output3=b"example binary data")
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2, input3) -> CallThreeBinariesMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
                "input3": input3,
            }
            return handler_callback_data

        server.handle_call_three_binaries(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": b"example binary data",
            "input2": b"example binary data",
            "input3": b"example binary data",
        }  # type: Dict[str, Any]
        method_obj = CallThreeBinariesMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callThreeBinaries".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_three_binaries' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_three_binaries'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_one_list_of_integers_method(self, server, mock_connection):
        """Test that the server can handle the 'call_one_list_of_integers' method."""
        handler_callback_data = [42, 2022]
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> List[int]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_one_list_of_integers(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": [2020, 42],
        }  # type: Dict[str, Any]
        method_obj = CallOneListOfIntegersMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOneListOfIntegers".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_one_list_of_integers' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_one_list_of_integers'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOneListOfIntegersMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_optional_list_of_floats_method(self, server, mock_connection):
        """Test that the server can handle the 'call_optional_list_of_floats' method."""
        handler_callback_data = [3.14, 1.0]
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1) -> List[float]:
            nonlocal received_args
            received_args = {
                "input1": input1,
            }
            return handler_callback_data

        server.handle_call_optional_list_of_floats(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": [1.0, 3.14],
        }  # type: Dict[str, Any]
        method_obj = CallOptionalListOfFloatsMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callOptionalListOfFloats".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_optional_list_of_floats' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_optional_list_of_floats'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = CallOptionalListOfFloatsMethodResponse(output1=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_call_two_lists_method(self, server, mock_connection):
        """Test that the server can handle the 'call_two_lists' method."""
        handler_callback_data = CallTwoListsMethodResponse(output1=[Numbers.ONE, Numbers.ONE], output2=["apples", "foo"])
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(input1, input2) -> CallTwoListsMethodResponse:
            nonlocal received_args
            received_args = {
                "input1": input1,
                "input2": input2,
            }
            return handler_callback_data

        server.handle_call_two_lists(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "input1": [Numbers.ONE, Numbers.ONE],
            "input2": ["apples", "foo"],
        }  # type: Dict[str, Any]
        method_obj = CallTwoListsMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="testable/{}/method/callTwoLists".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'call_two_lists' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'call_two_lists'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"
