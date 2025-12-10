"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the testable interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
import isodate
import functools
from concurrent.futures import Future

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from .connection import IBrokerConnection
from .method_codes import *
from .interface_types import *


from .property import TestableInitialPropertyValues


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T
    mutex = threading.Lock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)

    def get_value(self) -> T:
        with self.mutex:
            return self.value

    def set_value(self, new_value: T) -> T:
        with self.mutex:
            self.value = new_value
            return self.value


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
    callback: Optional[Callable] = None


class TestableServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str, initial_property_values: TestableInitialPropertyValues):
        self._logger = logging.getLogger(f"TestableServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing TestableServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_read_write_integer: PropertyControls[int] = PropertyControls(value=initial_property_values.read_write_integer, version=initial_property_values.read_write_integer_version)
        self._property_read_write_integer.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteInteger/setValue".format(self._instance_id), self._receive_read_write_integer_update_request_message
        )

        self._property_read_only_integer: PropertyControls[int] = PropertyControls(value=initial_property_values.read_only_integer, version=initial_property_values.read_only_integer_version)
        self._property_read_only_integer.subscription_id = self._conn.subscribe(
            "testable/{}/property/readOnlyInteger/setValue".format(self._instance_id), self._receive_read_only_integer_update_request_message
        )

        self._property_read_write_optional_integer: PropertyControls[int] = PropertyControls(
            value=initial_property_values.read_write_optional_integer, version=initial_property_values.read_write_optional_integer_version
        )
        self._property_read_write_optional_integer.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalInteger/setValue".format(self._instance_id), self._receive_read_write_optional_integer_update_request_message
        )

        self._property_read_write_two_integers: PropertyControls[ReadWriteTwoIntegersProperty] = PropertyControls(
            value=initial_property_values.read_write_two_integers, version=initial_property_values.read_write_two_integers_version
        )
        self._property_read_write_two_integers.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoIntegers/setValue".format(self._instance_id), self._receive_read_write_two_integers_update_request_message
        )

        self._property_read_only_string: PropertyControls[str] = PropertyControls(value=initial_property_values.read_only_string, version=initial_property_values.read_only_string_version)
        self._property_read_only_string.subscription_id = self._conn.subscribe(
            "testable/{}/property/readOnlyString/setValue".format(self._instance_id), self._receive_read_only_string_update_request_message
        )

        self._property_read_write_string: PropertyControls[str] = PropertyControls(value=initial_property_values.read_write_string, version=initial_property_values.read_write_string_version)
        self._property_read_write_string.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteString/setValue".format(self._instance_id), self._receive_read_write_string_update_request_message
        )

        self._property_read_write_optional_string: PropertyControls[str] = PropertyControls(
            value=initial_property_values.read_write_optional_string, version=initial_property_values.read_write_optional_string_version
        )
        self._property_read_write_optional_string.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalString/setValue".format(self._instance_id), self._receive_read_write_optional_string_update_request_message
        )

        self._property_read_write_two_strings: PropertyControls[ReadWriteTwoStringsProperty] = PropertyControls(
            value=initial_property_values.read_write_two_strings, version=initial_property_values.read_write_two_strings_version
        )
        self._property_read_write_two_strings.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoStrings/setValue".format(self._instance_id), self._receive_read_write_two_strings_update_request_message
        )

        self._property_read_write_struct: PropertyControls[AllTypes] = PropertyControls(value=initial_property_values.read_write_struct, version=initial_property_values.read_write_struct_version)
        self._property_read_write_struct.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteStruct/setValue".format(self._instance_id), self._receive_read_write_struct_update_request_message
        )

        self._property_read_write_optional_struct: PropertyControls[AllTypes] = PropertyControls(
            value=initial_property_values.read_write_optional_struct, version=initial_property_values.read_write_optional_struct_version
        )
        self._property_read_write_optional_struct.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalStruct/setValue".format(self._instance_id), self._receive_read_write_optional_struct_update_request_message
        )

        self._property_read_write_two_structs: PropertyControls[ReadWriteTwoStructsProperty] = PropertyControls(
            value=initial_property_values.read_write_two_structs, version=initial_property_values.read_write_two_structs_version
        )
        self._property_read_write_two_structs.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoStructs/setValue".format(self._instance_id), self._receive_read_write_two_structs_update_request_message
        )

        self._property_read_only_enum: PropertyControls[Numbers] = PropertyControls(value=initial_property_values.read_only_enum, version=initial_property_values.read_only_enum_version)
        self._property_read_only_enum.subscription_id = self._conn.subscribe(
            "testable/{}/property/readOnlyEnum/setValue".format(self._instance_id), self._receive_read_only_enum_update_request_message
        )

        self._property_read_write_enum: PropertyControls[Numbers] = PropertyControls(value=initial_property_values.read_write_enum, version=initial_property_values.read_write_enum_version)
        self._property_read_write_enum.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteEnum/setValue".format(self._instance_id), self._receive_read_write_enum_update_request_message
        )

        self._property_read_write_optional_enum: PropertyControls[Numbers] = PropertyControls(
            value=initial_property_values.read_write_optional_enum, version=initial_property_values.read_write_optional_enum_version
        )
        self._property_read_write_optional_enum.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalEnum/setValue".format(self._instance_id), self._receive_read_write_optional_enum_update_request_message
        )

        self._property_read_write_two_enums: PropertyControls[ReadWriteTwoEnumsProperty] = PropertyControls(
            value=initial_property_values.read_write_two_enums, version=initial_property_values.read_write_two_enums_version
        )
        self._property_read_write_two_enums.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoEnums/setValue".format(self._instance_id), self._receive_read_write_two_enums_update_request_message
        )

        self._property_read_write_datetime: PropertyControls[datetime] = PropertyControls(
            value=initial_property_values.read_write_datetime, version=initial_property_values.read_write_datetime_version
        )
        self._property_read_write_datetime.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteDatetime/setValue".format(self._instance_id), self._receive_read_write_datetime_update_request_message
        )

        self._property_read_write_optional_datetime: PropertyControls[datetime] = PropertyControls(
            value=initial_property_values.read_write_optional_datetime, version=initial_property_values.read_write_optional_datetime_version
        )
        self._property_read_write_optional_datetime.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalDatetime/setValue".format(self._instance_id), self._receive_read_write_optional_datetime_update_request_message
        )

        self._property_read_write_two_datetimes: PropertyControls[ReadWriteTwoDatetimesProperty] = PropertyControls(
            value=initial_property_values.read_write_two_datetimes, version=initial_property_values.read_write_two_datetimes_version
        )
        self._property_read_write_two_datetimes.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoDatetimes/setValue".format(self._instance_id), self._receive_read_write_two_datetimes_update_request_message
        )

        self._property_read_write_duration: PropertyControls[timedelta] = PropertyControls(
            value=initial_property_values.read_write_duration, version=initial_property_values.read_write_duration_version
        )
        self._property_read_write_duration.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteDuration/setValue".format(self._instance_id), self._receive_read_write_duration_update_request_message
        )

        self._property_read_write_optional_duration: PropertyControls[timedelta] = PropertyControls(
            value=initial_property_values.read_write_optional_duration, version=initial_property_values.read_write_optional_duration_version
        )
        self._property_read_write_optional_duration.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalDuration/setValue".format(self._instance_id), self._receive_read_write_optional_duration_update_request_message
        )

        self._property_read_write_two_durations: PropertyControls[ReadWriteTwoDurationsProperty] = PropertyControls(
            value=initial_property_values.read_write_two_durations, version=initial_property_values.read_write_two_durations_version
        )
        self._property_read_write_two_durations.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoDurations/setValue".format(self._instance_id), self._receive_read_write_two_durations_update_request_message
        )

        self._property_read_write_binary: PropertyControls[bytes] = PropertyControls(value=initial_property_values.read_write_binary, version=initial_property_values.read_write_binary_version)
        self._property_read_write_binary.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteBinary/setValue".format(self._instance_id), self._receive_read_write_binary_update_request_message
        )

        self._property_read_write_optional_binary: PropertyControls[bytes] = PropertyControls(
            value=initial_property_values.read_write_optional_binary, version=initial_property_values.read_write_optional_binary_version
        )
        self._property_read_write_optional_binary.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteOptionalBinary/setValue".format(self._instance_id), self._receive_read_write_optional_binary_update_request_message
        )

        self._property_read_write_two_binaries: PropertyControls[ReadWriteTwoBinariesProperty] = PropertyControls(
            value=initial_property_values.read_write_two_binaries, version=initial_property_values.read_write_two_binaries_version
        )
        self._property_read_write_two_binaries.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteTwoBinaries/setValue".format(self._instance_id), self._receive_read_write_two_binaries_update_request_message
        )

        self._property_read_write_list_of_strings: PropertyControls[list] = PropertyControls(
            value=initial_property_values.read_write_list_of_strings, version=initial_property_values.read_write_list_of_strings_version
        )
        self._property_read_write_list_of_strings.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteListOfStrings/setValue".format(self._instance_id), self._receive_read_write_list_of_strings_update_request_message
        )

        self._property_read_write_lists: PropertyControls[ReadWriteListsProperty] = PropertyControls(
            value=initial_property_values.read_write_lists, version=initial_property_values.read_write_lists_version
        )
        self._property_read_write_lists.subscription_id = self._conn.subscribe(
            "testable/{}/property/readWriteLists/setValue".format(self._instance_id), self._receive_read_write_lists_update_request_message
        )

        self._method_call_with_nothing = MethodControls()
        self._method_call_with_nothing.subscription_id = self._conn.subscribe("testable/{}/method/callWithNothing".format(self._instance_id), self._process_call_with_nothing_call)

        self._method_call_one_integer = MethodControls()
        self._method_call_one_integer.subscription_id = self._conn.subscribe("testable/{}/method/callOneInteger".format(self._instance_id), self._process_call_one_integer_call)

        self._method_call_optional_integer = MethodControls()
        self._method_call_optional_integer.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalInteger".format(self._instance_id), self._process_call_optional_integer_call)

        self._method_call_three_integers = MethodControls()
        self._method_call_three_integers.subscription_id = self._conn.subscribe("testable/{}/method/callThreeIntegers".format(self._instance_id), self._process_call_three_integers_call)

        self._method_call_one_string = MethodControls()
        self._method_call_one_string.subscription_id = self._conn.subscribe("testable/{}/method/callOneString".format(self._instance_id), self._process_call_one_string_call)

        self._method_call_optional_string = MethodControls()
        self._method_call_optional_string.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalString".format(self._instance_id), self._process_call_optional_string_call)

        self._method_call_three_strings = MethodControls()
        self._method_call_three_strings.subscription_id = self._conn.subscribe("testable/{}/method/callThreeStrings".format(self._instance_id), self._process_call_three_strings_call)

        self._method_call_one_enum = MethodControls()
        self._method_call_one_enum.subscription_id = self._conn.subscribe("testable/{}/method/callOneEnum".format(self._instance_id), self._process_call_one_enum_call)

        self._method_call_optional_enum = MethodControls()
        self._method_call_optional_enum.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalEnum".format(self._instance_id), self._process_call_optional_enum_call)

        self._method_call_three_enums = MethodControls()
        self._method_call_three_enums.subscription_id = self._conn.subscribe("testable/{}/method/callThreeEnums".format(self._instance_id), self._process_call_three_enums_call)

        self._method_call_one_struct = MethodControls()
        self._method_call_one_struct.subscription_id = self._conn.subscribe("testable/{}/method/callOneStruct".format(self._instance_id), self._process_call_one_struct_call)

        self._method_call_optional_struct = MethodControls()
        self._method_call_optional_struct.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalStruct".format(self._instance_id), self._process_call_optional_struct_call)

        self._method_call_three_structs = MethodControls()
        self._method_call_three_structs.subscription_id = self._conn.subscribe("testable/{}/method/callThreeStructs".format(self._instance_id), self._process_call_three_structs_call)

        self._method_call_one_date_time = MethodControls()
        self._method_call_one_date_time.subscription_id = self._conn.subscribe("testable/{}/method/callOneDateTime".format(self._instance_id), self._process_call_one_date_time_call)

        self._method_call_optional_date_time = MethodControls()
        self._method_call_optional_date_time.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalDateTime".format(self._instance_id), self._process_call_optional_date_time_call)

        self._method_call_three_date_times = MethodControls()
        self._method_call_three_date_times.subscription_id = self._conn.subscribe("testable/{}/method/callThreeDateTimes".format(self._instance_id), self._process_call_three_date_times_call)

        self._method_call_one_duration = MethodControls()
        self._method_call_one_duration.subscription_id = self._conn.subscribe("testable/{}/method/callOneDuration".format(self._instance_id), self._process_call_one_duration_call)

        self._method_call_optional_duration = MethodControls()
        self._method_call_optional_duration.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalDuration".format(self._instance_id), self._process_call_optional_duration_call)

        self._method_call_three_durations = MethodControls()
        self._method_call_three_durations.subscription_id = self._conn.subscribe("testable/{}/method/callThreeDurations".format(self._instance_id), self._process_call_three_durations_call)

        self._method_call_one_binary = MethodControls()
        self._method_call_one_binary.subscription_id = self._conn.subscribe("testable/{}/method/callOneBinary".format(self._instance_id), self._process_call_one_binary_call)

        self._method_call_optional_binary = MethodControls()
        self._method_call_optional_binary.subscription_id = self._conn.subscribe("testable/{}/method/callOptionalBinary".format(self._instance_id), self._process_call_optional_binary_call)

        self._method_call_three_binaries = MethodControls()
        self._method_call_three_binaries.subscription_id = self._conn.subscribe("testable/{}/method/callThreeBinaries".format(self._instance_id), self._process_call_three_binaries_call)

        self._method_call_one_list_of_integers = MethodControls()
        self._method_call_one_list_of_integers.subscription_id = self._conn.subscribe(
            "testable/{}/method/callOneListOfIntegers".format(self._instance_id), self._process_call_one_list_of_integers_call
        )

        self._method_call_optional_list_of_floats = MethodControls()
        self._method_call_optional_list_of_floats.subscription_id = self._conn.subscribe(
            "testable/{}/method/callOptionalListOfFloats".format(self._instance_id), self._process_call_optional_list_of_floats_call
        )

        self._method_call_two_lists = MethodControls()
        self._method_call_two_lists.subscription_id = self._conn.subscribe("testable/{}/method/callTwoLists".format(self._instance_id), self._process_call_two_lists_call)

        self._publish_all_properties()
        self._logger.debug("Starting interface advertisement thread")
        self._advertise_thread = threading.Thread(target=self.loop_publishing_interface_info)
        self._advertise_thread.start()

    def __del__(self):
        self._running = False
        self._conn.unpublish_retained(self._conn.online_topic)
        self._advertise_thread.join()

    def loop_publishing_interface_info(self):
        """We have a discovery topic separate from the MQTT client discovery topic.
        We publish it periodically, but with a Message Expiry interval."""
        self._publish_interface_info()
        while self._running:
            if self._conn.is_connected():
                self._publish_interface_info()
                sleep(self._re_advertise_server_interval_seconds)
            else:
                sleep(2)

    def _publish_interface_info(self):
        data = InterfaceInfo(instance=self._instance_id, connection_topic=self._conn.online_topic, timestamp=datetime.now(UTC).isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = "testable/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        self._conn.publish_status(topic, data, expiry)

    def _publish_all_properties(self):

        with self._property_read_write_integer.mutex:
            prop_obj = ReadWriteIntegerProperty(value=self._property_read_write_integer.value)
            self._conn.publish_property_state("testable/{}/property/readWriteInteger/value".format(self._instance_id), prop_obj, self._property_read_write_integer.version)

        with self._property_read_only_integer.mutex:
            prop_obj = ReadOnlyIntegerProperty(value=self._property_read_only_integer.value)
            self._conn.publish_property_state("testable/{}/property/readOnlyInteger/value".format(self._instance_id), prop_obj, self._property_read_only_integer.version)

        with self._property_read_write_optional_integer.mutex:
            prop_obj = ReadWriteOptionalIntegerProperty(value=self._property_read_write_optional_integer.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalInteger/value".format(self._instance_id), prop_obj, self._property_read_write_optional_integer.version)

        with self._property_read_write_two_integers.mutex:

            prop_obj = self._property_read_write_two_integers.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoIntegers/value".format(self._instance_id), prop_obj, self._property_read_write_two_integers.version)

        with self._property_read_only_string.mutex:
            prop_obj = ReadOnlyStringProperty(value=self._property_read_only_string.value)
            self._conn.publish_property_state("testable/{}/property/readOnlyString/value".format(self._instance_id), prop_obj, self._property_read_only_string.version)

        with self._property_read_write_string.mutex:
            prop_obj = ReadWriteStringProperty(value=self._property_read_write_string.value)
            self._conn.publish_property_state("testable/{}/property/readWriteString/value".format(self._instance_id), prop_obj, self._property_read_write_string.version)

        with self._property_read_write_optional_string.mutex:
            prop_obj = ReadWriteOptionalStringProperty(value=self._property_read_write_optional_string.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalString/value".format(self._instance_id), prop_obj, self._property_read_write_optional_string.version)

        with self._property_read_write_two_strings.mutex:

            prop_obj = self._property_read_write_two_strings.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoStrings/value".format(self._instance_id), prop_obj, self._property_read_write_two_strings.version)

        with self._property_read_write_struct.mutex:
            prop_obj = ReadWriteStructProperty(value=self._property_read_write_struct.value)
            self._conn.publish_property_state("testable/{}/property/readWriteStruct/value".format(self._instance_id), prop_obj, self._property_read_write_struct.version)

        with self._property_read_write_optional_struct.mutex:
            prop_obj = ReadWriteOptionalStructProperty(value=self._property_read_write_optional_struct.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalStruct/value".format(self._instance_id), prop_obj, self._property_read_write_optional_struct.version)

        with self._property_read_write_two_structs.mutex:

            prop_obj = self._property_read_write_two_structs.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoStructs/value".format(self._instance_id), prop_obj, self._property_read_write_two_structs.version)

        with self._property_read_only_enum.mutex:
            prop_obj = ReadOnlyEnumProperty(value=self._property_read_only_enum.value)
            self._conn.publish_property_state("testable/{}/property/readOnlyEnum/value".format(self._instance_id), prop_obj, self._property_read_only_enum.version)

        with self._property_read_write_enum.mutex:
            prop_obj = ReadWriteEnumProperty(value=self._property_read_write_enum.value)
            self._conn.publish_property_state("testable/{}/property/readWriteEnum/value".format(self._instance_id), prop_obj, self._property_read_write_enum.version)

        with self._property_read_write_optional_enum.mutex:
            prop_obj = ReadWriteOptionalEnumProperty(value=self._property_read_write_optional_enum.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalEnum/value".format(self._instance_id), prop_obj, self._property_read_write_optional_enum.version)

        with self._property_read_write_two_enums.mutex:

            prop_obj = self._property_read_write_two_enums.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoEnums/value".format(self._instance_id), prop_obj, self._property_read_write_two_enums.version)

        with self._property_read_write_datetime.mutex:
            prop_obj = ReadWriteDatetimeProperty(value=self._property_read_write_datetime.value)
            self._conn.publish_property_state("testable/{}/property/readWriteDatetime/value".format(self._instance_id), prop_obj, self._property_read_write_datetime.version)

        with self._property_read_write_optional_datetime.mutex:
            prop_obj = ReadWriteOptionalDatetimeProperty(value=self._property_read_write_optional_datetime.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalDatetime/value".format(self._instance_id), prop_obj, self._property_read_write_optional_datetime.version)

        with self._property_read_write_two_datetimes.mutex:

            prop_obj = self._property_read_write_two_datetimes.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoDatetimes/value".format(self._instance_id), prop_obj, self._property_read_write_two_datetimes.version)

        with self._property_read_write_duration.mutex:
            prop_obj = ReadWriteDurationProperty(value=self._property_read_write_duration.value)
            self._conn.publish_property_state("testable/{}/property/readWriteDuration/value".format(self._instance_id), prop_obj, self._property_read_write_duration.version)

        with self._property_read_write_optional_duration.mutex:
            prop_obj = ReadWriteOptionalDurationProperty(value=self._property_read_write_optional_duration.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalDuration/value".format(self._instance_id), prop_obj, self._property_read_write_optional_duration.version)

        with self._property_read_write_two_durations.mutex:

            prop_obj = self._property_read_write_two_durations.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoDurations/value".format(self._instance_id), prop_obj, self._property_read_write_two_durations.version)

        with self._property_read_write_binary.mutex:
            prop_obj = ReadWriteBinaryProperty(value=self._property_read_write_binary.value)
            self._conn.publish_property_state("testable/{}/property/readWriteBinary/value".format(self._instance_id), prop_obj, self._property_read_write_binary.version)

        with self._property_read_write_optional_binary.mutex:
            prop_obj = ReadWriteOptionalBinaryProperty(value=self._property_read_write_optional_binary.value)
            self._conn.publish_property_state("testable/{}/property/readWriteOptionalBinary/value".format(self._instance_id), prop_obj, self._property_read_write_optional_binary.version)

        with self._property_read_write_two_binaries.mutex:

            prop_obj = self._property_read_write_two_binaries.value
            self._conn.publish_property_state("testable/{}/property/readWriteTwoBinaries/value".format(self._instance_id), prop_obj, self._property_read_write_two_binaries.version)

        with self._property_read_write_list_of_strings.mutex:
            prop_obj = ReadWriteListOfStringsProperty(value=self._property_read_write_list_of_strings.value)
            self._conn.publish_property_state("testable/{}/property/readWriteListOfStrings/value".format(self._instance_id), prop_obj, self._property_read_write_list_of_strings.version)

        with self._property_read_write_lists.mutex:

            prop_obj = self._property_read_write_lists.value
            self._conn.publish_property_state("testable/{}/property/readWriteLists/value".format(self._instance_id), prop_obj, self._property_read_write_lists.version)

    def _send_reply_error_message(self, return_code: MethodReturnCode, request_properties: Dict[str, Any], debug_info: Optional[str] = None):
        correlation_id = request_properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = request_properties.get("ResponseTopic")  # type: Optional[str]
        if response_topic is not None:
            self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_info)

    def _receive_read_write_integer_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteIntegerProperty(value=self._property_read_write_integer.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_integer.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_integer.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_integer.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_integer.version}",
                    )
                return

            try:
                prop_obj = ReadWriteIntegerProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_integer.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_integer.mutex:
                self._property_read_write_integer.version += 1
                self._property_read_write_integer.set_value(prop_value)

                prop_obj = ReadWriteIntegerProperty(value=self._property_read_write_integer.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteInteger/value".format(self._instance_id), prop_obj, int(self._property_read_write_integer.version))

            if response_topic is not None:

                prop_obj = ReadWriteIntegerProperty(value=self._property_read_write_integer.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_integer.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_integer.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteIntegerProperty(value=self._property_read_write_integer.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_integer.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_integer_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalIntegerProperty(value=self._property_read_write_optional_integer.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_integer.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_integer.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_integer.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_integer.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalIntegerProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_integer.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_integer.mutex:
                self._property_read_write_optional_integer.version += 1
                self._property_read_write_optional_integer.set_value(prop_value)

                prop_obj = ReadWriteOptionalIntegerProperty(value=self._property_read_write_optional_integer.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalInteger/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_integer.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalIntegerProperty(value=self._property_read_write_optional_integer.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_integer.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_integer.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalIntegerProperty(value=self._property_read_write_optional_integer.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_integer.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_integers_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_integers.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_integers.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_integers.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_integers.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_integers.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoIntegersProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_integers.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_integers.mutex:
                self._property_read_write_two_integers.version += 1
                self._property_read_write_two_integers.set_value(prop_value)

                prop_obj = self._property_read_write_two_integers.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoIntegers/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_integers.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_integers.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_integers.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_integers.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_integers.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_integers.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_string_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteStringProperty(value=self._property_read_write_string.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_string.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_string.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_string.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_string.version}",
                    )
                return

            try:
                prop_obj = ReadWriteStringProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_string.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_string.mutex:
                self._property_read_write_string.version += 1
                self._property_read_write_string.set_value(prop_value)

                prop_obj = ReadWriteStringProperty(value=self._property_read_write_string.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteString/value".format(self._instance_id), prop_obj, int(self._property_read_write_string.version))

            if response_topic is not None:

                prop_obj = ReadWriteStringProperty(value=self._property_read_write_string.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_string.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_string.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteStringProperty(value=self._property_read_write_string.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_string.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_string_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalStringProperty(value=self._property_read_write_optional_string.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_string.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_string.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_string.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_string.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalStringProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_string.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_string.mutex:
                self._property_read_write_optional_string.version += 1
                self._property_read_write_optional_string.set_value(prop_value)

                prop_obj = ReadWriteOptionalStringProperty(value=self._property_read_write_optional_string.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalString/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_string.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalStringProperty(value=self._property_read_write_optional_string.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_string.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_string.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalStringProperty(value=self._property_read_write_optional_string.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_string.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_strings_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_strings.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_strings.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_strings.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_strings.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_strings.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoStringsProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_strings.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_strings.mutex:
                self._property_read_write_two_strings.version += 1
                self._property_read_write_two_strings.set_value(prop_value)

                prop_obj = self._property_read_write_two_strings.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoStrings/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_strings.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_strings.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_strings.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_strings.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_strings.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_strings.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_struct_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteStructProperty(value=self._property_read_write_struct.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_struct.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_struct.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_struct.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_struct.version}",
                    )
                return

            try:
                prop_obj = ReadWriteStructProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_struct.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_struct.mutex:
                self._property_read_write_struct.version += 1
                self._property_read_write_struct.set_value(prop_value)

                prop_obj = ReadWriteStructProperty(value=self._property_read_write_struct.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteStruct/value".format(self._instance_id), prop_obj, int(self._property_read_write_struct.version))

            if response_topic is not None:

                prop_obj = ReadWriteStructProperty(value=self._property_read_write_struct.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_struct.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_struct.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteStructProperty(value=self._property_read_write_struct.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_struct.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_struct_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalStructProperty(value=self._property_read_write_optional_struct.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_struct.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_struct.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_struct.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_struct.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalStructProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_struct.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_struct.mutex:
                self._property_read_write_optional_struct.version += 1
                self._property_read_write_optional_struct.set_value(prop_value)

                prop_obj = ReadWriteOptionalStructProperty(value=self._property_read_write_optional_struct.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalStruct/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_struct.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalStructProperty(value=self._property_read_write_optional_struct.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_struct.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_struct.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalStructProperty(value=self._property_read_write_optional_struct.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_struct.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_structs_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_structs.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_structs.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_structs.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_structs.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_structs.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoStructsProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_structs.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_structs.mutex:
                self._property_read_write_two_structs.version += 1
                self._property_read_write_two_structs.set_value(prop_value)

                prop_obj = self._property_read_write_two_structs.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoStructs/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_structs.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_structs.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_structs.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_structs.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_structs.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_structs.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_enum_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteEnumProperty(value=self._property_read_write_enum.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_enum.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_enum.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_enum.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_enum.version}",
                    )
                return

            try:
                prop_obj = ReadWriteEnumProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_enum.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_enum.mutex:
                self._property_read_write_enum.version += 1
                self._property_read_write_enum.set_value(prop_value)

                prop_obj = ReadWriteEnumProperty(value=self._property_read_write_enum.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteEnum/value".format(self._instance_id), prop_obj, int(self._property_read_write_enum.version))

            if response_topic is not None:

                prop_obj = ReadWriteEnumProperty(value=self._property_read_write_enum.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_enum.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_enum.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteEnumProperty(value=self._property_read_write_enum.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_enum.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_enum_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalEnumProperty(value=self._property_read_write_optional_enum.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_enum.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_enum.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_enum.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_enum.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalEnumProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_enum.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_enum.mutex:
                self._property_read_write_optional_enum.version += 1
                self._property_read_write_optional_enum.set_value(prop_value)

                prop_obj = ReadWriteOptionalEnumProperty(value=self._property_read_write_optional_enum.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalEnum/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_enum.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalEnumProperty(value=self._property_read_write_optional_enum.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_enum.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_enum.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalEnumProperty(value=self._property_read_write_optional_enum.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_enum.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_enums_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_enums.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_enums.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_enums.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_enums.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_enums.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoEnumsProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_enums.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_enums.mutex:
                self._property_read_write_two_enums.version += 1
                self._property_read_write_two_enums.set_value(prop_value)

                prop_obj = self._property_read_write_two_enums.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoEnums/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_enums.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_enums.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_enums.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_enums.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_enums.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_enums.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_datetime_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteDatetimeProperty(value=self._property_read_write_datetime.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_datetime.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_datetime.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_datetime.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_datetime.version}",
                    )
                return

            try:
                prop_obj = ReadWriteDatetimeProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_datetime.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_datetime.mutex:
                self._property_read_write_datetime.version += 1
                self._property_read_write_datetime.set_value(prop_value)

                prop_obj = ReadWriteDatetimeProperty(value=self._property_read_write_datetime.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteDatetime/value".format(self._instance_id), prop_obj, int(self._property_read_write_datetime.version))

            if response_topic is not None:

                prop_obj = ReadWriteDatetimeProperty(value=self._property_read_write_datetime.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_datetime.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_datetime.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteDatetimeProperty(value=self._property_read_write_datetime.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_datetime.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_datetime_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalDatetimeProperty(value=self._property_read_write_optional_datetime.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_datetime.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_datetime.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_datetime.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_datetime.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalDatetimeProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_datetime.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_datetime.mutex:
                self._property_read_write_optional_datetime.version += 1
                self._property_read_write_optional_datetime.set_value(prop_value)

                prop_obj = ReadWriteOptionalDatetimeProperty(value=self._property_read_write_optional_datetime.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalDatetime/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_datetime.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalDatetimeProperty(value=self._property_read_write_optional_datetime.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_datetime.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_datetime.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalDatetimeProperty(value=self._property_read_write_optional_datetime.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_datetime.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_datetimes_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_datetimes.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_datetimes.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_datetimes.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_datetimes.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_datetimes.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoDatetimesProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_datetimes.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_datetimes.mutex:
                self._property_read_write_two_datetimes.version += 1
                self._property_read_write_two_datetimes.set_value(prop_value)

                prop_obj = self._property_read_write_two_datetimes.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoDatetimes/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_datetimes.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_datetimes.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_datetimes.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_datetimes.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_datetimes.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_datetimes.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_duration_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteDurationProperty(value=self._property_read_write_duration.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_duration.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_duration.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_duration.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_duration.version}",
                    )
                return

            try:
                prop_obj = ReadWriteDurationProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_duration.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_duration.mutex:
                self._property_read_write_duration.version += 1
                self._property_read_write_duration.set_value(prop_value)

                prop_obj = ReadWriteDurationProperty(value=self._property_read_write_duration.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteDuration/value".format(self._instance_id), prop_obj, int(self._property_read_write_duration.version))

            if response_topic is not None:

                prop_obj = ReadWriteDurationProperty(value=self._property_read_write_duration.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_duration.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_duration.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteDurationProperty(value=self._property_read_write_duration.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_duration.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_duration_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalDurationProperty(value=self._property_read_write_optional_duration.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_duration.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_duration.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_duration.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_duration.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalDurationProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_duration.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_duration.mutex:
                self._property_read_write_optional_duration.version += 1
                self._property_read_write_optional_duration.set_value(prop_value)

                prop_obj = ReadWriteOptionalDurationProperty(value=self._property_read_write_optional_duration.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalDuration/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_duration.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalDurationProperty(value=self._property_read_write_optional_duration.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_duration.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_duration.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalDurationProperty(value=self._property_read_write_optional_duration.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_duration.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_durations_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_durations.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_durations.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_durations.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_durations.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_durations.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoDurationsProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_durations.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_durations.mutex:
                self._property_read_write_two_durations.version += 1
                self._property_read_write_two_durations.set_value(prop_value)

                prop_obj = self._property_read_write_two_durations.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoDurations/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_durations.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_durations.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_durations.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_durations.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_durations.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_durations.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_binary_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteBinaryProperty(value=self._property_read_write_binary.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_binary.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_binary.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_binary.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_binary.version}",
                    )
                return

            try:
                prop_obj = ReadWriteBinaryProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_binary.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_binary.mutex:
                self._property_read_write_binary.version += 1
                self._property_read_write_binary.set_value(prop_value)

                prop_obj = ReadWriteBinaryProperty(value=self._property_read_write_binary.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteBinary/value".format(self._instance_id), prop_obj, int(self._property_read_write_binary.version))

            if response_topic is not None:

                prop_obj = ReadWriteBinaryProperty(value=self._property_read_write_binary.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_binary.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_binary.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteBinaryProperty(value=self._property_read_write_binary.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_binary.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_optional_binary_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteOptionalBinaryProperty(value=self._property_read_write_optional_binary.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_optional_binary.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_optional_binary.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_optional_binary.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_optional_binary.version}",
                    )
                return

            try:
                prop_obj = ReadWriteOptionalBinaryProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_optional_binary.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_optional_binary.mutex:
                self._property_read_write_optional_binary.version += 1
                self._property_read_write_optional_binary.set_value(prop_value)

                prop_obj = ReadWriteOptionalBinaryProperty(value=self._property_read_write_optional_binary.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteOptionalBinary/value".format(self._instance_id), prop_obj, int(self._property_read_write_optional_binary.version))

            if response_topic is not None:

                prop_obj = ReadWriteOptionalBinaryProperty(value=self._property_read_write_optional_binary.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_binary.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_optional_binary.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteOptionalBinaryProperty(value=self._property_read_write_optional_binary.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_optional_binary.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_two_binaries_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_two_binaries.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_two_binaries.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_two_binaries.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_two_binaries.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_two_binaries.version}",
                    )
                return

            try:
                prop_obj = ReadWriteTwoBinariesProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_two_binaries.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_two_binaries.mutex:
                self._property_read_write_two_binaries.version += 1
                self._property_read_write_two_binaries.set_value(prop_value)

                prop_obj = self._property_read_write_two_binaries.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteTwoBinaries/value".format(self._instance_id), prop_obj, int(self._property_read_write_two_binaries.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_two_binaries.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_binaries.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_two_binaries.callbacks:
                callback(
                    prop_value.first,
                    prop_value.second,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_two_binaries.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_two_binaries.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_list_of_strings_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = ReadWriteListOfStringsProperty(value=self._property_read_write_list_of_strings.get_value())

        try:
            if int(prop_version) != int(self._property_read_write_list_of_strings.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_list_of_strings.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_list_of_strings.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_list_of_strings.version}",
                    )
                return

            try:
                prop_obj = ReadWriteListOfStringsProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_list_of_strings.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj.value
            with self._property_read_write_list_of_strings.mutex:
                self._property_read_write_list_of_strings.version += 1
                self._property_read_write_list_of_strings.set_value(prop_value)

                prop_obj = ReadWriteListOfStringsProperty(value=self._property_read_write_list_of_strings.get_value())

                self._conn.publish_property_state("testable/{}/property/readWriteListOfStrings/value".format(self._instance_id), prop_obj, int(self._property_read_write_list_of_strings.version))

            if response_topic is not None:

                prop_obj = ReadWriteListOfStringsProperty(value=self._property_read_write_list_of_strings.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_list_of_strings.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_list_of_strings.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = ReadWriteListOfStringsProperty(value=self._property_read_write_list_of_strings.get_value())

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_list_of_strings.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_read_write_lists_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", dict())  # type: Optional[Dict[str, str]]
        prop_version = user_properties.get("PropertyVersion", -1)  # type: int
        correlation_id = properties.get("CorrelationData", "")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]

        existing_prop_obj = self._property_read_write_lists.get_value()

        try:
            if int(prop_version) != int(self._property_read_write_lists.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", topic, prop_version, self._property_read_write_lists.version)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_read_write_lists.version),
                        MethodReturnCode.OUT_OF_SYNC,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_read_write_lists.version}",
                    )
                return

            try:
                prop_obj = ReadWriteListsProperty.model_validate_json(payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", topic, e)
                if response_topic is not None:
                    self._conn.publish_property_response(
                        response_topic, existing_prop_obj, str(self._property_read_write_lists.version), MethodReturnCode.SERVER_DESERIALIZATION_ERROR, correlation_id, str(e)
                    )
                return
            prop_value = prop_obj
            with self._property_read_write_lists.mutex:
                self._property_read_write_lists.version += 1
                self._property_read_write_lists.set_value(prop_value)

                prop_obj = self._property_read_write_lists.get_value()

                self._conn.publish_property_state("testable/{}/property/readWriteLists/value".format(self._instance_id), prop_obj, int(self._property_read_write_lists.version))

            if response_topic is not None:

                prop_obj = self._property_read_write_lists.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_lists.version), MethodReturnCode.SUCCESS, correlation_id)
            else:
                self._logger.warning("No response topic provided for property update of %s", topic)

            for callback in self._property_read_write_lists.callbacks:
                callback(
                    prop_value.the_list,
                    prop_value.optional_list,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", topic, exc_info=e)
            if response_topic is not None:

                prop_obj = self._property_read_write_lists.value

                self._conn.publish_property_response(response_topic, prop_obj, str(self._property_read_write_lists.version), MethodReturnCode.SERVER_ERROR, correlation_id, str(e))

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_empty(
        self,
    ):
        """Server application code should call this method to emit the 'empty' signal.

        EmptySignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = EmptySignalPayload()
        self._conn.publish("testable/{}/signal/empty".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_int(self, value: int):
        """Server application code should call this method to emit the 'singleInt' signal.

        SingleIntSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, int), f"The 'value' argument must be of type int, but was {type(value)}"

        payload = SingleIntSignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleInt".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_int(self, value: Optional[int]):
        """Server application code should call this method to emit the 'singleOptionalInt' signal.

        SingleOptionalIntSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, int) or value is None, f"The 'value' argument must be of type Optional[int], but was {type(value)}"

        payload = SingleOptionalIntSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalInt".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_integers(self, first: int, second: int, third: Optional[int]):
        """Server application code should call this method to emit the 'threeIntegers' signal.

        ThreeIntegersSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, int), f"The 'first' argument must be of type int, but was {type(first)}"

        assert isinstance(second, int), f"The 'second' argument must be of type int, but was {type(second)}"

        assert isinstance(third, int) or third is None, f"The 'third' argument must be of type Optional[int], but was {type(third)}"

        payload = ThreeIntegersSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeIntegers".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_string(self, value: str):
        """Server application code should call this method to emit the 'singleString' signal.

        SingleStringSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, str), f"The 'value' argument must be of type str, but was {type(value)}"

        payload = SingleStringSignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleString".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_string(self, value: Optional[str]):
        """Server application code should call this method to emit the 'singleOptionalString' signal.

        SingleOptionalStringSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, str) or value is None, f"The 'value' argument must be of type Optional[str], but was {type(value)}"

        payload = SingleOptionalStringSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalString".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_strings(self, first: str, second: str, third: Optional[str]):
        """Server application code should call this method to emit the 'threeStrings' signal.

        ThreeStringsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, str), f"The 'first' argument must be of type str, but was {type(first)}"

        assert isinstance(second, str), f"The 'second' argument must be of type str, but was {type(second)}"

        assert isinstance(third, str) or third is None, f"The 'third' argument must be of type Optional[str], but was {type(third)}"

        payload = ThreeStringsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeStrings".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_enum(self, value: Numbers):
        """Server application code should call this method to emit the 'singleEnum' signal.

        SingleEnumSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, Numbers), f"The 'value' argument must be of type Numbers, but was {type(value)}"

        payload = SingleEnumSignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleEnum".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_enum(self, value: Optional[Numbers]):
        """Server application code should call this method to emit the 'singleOptionalEnum' signal.

        SingleOptionalEnumSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, Numbers) or value is None, f"The 'value' argument must be of type Optional[Numbers], but was {type(value)}"

        payload = SingleOptionalEnumSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalEnum".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_enums(self, first: Numbers, second: Numbers, third: Optional[Numbers]):
        """Server application code should call this method to emit the 'threeEnums' signal.

        ThreeEnumsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, Numbers), f"The 'first' argument must be of type Numbers, but was {type(first)}"

        assert isinstance(second, Numbers), f"The 'second' argument must be of type Numbers, but was {type(second)}"

        assert isinstance(third, Numbers) or third is None, f"The 'third' argument must be of type Optional[Numbers], but was {type(third)}"

        payload = ThreeEnumsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeEnums".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_struct(self, value: AllTypes):
        """Server application code should call this method to emit the 'singleStruct' signal.

        SingleStructSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, AllTypes), f"The 'value' argument must be of type AllTypes, but was {type(value)}"

        payload = SingleStructSignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleStruct".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_struct(self, value: AllTypes):
        """Server application code should call this method to emit the 'singleOptionalStruct' signal.

        SingleOptionalStructSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, AllTypes) or value is None, f"The 'value' argument must be of type AllTypes, but was {type(value)}"

        payload = SingleOptionalStructSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalStruct".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_structs(self, first: AllTypes, second: AllTypes, third: AllTypes):
        """Server application code should call this method to emit the 'threeStructs' signal.

        ThreeStructsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, AllTypes), f"The 'first' argument must be of type AllTypes, but was {type(first)}"

        assert isinstance(second, AllTypes), f"The 'second' argument must be of type AllTypes, but was {type(second)}"

        assert isinstance(third, AllTypes) or third is None, f"The 'third' argument must be of type AllTypes, but was {type(third)}"

        payload = ThreeStructsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeStructs".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_date_time(self, value: datetime):
        """Server application code should call this method to emit the 'singleDateTime' signal.

        SingleDateTimeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, datetime), f"The 'value' argument must be of type datetime, but was {type(value)}"

        payload = SingleDateTimeSignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleDateTime".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_datetime(self, value: Optional[datetime]):
        """Server application code should call this method to emit the 'singleOptionalDatetime' signal.

        SingleOptionalDatetimeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, datetime) or value is None, f"The 'value' argument must be of type Optional[datetime], but was {type(value)}"

        payload = SingleOptionalDatetimeSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalDatetime".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_date_times(self, first: datetime, second: datetime, third: Optional[datetime]):
        """Server application code should call this method to emit the 'threeDateTimes' signal.

        ThreeDateTimesSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, datetime), f"The 'first' argument must be of type datetime, but was {type(first)}"

        assert isinstance(second, datetime), f"The 'second' argument must be of type datetime, but was {type(second)}"

        assert isinstance(third, datetime) or third is None, f"The 'third' argument must be of type Optional[datetime], but was {type(third)}"

        payload = ThreeDateTimesSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeDateTimes".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_duration(self, value: timedelta):
        """Server application code should call this method to emit the 'singleDuration' signal.

        SingleDurationSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, timedelta), f"The 'value' argument must be of type timedelta, but was {type(value)}"

        payload = SingleDurationSignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleDuration".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_duration(self, value: Optional[timedelta]):
        """Server application code should call this method to emit the 'singleOptionalDuration' signal.

        SingleOptionalDurationSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, timedelta) or value is None, f"The 'value' argument must be of type Optional[timedelta], but was {type(value)}"

        payload = SingleOptionalDurationSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalDuration".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_durations(self, first: timedelta, second: timedelta, third: Optional[timedelta]):
        """Server application code should call this method to emit the 'threeDurations' signal.

        ThreeDurationsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, timedelta), f"The 'first' argument must be of type timedelta, but was {type(first)}"

        assert isinstance(second, timedelta), f"The 'second' argument must be of type timedelta, but was {type(second)}"

        assert isinstance(third, timedelta) or third is None, f"The 'third' argument must be of type Optional[timedelta], but was {type(third)}"

        payload = ThreeDurationsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeDurations".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_binary(self, value: bytes):
        """Server application code should call this method to emit the 'singleBinary' signal.

        SingleBinarySignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, bytes), f"The 'value' argument must be of type bytes, but was {type(value)}"

        payload = SingleBinarySignalPayload(
            value=value,
        )
        self._conn.publish("testable/{}/signal/singleBinary".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_binary(self, value: bytes):
        """Server application code should call this method to emit the 'singleOptionalBinary' signal.

        SingleOptionalBinarySignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(value, bytes) or value is None, f"The 'value' argument must be of type bytes, but was {type(value)}"

        payload = SingleOptionalBinarySignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalBinary".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_three_binaries(self, first: bytes, second: bytes, third: bytes):
        """Server application code should call this method to emit the 'threeBinaries' signal.

        ThreeBinariesSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first, bytes), f"The 'first' argument must be of type bytes, but was {type(first)}"

        assert isinstance(second, bytes), f"The 'second' argument must be of type bytes, but was {type(second)}"

        assert isinstance(third, bytes) or third is None, f"The 'third' argument must be of type bytes, but was {type(third)}"

        payload = ThreeBinariesSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testable/{}/signal/threeBinaries".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_array_of_integers(self, values: List[int]):
        """Server application code should call this method to emit the 'singleArrayOfIntegers' signal.

        SingleArrayOfIntegersSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(values, list), f"The 'values' argument must be of type List[int], but was {type(values)}"

        payload = SingleArrayOfIntegersSignalPayload(
            values=values,
        )
        self._conn.publish("testable/{}/signal/singleArrayOfIntegers".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_single_optional_array_of_strings(self, values: List[str]):
        """Server application code should call this method to emit the 'singleOptionalArrayOfStrings' signal.

        SingleOptionalArrayOfStringsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(values, list) or values is None, f"The 'values' argument must be of type List[str], but was {type(values)}"

        payload = SingleOptionalArrayOfStringsSignalPayload(
            values=values if values is not None else None,
        )
        self._conn.publish("testable/{}/signal/singleOptionalArrayOfStrings".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_array_of_every_type(
        self,
        first_of_integers: List[int],
        second_of_floats: List[float],
        third_of_strings: List[str],
        fourth_of_enums: List[Numbers],
        fifth_of_structs: List[Entry],
        sixth_of_datetimes: List[datetime],
        seventh_of_durations: List[timedelta],
        eighth_of_binaries: List[bytes],
    ):
        """Server application code should call this method to emit the 'arrayOfEveryType' signal.

        ArrayOfEveryTypeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(first_of_integers, list), f"The 'first_of_integers' argument must be of type List[int], but was {type(first_of_integers)}"

        assert isinstance(second_of_floats, list), f"The 'second_of_floats' argument must be of type List[float], but was {type(second_of_floats)}"

        assert isinstance(third_of_strings, list), f"The 'third_of_strings' argument must be of type List[str], but was {type(third_of_strings)}"

        assert isinstance(fourth_of_enums, list), f"The 'fourth_of_enums' argument must be of type List[Numbers], but was {type(fourth_of_enums)}"

        assert isinstance(fifth_of_structs, list), f"The 'fifth_of_structs' argument must be of type List[Entry], but was {type(fifth_of_structs)}"

        assert isinstance(sixth_of_datetimes, list), f"The 'sixth_of_datetimes' argument must be of type List[datetime], but was {type(sixth_of_datetimes)}"

        assert isinstance(seventh_of_durations, list), f"The 'seventh_of_durations' argument must be of type List[timedelta], but was {type(seventh_of_durations)}"

        assert isinstance(eighth_of_binaries, list), f"The 'eighth_of_binaries' argument must be of type List[bytes], but was {type(eighth_of_binaries)}"

        payload = ArrayOfEveryTypeSignalPayload(
            first_of_integers=first_of_integers,
            second_of_floats=second_of_floats,
            third_of_strings=third_of_strings,
            fourth_of_enums=fourth_of_enums,
            fifth_of_structs=fifth_of_structs,
            sixth_of_datetimes=sixth_of_datetimes,
            seventh_of_durations=seventh_of_durations,
            eighth_of_binaries=eighth_of_binaries,
        )
        self._conn.publish("testable/{}/signal/arrayOfEveryType".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def handle_call_with_nothing(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'callWithNothing' method calls."""
        if self._method_call_with_nothing.callback is None and handler is not None:
            self._method_call_with_nothing.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_with_nothing_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callWithNothing' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallWithNothingMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callWithNothing' request: %s", correlation_id)
        if self._method_call_with_nothing.callback is not None:
            method_args = []

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    self._method_call_with_nothing.callback(*method_args)

                    return_json = "{}"

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callWithNothing: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callWithNothing", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_integer(self, handler: Callable[[int], int]):
        """This is a decorator to decorate a method that will handle the 'callOneInteger' method calls."""
        if self._method_call_one_integer.callback is None and handler is not None:
            self._method_call_one_integer.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_integer_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneInteger' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneIntegerMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneInteger' request: %s", correlation_id)
        if self._method_call_one_integer.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_integer.callback(*method_args)

                    if not isinstance(return_values, int):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type int, but was {type(return_values)}")
                    ret_obj = CallOneIntegerMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneInteger: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneInteger", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_integer(self, handler: Callable[[Optional[int]], Optional[int]]):
        """This is a decorator to decorate a method that will handle the 'callOptionalInteger' method calls."""
        if self._method_call_optional_integer.callback is None and handler is not None:
            self._method_call_optional_integer.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_integer_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalInteger' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalIntegerMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalInteger' request: %s", correlation_id)
        if self._method_call_optional_integer.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_integer.callback(*method_args)

                    if not isinstance(return_values, int) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type int, but was {type(return_values)}")
                    ret_obj = CallOptionalIntegerMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalInteger: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalInteger", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_integers(self, handler: Callable[[int, int, Optional[int]], CallThreeIntegersMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeIntegers' method calls."""
        if self._method_call_three_integers.callback is None and handler is not None:
            self._method_call_three_integers.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_integers_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeIntegers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeIntegersMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeIntegers' request: %s", correlation_id)
        if self._method_call_three_integers.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_integers.callback(*method_args)

                    if not isinstance(return_values, CallThreeIntegersMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeIntegersMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeIntegers: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeIntegers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_string(self, handler: Callable[[str], str]):
        """This is a decorator to decorate a method that will handle the 'callOneString' method calls."""
        if self._method_call_one_string.callback is None and handler is not None:
            self._method_call_one_string.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_string_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneString' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneStringMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneString' request: %s", correlation_id)
        if self._method_call_one_string.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_string.callback(*method_args)

                    if not isinstance(return_values, str):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type str, but was {type(return_values)}")
                    ret_obj = CallOneStringMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneString: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneString", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_string(self, handler: Callable[[Optional[str]], Optional[str]]):
        """This is a decorator to decorate a method that will handle the 'callOptionalString' method calls."""
        if self._method_call_optional_string.callback is None and handler is not None:
            self._method_call_optional_string.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_string_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalString' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalStringMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalString' request: %s", correlation_id)
        if self._method_call_optional_string.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_string.callback(*method_args)

                    if not isinstance(return_values, str) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type str, but was {type(return_values)}")
                    ret_obj = CallOptionalStringMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalString: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalString", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_strings(self, handler: Callable[[str, Optional[str], str], CallThreeStringsMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeStrings' method calls."""
        if self._method_call_three_strings.callback is None and handler is not None:
            self._method_call_three_strings.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_strings_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeStrings' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeStringsMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeStrings' request: %s", correlation_id)
        if self._method_call_three_strings.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_strings.callback(*method_args)

                    if not isinstance(return_values, CallThreeStringsMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeStringsMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeStrings: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeStrings", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_enum(self, handler: Callable[[Numbers], Numbers]):
        """This is a decorator to decorate a method that will handle the 'callOneEnum' method calls."""
        if self._method_call_one_enum.callback is None and handler is not None:
            self._method_call_one_enum.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_enum_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneEnum' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneEnumMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneEnum' request: %s", correlation_id)
        if self._method_call_one_enum.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_enum.callback(*method_args)

                    if not isinstance(return_values, Numbers):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type Numbers, but was {type(return_values)}")
                    ret_obj = CallOneEnumMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneEnum: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneEnum", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_enum(self, handler: Callable[[Optional[Numbers]], Optional[Numbers]]):
        """This is a decorator to decorate a method that will handle the 'callOptionalEnum' method calls."""
        if self._method_call_optional_enum.callback is None and handler is not None:
            self._method_call_optional_enum.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_enum_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalEnum' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalEnumMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalEnum' request: %s", correlation_id)
        if self._method_call_optional_enum.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_enum.callback(*method_args)

                    if not isinstance(return_values, Numbers) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type Numbers, but was {type(return_values)}")
                    ret_obj = CallOptionalEnumMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalEnum: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalEnum", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_enums(self, handler: Callable[[Numbers, Numbers, Optional[Numbers]], CallThreeEnumsMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeEnums' method calls."""
        if self._method_call_three_enums.callback is None and handler is not None:
            self._method_call_three_enums.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_enums_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeEnums' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeEnumsMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeEnums' request: %s", correlation_id)
        if self._method_call_three_enums.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_enums.callback(*method_args)

                    if not isinstance(return_values, CallThreeEnumsMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeEnumsMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeEnums: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeEnums", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_struct(self, handler: Callable[[AllTypes], AllTypes]):
        """This is a decorator to decorate a method that will handle the 'callOneStruct' method calls."""
        if self._method_call_one_struct.callback is None and handler is not None:
            self._method_call_one_struct.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_struct_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneStruct' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneStructMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneStruct' request: %s", correlation_id)
        if self._method_call_one_struct.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_struct.callback(*method_args)

                    if not isinstance(return_values, AllTypes):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type AllTypes, but was {type(return_values)}")
                    ret_obj = CallOneStructMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneStruct: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneStruct", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_struct(self, handler: Callable[[AllTypes], AllTypes]):
        """This is a decorator to decorate a method that will handle the 'callOptionalStruct' method calls."""
        if self._method_call_optional_struct.callback is None and handler is not None:
            self._method_call_optional_struct.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_struct_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalStruct' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalStructMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalStruct' request: %s", correlation_id)
        if self._method_call_optional_struct.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_struct.callback(*method_args)

                    if not isinstance(return_values, AllTypes) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type AllTypes, but was {type(return_values)}")
                    ret_obj = CallOptionalStructMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalStruct: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalStruct", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_structs(self, handler: Callable[[AllTypes, AllTypes, AllTypes], CallThreeStructsMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeStructs' method calls."""
        if self._method_call_three_structs.callback is None and handler is not None:
            self._method_call_three_structs.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_structs_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeStructs' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeStructsMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeStructs' request: %s", correlation_id)
        if self._method_call_three_structs.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_structs.callback(*method_args)

                    if not isinstance(return_values, CallThreeStructsMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeStructsMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeStructs: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeStructs", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_date_time(self, handler: Callable[[datetime], datetime]):
        """This is a decorator to decorate a method that will handle the 'callOneDateTime' method calls."""
        if self._method_call_one_date_time.callback is None and handler is not None:
            self._method_call_one_date_time.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_date_time_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneDateTime' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneDateTimeMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneDateTime' request: %s", correlation_id)
        if self._method_call_one_date_time.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_date_time.callback(*method_args)

                    if not isinstance(return_values, datetime):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type datetime, but was {type(return_values)}")
                    ret_obj = CallOneDateTimeMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneDateTime: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneDateTime", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_date_time(self, handler: Callable[[Optional[datetime]], Optional[datetime]]):
        """This is a decorator to decorate a method that will handle the 'callOptionalDateTime' method calls."""
        if self._method_call_optional_date_time.callback is None and handler is not None:
            self._method_call_optional_date_time.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_date_time_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalDateTime' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalDateTimeMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalDateTime' request: %s", correlation_id)
        if self._method_call_optional_date_time.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_date_time.callback(*method_args)

                    if not isinstance(return_values, datetime) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type datetime, but was {type(return_values)}")
                    ret_obj = CallOptionalDateTimeMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalDateTime: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalDateTime", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_date_times(self, handler: Callable[[datetime, datetime, Optional[datetime]], CallThreeDateTimesMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeDateTimes' method calls."""
        if self._method_call_three_date_times.callback is None and handler is not None:
            self._method_call_three_date_times.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_date_times_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeDateTimes' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeDateTimesMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeDateTimes' request: %s", correlation_id)
        if self._method_call_three_date_times.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_date_times.callback(*method_args)

                    if not isinstance(return_values, CallThreeDateTimesMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeDateTimesMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeDateTimes: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeDateTimes", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_duration(self, handler: Callable[[timedelta], timedelta]):
        """This is a decorator to decorate a method that will handle the 'callOneDuration' method calls."""
        if self._method_call_one_duration.callback is None and handler is not None:
            self._method_call_one_duration.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_duration_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneDuration' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneDurationMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneDuration' request: %s", correlation_id)
        if self._method_call_one_duration.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_duration.callback(*method_args)

                    if not isinstance(return_values, timedelta):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type timedelta, but was {type(return_values)}")
                    ret_obj = CallOneDurationMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneDuration: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneDuration", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_duration(self, handler: Callable[[Optional[timedelta]], Optional[timedelta]]):
        """This is a decorator to decorate a method that will handle the 'callOptionalDuration' method calls."""
        if self._method_call_optional_duration.callback is None and handler is not None:
            self._method_call_optional_duration.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_duration_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalDuration' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalDurationMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalDuration' request: %s", correlation_id)
        if self._method_call_optional_duration.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_duration.callback(*method_args)

                    if not isinstance(return_values, timedelta) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type timedelta, but was {type(return_values)}")
                    ret_obj = CallOptionalDurationMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalDuration: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalDuration", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_durations(self, handler: Callable[[timedelta, timedelta, Optional[timedelta]], CallThreeDurationsMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeDurations' method calls."""
        if self._method_call_three_durations.callback is None and handler is not None:
            self._method_call_three_durations.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_durations_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeDurations' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeDurationsMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeDurations' request: %s", correlation_id)
        if self._method_call_three_durations.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_durations.callback(*method_args)

                    if not isinstance(return_values, CallThreeDurationsMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeDurationsMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeDurations: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeDurations", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_binary(self, handler: Callable[[bytes], bytes]):
        """This is a decorator to decorate a method that will handle the 'callOneBinary' method calls."""
        if self._method_call_one_binary.callback is None and handler is not None:
            self._method_call_one_binary.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_binary_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneBinary' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneBinaryMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneBinary' request: %s", correlation_id)
        if self._method_call_one_binary.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_binary.callback(*method_args)

                    if not isinstance(return_values, bytes):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type bytes, but was {type(return_values)}")
                    ret_obj = CallOneBinaryMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneBinary: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneBinary", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_binary(self, handler: Callable[[bytes], bytes]):
        """This is a decorator to decorate a method that will handle the 'callOptionalBinary' method calls."""
        if self._method_call_optional_binary.callback is None and handler is not None:
            self._method_call_optional_binary.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_binary_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalBinary' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalBinaryMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalBinary' request: %s", correlation_id)
        if self._method_call_optional_binary.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_binary.callback(*method_args)

                    if not isinstance(return_values, bytes) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type bytes, but was {type(return_values)}")
                    ret_obj = CallOptionalBinaryMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalBinary: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalBinary", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_binaries(self, handler: Callable[[bytes, bytes, bytes], CallThreeBinariesMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callThreeBinaries' method calls."""
        if self._method_call_three_binaries.callback is None and handler is not None:
            self._method_call_three_binaries.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_three_binaries_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callThreeBinaries' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallThreeBinariesMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callThreeBinaries' request: %s", correlation_id)
        if self._method_call_three_binaries.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
                payload.input3,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_three_binaries.callback(*method_args)

                    if not isinstance(return_values, CallThreeBinariesMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallThreeBinariesMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callThreeBinaries: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callThreeBinaries", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_list_of_integers(self, handler: Callable[[List[int]], List[int]]):
        """This is a decorator to decorate a method that will handle the 'callOneListOfIntegers' method calls."""
        if self._method_call_one_list_of_integers.callback is None and handler is not None:
            self._method_call_one_list_of_integers.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_one_list_of_integers_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOneListOfIntegers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOneListOfIntegersMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOneListOfIntegers' request: %s", correlation_id)
        if self._method_call_one_list_of_integers.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_one_list_of_integers.callback(*method_args)

                    if not isinstance(return_values, list):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type list, but was {type(return_values)}")
                    ret_obj = CallOneListOfIntegersMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOneListOfIntegers: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOneListOfIntegers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_list_of_floats(self, handler: Callable[[List[float]], List[float]]):
        """This is a decorator to decorate a method that will handle the 'callOptionalListOfFloats' method calls."""
        if self._method_call_optional_list_of_floats.callback is None and handler is not None:
            self._method_call_optional_list_of_floats.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_optional_list_of_floats_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callOptionalListOfFloats' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallOptionalListOfFloatsMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callOptionalListOfFloats' request: %s", correlation_id)
        if self._method_call_optional_list_of_floats.callback is not None:
            method_args = [
                payload.input1,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_optional_list_of_floats.callback(*method_args)

                    if not isinstance(return_values, list) and return_values is not None:
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type list, but was {type(return_values)}")
                    ret_obj = CallOptionalListOfFloatsMethodResponse(output1=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callOptionalListOfFloats: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalListOfFloats", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_two_lists(self, handler: Callable[[List[Numbers], List[str]], CallTwoListsMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'callTwoLists' method calls."""
        if self._method_call_two_lists.callback is None and handler is not None:
            self._method_call_two_lists.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_call_two_lists_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'callTwoLists' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = CallTwoListsMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'callTwoLists' request: %s", correlation_id)
        if self._method_call_two_lists.callback is not None:
            method_args = [
                payload.input1,
                payload.input2,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_call_two_lists.callback(*method_args)

                    if not isinstance(return_values, CallTwoListsMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type CallTwoListsMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling callTwoLists: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling callTwoLists", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    @property
    def read_write_integer(self) -> Optional[int]:
        """This property returns the last received value for the 'read_write_integer' property."""
        with self._property_read_write_integer_mutex:
            return self._property_read_write_integer

    @read_write_integer.setter
    def read_write_integer(self, value: int):
        """This property sets (publishes) a new value for the 'read_write_integer' property."""

        if not isinstance(value, int):
            raise ValueError(f"The value must be int .")

        prop_obj = ReadWriteIntegerProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_integer.value is None or value != self._property_read_write_integer.value.value:
            with self._property_read_write_integer.mutex:
                self._property_read_write_integer.value = prop_obj
                self._property_read_write_integer.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteInteger/value".format(self._instance_id), payload, self._property_read_write_integer.version)
            for callback in self._property_read_write_integer.callbacks:
                callback(prop_obj.value)

    def set_read_write_integer(self, value: int):
        """This method sets (publishes) a new value for the 'read_write_integer' property."""
        if not isinstance(value, int):
            raise ValueError(f"The 'value' value must be int.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_integer = obj

    def on_read_write_integer_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'read_write_integer' property update is received."""
        if handler is not None:
            self._property_read_write_integer.callbacks.append(handler)

    @property
    def read_only_integer(self) -> Optional[int]:
        """This property returns the last received value for the 'read_only_integer' property."""
        with self._property_read_only_integer_mutex:
            return self._property_read_only_integer

    @read_only_integer.setter
    def read_only_integer(self, value: int):
        """This property sets (publishes) a new value for the 'read_only_integer' property."""

        if not isinstance(value, int):
            raise ValueError(f"The value must be int .")

        prop_obj = ReadOnlyIntegerProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_only_integer.value is None or value != self._property_read_only_integer.value.value:
            with self._property_read_only_integer.mutex:
                self._property_read_only_integer.value = prop_obj
                self._property_read_only_integer.version += 1
                self._conn.publish_property_state("testable/{}/property/readOnlyInteger/value".format(self._instance_id), payload, self._property_read_only_integer.version)
            for callback in self._property_read_only_integer.callbacks:
                callback(prop_obj.value)

    def set_read_only_integer(self, value: int):
        """This method sets (publishes) a new value for the 'read_only_integer' property."""
        if not isinstance(value, int):
            raise ValueError(f"The 'value' value must be int.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_only_integer = obj

    def on_read_only_integer_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'read_only_integer' property update is received."""
        if handler is not None:
            self._property_read_only_integer.callbacks.append(handler)

    @property
    def read_write_optional_integer(self) -> Optional[int]:
        """This property returns the last received value for the 'read_write_optional_integer' property."""
        with self._property_read_write_optional_integer_mutex:
            return self._property_read_write_optional_integer

    @read_write_optional_integer.setter
    def read_write_optional_integer(self, value: Optional[int]):
        """This property sets (publishes) a new value for the 'read_write_optional_integer' property."""

        if (value is not None) and (not isinstance(value, int)):
            raise ValueError(f"The value must be int or None.")

        prop_obj = ReadWriteOptionalIntegerProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_integer.value is None or value != self._property_read_write_optional_integer.value.value:
            with self._property_read_write_optional_integer.mutex:
                self._property_read_write_optional_integer.value = prop_obj
                self._property_read_write_optional_integer.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalInteger/value".format(self._instance_id), payload, self._property_read_write_optional_integer.version)
            for callback in self._property_read_write_optional_integer.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_integer(self, value: Optional[int]):
        """This method sets (publishes) a new value for the 'read_write_optional_integer' property."""
        if not isinstance(value, int) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[int].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_integer = obj

    def on_read_write_optional_integer_updates(self, handler: Callable[[Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_integer' property update is received."""
        if handler is not None:
            self._property_read_write_optional_integer.callbacks.append(handler)

    @property
    def read_write_two_integers(self) -> Optional[ReadWriteTwoIntegersProperty]:
        """This property returns the last received value for the 'read_write_two_integers' property."""
        with self._property_read_write_two_integers_mutex:
            return self._property_read_write_two_integers

    @read_write_two_integers.setter
    def read_write_two_integers(self, value: ReadWriteTwoIntegersProperty):
        """This property sets (publishes) a new value for the 'read_write_two_integers' property."""

        if not isinstance(value, ReadWriteTwoIntegersProperty):
            raise ValueError(f"The value must be ReadWriteTwoIntegersProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_integers.value:
            with self._property_read_write_two_integers.mutex:
                self._property_read_write_two_integers.value = value
                self._property_read_write_two_integers.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoIntegers/value".format(self._instance_id), payload, self._property_read_write_two_integers.version)
            for callback in self._property_read_write_two_integers.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_integers(self, first: int, second: Optional[int]):
        """This method sets (publishes) a new value for the 'read_write_two_integers' property."""
        if not isinstance(first, int):
            raise ValueError(f"The 'first' value must be int.")
        if not isinstance(second, int) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[int].")

        obj = interface_types.ReadWriteTwoIntegersProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_integers = obj

    def on_read_write_two_integers_updates(self, handler: Callable[[int, Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_integers' property update is received."""
        if handler is not None:
            self._property_read_write_two_integers.callbacks.append(handler)

    @property
    def read_only_string(self) -> Optional[str]:
        """This property returns the last received value for the 'read_only_string' property."""
        with self._property_read_only_string_mutex:
            return self._property_read_only_string

    @read_only_string.setter
    def read_only_string(self, value: str):
        """This property sets (publishes) a new value for the 'read_only_string' property."""

        if not isinstance(value, str):
            raise ValueError(f"The value must be str .")

        prop_obj = ReadOnlyStringProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_only_string.value is None or value != self._property_read_only_string.value.value:
            with self._property_read_only_string.mutex:
                self._property_read_only_string.value = prop_obj
                self._property_read_only_string.version += 1
                self._conn.publish_property_state("testable/{}/property/readOnlyString/value".format(self._instance_id), payload, self._property_read_only_string.version)
            for callback in self._property_read_only_string.callbacks:
                callback(prop_obj.value)

    def set_read_only_string(self, value: str):
        """This method sets (publishes) a new value for the 'read_only_string' property."""
        if not isinstance(value, str):
            raise ValueError(f"The 'value' value must be str.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_only_string = obj

    def on_read_only_string_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'read_only_string' property update is received."""
        if handler is not None:
            self._property_read_only_string.callbacks.append(handler)

    @property
    def read_write_string(self) -> Optional[str]:
        """This property returns the last received value for the 'read_write_string' property."""
        with self._property_read_write_string_mutex:
            return self._property_read_write_string

    @read_write_string.setter
    def read_write_string(self, value: str):
        """This property sets (publishes) a new value for the 'read_write_string' property."""

        if not isinstance(value, str):
            raise ValueError(f"The value must be str .")

        prop_obj = ReadWriteStringProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_string.value is None or value != self._property_read_write_string.value.value:
            with self._property_read_write_string.mutex:
                self._property_read_write_string.value = prop_obj
                self._property_read_write_string.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteString/value".format(self._instance_id), payload, self._property_read_write_string.version)
            for callback in self._property_read_write_string.callbacks:
                callback(prop_obj.value)

    def set_read_write_string(self, value: str):
        """This method sets (publishes) a new value for the 'read_write_string' property."""
        if not isinstance(value, str):
            raise ValueError(f"The 'value' value must be str.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_string = obj

    def on_read_write_string_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'read_write_string' property update is received."""
        if handler is not None:
            self._property_read_write_string.callbacks.append(handler)

    @property
    def read_write_optional_string(self) -> Optional[str]:
        """This property returns the last received value for the 'read_write_optional_string' property."""
        with self._property_read_write_optional_string_mutex:
            return self._property_read_write_optional_string

    @read_write_optional_string.setter
    def read_write_optional_string(self, value: Optional[str]):
        """This property sets (publishes) a new value for the 'read_write_optional_string' property."""

        if (value is not None) and (not isinstance(value, str)):
            raise ValueError(f"The value must be str or None.")

        prop_obj = ReadWriteOptionalStringProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_string.value is None or value != self._property_read_write_optional_string.value.value:
            with self._property_read_write_optional_string.mutex:
                self._property_read_write_optional_string.value = prop_obj
                self._property_read_write_optional_string.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalString/value".format(self._instance_id), payload, self._property_read_write_optional_string.version)
            for callback in self._property_read_write_optional_string.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_string(self, value: Optional[str]):
        """This method sets (publishes) a new value for the 'read_write_optional_string' property."""
        if not isinstance(value, str) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[str].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_string = obj

    def on_read_write_optional_string_updates(self, handler: Callable[[Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_string' property update is received."""
        if handler is not None:
            self._property_read_write_optional_string.callbacks.append(handler)

    @property
    def read_write_two_strings(self) -> Optional[ReadWriteTwoStringsProperty]:
        """This property returns the last received value for the 'read_write_two_strings' property."""
        with self._property_read_write_two_strings_mutex:
            return self._property_read_write_two_strings

    @read_write_two_strings.setter
    def read_write_two_strings(self, value: ReadWriteTwoStringsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_strings' property."""

        if not isinstance(value, ReadWriteTwoStringsProperty):
            raise ValueError(f"The value must be ReadWriteTwoStringsProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_strings.value:
            with self._property_read_write_two_strings.mutex:
                self._property_read_write_two_strings.value = value
                self._property_read_write_two_strings.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoStrings/value".format(self._instance_id), payload, self._property_read_write_two_strings.version)
            for callback in self._property_read_write_two_strings.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_strings(self, first: str, second: Optional[str]):
        """This method sets (publishes) a new value for the 'read_write_two_strings' property."""
        if not isinstance(first, str):
            raise ValueError(f"The 'first' value must be str.")
        if not isinstance(second, str) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[str].")

        obj = interface_types.ReadWriteTwoStringsProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_strings = obj

    def on_read_write_two_strings_updates(self, handler: Callable[[str, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_strings' property update is received."""
        if handler is not None:
            self._property_read_write_two_strings.callbacks.append(handler)

    @property
    def read_write_struct(self) -> Optional[AllTypes]:
        """This property returns the last received value for the 'read_write_struct' property."""
        with self._property_read_write_struct_mutex:
            return self._property_read_write_struct

    @read_write_struct.setter
    def read_write_struct(self, value: AllTypes):
        """This property sets (publishes) a new value for the 'read_write_struct' property."""

        if not isinstance(value, AllTypes):
            raise ValueError(f"The value must be AllTypes .")

        prop_obj = ReadWriteStructProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_struct.value is None or value != self._property_read_write_struct.value.value:
            with self._property_read_write_struct.mutex:
                self._property_read_write_struct.value = prop_obj
                self._property_read_write_struct.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteStruct/value".format(self._instance_id), payload, self._property_read_write_struct.version)
            for callback in self._property_read_write_struct.callbacks:
                callback(prop_obj.value)

    def set_read_write_struct(self, value: AllTypes):
        """This method sets (publishes) a new value for the 'read_write_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError(f"The 'value' value must be AllTypes.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_struct = obj

    def on_read_write_struct_updates(self, handler: Callable[[AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_struct' property update is received."""
        if handler is not None:
            self._property_read_write_struct.callbacks.append(handler)

    @property
    def read_write_optional_struct(self) -> AllTypes:
        """This property returns the last received value for the 'read_write_optional_struct' property."""
        with self._property_read_write_optional_struct_mutex:
            return self._property_read_write_optional_struct

    @read_write_optional_struct.setter
    def read_write_optional_struct(self, value: AllTypes):
        """This property sets (publishes) a new value for the 'read_write_optional_struct' property."""

        if (value is not None) and (not isinstance(value, AllTypes)):
            raise ValueError(f"The value must be AllTypes or None.")

        prop_obj = ReadWriteOptionalStructProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_struct.value is None or value != self._property_read_write_optional_struct.value.value:
            with self._property_read_write_optional_struct.mutex:
                self._property_read_write_optional_struct.value = prop_obj
                self._property_read_write_optional_struct.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalStruct/value".format(self._instance_id), payload, self._property_read_write_optional_struct.version)
            for callback in self._property_read_write_optional_struct.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_struct(self, value: AllTypes):
        """This method sets (publishes) a new value for the 'read_write_optional_struct' property."""
        if not isinstance(value, AllTypes) and value is not None:
            raise ValueError(f"The 'value' value must be AllTypes.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_struct = obj

    def on_read_write_optional_struct_updates(self, handler: Callable[[AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_struct' property update is received."""
        if handler is not None:
            self._property_read_write_optional_struct.callbacks.append(handler)

    @property
    def read_write_two_structs(self) -> Optional[ReadWriteTwoStructsProperty]:
        """This property returns the last received value for the 'read_write_two_structs' property."""
        with self._property_read_write_two_structs_mutex:
            return self._property_read_write_two_structs

    @read_write_two_structs.setter
    def read_write_two_structs(self, value: ReadWriteTwoStructsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_structs' property."""

        if not isinstance(value, ReadWriteTwoStructsProperty):
            raise ValueError(f"The value must be ReadWriteTwoStructsProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_structs.value:
            with self._property_read_write_two_structs.mutex:
                self._property_read_write_two_structs.value = value
                self._property_read_write_two_structs.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoStructs/value".format(self._instance_id), payload, self._property_read_write_two_structs.version)
            for callback in self._property_read_write_two_structs.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_structs(self, first: AllTypes, second: AllTypes):
        """This method sets (publishes) a new value for the 'read_write_two_structs' property."""
        if not isinstance(first, AllTypes):
            raise ValueError(f"The 'first' value must be AllTypes.")
        if not isinstance(second, AllTypes) and second is not None:
            raise ValueError(f"The 'second' value must be AllTypes.")

        obj = interface_types.ReadWriteTwoStructsProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_structs = obj

    def on_read_write_two_structs_updates(self, handler: Callable[[AllTypes, AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_structs' property update is received."""
        if handler is not None:
            self._property_read_write_two_structs.callbacks.append(handler)

    @property
    def read_only_enum(self) -> Optional[Numbers]:
        """This property returns the last received value for the 'read_only_enum' property."""
        with self._property_read_only_enum_mutex:
            return self._property_read_only_enum

    @read_only_enum.setter
    def read_only_enum(self, value: Numbers):
        """This property sets (publishes) a new value for the 'read_only_enum' property."""

        if not isinstance(value, Numbers):
            raise ValueError(f"The value must be Numbers .")

        prop_obj = ReadOnlyEnumProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_only_enum.value is None or value != self._property_read_only_enum.value.value:
            with self._property_read_only_enum.mutex:
                self._property_read_only_enum.value = prop_obj
                self._property_read_only_enum.version += 1
                self._conn.publish_property_state("testable/{}/property/readOnlyEnum/value".format(self._instance_id), payload, self._property_read_only_enum.version)
            for callback in self._property_read_only_enum.callbacks:
                callback(prop_obj.value)

    def set_read_only_enum(self, value: Numbers):
        """This method sets (publishes) a new value for the 'read_only_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError(f"The 'value' value must be Numbers.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_only_enum = obj

    def on_read_only_enum_updates(self, handler: Callable[[Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_only_enum' property update is received."""
        if handler is not None:
            self._property_read_only_enum.callbacks.append(handler)

    @property
    def read_write_enum(self) -> Optional[Numbers]:
        """This property returns the last received value for the 'read_write_enum' property."""
        with self._property_read_write_enum_mutex:
            return self._property_read_write_enum

    @read_write_enum.setter
    def read_write_enum(self, value: Numbers):
        """This property sets (publishes) a new value for the 'read_write_enum' property."""

        if not isinstance(value, Numbers):
            raise ValueError(f"The value must be Numbers .")

        prop_obj = ReadWriteEnumProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_enum.value is None or value != self._property_read_write_enum.value.value:
            with self._property_read_write_enum.mutex:
                self._property_read_write_enum.value = prop_obj
                self._property_read_write_enum.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteEnum/value".format(self._instance_id), payload, self._property_read_write_enum.version)
            for callback in self._property_read_write_enum.callbacks:
                callback(prop_obj.value)

    def set_read_write_enum(self, value: Numbers):
        """This method sets (publishes) a new value for the 'read_write_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError(f"The 'value' value must be Numbers.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_enum = obj

    def on_read_write_enum_updates(self, handler: Callable[[Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_write_enum' property update is received."""
        if handler is not None:
            self._property_read_write_enum.callbacks.append(handler)

    @property
    def read_write_optional_enum(self) -> Optional[Numbers]:
        """This property returns the last received value for the 'read_write_optional_enum' property."""
        with self._property_read_write_optional_enum_mutex:
            return self._property_read_write_optional_enum

    @read_write_optional_enum.setter
    def read_write_optional_enum(self, value: Optional[Numbers]):
        """This property sets (publishes) a new value for the 'read_write_optional_enum' property."""

        if (value is not None) and (not isinstance(value, Numbers)):
            raise ValueError(f"The value must be Numbers or None.")

        prop_obj = ReadWriteOptionalEnumProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_enum.value is None or value != self._property_read_write_optional_enum.value.value:
            with self._property_read_write_optional_enum.mutex:
                self._property_read_write_optional_enum.value = prop_obj
                self._property_read_write_optional_enum.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalEnum/value".format(self._instance_id), payload, self._property_read_write_optional_enum.version)
            for callback in self._property_read_write_optional_enum.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_enum(self, value: Optional[Numbers]):
        """This method sets (publishes) a new value for the 'read_write_optional_enum' property."""
        if not isinstance(value, Numbers) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[Numbers].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_enum = obj

    def on_read_write_optional_enum_updates(self, handler: Callable[[Optional[Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_enum' property update is received."""
        if handler is not None:
            self._property_read_write_optional_enum.callbacks.append(handler)

    @property
    def read_write_two_enums(self) -> Optional[ReadWriteTwoEnumsProperty]:
        """This property returns the last received value for the 'read_write_two_enums' property."""
        with self._property_read_write_two_enums_mutex:
            return self._property_read_write_two_enums

    @read_write_two_enums.setter
    def read_write_two_enums(self, value: ReadWriteTwoEnumsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_enums' property."""

        if not isinstance(value, ReadWriteTwoEnumsProperty):
            raise ValueError(f"The value must be ReadWriteTwoEnumsProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_enums.value:
            with self._property_read_write_two_enums.mutex:
                self._property_read_write_two_enums.value = value
                self._property_read_write_two_enums.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoEnums/value".format(self._instance_id), payload, self._property_read_write_two_enums.version)
            for callback in self._property_read_write_two_enums.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_enums(self, first: Numbers, second: Optional[Numbers]):
        """This method sets (publishes) a new value for the 'read_write_two_enums' property."""
        if not isinstance(first, Numbers):
            raise ValueError(f"The 'first' value must be Numbers.")
        if not isinstance(second, Numbers) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[Numbers].")

        obj = interface_types.ReadWriteTwoEnumsProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_enums = obj

    def on_read_write_two_enums_updates(self, handler: Callable[[Numbers, Optional[Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_enums' property update is received."""
        if handler is not None:
            self._property_read_write_two_enums.callbacks.append(handler)

    @property
    def read_write_datetime(self) -> Optional[datetime]:
        """This property returns the last received value for the 'read_write_datetime' property."""
        with self._property_read_write_datetime_mutex:
            return self._property_read_write_datetime

    @read_write_datetime.setter
    def read_write_datetime(self, value: datetime):
        """This property sets (publishes) a new value for the 'read_write_datetime' property."""

        if not isinstance(value, datetime):
            raise ValueError(f"The value must be datetime .")

        prop_obj = ReadWriteDatetimeProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_datetime.value is None or value != self._property_read_write_datetime.value.value:
            with self._property_read_write_datetime.mutex:
                self._property_read_write_datetime.value = prop_obj
                self._property_read_write_datetime.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteDatetime/value".format(self._instance_id), payload, self._property_read_write_datetime.version)
            for callback in self._property_read_write_datetime.callbacks:
                callback(prop_obj.value)

    def set_read_write_datetime(self, value: datetime):
        """This method sets (publishes) a new value for the 'read_write_datetime' property."""
        if not isinstance(value, datetime):
            raise ValueError(f"The 'value' value must be datetime.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_datetime = obj

    def on_read_write_datetime_updates(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'read_write_datetime' property update is received."""
        if handler is not None:
            self._property_read_write_datetime.callbacks.append(handler)

    @property
    def read_write_optional_datetime(self) -> Optional[datetime]:
        """This property returns the last received value for the 'read_write_optional_datetime' property."""
        with self._property_read_write_optional_datetime_mutex:
            return self._property_read_write_optional_datetime

    @read_write_optional_datetime.setter
    def read_write_optional_datetime(self, value: Optional[datetime]):
        """This property sets (publishes) a new value for the 'read_write_optional_datetime' property."""

        if (value is not None) and (not isinstance(value, datetime)):
            raise ValueError(f"The value must be datetime or None.")

        prop_obj = ReadWriteOptionalDatetimeProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_datetime.value is None or value != self._property_read_write_optional_datetime.value.value:
            with self._property_read_write_optional_datetime.mutex:
                self._property_read_write_optional_datetime.value = prop_obj
                self._property_read_write_optional_datetime.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalDatetime/value".format(self._instance_id), payload, self._property_read_write_optional_datetime.version)
            for callback in self._property_read_write_optional_datetime.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_datetime(self, value: Optional[datetime]):
        """This method sets (publishes) a new value for the 'read_write_optional_datetime' property."""
        if not isinstance(value, datetime) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[datetime].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_datetime = obj

    def on_read_write_optional_datetime_updates(self, handler: Callable[[Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_datetime' property update is received."""
        if handler is not None:
            self._property_read_write_optional_datetime.callbacks.append(handler)

    @property
    def read_write_two_datetimes(self) -> Optional[ReadWriteTwoDatetimesProperty]:
        """This property returns the last received value for the 'read_write_two_datetimes' property."""
        with self._property_read_write_two_datetimes_mutex:
            return self._property_read_write_two_datetimes

    @read_write_two_datetimes.setter
    def read_write_two_datetimes(self, value: ReadWriteTwoDatetimesProperty):
        """This property sets (publishes) a new value for the 'read_write_two_datetimes' property."""

        if not isinstance(value, ReadWriteTwoDatetimesProperty):
            raise ValueError(f"The value must be ReadWriteTwoDatetimesProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_datetimes.value:
            with self._property_read_write_two_datetimes.mutex:
                self._property_read_write_two_datetimes.value = value
                self._property_read_write_two_datetimes.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoDatetimes/value".format(self._instance_id), payload, self._property_read_write_two_datetimes.version)
            for callback in self._property_read_write_two_datetimes.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_datetimes(self, first: datetime, second: Optional[datetime]):
        """This method sets (publishes) a new value for the 'read_write_two_datetimes' property."""
        if not isinstance(first, datetime):
            raise ValueError(f"The 'first' value must be datetime.")
        if not isinstance(second, datetime) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[datetime].")

        obj = interface_types.ReadWriteTwoDatetimesProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_datetimes = obj

    def on_read_write_two_datetimes_updates(self, handler: Callable[[datetime, Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_datetimes' property update is received."""
        if handler is not None:
            self._property_read_write_two_datetimes.callbacks.append(handler)

    @property
    def read_write_duration(self) -> Optional[timedelta]:
        """This property returns the last received value for the 'read_write_duration' property."""
        with self._property_read_write_duration_mutex:
            return self._property_read_write_duration

    @read_write_duration.setter
    def read_write_duration(self, value: timedelta):
        """This property sets (publishes) a new value for the 'read_write_duration' property."""

        if not isinstance(value, timedelta):
            raise ValueError(f"The value must be timedelta .")

        prop_obj = ReadWriteDurationProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_duration.value is None or value != self._property_read_write_duration.value.value:
            with self._property_read_write_duration.mutex:
                self._property_read_write_duration.value = prop_obj
                self._property_read_write_duration.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteDuration/value".format(self._instance_id), payload, self._property_read_write_duration.version)
            for callback in self._property_read_write_duration.callbacks:
                callback(prop_obj.value)

    def set_read_write_duration(self, value: timedelta):
        """This method sets (publishes) a new value for the 'read_write_duration' property."""
        if not isinstance(value, timedelta):
            raise ValueError(f"The 'value' value must be timedelta.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_duration = obj

    def on_read_write_duration_updates(self, handler: Callable[[timedelta], None]):
        """This method registers a callback to be called whenever a new 'read_write_duration' property update is received."""
        if handler is not None:
            self._property_read_write_duration.callbacks.append(handler)

    @property
    def read_write_optional_duration(self) -> Optional[timedelta]:
        """This property returns the last received value for the 'read_write_optional_duration' property."""
        with self._property_read_write_optional_duration_mutex:
            return self._property_read_write_optional_duration

    @read_write_optional_duration.setter
    def read_write_optional_duration(self, value: Optional[timedelta]):
        """This property sets (publishes) a new value for the 'read_write_optional_duration' property."""

        if (value is not None) and (not isinstance(value, timedelta)):
            raise ValueError(f"The value must be timedelta or None.")

        prop_obj = ReadWriteOptionalDurationProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_duration.value is None or value != self._property_read_write_optional_duration.value.value:
            with self._property_read_write_optional_duration.mutex:
                self._property_read_write_optional_duration.value = prop_obj
                self._property_read_write_optional_duration.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalDuration/value".format(self._instance_id), payload, self._property_read_write_optional_duration.version)
            for callback in self._property_read_write_optional_duration.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_duration(self, value: Optional[timedelta]):
        """This method sets (publishes) a new value for the 'read_write_optional_duration' property."""
        if not isinstance(value, timedelta) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[timedelta].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_duration = obj

    def on_read_write_optional_duration_updates(self, handler: Callable[[Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_duration' property update is received."""
        if handler is not None:
            self._property_read_write_optional_duration.callbacks.append(handler)

    @property
    def read_write_two_durations(self) -> Optional[ReadWriteTwoDurationsProperty]:
        """This property returns the last received value for the 'read_write_two_durations' property."""
        with self._property_read_write_two_durations_mutex:
            return self._property_read_write_two_durations

    @read_write_two_durations.setter
    def read_write_two_durations(self, value: ReadWriteTwoDurationsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_durations' property."""

        if not isinstance(value, ReadWriteTwoDurationsProperty):
            raise ValueError(f"The value must be ReadWriteTwoDurationsProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_durations.value:
            with self._property_read_write_two_durations.mutex:
                self._property_read_write_two_durations.value = value
                self._property_read_write_two_durations.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoDurations/value".format(self._instance_id), payload, self._property_read_write_two_durations.version)
            for callback in self._property_read_write_two_durations.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_durations(self, first: timedelta, second: Optional[timedelta]):
        """This method sets (publishes) a new value for the 'read_write_two_durations' property."""
        if not isinstance(first, timedelta):
            raise ValueError(f"The 'first' value must be timedelta.")
        if not isinstance(second, timedelta) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[timedelta].")

        obj = interface_types.ReadWriteTwoDurationsProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_durations = obj

    def on_read_write_two_durations_updates(self, handler: Callable[[timedelta, Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_durations' property update is received."""
        if handler is not None:
            self._property_read_write_two_durations.callbacks.append(handler)

    @property
    def read_write_binary(self) -> Optional[bytes]:
        """This property returns the last received value for the 'read_write_binary' property."""
        with self._property_read_write_binary_mutex:
            return self._property_read_write_binary

    @read_write_binary.setter
    def read_write_binary(self, value: bytes):
        """This property sets (publishes) a new value for the 'read_write_binary' property."""

        if not isinstance(value, bytes):
            raise ValueError(f"The value must be bytes .")

        prop_obj = ReadWriteBinaryProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_binary.value is None or value != self._property_read_write_binary.value.value:
            with self._property_read_write_binary.mutex:
                self._property_read_write_binary.value = prop_obj
                self._property_read_write_binary.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteBinary/value".format(self._instance_id), payload, self._property_read_write_binary.version)
            for callback in self._property_read_write_binary.callbacks:
                callback(prop_obj.value)

    def set_read_write_binary(self, value: bytes):
        """This method sets (publishes) a new value for the 'read_write_binary' property."""
        if not isinstance(value, bytes):
            raise ValueError(f"The 'value' value must be bytes.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_binary = obj

    def on_read_write_binary_updates(self, handler: Callable[[bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_binary' property update is received."""
        if handler is not None:
            self._property_read_write_binary.callbacks.append(handler)

    @property
    def read_write_optional_binary(self) -> bytes:
        """This property returns the last received value for the 'read_write_optional_binary' property."""
        with self._property_read_write_optional_binary_mutex:
            return self._property_read_write_optional_binary

    @read_write_optional_binary.setter
    def read_write_optional_binary(self, value: bytes):
        """This property sets (publishes) a new value for the 'read_write_optional_binary' property."""

        if (value is not None) and (not isinstance(value, bytes)):
            raise ValueError(f"The value must be bytes or None.")

        prop_obj = ReadWriteOptionalBinaryProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_optional_binary.value is None or value != self._property_read_write_optional_binary.value.value:
            with self._property_read_write_optional_binary.mutex:
                self._property_read_write_optional_binary.value = prop_obj
                self._property_read_write_optional_binary.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteOptionalBinary/value".format(self._instance_id), payload, self._property_read_write_optional_binary.version)
            for callback in self._property_read_write_optional_binary.callbacks:
                callback(prop_obj.value)

    def set_read_write_optional_binary(self, value: bytes):
        """This method sets (publishes) a new value for the 'read_write_optional_binary' property."""
        if not isinstance(value, bytes) and value is not None:
            raise ValueError(f"The 'value' value must be bytes.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_binary = obj

    def on_read_write_optional_binary_updates(self, handler: Callable[[bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_binary' property update is received."""
        if handler is not None:
            self._property_read_write_optional_binary.callbacks.append(handler)

    @property
    def read_write_two_binaries(self) -> Optional[ReadWriteTwoBinariesProperty]:
        """This property returns the last received value for the 'read_write_two_binaries' property."""
        with self._property_read_write_two_binaries_mutex:
            return self._property_read_write_two_binaries

    @read_write_two_binaries.setter
    def read_write_two_binaries(self, value: ReadWriteTwoBinariesProperty):
        """This property sets (publishes) a new value for the 'read_write_two_binaries' property."""

        if not isinstance(value, ReadWriteTwoBinariesProperty):
            raise ValueError(f"The value must be ReadWriteTwoBinariesProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_two_binaries.value:
            with self._property_read_write_two_binaries.mutex:
                self._property_read_write_two_binaries.value = value
                self._property_read_write_two_binaries.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteTwoBinaries/value".format(self._instance_id), payload, self._property_read_write_two_binaries.version)
            for callback in self._property_read_write_two_binaries.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_binaries(self, first: bytes, second: bytes):
        """This method sets (publishes) a new value for the 'read_write_two_binaries' property."""
        if not isinstance(first, bytes):
            raise ValueError(f"The 'first' value must be bytes.")
        if not isinstance(second, bytes) and second is not None:
            raise ValueError(f"The 'second' value must be bytes.")

        obj = interface_types.ReadWriteTwoBinariesProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_binaries = obj

    def on_read_write_two_binaries_updates(self, handler: Callable[[bytes, bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_binaries' property update is received."""
        if handler is not None:
            self._property_read_write_two_binaries.callbacks.append(handler)

    @property
    def read_write_list_of_strings(self) -> Optional[List[str]]:
        """This property returns the last received value for the 'read_write_list_of_strings' property."""
        with self._property_read_write_list_of_strings_mutex:
            return self._property_read_write_list_of_strings

    @read_write_list_of_strings.setter
    def read_write_list_of_strings(self, value: List[str]):
        """This property sets (publishes) a new value for the 'read_write_list_of_strings' property."""

        if not isinstance(value, list):
            raise ValueError(f"The value must be list .")

        prop_obj = ReadWriteListOfStringsProperty(value=value)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_read_write_list_of_strings.value is None or value != self._property_read_write_list_of_strings.value.value:
            with self._property_read_write_list_of_strings.mutex:
                self._property_read_write_list_of_strings.value = prop_obj
                self._property_read_write_list_of_strings.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteListOfStrings/value".format(self._instance_id), payload, self._property_read_write_list_of_strings.version)
            for callback in self._property_read_write_list_of_strings.callbacks:
                callback(prop_obj.value)

    def set_read_write_list_of_strings(self, value: List[str]):
        """This method sets (publishes) a new value for the 'read_write_list_of_strings' property."""
        if not isinstance(value, list):
            raise ValueError(f"The 'value' value must be List[str].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_list_of_strings = obj

    def on_read_write_list_of_strings_updates(self, handler: Callable[[List[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_list_of_strings' property update is received."""
        if handler is not None:
            self._property_read_write_list_of_strings.callbacks.append(handler)

    @property
    def read_write_lists(self) -> Optional[ReadWriteListsProperty]:
        """This property returns the last received value for the 'read_write_lists' property."""
        with self._property_read_write_lists_mutex:
            return self._property_read_write_lists

    @read_write_lists.setter
    def read_write_lists(self, value: ReadWriteListsProperty):
        """This property sets (publishes) a new value for the 'read_write_lists' property."""

        if not isinstance(value, ReadWriteListsProperty):
            raise ValueError(f"The value must be ReadWriteListsProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_read_write_lists.value:
            with self._property_read_write_lists.mutex:
                self._property_read_write_lists.value = value
                self._property_read_write_lists.version += 1
                self._conn.publish_property_state("testable/{}/property/readWriteLists/value".format(self._instance_id), payload, self._property_read_write_lists.version)
            for callback in self._property_read_write_lists.callbacks:
                callback(value.the_list, value.optional_list)

    def set_read_write_lists(self, the_list: List[Numbers], optional_list: List[datetime]):
        """This method sets (publishes) a new value for the 'read_write_lists' property."""
        if not isinstance(the_list, list):
            raise ValueError(f"The 'the_list' value must be List[Numbers].")
        if not isinstance(optional_list, list) and optional_list is not None:
            raise ValueError(f"The 'optional_list' value must be List[datetime].")

        obj = interface_types.ReadWriteListsProperty(
            the_list=the_list,
            optionalList=optional_list,
        )

        # Use the property.setter to do that actual work.
        self.read_write_lists = obj

    def on_read_write_lists_updates(self, handler: Callable[[List[Numbers], List[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_lists' property update is received."""
        if handler is not None:
            self._property_read_write_lists.callbacks.append(handler)


class TestableServerBuilder:
    """
    This is a builder for the TestableServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._call_with_nothing_method_handler: Optional[Callable[[None], None]] = None
        self._call_one_integer_method_handler: Optional[Callable[[int], int]] = None
        self._call_optional_integer_method_handler: Optional[Callable[[Optional[int]], Optional[int]]] = None
        self._call_three_integers_method_handler: Optional[Callable[[int, int, Optional[int]], CallThreeIntegersMethodResponse]] = None
        self._call_one_string_method_handler: Optional[Callable[[str], str]] = None
        self._call_optional_string_method_handler: Optional[Callable[[Optional[str]], Optional[str]]] = None
        self._call_three_strings_method_handler: Optional[Callable[[str, Optional[str], str], CallThreeStringsMethodResponse]] = None
        self._call_one_enum_method_handler: Optional[Callable[[Numbers], Numbers]] = None
        self._call_optional_enum_method_handler: Optional[Callable[[Optional[Numbers]], Optional[Numbers]]] = None
        self._call_three_enums_method_handler: Optional[Callable[[Numbers, Numbers, Optional[Numbers]], CallThreeEnumsMethodResponse]] = None
        self._call_one_struct_method_handler: Optional[Callable[[AllTypes], AllTypes]] = None
        self._call_optional_struct_method_handler: Optional[Callable[[AllTypes], AllTypes]] = None
        self._call_three_structs_method_handler: Optional[Callable[[AllTypes, AllTypes, AllTypes], CallThreeStructsMethodResponse]] = None
        self._call_one_date_time_method_handler: Optional[Callable[[datetime], datetime]] = None
        self._call_optional_date_time_method_handler: Optional[Callable[[Optional[datetime]], Optional[datetime]]] = None
        self._call_three_date_times_method_handler: Optional[Callable[[datetime, datetime, Optional[datetime]], CallThreeDateTimesMethodResponse]] = None
        self._call_one_duration_method_handler: Optional[Callable[[timedelta], timedelta]] = None
        self._call_optional_duration_method_handler: Optional[Callable[[Optional[timedelta]], Optional[timedelta]]] = None
        self._call_three_durations_method_handler: Optional[Callable[[timedelta, timedelta, Optional[timedelta]], CallThreeDurationsMethodResponse]] = None
        self._call_one_binary_method_handler: Optional[Callable[[bytes], bytes]] = None
        self._call_optional_binary_method_handler: Optional[Callable[[bytes], bytes]] = None
        self._call_three_binaries_method_handler: Optional[Callable[[bytes, bytes, bytes], CallThreeBinariesMethodResponse]] = None
        self._call_one_list_of_integers_method_handler: Optional[Callable[[List[int]], List[int]]] = None
        self._call_optional_list_of_floats_method_handler: Optional[Callable[[List[float]], List[float]]] = None
        self._call_two_lists_method_handler: Optional[Callable[[List[Numbers], List[str]], CallTwoListsMethodResponse]] = None

        self._read_write_integer_property_callbacks: List[Callable[[int], None]] = []
        self._read_only_integer_property_callbacks: List[Callable[[int], None]] = []
        self._read_write_optional_integer_property_callbacks: List[Callable[[Optional[int]], None]] = []
        self._read_write_two_integers_property_callbacks: List[Callable[[int, Optional[int]], None]] = []
        self._read_only_string_property_callbacks: List[Callable[[str], None]] = []
        self._read_write_string_property_callbacks: List[Callable[[str], None]] = []
        self._read_write_optional_string_property_callbacks: List[Callable[[Optional[str]], None]] = []
        self._read_write_two_strings_property_callbacks: List[Callable[[str, Optional[str]], None]] = []
        self._read_write_struct_property_callbacks: List[Callable[[AllTypes], None]] = []
        self._read_write_optional_struct_property_callbacks: List[Callable[[AllTypes], None]] = []
        self._read_write_two_structs_property_callbacks: List[Callable[[AllTypes, AllTypes], None]] = []
        self._read_only_enum_property_callbacks: List[Callable[[Numbers], None]] = []
        self._read_write_enum_property_callbacks: List[Callable[[Numbers], None]] = []
        self._read_write_optional_enum_property_callbacks: List[Callable[[Optional[Numbers]], None]] = []
        self._read_write_two_enums_property_callbacks: List[Callable[[Numbers, Optional[Numbers]], None]] = []
        self._read_write_datetime_property_callbacks: List[Callable[[datetime], None]] = []
        self._read_write_optional_datetime_property_callbacks: List[Callable[[Optional[datetime]], None]] = []
        self._read_write_two_datetimes_property_callbacks: List[Callable[[datetime, Optional[datetime]], None]] = []
        self._read_write_duration_property_callbacks: List[Callable[[timedelta], None]] = []
        self._read_write_optional_duration_property_callbacks: List[Callable[[Optional[timedelta]], None]] = []
        self._read_write_two_durations_property_callbacks: List[Callable[[timedelta, Optional[timedelta]], None]] = []
        self._read_write_binary_property_callbacks: List[Callable[[bytes], None]] = []
        self._read_write_optional_binary_property_callbacks: List[Callable[[bytes], None]] = []
        self._read_write_two_binaries_property_callbacks: List[Callable[[bytes, bytes], None]] = []
        self._read_write_list_of_strings_property_callbacks: List[Callable[[List[str]], None]] = []
        self._read_write_lists_property_callbacks: List[Callable[[List[Numbers], List[datetime]], None]] = []

    def handle_call_with_nothing(self, handler: Callable[[None], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_with_nothing_method_handler is None and handler is not None:
            self._call_with_nothing_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_integer(self, handler: Callable[[int], int]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_integer_method_handler is None and handler is not None:
            self._call_one_integer_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_integer(self, handler: Callable[[Optional[int]], Optional[int]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_integer_method_handler is None and handler is not None:
            self._call_optional_integer_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_integers(self, handler: Callable[[int, int, Optional[int]], CallThreeIntegersMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_integers_method_handler is None and handler is not None:
            self._call_three_integers_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_string(self, handler: Callable[[str], str]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_string_method_handler is None and handler is not None:
            self._call_one_string_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_string(self, handler: Callable[[Optional[str]], Optional[str]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_string_method_handler is None and handler is not None:
            self._call_optional_string_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_strings(self, handler: Callable[[str, Optional[str], str], CallThreeStringsMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_strings_method_handler is None and handler is not None:
            self._call_three_strings_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_enum(self, handler: Callable[[Numbers], Numbers]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_enum_method_handler is None and handler is not None:
            self._call_one_enum_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_enum(self, handler: Callable[[Optional[Numbers]], Optional[Numbers]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_enum_method_handler is None and handler is not None:
            self._call_optional_enum_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_enums(self, handler: Callable[[Numbers, Numbers, Optional[Numbers]], CallThreeEnumsMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_enums_method_handler is None and handler is not None:
            self._call_three_enums_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_struct(self, handler: Callable[[AllTypes], AllTypes]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_struct_method_handler is None and handler is not None:
            self._call_one_struct_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_struct(self, handler: Callable[[AllTypes], AllTypes]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_struct_method_handler is None and handler is not None:
            self._call_optional_struct_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_structs(self, handler: Callable[[AllTypes, AllTypes, AllTypes], CallThreeStructsMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_structs_method_handler is None and handler is not None:
            self._call_three_structs_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_date_time(self, handler: Callable[[datetime], datetime]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_date_time_method_handler is None and handler is not None:
            self._call_one_date_time_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_date_time(self, handler: Callable[[Optional[datetime]], Optional[datetime]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_date_time_method_handler is None and handler is not None:
            self._call_optional_date_time_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_date_times(self, handler: Callable[[datetime, datetime, Optional[datetime]], CallThreeDateTimesMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_date_times_method_handler is None and handler is not None:
            self._call_three_date_times_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_duration(self, handler: Callable[[timedelta], timedelta]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_duration_method_handler is None and handler is not None:
            self._call_one_duration_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_duration(self, handler: Callable[[Optional[timedelta]], Optional[timedelta]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_duration_method_handler is None and handler is not None:
            self._call_optional_duration_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_durations(self, handler: Callable[[timedelta, timedelta, Optional[timedelta]], CallThreeDurationsMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_durations_method_handler is None and handler is not None:
            self._call_three_durations_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_binary(self, handler: Callable[[bytes], bytes]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_binary_method_handler is None and handler is not None:
            self._call_one_binary_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_binary(self, handler: Callable[[bytes], bytes]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_binary_method_handler is None and handler is not None:
            self._call_optional_binary_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_three_binaries(self, handler: Callable[[bytes, bytes, bytes], CallThreeBinariesMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_three_binaries_method_handler is None and handler is not None:
            self._call_three_binaries_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_one_list_of_integers(self, handler: Callable[[List[int]], List[int]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_one_list_of_integers_method_handler is None and handler is not None:
            self._call_one_list_of_integers_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_optional_list_of_floats(self, handler: Callable[[List[float]], List[float]]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_optional_list_of_floats_method_handler is None and handler is not None:
            self._call_optional_list_of_floats_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_call_two_lists(self, handler: Callable[[List[Numbers], List[str]], CallTwoListsMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._call_two_lists_method_handler is None and handler is not None:
            self._call_two_lists_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def on_read_write_integer_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'read_write_integer' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_integer_property_callbacks.append(wrapper)
        return wrapper

    def on_read_only_integer_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'read_only_integer' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_only_integer_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_integer_updates(self, handler: Callable[[Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_integer' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_integer_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_integers_updates(self, handler: Callable[[int, Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_integers' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_integers_property_callbacks.append(wrapper)
        return wrapper

    def on_read_only_string_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'read_only_string' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_only_string_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_string_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'read_write_string' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_string_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_string_updates(self, handler: Callable[[Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_string' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_string_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_strings_updates(self, handler: Callable[[str, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_strings' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_strings_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_struct_updates(self, handler: Callable[[AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_struct' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_struct_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_struct_updates(self, handler: Callable[[AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_struct' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_struct_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_structs_updates(self, handler: Callable[[AllTypes, AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_structs' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_structs_property_callbacks.append(wrapper)
        return wrapper

    def on_read_only_enum_updates(self, handler: Callable[[Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_only_enum' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_only_enum_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_enum_updates(self, handler: Callable[[Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_write_enum' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_enum_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_enum_updates(self, handler: Callable[[Optional[Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_enum' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_enum_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_enums_updates(self, handler: Callable[[Numbers, Optional[Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_enums' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_enums_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_datetime_updates(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'read_write_datetime' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_datetime_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_datetime_updates(self, handler: Callable[[Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_datetime' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_datetime_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_datetimes_updates(self, handler: Callable[[datetime, Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_datetimes' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_datetimes_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_duration_updates(self, handler: Callable[[timedelta], None]):
        """This method registers a callback to be called whenever a new 'read_write_duration' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_duration_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_duration_updates(self, handler: Callable[[Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_duration' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_duration_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_durations_updates(self, handler: Callable[[timedelta, Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_durations' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_durations_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_binary_updates(self, handler: Callable[[bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_binary' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_binary_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_optional_binary_updates(self, handler: Callable[[bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_binary' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_optional_binary_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_two_binaries_updates(self, handler: Callable[[bytes, bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_binaries' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_two_binaries_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_list_of_strings_updates(self, handler: Callable[[List[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_list_of_strings' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_list_of_strings_property_callbacks.append(wrapper)
        return wrapper

    def on_read_write_lists_updates(self, handler: Callable[[List[Numbers], List[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_lists' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._read_write_lists_property_callbacks.append(wrapper)
        return wrapper

    def build(self, connection: IBrokerConnection, instance_id: str, initial_property_values: TestableInitialPropertyValues, binding: Optional[Any] = None) -> TestableServer:
        new_server = TestableServer(connection, instance_id, initial_property_values)

        if self._call_with_nothing_method_handler is not None:
            if binding:
                binding_cb = self._call_with_nothing_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_with_nothing(binding_cb)
            else:
                new_server.handle_call_with_nothing(self._call_with_nothing_method_handler)
        if self._call_one_integer_method_handler is not None:
            if binding:
                binding_cb = self._call_one_integer_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_integer(binding_cb)
            else:
                new_server.handle_call_one_integer(self._call_one_integer_method_handler)
        if self._call_optional_integer_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_integer_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_integer(binding_cb)
            else:
                new_server.handle_call_optional_integer(self._call_optional_integer_method_handler)
        if self._call_three_integers_method_handler is not None:
            if binding:
                binding_cb = self._call_three_integers_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_integers(binding_cb)
            else:
                new_server.handle_call_three_integers(self._call_three_integers_method_handler)
        if self._call_one_string_method_handler is not None:
            if binding:
                binding_cb = self._call_one_string_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_string(binding_cb)
            else:
                new_server.handle_call_one_string(self._call_one_string_method_handler)
        if self._call_optional_string_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_string_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_string(binding_cb)
            else:
                new_server.handle_call_optional_string(self._call_optional_string_method_handler)
        if self._call_three_strings_method_handler is not None:
            if binding:
                binding_cb = self._call_three_strings_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_strings(binding_cb)
            else:
                new_server.handle_call_three_strings(self._call_three_strings_method_handler)
        if self._call_one_enum_method_handler is not None:
            if binding:
                binding_cb = self._call_one_enum_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_enum(binding_cb)
            else:
                new_server.handle_call_one_enum(self._call_one_enum_method_handler)
        if self._call_optional_enum_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_enum_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_enum(binding_cb)
            else:
                new_server.handle_call_optional_enum(self._call_optional_enum_method_handler)
        if self._call_three_enums_method_handler is not None:
            if binding:
                binding_cb = self._call_three_enums_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_enums(binding_cb)
            else:
                new_server.handle_call_three_enums(self._call_three_enums_method_handler)
        if self._call_one_struct_method_handler is not None:
            if binding:
                binding_cb = self._call_one_struct_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_struct(binding_cb)
            else:
                new_server.handle_call_one_struct(self._call_one_struct_method_handler)
        if self._call_optional_struct_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_struct_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_struct(binding_cb)
            else:
                new_server.handle_call_optional_struct(self._call_optional_struct_method_handler)
        if self._call_three_structs_method_handler is not None:
            if binding:
                binding_cb = self._call_three_structs_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_structs(binding_cb)
            else:
                new_server.handle_call_three_structs(self._call_three_structs_method_handler)
        if self._call_one_date_time_method_handler is not None:
            if binding:
                binding_cb = self._call_one_date_time_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_date_time(binding_cb)
            else:
                new_server.handle_call_one_date_time(self._call_one_date_time_method_handler)
        if self._call_optional_date_time_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_date_time_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_date_time(binding_cb)
            else:
                new_server.handle_call_optional_date_time(self._call_optional_date_time_method_handler)
        if self._call_three_date_times_method_handler is not None:
            if binding:
                binding_cb = self._call_three_date_times_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_date_times(binding_cb)
            else:
                new_server.handle_call_three_date_times(self._call_three_date_times_method_handler)
        if self._call_one_duration_method_handler is not None:
            if binding:
                binding_cb = self._call_one_duration_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_duration(binding_cb)
            else:
                new_server.handle_call_one_duration(self._call_one_duration_method_handler)
        if self._call_optional_duration_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_duration_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_duration(binding_cb)
            else:
                new_server.handle_call_optional_duration(self._call_optional_duration_method_handler)
        if self._call_three_durations_method_handler is not None:
            if binding:
                binding_cb = self._call_three_durations_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_durations(binding_cb)
            else:
                new_server.handle_call_three_durations(self._call_three_durations_method_handler)
        if self._call_one_binary_method_handler is not None:
            if binding:
                binding_cb = self._call_one_binary_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_binary(binding_cb)
            else:
                new_server.handle_call_one_binary(self._call_one_binary_method_handler)
        if self._call_optional_binary_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_binary_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_binary(binding_cb)
            else:
                new_server.handle_call_optional_binary(self._call_optional_binary_method_handler)
        if self._call_three_binaries_method_handler is not None:
            if binding:
                binding_cb = self._call_three_binaries_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_three_binaries(binding_cb)
            else:
                new_server.handle_call_three_binaries(self._call_three_binaries_method_handler)
        if self._call_one_list_of_integers_method_handler is not None:
            if binding:
                binding_cb = self._call_one_list_of_integers_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_one_list_of_integers(binding_cb)
            else:
                new_server.handle_call_one_list_of_integers(self._call_one_list_of_integers_method_handler)
        if self._call_optional_list_of_floats_method_handler is not None:
            if binding:
                binding_cb = self._call_optional_list_of_floats_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_optional_list_of_floats(binding_cb)
            else:
                new_server.handle_call_optional_list_of_floats(self._call_optional_list_of_floats_method_handler)
        if self._call_two_lists_method_handler is not None:
            if binding:
                binding_cb = self._call_two_lists_method_handler.__get__(binding, binding.__class__)
                new_server.handle_call_two_lists(binding_cb)
            else:
                new_server.handle_call_two_lists(self._call_two_lists_method_handler)

        for callback in self._read_write_integer_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_integer_updates(binding_cb)
            else:
                new_server.on_read_write_integer_updates(callback)

        for callback in self._read_only_integer_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_only_integer_updates(binding_cb)
            else:
                new_server.on_read_only_integer_updates(callback)

        for callback in self._read_write_optional_integer_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_integer_updates(binding_cb)
            else:
                new_server.on_read_write_optional_integer_updates(callback)

        for callback in self._read_write_two_integers_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_integers_updates(binding_cb)
            else:
                new_server.on_read_write_two_integers_updates(callback)

        for callback in self._read_only_string_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_only_string_updates(binding_cb)
            else:
                new_server.on_read_only_string_updates(callback)

        for callback in self._read_write_string_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_string_updates(binding_cb)
            else:
                new_server.on_read_write_string_updates(callback)

        for callback in self._read_write_optional_string_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_string_updates(binding_cb)
            else:
                new_server.on_read_write_optional_string_updates(callback)

        for callback in self._read_write_two_strings_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_strings_updates(binding_cb)
            else:
                new_server.on_read_write_two_strings_updates(callback)

        for callback in self._read_write_struct_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_struct_updates(binding_cb)
            else:
                new_server.on_read_write_struct_updates(callback)

        for callback in self._read_write_optional_struct_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_struct_updates(binding_cb)
            else:
                new_server.on_read_write_optional_struct_updates(callback)

        for callback in self._read_write_two_structs_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_structs_updates(binding_cb)
            else:
                new_server.on_read_write_two_structs_updates(callback)

        for callback in self._read_only_enum_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_only_enum_updates(binding_cb)
            else:
                new_server.on_read_only_enum_updates(callback)

        for callback in self._read_write_enum_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_enum_updates(binding_cb)
            else:
                new_server.on_read_write_enum_updates(callback)

        for callback in self._read_write_optional_enum_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_enum_updates(binding_cb)
            else:
                new_server.on_read_write_optional_enum_updates(callback)

        for callback in self._read_write_two_enums_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_enums_updates(binding_cb)
            else:
                new_server.on_read_write_two_enums_updates(callback)

        for callback in self._read_write_datetime_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_datetime_updates(binding_cb)
            else:
                new_server.on_read_write_datetime_updates(callback)

        for callback in self._read_write_optional_datetime_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_datetime_updates(binding_cb)
            else:
                new_server.on_read_write_optional_datetime_updates(callback)

        for callback in self._read_write_two_datetimes_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_datetimes_updates(binding_cb)
            else:
                new_server.on_read_write_two_datetimes_updates(callback)

        for callback in self._read_write_duration_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_duration_updates(binding_cb)
            else:
                new_server.on_read_write_duration_updates(callback)

        for callback in self._read_write_optional_duration_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_duration_updates(binding_cb)
            else:
                new_server.on_read_write_optional_duration_updates(callback)

        for callback in self._read_write_two_durations_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_durations_updates(binding_cb)
            else:
                new_server.on_read_write_two_durations_updates(callback)

        for callback in self._read_write_binary_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_binary_updates(binding_cb)
            else:
                new_server.on_read_write_binary_updates(callback)

        for callback in self._read_write_optional_binary_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_optional_binary_updates(binding_cb)
            else:
                new_server.on_read_write_optional_binary_updates(callback)

        for callback in self._read_write_two_binaries_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_two_binaries_updates(binding_cb)
            else:
                new_server.on_read_write_two_binaries_updates(callback)

        for callback in self._read_write_list_of_strings_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_list_of_strings_updates(binding_cb)
            else:
                new_server.on_read_write_list_of_strings_updates(callback)

        for callback in self._read_write_lists_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_read_write_lists_updates(binding_cb)
            else:
                new_server.on_read_write_lists_updates(callback)

        return new_server
