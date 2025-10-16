"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Test Able interface.
"""

from typing import Dict, Callable, List, Any, Optional
from uuid import uuid4
from functools import partial
import json
import logging
from datetime import datetime, timedelta, UTC
from isodate import parse_duration

import asyncio
import concurrent.futures as futures
from .method_codes import *
from .interface_types import *
import threading

from .connection import IBrokerConnection
from . import interface_types as interface_types

logging.basicConfig(level=logging.DEBUG)

EmptySignalCallbackType = Callable[[], None]
SingleIntSignalCallbackType = Callable[[int], None]
SingleOptionalIntSignalCallbackType = Callable[[Optional[int]], None]
ThreeIntegersSignalCallbackType = Callable[[int, int, Optional[int]], None]
SingleStringSignalCallbackType = Callable[[str], None]
SingleOptionalStringSignalCallbackType = Callable[[Optional[str]], None]
ThreeStringsSignalCallbackType = Callable[[str, str, Optional[str]], None]
SingleEnumSignalCallbackType = Callable[[interface_types.Numbers], None]
SingleOptionalEnumSignalCallbackType = Callable[[Optional[interface_types.Numbers]], None]
ThreeEnumsSignalCallbackType = Callable[[interface_types.Numbers, interface_types.Numbers, Optional[interface_types.Numbers]], None]
SingleStructSignalCallbackType = Callable[[interface_types.AllTypes], None]
SingleOptionalStructSignalCallbackType = Callable[[interface_types.AllTypes], None]
ThreeStructsSignalCallbackType = Callable[[interface_types.AllTypes, interface_types.AllTypes, interface_types.AllTypes], None]
SingleDateTimeSignalCallbackType = Callable[[datetime], None]
SingleOptionalDatetimeSignalCallbackType = Callable[[Optional[datetime]], None]
ThreeDateTimesSignalCallbackType = Callable[[datetime, datetime, Optional[datetime]], None]
SingleDurationSignalCallbackType = Callable[[timedelta], None]
SingleOptionalDurationSignalCallbackType = Callable[[Optional[timedelta]], None]
ThreeDurationsSignalCallbackType = Callable[[timedelta, timedelta, Optional[timedelta]], None]
SingleBinarySignalCallbackType = Callable[[bytes], None]
SingleOptionalBinarySignalCallbackType = Callable[[bytes], None]
ThreeBinariesSignalCallbackType = Callable[[bytes, bytes, bytes], None]
CallWithNothingMethodResponseCallbackType = Callable[[], None]
CallOneIntegerMethodResponseCallbackType = Callable[[int], None]
CallOptionalIntegerMethodResponseCallbackType = Callable[[Optional[int]], None]
CallThreeIntegersMethodResponseCallbackType = Callable[[interface_types.CallThreeIntegersMethodResponse], None]
CallOneStringMethodResponseCallbackType = Callable[[str], None]
CallOptionalStringMethodResponseCallbackType = Callable[[Optional[str]], None]
CallThreeStringsMethodResponseCallbackType = Callable[[interface_types.CallThreeStringsMethodResponse], None]
CallOneEnumMethodResponseCallbackType = Callable[[interface_types.Numbers], None]
CallOptionalEnumMethodResponseCallbackType = Callable[[Optional[interface_types.Numbers]], None]
CallThreeEnumsMethodResponseCallbackType = Callable[[interface_types.CallThreeEnumsMethodResponse], None]
CallOneStructMethodResponseCallbackType = Callable[[interface_types.AllTypes], None]
CallOptionalStructMethodResponseCallbackType = Callable[[interface_types.AllTypes], None]
CallThreeStructsMethodResponseCallbackType = Callable[[interface_types.CallThreeStructsMethodResponse], None]
CallOneDateTimeMethodResponseCallbackType = Callable[[datetime], None]
CallOptionalDateTimeMethodResponseCallbackType = Callable[[Optional[datetime]], None]
CallThreeDateTimesMethodResponseCallbackType = Callable[[interface_types.CallThreeDateTimesMethodResponse], None]
CallOneDurationMethodResponseCallbackType = Callable[[timedelta], None]
CallOptionalDurationMethodResponseCallbackType = Callable[[Optional[timedelta]], None]
CallThreeDurationsMethodResponseCallbackType = Callable[[interface_types.CallThreeDurationsMethodResponse], None]
CallOneBinaryMethodResponseCallbackType = Callable[[bytes], None]
CallOptionalBinaryMethodResponseCallbackType = Callable[[bytes], None]
CallThreeBinariesMethodResponseCallbackType = Callable[[interface_types.CallThreeBinariesMethodResponse], None]

ReadWriteIntegerPropertyUpdatedCallbackType = Callable[[int], None]
ReadOnlyIntegerPropertyUpdatedCallbackType = Callable[[int], None]
ReadWriteOptionalIntegerPropertyUpdatedCallbackType = Callable[[Optional[int]], None]
ReadWriteTwoIntegersPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoIntegersProperty], None]
ReadOnlyStringPropertyUpdatedCallbackType = Callable[[str], None]
ReadWriteStringPropertyUpdatedCallbackType = Callable[[str], None]
ReadWriteOptionalStringPropertyUpdatedCallbackType = Callable[[Optional[str]], None]
ReadWriteTwoStringsPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoStringsProperty], None]
ReadWriteStructPropertyUpdatedCallbackType = Callable[[interface_types.AllTypes], None]
ReadWriteOptionalStructPropertyUpdatedCallbackType = Callable[[interface_types.AllTypes], None]
ReadWriteTwoStructsPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoStructsProperty], None]
ReadOnlyEnumPropertyUpdatedCallbackType = Callable[[interface_types.Numbers], None]
ReadWriteEnumPropertyUpdatedCallbackType = Callable[[interface_types.Numbers], None]
ReadWriteOptionalEnumPropertyUpdatedCallbackType = Callable[[Optional[interface_types.Numbers]], None]
ReadWriteTwoEnumsPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoEnumsProperty], None]
ReadWriteDatetimePropertyUpdatedCallbackType = Callable[[datetime], None]
ReadWriteOptionalDatetimePropertyUpdatedCallbackType = Callable[[Optional[datetime]], None]
ReadWriteTwoDatetimesPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoDatetimesProperty], None]
ReadWriteDurationPropertyUpdatedCallbackType = Callable[[timedelta], None]
ReadWriteOptionalDurationPropertyUpdatedCallbackType = Callable[[Optional[timedelta]], None]
ReadWriteTwoDurationsPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoDurationsProperty], None]
ReadWriteBinaryPropertyUpdatedCallbackType = Callable[[bytes], None]
ReadWriteOptionalBinaryPropertyUpdatedCallbackType = Callable[[bytes], None]
ReadWriteTwoBinariesPropertyUpdatedCallbackType = Callable[[interface_types.ReadWriteTwoBinariesProperty], None]


class TestAbleClient:

    def __init__(self, connection: IBrokerConnection, service_instance_id: str):
        """Constructor for a `TestAbleClient` object."""
        self._logger = logging.getLogger("TestAbleClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing TestAbleClient")
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = service_instance_id

        self._pending_method_responses: dict[str, Callable[..., None]] = {}

        self._property_read_write_integer = None  # type: Optional[int]
        self._property_read_write_integer_mutex = threading.Lock()
        self._property_read_write_integer_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteInteger/value".format(self._service_id), self._receive_read_write_integer_property_update_message)
        self._changed_value_callbacks_for_read_write_integer: list[ReadWriteIntegerPropertyUpdatedCallbackType] = []
        self._property_read_only_integer = None  # type: Optional[int]
        self._property_read_only_integer_mutex = threading.Lock()
        self._property_read_only_integer_version = -1
        self._conn.subscribe("testAble/{}/property/readOnlyInteger/value".format(self._service_id), self._receive_read_only_integer_property_update_message)
        self._changed_value_callbacks_for_read_only_integer: list[ReadOnlyIntegerPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_integer = None  # type: Optional[int]
        self._property_read_write_optional_integer_mutex = threading.Lock()
        self._property_read_write_optional_integer_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalInteger/value".format(self._service_id), self._receive_read_write_optional_integer_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_integer: list[ReadWriteOptionalIntegerPropertyUpdatedCallbackType] = []
        self._property_read_write_two_integers = None  # type: Optional[interface_types.ReadWriteTwoIntegersProperty]
        self._property_read_write_two_integers_mutex = threading.Lock()
        self._property_read_write_two_integers_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoIntegers/value".format(self._service_id), self._receive_read_write_two_integers_property_update_message)
        self._changed_value_callbacks_for_read_write_two_integers: list[ReadWriteTwoIntegersPropertyUpdatedCallbackType] = []
        self._property_read_only_string = None  # type: Optional[str]
        self._property_read_only_string_mutex = threading.Lock()
        self._property_read_only_string_version = -1
        self._conn.subscribe("testAble/{}/property/readOnlyString/value".format(self._service_id), self._receive_read_only_string_property_update_message)
        self._changed_value_callbacks_for_read_only_string: list[ReadOnlyStringPropertyUpdatedCallbackType] = []
        self._property_read_write_string = None  # type: Optional[str]
        self._property_read_write_string_mutex = threading.Lock()
        self._property_read_write_string_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteString/value".format(self._service_id), self._receive_read_write_string_property_update_message)
        self._changed_value_callbacks_for_read_write_string: list[ReadWriteStringPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_string = None  # type: Optional[str]
        self._property_read_write_optional_string_mutex = threading.Lock()
        self._property_read_write_optional_string_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalString/value".format(self._service_id), self._receive_read_write_optional_string_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_string: list[ReadWriteOptionalStringPropertyUpdatedCallbackType] = []
        self._property_read_write_two_strings = None  # type: Optional[interface_types.ReadWriteTwoStringsProperty]
        self._property_read_write_two_strings_mutex = threading.Lock()
        self._property_read_write_two_strings_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoStrings/value".format(self._service_id), self._receive_read_write_two_strings_property_update_message)
        self._changed_value_callbacks_for_read_write_two_strings: list[ReadWriteTwoStringsPropertyUpdatedCallbackType] = []
        self._property_read_write_struct = None  # type: Optional[interface_types.AllTypes]
        self._property_read_write_struct_mutex = threading.Lock()
        self._property_read_write_struct_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteStruct/value".format(self._service_id), self._receive_read_write_struct_property_update_message)
        self._changed_value_callbacks_for_read_write_struct: list[ReadWriteStructPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_struct = None  # type: Optional[interface_types.AllTypes]
        self._property_read_write_optional_struct_mutex = threading.Lock()
        self._property_read_write_optional_struct_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalStruct/value".format(self._service_id), self._receive_read_write_optional_struct_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_struct: list[ReadWriteOptionalStructPropertyUpdatedCallbackType] = []
        self._property_read_write_two_structs = None  # type: Optional[interface_types.ReadWriteTwoStructsProperty]
        self._property_read_write_two_structs_mutex = threading.Lock()
        self._property_read_write_two_structs_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoStructs/value".format(self._service_id), self._receive_read_write_two_structs_property_update_message)
        self._changed_value_callbacks_for_read_write_two_structs: list[ReadWriteTwoStructsPropertyUpdatedCallbackType] = []
        self._property_read_only_enum = None  # type: Optional[interface_types.Numbers]
        self._property_read_only_enum_mutex = threading.Lock()
        self._property_read_only_enum_version = -1
        self._conn.subscribe("testAble/{}/property/readOnlyEnum/value".format(self._service_id), self._receive_read_only_enum_property_update_message)
        self._changed_value_callbacks_for_read_only_enum: list[ReadOnlyEnumPropertyUpdatedCallbackType] = []
        self._property_read_write_enum = None  # type: Optional[interface_types.Numbers]
        self._property_read_write_enum_mutex = threading.Lock()
        self._property_read_write_enum_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteEnum/value".format(self._service_id), self._receive_read_write_enum_property_update_message)
        self._changed_value_callbacks_for_read_write_enum: list[ReadWriteEnumPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_enum = None  # type: Optional[interface_types.Numbers]
        self._property_read_write_optional_enum_mutex = threading.Lock()
        self._property_read_write_optional_enum_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalEnum/value".format(self._service_id), self._receive_read_write_optional_enum_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_enum: list[ReadWriteOptionalEnumPropertyUpdatedCallbackType] = []
        self._property_read_write_two_enums = None  # type: Optional[interface_types.ReadWriteTwoEnumsProperty]
        self._property_read_write_two_enums_mutex = threading.Lock()
        self._property_read_write_two_enums_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoEnums/value".format(self._service_id), self._receive_read_write_two_enums_property_update_message)
        self._changed_value_callbacks_for_read_write_two_enums: list[ReadWriteTwoEnumsPropertyUpdatedCallbackType] = []
        self._property_read_write_datetime = None  # type: Optional[datetime.datetime]
        self._property_read_write_datetime_mutex = threading.Lock()
        self._property_read_write_datetime_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteDatetime/value".format(self._service_id), self._receive_read_write_datetime_property_update_message)
        self._changed_value_callbacks_for_read_write_datetime: list[ReadWriteDatetimePropertyUpdatedCallbackType] = []
        self._property_read_write_optional_datetime = None  # type: Optional[datetime.datetime]
        self._property_read_write_optional_datetime_mutex = threading.Lock()
        self._property_read_write_optional_datetime_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalDatetime/value".format(self._service_id), self._receive_read_write_optional_datetime_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_datetime: list[ReadWriteOptionalDatetimePropertyUpdatedCallbackType] = []
        self._property_read_write_two_datetimes = None  # type: Optional[interface_types.ReadWriteTwoDatetimesProperty]
        self._property_read_write_two_datetimes_mutex = threading.Lock()
        self._property_read_write_two_datetimes_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoDatetimes/value".format(self._service_id), self._receive_read_write_two_datetimes_property_update_message)
        self._changed_value_callbacks_for_read_write_two_datetimes: list[ReadWriteTwoDatetimesPropertyUpdatedCallbackType] = []
        self._property_read_write_duration = None  # type: Optional[datetime.timedelta]
        self._property_read_write_duration_mutex = threading.Lock()
        self._property_read_write_duration_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteDuration/value".format(self._service_id), self._receive_read_write_duration_property_update_message)
        self._changed_value_callbacks_for_read_write_duration: list[ReadWriteDurationPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_duration = None  # type: Optional[datetime.timedelta]
        self._property_read_write_optional_duration_mutex = threading.Lock()
        self._property_read_write_optional_duration_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalDuration/value".format(self._service_id), self._receive_read_write_optional_duration_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_duration: list[ReadWriteOptionalDurationPropertyUpdatedCallbackType] = []
        self._property_read_write_two_durations = None  # type: Optional[interface_types.ReadWriteTwoDurationsProperty]
        self._property_read_write_two_durations_mutex = threading.Lock()
        self._property_read_write_two_durations_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoDurations/value".format(self._service_id), self._receive_read_write_two_durations_property_update_message)
        self._changed_value_callbacks_for_read_write_two_durations: list[ReadWriteTwoDurationsPropertyUpdatedCallbackType] = []
        self._property_read_write_binary = None  # type: Optional[bytes]
        self._property_read_write_binary_mutex = threading.Lock()
        self._property_read_write_binary_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteBinary/value".format(self._service_id), self._receive_read_write_binary_property_update_message)
        self._changed_value_callbacks_for_read_write_binary: list[ReadWriteBinaryPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_binary = None  # type: Optional[bytes]
        self._property_read_write_optional_binary_mutex = threading.Lock()
        self._property_read_write_optional_binary_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteOptionalBinary/value".format(self._service_id), self._receive_read_write_optional_binary_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_binary: list[ReadWriteOptionalBinaryPropertyUpdatedCallbackType] = []
        self._property_read_write_two_binaries = None  # type: Optional[interface_types.ReadWriteTwoBinariesProperty]
        self._property_read_write_two_binaries_mutex = threading.Lock()
        self._property_read_write_two_binaries_version = -1
        self._conn.subscribe("testAble/{}/property/readWriteTwoBinaries/value".format(self._service_id), self._receive_read_write_two_binaries_property_update_message)
        self._changed_value_callbacks_for_read_write_two_binaries: list[ReadWriteTwoBinariesPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_empty: list[EmptySignalCallbackType] = []
        self._signal_recv_callbacks_for_single_int: list[SingleIntSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_int: list[SingleOptionalIntSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_integers: list[ThreeIntegersSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_string: list[SingleStringSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_string: list[SingleOptionalStringSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_strings: list[ThreeStringsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_enum: list[SingleEnumSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_enum: list[SingleOptionalEnumSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_enums: list[ThreeEnumsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_struct: list[SingleStructSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_struct: list[SingleOptionalStructSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_structs: list[ThreeStructsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_date_time: list[SingleDateTimeSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_datetime: list[SingleOptionalDatetimeSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_date_times: list[ThreeDateTimesSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_duration: list[SingleDurationSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_duration: list[SingleOptionalDurationSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_durations: list[ThreeDurationsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_binary: list[SingleBinarySignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_binary: list[SingleOptionalBinarySignalCallbackType] = []
        self._signal_recv_callbacks_for_three_binaries: list[ThreeBinariesSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/callWithNothing/response", self._receive_call_with_nothing_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneInteger/response", self._receive_call_one_integer_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalInteger/response", self._receive_call_optional_integer_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeIntegers/response", self._receive_call_three_integers_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneString/response", self._receive_call_one_string_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalString/response", self._receive_call_optional_string_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeStrings/response", self._receive_call_three_strings_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneEnum/response", self._receive_call_one_enum_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalEnum/response", self._receive_call_optional_enum_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeEnums/response", self._receive_call_three_enums_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneStruct/response", self._receive_call_one_struct_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalStruct/response", self._receive_call_optional_struct_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeStructs/response", self._receive_call_three_structs_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneDateTime/response", self._receive_call_one_date_time_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalDateTime/response", self._receive_call_optional_date_time_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeDateTimes/response", self._receive_call_three_date_times_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneDuration/response", self._receive_call_one_duration_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalDuration/response", self._receive_call_optional_duration_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeDurations/response", self._receive_call_three_durations_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOneBinary/response", self._receive_call_one_binary_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callOptionalBinary/response", self._receive_call_optional_binary_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/callThreeBinaries/response", self._receive_call_three_binaries_response_message)

    @property
    def read_write_integer(self) -> Optional[int]:
        """Property 'read_write_integer' getter."""
        return self._property_read_write_integer

    @read_write_integer.setter
    def read_write_integer(self, value: int):
        """Serializes and publishes the 'read_write_integer' property."""
        if not isinstance(value, int):
            raise ValueError("The 'read_write_integer' property must be a int")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_integer' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteInteger/setValue".format(self._service_id), serialized, qos=1)

    def read_write_integer_changed(self, handler: ReadWriteIntegerPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_integer' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_integer_mutex:
            self._changed_value_callbacks_for_read_write_integer.append(handler)
            if call_immediately and self._property_read_write_integer is not None:
                handler(self._property_read_write_integer)
        return handler

    @property
    def read_only_integer(self) -> Optional[int]:
        """Property 'read_only_integer' getter."""
        return self._property_read_only_integer

    def read_only_integer_changed(self, handler: ReadOnlyIntegerPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_only_integer' property changes.
        Can be used as a decorator.
        """
        with self._property_read_only_integer_mutex:
            self._changed_value_callbacks_for_read_only_integer.append(handler)
            if call_immediately and self._property_read_only_integer is not None:
                handler(self._property_read_only_integer)
        return handler

    @property
    def read_write_optional_integer(self) -> Optional[Optional[int]]:
        """Property 'read_write_optional_integer' getter."""
        return self._property_read_write_optional_integer

    @read_write_optional_integer.setter
    def read_write_optional_integer(self, value: Optional[int]):
        """Serializes and publishes the 'read_write_optional_integer' property."""
        if not isinstance(value, int):
            raise ValueError("The 'read_write_optional_integer' property must be a int")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_integer' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalInteger/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_integer_changed(self, handler: ReadWriteOptionalIntegerPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_integer' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_integer_mutex:
            self._changed_value_callbacks_for_read_write_optional_integer.append(handler)
            if call_immediately and self._property_read_write_optional_integer is not None:
                handler(self._property_read_write_optional_integer)
        return handler

    @property
    def read_write_two_integers(self) -> Optional[interface_types.ReadWriteTwoIntegersProperty]:
        """Property 'read_write_two_integers' getter."""
        return self._property_read_write_two_integers

    @read_write_two_integers.setter
    def read_write_two_integers(self, value: interface_types.ReadWriteTwoIntegersProperty):
        """Serializes and publishes the 'read_write_two_integers' property."""
        if not isinstance(value, ReadWriteTwoIntegersProperty):
            raise ValueError("The 'read_write_two_integers' property must be a interface_types.ReadWriteTwoIntegersProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_integers' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoIntegers/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_integers_changed(self, handler: ReadWriteTwoIntegersPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_integers' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_integers_mutex:
            self._changed_value_callbacks_for_read_write_two_integers.append(handler)
            if call_immediately and self._property_read_write_two_integers is not None:
                handler(self._property_read_write_two_integers)
        return handler

    @property
    def read_only_string(self) -> Optional[str]:
        """Property 'read_only_string' getter."""
        return self._property_read_only_string

    def read_only_string_changed(self, handler: ReadOnlyStringPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_only_string' property changes.
        Can be used as a decorator.
        """
        with self._property_read_only_string_mutex:
            self._changed_value_callbacks_for_read_only_string.append(handler)
            if call_immediately and self._property_read_only_string is not None:
                handler(self._property_read_only_string)
        return handler

    @property
    def read_write_string(self) -> Optional[str]:
        """Property 'read_write_string' getter."""
        return self._property_read_write_string

    @read_write_string.setter
    def read_write_string(self, value: str):
        """Serializes and publishes the 'read_write_string' property."""
        if not isinstance(value, str):
            raise ValueError("The 'read_write_string' property must be a str")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_string' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteString/setValue".format(self._service_id), serialized, qos=1)

    def read_write_string_changed(self, handler: ReadWriteStringPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_string' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_string_mutex:
            self._changed_value_callbacks_for_read_write_string.append(handler)
            if call_immediately and self._property_read_write_string is not None:
                handler(self._property_read_write_string)
        return handler

    @property
    def read_write_optional_string(self) -> Optional[Optional[str]]:
        """Property 'read_write_optional_string' getter."""
        return self._property_read_write_optional_string

    @read_write_optional_string.setter
    def read_write_optional_string(self, value: Optional[str]):
        """Serializes and publishes the 'read_write_optional_string' property."""
        if not isinstance(value, str):
            raise ValueError("The 'read_write_optional_string' property must be a str")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_string' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalString/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_string_changed(self, handler: ReadWriteOptionalStringPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_string' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_string_mutex:
            self._changed_value_callbacks_for_read_write_optional_string.append(handler)
            if call_immediately and self._property_read_write_optional_string is not None:
                handler(self._property_read_write_optional_string)
        return handler

    @property
    def read_write_two_strings(self) -> Optional[interface_types.ReadWriteTwoStringsProperty]:
        """Property 'read_write_two_strings' getter."""
        return self._property_read_write_two_strings

    @read_write_two_strings.setter
    def read_write_two_strings(self, value: interface_types.ReadWriteTwoStringsProperty):
        """Serializes and publishes the 'read_write_two_strings' property."""
        if not isinstance(value, ReadWriteTwoStringsProperty):
            raise ValueError("The 'read_write_two_strings' property must be a interface_types.ReadWriteTwoStringsProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_strings' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoStrings/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_strings_changed(self, handler: ReadWriteTwoStringsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_strings' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_strings_mutex:
            self._changed_value_callbacks_for_read_write_two_strings.append(handler)
            if call_immediately and self._property_read_write_two_strings is not None:
                handler(self._property_read_write_two_strings)
        return handler

    @property
    def read_write_struct(self) -> Optional[interface_types.AllTypes]:
        """Property 'read_write_struct' getter."""
        return self._property_read_write_struct

    @read_write_struct.setter
    def read_write_struct(self, value: interface_types.AllTypes):
        """Serializes and publishes the 'read_write_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError("The 'read_write_struct' property must be a interface_types.AllTypes")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_struct' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteStruct/setValue".format(self._service_id), serialized, qos=1)

    def read_write_struct_changed(self, handler: ReadWriteStructPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_struct' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_struct_mutex:
            self._changed_value_callbacks_for_read_write_struct.append(handler)
            if call_immediately and self._property_read_write_struct is not None:
                handler(self._property_read_write_struct)
        return handler

    @property
    def read_write_optional_struct(self) -> Optional[interface_types.AllTypes]:
        """Property 'read_write_optional_struct' getter."""
        return self._property_read_write_optional_struct

    @read_write_optional_struct.setter
    def read_write_optional_struct(self, value: interface_types.AllTypes):
        """Serializes and publishes the 'read_write_optional_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError("The 'read_write_optional_struct' property must be a interface_types.AllTypes")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_struct' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalStruct/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_struct_changed(self, handler: ReadWriteOptionalStructPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_struct' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_struct_mutex:
            self._changed_value_callbacks_for_read_write_optional_struct.append(handler)
            if call_immediately and self._property_read_write_optional_struct is not None:
                handler(self._property_read_write_optional_struct)
        return handler

    @property
    def read_write_two_structs(self) -> Optional[interface_types.ReadWriteTwoStructsProperty]:
        """Property 'read_write_two_structs' getter."""
        return self._property_read_write_two_structs

    @read_write_two_structs.setter
    def read_write_two_structs(self, value: interface_types.ReadWriteTwoStructsProperty):
        """Serializes and publishes the 'read_write_two_structs' property."""
        if not isinstance(value, ReadWriteTwoStructsProperty):
            raise ValueError("The 'read_write_two_structs' property must be a interface_types.ReadWriteTwoStructsProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_structs' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoStructs/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_structs_changed(self, handler: ReadWriteTwoStructsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_structs' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_structs_mutex:
            self._changed_value_callbacks_for_read_write_two_structs.append(handler)
            if call_immediately and self._property_read_write_two_structs is not None:
                handler(self._property_read_write_two_structs)
        return handler

    @property
    def read_only_enum(self) -> Optional[interface_types.Numbers]:
        """Property 'read_only_enum' getter."""
        return self._property_read_only_enum

    def read_only_enum_changed(self, handler: ReadOnlyEnumPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_only_enum' property changes.
        Can be used as a decorator.
        """
        with self._property_read_only_enum_mutex:
            self._changed_value_callbacks_for_read_only_enum.append(handler)
            if call_immediately and self._property_read_only_enum is not None:
                handler(self._property_read_only_enum)
        return handler

    @property
    def read_write_enum(self) -> Optional[interface_types.Numbers]:
        """Property 'read_write_enum' getter."""
        return self._property_read_write_enum

    @read_write_enum.setter
    def read_write_enum(self, value: interface_types.Numbers):
        """Serializes and publishes the 'read_write_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError("The 'read_write_enum' property must be a interface_types.Numbers")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_enum' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteEnum/setValue".format(self._service_id), serialized, qos=1)

    def read_write_enum_changed(self, handler: ReadWriteEnumPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_enum' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_enum_mutex:
            self._changed_value_callbacks_for_read_write_enum.append(handler)
            if call_immediately and self._property_read_write_enum is not None:
                handler(self._property_read_write_enum)
        return handler

    @property
    def read_write_optional_enum(self) -> Optional[Optional[interface_types.Numbers]]:
        """Property 'read_write_optional_enum' getter."""
        return self._property_read_write_optional_enum

    @read_write_optional_enum.setter
    def read_write_optional_enum(self, value: Optional[interface_types.Numbers]):
        """Serializes and publishes the 'read_write_optional_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError("The 'read_write_optional_enum' property must be a interface_types.Numbers")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_enum' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalEnum/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_enum_changed(self, handler: ReadWriteOptionalEnumPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_enum' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_enum_mutex:
            self._changed_value_callbacks_for_read_write_optional_enum.append(handler)
            if call_immediately and self._property_read_write_optional_enum is not None:
                handler(self._property_read_write_optional_enum)
        return handler

    @property
    def read_write_two_enums(self) -> Optional[interface_types.ReadWriteTwoEnumsProperty]:
        """Property 'read_write_two_enums' getter."""
        return self._property_read_write_two_enums

    @read_write_two_enums.setter
    def read_write_two_enums(self, value: interface_types.ReadWriteTwoEnumsProperty):
        """Serializes and publishes the 'read_write_two_enums' property."""
        if not isinstance(value, ReadWriteTwoEnumsProperty):
            raise ValueError("The 'read_write_two_enums' property must be a interface_types.ReadWriteTwoEnumsProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_enums' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoEnums/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_enums_changed(self, handler: ReadWriteTwoEnumsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_enums' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_enums_mutex:
            self._changed_value_callbacks_for_read_write_two_enums.append(handler)
            if call_immediately and self._property_read_write_two_enums is not None:
                handler(self._property_read_write_two_enums)
        return handler

    @property
    def read_write_datetime(self) -> Optional[datetime]:
        """Property 'read_write_datetime' getter."""
        return self._property_read_write_datetime

    @read_write_datetime.setter
    def read_write_datetime(self, value: datetime):
        """Serializes and publishes the 'read_write_datetime' property."""
        if not isinstance(value, datetime):
            raise ValueError("The 'read_write_datetime' property must be a datetime.datetime")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_datetime' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteDatetime/setValue".format(self._service_id), serialized, qos=1)

    def read_write_datetime_changed(self, handler: ReadWriteDatetimePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_datetime' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_datetime_mutex:
            self._changed_value_callbacks_for_read_write_datetime.append(handler)
            if call_immediately and self._property_read_write_datetime is not None:
                handler(self._property_read_write_datetime)
        return handler

    @property
    def read_write_optional_datetime(self) -> Optional[Optional[datetime]]:
        """Property 'read_write_optional_datetime' getter."""
        return self._property_read_write_optional_datetime

    @read_write_optional_datetime.setter
    def read_write_optional_datetime(self, value: Optional[datetime]):
        """Serializes and publishes the 'read_write_optional_datetime' property."""
        if not isinstance(value, datetime):
            raise ValueError("The 'read_write_optional_datetime' property must be a datetime.datetime")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_datetime' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalDatetime/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_datetime_changed(self, handler: ReadWriteOptionalDatetimePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_datetime' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_datetime_mutex:
            self._changed_value_callbacks_for_read_write_optional_datetime.append(handler)
            if call_immediately and self._property_read_write_optional_datetime is not None:
                handler(self._property_read_write_optional_datetime)
        return handler

    @property
    def read_write_two_datetimes(self) -> Optional[interface_types.ReadWriteTwoDatetimesProperty]:
        """Property 'read_write_two_datetimes' getter."""
        return self._property_read_write_two_datetimes

    @read_write_two_datetimes.setter
    def read_write_two_datetimes(self, value: interface_types.ReadWriteTwoDatetimesProperty):
        """Serializes and publishes the 'read_write_two_datetimes' property."""
        if not isinstance(value, ReadWriteTwoDatetimesProperty):
            raise ValueError("The 'read_write_two_datetimes' property must be a interface_types.ReadWriteTwoDatetimesProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_datetimes' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoDatetimes/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_datetimes_changed(self, handler: ReadWriteTwoDatetimesPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_datetimes' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_datetimes_mutex:
            self._changed_value_callbacks_for_read_write_two_datetimes.append(handler)
            if call_immediately and self._property_read_write_two_datetimes is not None:
                handler(self._property_read_write_two_datetimes)
        return handler

    @property
    def read_write_duration(self) -> Optional[timedelta]:
        """Property 'read_write_duration' getter."""
        return self._property_read_write_duration

    @read_write_duration.setter
    def read_write_duration(self, value: timedelta):
        """Serializes and publishes the 'read_write_duration' property."""
        if not isinstance(value, timedelta):
            raise ValueError("The 'read_write_duration' property must be a datetime.timedelta")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_duration' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteDuration/setValue".format(self._service_id), serialized, qos=1)

    def read_write_duration_changed(self, handler: ReadWriteDurationPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_duration' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_duration_mutex:
            self._changed_value_callbacks_for_read_write_duration.append(handler)
            if call_immediately and self._property_read_write_duration is not None:
                handler(self._property_read_write_duration)
        return handler

    @property
    def read_write_optional_duration(self) -> Optional[Optional[timedelta]]:
        """Property 'read_write_optional_duration' getter."""
        return self._property_read_write_optional_duration

    @read_write_optional_duration.setter
    def read_write_optional_duration(self, value: Optional[timedelta]):
        """Serializes and publishes the 'read_write_optional_duration' property."""
        if not isinstance(value, timedelta):
            raise ValueError("The 'read_write_optional_duration' property must be a datetime.timedelta")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_duration' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalDuration/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_duration_changed(self, handler: ReadWriteOptionalDurationPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_duration' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_duration_mutex:
            self._changed_value_callbacks_for_read_write_optional_duration.append(handler)
            if call_immediately and self._property_read_write_optional_duration is not None:
                handler(self._property_read_write_optional_duration)
        return handler

    @property
    def read_write_two_durations(self) -> Optional[interface_types.ReadWriteTwoDurationsProperty]:
        """Property 'read_write_two_durations' getter."""
        return self._property_read_write_two_durations

    @read_write_two_durations.setter
    def read_write_two_durations(self, value: interface_types.ReadWriteTwoDurationsProperty):
        """Serializes and publishes the 'read_write_two_durations' property."""
        if not isinstance(value, ReadWriteTwoDurationsProperty):
            raise ValueError("The 'read_write_two_durations' property must be a interface_types.ReadWriteTwoDurationsProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_durations' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoDurations/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_durations_changed(self, handler: ReadWriteTwoDurationsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_durations' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_durations_mutex:
            self._changed_value_callbacks_for_read_write_two_durations.append(handler)
            if call_immediately and self._property_read_write_two_durations is not None:
                handler(self._property_read_write_two_durations)
        return handler

    @property
    def read_write_binary(self) -> Optional[bytes]:
        """Property 'read_write_binary' getter."""
        return self._property_read_write_binary

    @read_write_binary.setter
    def read_write_binary(self, value: bytes):
        """Serializes and publishes the 'read_write_binary' property."""
        if not isinstance(value, bytes):
            raise ValueError("The 'read_write_binary' property must be a bytes")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_binary' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteBinary/setValue".format(self._service_id), serialized, qos=1)

    def read_write_binary_changed(self, handler: ReadWriteBinaryPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_binary' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_binary_mutex:
            self._changed_value_callbacks_for_read_write_binary.append(handler)
            if call_immediately and self._property_read_write_binary is not None:
                handler(self._property_read_write_binary)
        return handler

    @property
    def read_write_optional_binary(self) -> Optional[bytes]:
        """Property 'read_write_optional_binary' getter."""
        return self._property_read_write_optional_binary

    @read_write_optional_binary.setter
    def read_write_optional_binary(self, value: bytes):
        """Serializes and publishes the 'read_write_optional_binary' property."""
        if not isinstance(value, bytes):
            raise ValueError("The 'read_write_optional_binary' property must be a bytes")
        serialized = json.dumps({"value": value.value})
        self._logger.debug("Setting 'read_write_optional_binary' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteOptionalBinary/setValue".format(self._service_id), serialized, qos=1)

    def read_write_optional_binary_changed(self, handler: ReadWriteOptionalBinaryPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_binary' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_binary_mutex:
            self._changed_value_callbacks_for_read_write_optional_binary.append(handler)
            if call_immediately and self._property_read_write_optional_binary is not None:
                handler(self._property_read_write_optional_binary)
        return handler

    @property
    def read_write_two_binaries(self) -> Optional[interface_types.ReadWriteTwoBinariesProperty]:
        """Property 'read_write_two_binaries' getter."""
        return self._property_read_write_two_binaries

    @read_write_two_binaries.setter
    def read_write_two_binaries(self, value: interface_types.ReadWriteTwoBinariesProperty):
        """Serializes and publishes the 'read_write_two_binaries' property."""
        if not isinstance(value, ReadWriteTwoBinariesProperty):
            raise ValueError("The 'read_write_two_binaries' property must be a interface_types.ReadWriteTwoBinariesProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'read_write_two_binaries' property to %s", serialized)
        self._conn.publish("testAble/{}/property/readWriteTwoBinaries/setValue".format(self._service_id), serialized, qos=1)

    def read_write_two_binaries_changed(self, handler: ReadWriteTwoBinariesPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_binaries' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_binaries_mutex:
            self._changed_value_callbacks_for_read_write_two_binaries.append(handler)
            if call_immediately and self._property_read_write_two_binaries is not None:
                handler(self._property_read_write_two_binaries)
        return handler

    def _do_callbacks_for(self, callbacks: List[Callable[..., None]], **kwargs):
        """Call each callback in the callback dictionary with the provided args."""
        for cb in callbacks:
            cb(**kwargs)

    @staticmethod
    def _filter_for_args(args: Dict[str, Any], allowed_args: List[str]) -> Dict[str, Any]:
        """Given a dictionary, reduce the dictionary so that it only has keys in the allowed list."""
        filtered_args = {}
        for k, v in args.items():
            if k in allowed_args:
                filtered_args[k] = v
        return filtered_args

    def _receive_empty_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'empty' signal with non-JSON content type")
            return

        model = EmptySignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_empty, **kwargs)

    def _receive_single_int_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleInt' signal with non-JSON content type")
            return

        model = SingleIntSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_int, **kwargs)

    def _receive_single_optional_int_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalInt' signal with non-JSON content type")
            return

        model = SingleOptionalIntSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_int, **kwargs)

    def _receive_three_integers_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeIntegers' signal with non-JSON content type")
            return

        model = ThreeIntegersSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_integers, **kwargs)

    def _receive_single_string_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleString' signal with non-JSON content type")
            return

        model = SingleStringSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_string, **kwargs)

    def _receive_single_optional_string_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalString' signal with non-JSON content type")
            return

        model = SingleOptionalStringSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_string, **kwargs)

    def _receive_three_strings_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeStrings' signal with non-JSON content type")
            return

        model = ThreeStringsSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_strings, **kwargs)

    def _receive_single_enum_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleEnum' signal with non-JSON content type")
            return

        model = SingleEnumSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_enum, **kwargs)

    def _receive_single_optional_enum_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalEnum' signal with non-JSON content type")
            return

        model = SingleOptionalEnumSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_enum, **kwargs)

    def _receive_three_enums_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeEnums' signal with non-JSON content type")
            return

        model = ThreeEnumsSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_enums, **kwargs)

    def _receive_single_struct_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleStruct' signal with non-JSON content type")
            return

        model = SingleStructSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_struct, **kwargs)

    def _receive_single_optional_struct_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalStruct' signal with non-JSON content type")
            return

        model = SingleOptionalStructSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_struct, **kwargs)

    def _receive_three_structs_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeStructs' signal with non-JSON content type")
            return

        model = ThreeStructsSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_structs, **kwargs)

    def _receive_single_date_time_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleDateTime' signal with non-JSON content type")
            return

        model = SingleDateTimeSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_date_time, **kwargs)

    def _receive_single_optional_datetime_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalDatetime' signal with non-JSON content type")
            return

        model = SingleOptionalDatetimeSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_datetime, **kwargs)

    def _receive_three_date_times_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeDateTimes' signal with non-JSON content type")
            return

        model = ThreeDateTimesSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_date_times, **kwargs)

    def _receive_single_duration_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleDuration' signal with non-JSON content type")
            return

        model = SingleDurationSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_duration, **kwargs)

    def _receive_single_optional_duration_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalDuration' signal with non-JSON content type")
            return

        model = SingleOptionalDurationSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_duration, **kwargs)

    def _receive_three_durations_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeDurations' signal with non-JSON content type")
            return

        model = ThreeDurationsSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_durations, **kwargs)

    def _receive_single_binary_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleBinary' signal with non-JSON content type")
            return

        model = SingleBinarySignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_binary, **kwargs)

    def _receive_single_optional_binary_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'singleOptionalBinary' signal with non-JSON content type")
            return

        model = SingleOptionalBinarySignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_binary, **kwargs)

    def _receive_three_binaries_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'threeBinaries' signal with non-JSON content type")
            return

        model = ThreeBinariesSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_binaries, **kwargs)

    def _receive_call_with_nothing_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callWithNothing' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_integer_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneInteger' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_integer_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalInteger' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_integers_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeIntegers' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_string_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneString' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_string_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalString' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_strings_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeStrings' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_enum_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneEnum' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_enum_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalEnum' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_enums_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeEnums' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_struct_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneStruct' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_struct_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalStruct' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_structs_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeStructs' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_date_time_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneDateTime' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_date_time_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalDateTime' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_date_times_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeDateTimes' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_duration_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneDuration' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_duration_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalDuration' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_durations_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeDurations' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_one_binary_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOneBinary' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_optional_binary_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callOptionalBinary' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_call_three_binaries_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'callThreeBinaries' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_read_write_integer_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_integer' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_integer' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteIntegerProperty.model_validate_json(payload)
            with self._property_read_write_integer_mutex:
                self._property_read_write_integer = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_integer_version:
                        self._property_read_write_integer_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_integer, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_integer' property change: %s", exc_info=e)

    def _receive_read_only_integer_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_only_integer' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_only_integer' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadOnlyIntegerProperty.model_validate_json(payload)
            with self._property_read_only_integer_mutex:
                self._property_read_only_integer = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_only_integer_version:
                        self._property_read_only_integer_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_only_integer, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_only_integer' property change: %s", exc_info=e)

    def _receive_read_write_optional_integer_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_integer' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_integer' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalIntegerProperty.model_validate_json(payload)
            with self._property_read_write_optional_integer_mutex:
                self._property_read_write_optional_integer = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_integer_version:
                        self._property_read_write_optional_integer_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_integer, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_integer' property change: %s", exc_info=e)

    def _receive_read_write_two_integers_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_integers' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_integers' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoIntegersProperty.model_validate_json(payload)
            with self._property_read_write_two_integers_mutex:
                self._property_read_write_two_integers = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_integers_version:
                        self._property_read_write_two_integers_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_integers, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_integers' property change: %s", exc_info=e)

    def _receive_read_only_string_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_only_string' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_only_string' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadOnlyStringProperty.model_validate_json(payload)
            with self._property_read_only_string_mutex:
                self._property_read_only_string = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_only_string_version:
                        self._property_read_only_string_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_only_string, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_only_string' property change: %s", exc_info=e)

    def _receive_read_write_string_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_string' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_string' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteStringProperty.model_validate_json(payload)
            with self._property_read_write_string_mutex:
                self._property_read_write_string = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_string_version:
                        self._property_read_write_string_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_string, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_string' property change: %s", exc_info=e)

    def _receive_read_write_optional_string_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_string' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_string' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalStringProperty.model_validate_json(payload)
            with self._property_read_write_optional_string_mutex:
                self._property_read_write_optional_string = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_string_version:
                        self._property_read_write_optional_string_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_string, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_string' property change: %s", exc_info=e)

    def _receive_read_write_two_strings_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_strings' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_strings' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoStringsProperty.model_validate_json(payload)
            with self._property_read_write_two_strings_mutex:
                self._property_read_write_two_strings = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_strings_version:
                        self._property_read_write_two_strings_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_strings, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_strings' property change: %s", exc_info=e)

    def _receive_read_write_struct_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_struct' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_struct' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteStructProperty.model_validate_json(payload)
            with self._property_read_write_struct_mutex:
                self._property_read_write_struct = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_struct_version:
                        self._property_read_write_struct_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_struct, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_struct' property change: %s", exc_info=e)

    def _receive_read_write_optional_struct_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_struct' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_struct' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalStructProperty.model_validate_json(payload)
            with self._property_read_write_optional_struct_mutex:
                self._property_read_write_optional_struct = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_struct_version:
                        self._property_read_write_optional_struct_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_struct, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_struct' property change: %s", exc_info=e)

    def _receive_read_write_two_structs_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_structs' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_structs' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoStructsProperty.model_validate_json(payload)
            with self._property_read_write_two_structs_mutex:
                self._property_read_write_two_structs = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_structs_version:
                        self._property_read_write_two_structs_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_structs, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_structs' property change: %s", exc_info=e)

    def _receive_read_only_enum_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_only_enum' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_only_enum' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadOnlyEnumProperty.model_validate_json(payload)
            with self._property_read_only_enum_mutex:
                self._property_read_only_enum = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_only_enum_version:
                        self._property_read_only_enum_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_only_enum, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_only_enum' property change: %s", exc_info=e)

    def _receive_read_write_enum_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_enum' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_enum' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteEnumProperty.model_validate_json(payload)
            with self._property_read_write_enum_mutex:
                self._property_read_write_enum = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_enum_version:
                        self._property_read_write_enum_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_enum, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_enum' property change: %s", exc_info=e)

    def _receive_read_write_optional_enum_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_enum' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_enum' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalEnumProperty.model_validate_json(payload)
            with self._property_read_write_optional_enum_mutex:
                self._property_read_write_optional_enum = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_enum_version:
                        self._property_read_write_optional_enum_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_enum, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_enum' property change: %s", exc_info=e)

    def _receive_read_write_two_enums_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_enums' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_enums' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoEnumsProperty.model_validate_json(payload)
            with self._property_read_write_two_enums_mutex:
                self._property_read_write_two_enums = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_enums_version:
                        self._property_read_write_two_enums_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_enums, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_enums' property change: %s", exc_info=e)

    def _receive_read_write_datetime_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_datetime' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_datetime' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteDatetimeProperty.model_validate_json(payload)
            with self._property_read_write_datetime_mutex:
                self._property_read_write_datetime = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_datetime_version:
                        self._property_read_write_datetime_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_datetime, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_datetime' property change: %s", exc_info=e)

    def _receive_read_write_optional_datetime_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_datetime' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_datetime' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalDatetimeProperty.model_validate_json(payload)
            with self._property_read_write_optional_datetime_mutex:
                self._property_read_write_optional_datetime = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_datetime_version:
                        self._property_read_write_optional_datetime_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_datetime, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_datetime' property change: %s", exc_info=e)

    def _receive_read_write_two_datetimes_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_datetimes' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_datetimes' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoDatetimesProperty.model_validate_json(payload)
            with self._property_read_write_two_datetimes_mutex:
                self._property_read_write_two_datetimes = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_datetimes_version:
                        self._property_read_write_two_datetimes_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_datetimes, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_datetimes' property change: %s", exc_info=e)

    def _receive_read_write_duration_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_duration' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_duration' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteDurationProperty.model_validate_json(payload)
            with self._property_read_write_duration_mutex:
                self._property_read_write_duration = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_duration_version:
                        self._property_read_write_duration_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_duration, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_duration' property change: %s", exc_info=e)

    def _receive_read_write_optional_duration_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_duration' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_duration' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalDurationProperty.model_validate_json(payload)
            with self._property_read_write_optional_duration_mutex:
                self._property_read_write_optional_duration = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_duration_version:
                        self._property_read_write_optional_duration_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_duration, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_duration' property change: %s", exc_info=e)

    def _receive_read_write_two_durations_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_durations' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_durations' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoDurationsProperty.model_validate_json(payload)
            with self._property_read_write_two_durations_mutex:
                self._property_read_write_two_durations = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_durations_version:
                        self._property_read_write_two_durations_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_durations, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_durations' property change: %s", exc_info=e)

    def _receive_read_write_binary_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_binary' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_binary' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteBinaryProperty.model_validate_json(payload)
            with self._property_read_write_binary_mutex:
                self._property_read_write_binary = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_binary_version:
                        self._property_read_write_binary_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_binary, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_binary' property change: %s", exc_info=e)

    def _receive_read_write_optional_binary_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_optional_binary' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_optional_binary' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalBinaryProperty.model_validate_json(payload)
            with self._property_read_write_optional_binary_mutex:
                self._property_read_write_optional_binary = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_optional_binary_version:
                        self._property_read_write_optional_binary_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_binary, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_binary' property change: %s", exc_info=e)

    def _receive_read_write_two_binaries_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'read_write_two_binaries' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'read_write_two_binaries' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoBinariesProperty.model_validate_json(payload)
            with self._property_read_write_two_binaries_mutex:
                self._property_read_write_two_binaries = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_read_write_two_binaries_version:
                        self._property_read_write_two_binaries_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_binaries, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_binaries' property change: %s", exc_info=e)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.warning("Receiving message sent to %s, but without a handler", topic)

    def receive_empty(self, handler: EmptySignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_empty.append(handler)
        if len(self._signal_recv_callbacks_for_empty) == 1:
            self._conn.subscribe("testAble/{}/signal/empty".format(self._service_id), self._receive_empty_signal_message)
        return handler

    def receive_single_int(self, handler: SingleIntSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_int.append(handler)
        if len(self._signal_recv_callbacks_for_single_int) == 1:
            self._conn.subscribe("testAble/{}/signal/singleInt".format(self._service_id), self._receive_single_int_signal_message)
        return handler

    def receive_single_optional_int(self, handler: SingleOptionalIntSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_int.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_int) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalInt".format(self._service_id), self._receive_single_optional_int_signal_message)
        return handler

    def receive_three_integers(self, handler: ThreeIntegersSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_integers.append(handler)
        if len(self._signal_recv_callbacks_for_three_integers) == 1:
            self._conn.subscribe("testAble/{}/signal/threeIntegers".format(self._service_id), self._receive_three_integers_signal_message)
        return handler

    def receive_single_string(self, handler: SingleStringSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_string.append(handler)
        if len(self._signal_recv_callbacks_for_single_string) == 1:
            self._conn.subscribe("testAble/{}/signal/singleString".format(self._service_id), self._receive_single_string_signal_message)
        return handler

    def receive_single_optional_string(self, handler: SingleOptionalStringSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_string.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_string) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalString".format(self._service_id), self._receive_single_optional_string_signal_message)
        return handler

    def receive_three_strings(self, handler: ThreeStringsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_strings.append(handler)
        if len(self._signal_recv_callbacks_for_three_strings) == 1:
            self._conn.subscribe("testAble/{}/signal/threeStrings".format(self._service_id), self._receive_three_strings_signal_message)
        return handler

    def receive_single_enum(self, handler: SingleEnumSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_enum.append(handler)
        if len(self._signal_recv_callbacks_for_single_enum) == 1:
            self._conn.subscribe("testAble/{}/signal/singleEnum".format(self._service_id), self._receive_single_enum_signal_message)
        return handler

    def receive_single_optional_enum(self, handler: SingleOptionalEnumSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_enum.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_enum) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalEnum".format(self._service_id), self._receive_single_optional_enum_signal_message)
        return handler

    def receive_three_enums(self, handler: ThreeEnumsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_enums.append(handler)
        if len(self._signal_recv_callbacks_for_three_enums) == 1:
            self._conn.subscribe("testAble/{}/signal/threeEnums".format(self._service_id), self._receive_three_enums_signal_message)
        return handler

    def receive_single_struct(self, handler: SingleStructSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_struct.append(handler)
        if len(self._signal_recv_callbacks_for_single_struct) == 1:
            self._conn.subscribe("testAble/{}/signal/singleStruct".format(self._service_id), self._receive_single_struct_signal_message)
        return handler

    def receive_single_optional_struct(self, handler: SingleOptionalStructSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_struct.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_struct) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalStruct".format(self._service_id), self._receive_single_optional_struct_signal_message)
        return handler

    def receive_three_structs(self, handler: ThreeStructsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_structs.append(handler)
        if len(self._signal_recv_callbacks_for_three_structs) == 1:
            self._conn.subscribe("testAble/{}/signal/threeStructs".format(self._service_id), self._receive_three_structs_signal_message)
        return handler

    def receive_single_date_time(self, handler: SingleDateTimeSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_date_time.append(handler)
        if len(self._signal_recv_callbacks_for_single_date_time) == 1:
            self._conn.subscribe("testAble/{}/signal/singleDateTime".format(self._service_id), self._receive_single_date_time_signal_message)
        return handler

    def receive_single_optional_datetime(self, handler: SingleOptionalDatetimeSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_datetime.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_datetime) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalDatetime".format(self._service_id), self._receive_single_optional_datetime_signal_message)
        return handler

    def receive_three_date_times(self, handler: ThreeDateTimesSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_date_times.append(handler)
        if len(self._signal_recv_callbacks_for_three_date_times) == 1:
            self._conn.subscribe("testAble/{}/signal/threeDateTimes".format(self._service_id), self._receive_three_date_times_signal_message)
        return handler

    def receive_single_duration(self, handler: SingleDurationSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_duration.append(handler)
        if len(self._signal_recv_callbacks_for_single_duration) == 1:
            self._conn.subscribe("testAble/{}/signal/singleDuration".format(self._service_id), self._receive_single_duration_signal_message)
        return handler

    def receive_single_optional_duration(self, handler: SingleOptionalDurationSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_duration.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_duration) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalDuration".format(self._service_id), self._receive_single_optional_duration_signal_message)
        return handler

    def receive_three_durations(self, handler: ThreeDurationsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_durations.append(handler)
        if len(self._signal_recv_callbacks_for_three_durations) == 1:
            self._conn.subscribe("testAble/{}/signal/threeDurations".format(self._service_id), self._receive_three_durations_signal_message)
        return handler

    def receive_single_binary(self, handler: SingleBinarySignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_binary.append(handler)
        if len(self._signal_recv_callbacks_for_single_binary) == 1:
            self._conn.subscribe("testAble/{}/signal/singleBinary".format(self._service_id), self._receive_single_binary_signal_message)
        return handler

    def receive_single_optional_binary(self, handler: SingleOptionalBinarySignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_binary.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_binary) == 1:
            self._conn.subscribe("testAble/{}/signal/singleOptionalBinary".format(self._service_id), self._receive_single_optional_binary_signal_message)
        return handler

    def receive_three_binaries(self, handler: ThreeBinariesSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_binaries.append(handler)
        if len(self._signal_recv_callbacks_for_three_binaries) == 1:
            self._conn.subscribe("testAble/{}/signal/threeBinaries".format(self._service_id), self._receive_three_binaries_signal_message)
        return handler

    def call_with_nothing(
        self,
    ) -> futures.Future:
        """Calling this initiates a `callWithNothing` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_with_nothing_response, fut)
        payload = CallWithNothingMethodRequest()
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callWithNothing' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callWithNothing".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callWithNothing/response",
        )
        return fut

    def _handle_call_with_nothing_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callWithNothing` IPC method call."""
        self._logger.debug("Handling call_with_nothing response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callWithNothing' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallWithNothingMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callWithNothing' method: {e}"))

        if not fut.done():
            fut.set_result(None)
            return
        else:
            self._logger.warning("Future for 'callWithNothing' method was already done!")

    def call_one_integer(self, input1: int) -> futures.Future:
        """Calling this initiates a `callOneInteger` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_integer_response, fut)
        payload = CallOneIntegerMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneInteger' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneInteger".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneInteger/response",
        )
        return fut

    def _handle_call_one_integer_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneInteger` IPC method call."""
        self._logger.debug("Handling call_one_integer response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneInteger' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneIntegerMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneInteger' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneInteger' method was already done!")

    def call_optional_integer(self, input1: Optional[int]) -> futures.Future:
        """Calling this initiates a `callOptionalInteger` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_integer_response, fut)
        payload = CallOptionalIntegerMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalInteger' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalInteger".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalInteger/response",
        )
        return fut

    def _handle_call_optional_integer_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalInteger` IPC method call."""
        self._logger.debug("Handling call_optional_integer response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalInteger' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalIntegerMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalInteger' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalInteger' method was already done!")

    def call_three_integers(self, input1: int, input2: int, input3: Optional[int]) -> futures.Future:
        """Calling this initiates a `callThreeIntegers` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_integers_response, fut)
        payload = CallThreeIntegersMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeIntegers' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeIntegers".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeIntegers/response",
        )
        return fut

    def _handle_call_three_integers_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeIntegers` IPC method call."""
        self._logger.debug("Handling call_three_integers response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeIntegers' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeIntegersMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeIntegers' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeIntegers' method was already done!")

    def call_one_string(self, input1: str) -> futures.Future:
        """Calling this initiates a `callOneString` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_string_response, fut)
        payload = CallOneStringMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneString' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneString".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneString/response",
        )
        return fut

    def _handle_call_one_string_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneString` IPC method call."""
        self._logger.debug("Handling call_one_string response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneString' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneStringMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneString' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneString' method was already done!")

    def call_optional_string(self, input1: Optional[str]) -> futures.Future:
        """Calling this initiates a `callOptionalString` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_string_response, fut)
        payload = CallOptionalStringMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalString' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalString".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalString/response",
        )
        return fut

    def _handle_call_optional_string_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalString` IPC method call."""
        self._logger.debug("Handling call_optional_string response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalString' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalStringMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalString' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalString' method was already done!")

    def call_three_strings(self, input1: str, input2: Optional[str], input3: str) -> futures.Future:
        """Calling this initiates a `callThreeStrings` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_strings_response, fut)
        payload = CallThreeStringsMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeStrings' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeStrings".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeStrings/response",
        )
        return fut

    def _handle_call_three_strings_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeStrings` IPC method call."""
        self._logger.debug("Handling call_three_strings response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeStrings' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeStringsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeStrings' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeStrings' method was already done!")

    def call_one_enum(self, input1: interface_types.Numbers) -> futures.Future:
        """Calling this initiates a `callOneEnum` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_enum_response, fut)
        payload = CallOneEnumMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneEnum' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneEnum".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneEnum/response",
        )
        return fut

    def _handle_call_one_enum_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneEnum` IPC method call."""
        self._logger.debug("Handling call_one_enum response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneEnum' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneEnumMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneEnum' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneEnum' method was already done!")

    def call_optional_enum(self, input1: Optional[interface_types.Numbers]) -> futures.Future:
        """Calling this initiates a `callOptionalEnum` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_enum_response, fut)
        payload = CallOptionalEnumMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalEnum' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalEnum".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalEnum/response",
        )
        return fut

    def _handle_call_optional_enum_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalEnum` IPC method call."""
        self._logger.debug("Handling call_optional_enum response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalEnum' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalEnumMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalEnum' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalEnum' method was already done!")

    def call_three_enums(self, input1: interface_types.Numbers, input2: interface_types.Numbers, input3: Optional[interface_types.Numbers]) -> futures.Future:
        """Calling this initiates a `callThreeEnums` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_enums_response, fut)
        payload = CallThreeEnumsMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeEnums' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeEnums".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeEnums/response",
        )
        return fut

    def _handle_call_three_enums_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeEnums` IPC method call."""
        self._logger.debug("Handling call_three_enums response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeEnums' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeEnumsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeEnums' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeEnums' method was already done!")

    def call_one_struct(self, input1: interface_types.AllTypes) -> futures.Future:
        """Calling this initiates a `callOneStruct` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_struct_response, fut)
        payload = CallOneStructMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneStruct' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneStruct".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneStruct/response",
        )
        return fut

    def _handle_call_one_struct_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneStruct` IPC method call."""
        self._logger.debug("Handling call_one_struct response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneStruct' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneStructMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneStruct' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneStruct' method was already done!")

    def call_optional_struct(self, input1: interface_types.AllTypes) -> futures.Future:
        """Calling this initiates a `callOptionalStruct` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_struct_response, fut)
        payload = CallOptionalStructMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalStruct' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalStruct".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalStruct/response",
        )
        return fut

    def _handle_call_optional_struct_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalStruct` IPC method call."""
        self._logger.debug("Handling call_optional_struct response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalStruct' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalStructMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalStruct' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalStruct' method was already done!")

    def call_three_structs(self, input1: interface_types.AllTypes, input2: interface_types.AllTypes, input3: interface_types.AllTypes) -> futures.Future:
        """Calling this initiates a `callThreeStructs` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_structs_response, fut)
        payload = CallThreeStructsMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeStructs' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeStructs".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeStructs/response",
        )
        return fut

    def _handle_call_three_structs_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeStructs` IPC method call."""
        self._logger.debug("Handling call_three_structs response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeStructs' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeStructsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeStructs' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeStructs' method was already done!")

    def call_one_date_time(self, input1: datetime) -> futures.Future:
        """Calling this initiates a `callOneDateTime` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_date_time_response, fut)
        payload = CallOneDateTimeMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneDateTime' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneDateTime".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneDateTime/response",
        )
        return fut

    def _handle_call_one_date_time_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneDateTime` IPC method call."""
        self._logger.debug("Handling call_one_date_time response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneDateTime' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneDateTimeMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneDateTime' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneDateTime' method was already done!")

    def call_optional_date_time(self, input1: Optional[datetime]) -> futures.Future:
        """Calling this initiates a `callOptionalDateTime` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_date_time_response, fut)
        payload = CallOptionalDateTimeMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalDateTime' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalDateTime".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalDateTime/response",
        )
        return fut

    def _handle_call_optional_date_time_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalDateTime` IPC method call."""
        self._logger.debug("Handling call_optional_date_time response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalDateTime' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalDateTimeMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalDateTime' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalDateTime' method was already done!")

    def call_three_date_times(self, input1: datetime, input2: datetime, input3: Optional[datetime]) -> futures.Future:
        """Calling this initiates a `callThreeDateTimes` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_date_times_response, fut)
        payload = CallThreeDateTimesMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeDateTimes' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeDateTimes".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeDateTimes/response",
        )
        return fut

    def _handle_call_three_date_times_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeDateTimes` IPC method call."""
        self._logger.debug("Handling call_three_date_times response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeDateTimes' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeDateTimesMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeDateTimes' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeDateTimes' method was already done!")

    def call_one_duration(self, input1: timedelta) -> futures.Future:
        """Calling this initiates a `callOneDuration` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_duration_response, fut)
        payload = CallOneDurationMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneDuration' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneDuration".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneDuration/response",
        )
        return fut

    def _handle_call_one_duration_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneDuration` IPC method call."""
        self._logger.debug("Handling call_one_duration response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneDuration' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneDurationMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneDuration' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneDuration' method was already done!")

    def call_optional_duration(self, input1: Optional[timedelta]) -> futures.Future:
        """Calling this initiates a `callOptionalDuration` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_duration_response, fut)
        payload = CallOptionalDurationMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalDuration' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalDuration".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalDuration/response",
        )
        return fut

    def _handle_call_optional_duration_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalDuration` IPC method call."""
        self._logger.debug("Handling call_optional_duration response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalDuration' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalDurationMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalDuration' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalDuration' method was already done!")

    def call_three_durations(self, input1: timedelta, input2: timedelta, input3: Optional[timedelta]) -> futures.Future:
        """Calling this initiates a `callThreeDurations` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_durations_response, fut)
        payload = CallThreeDurationsMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeDurations' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeDurations".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeDurations/response",
        )
        return fut

    def _handle_call_three_durations_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeDurations` IPC method call."""
        self._logger.debug("Handling call_three_durations response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeDurations' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeDurationsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeDurations' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeDurations' method was already done!")

    def call_one_binary(self, input1: bytes) -> futures.Future:
        """Calling this initiates a `callOneBinary` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_binary_response, fut)
        payload = CallOneBinaryMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOneBinary' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOneBinary".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOneBinary/response",
        )
        return fut

    def _handle_call_one_binary_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneBinary` IPC method call."""
        self._logger.debug("Handling call_one_binary response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneBinary' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneBinaryMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneBinary' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneBinary' method was already done!")

    def call_optional_binary(self, input1: bytes) -> futures.Future:
        """Calling this initiates a `callOptionalBinary` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_binary_response, fut)
        payload = CallOptionalBinaryMethodRequest(
            input1=input1,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callOptionalBinary' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callOptionalBinary".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callOptionalBinary/response",
        )
        return fut

    def _handle_call_optional_binary_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalBinary` IPC method call."""
        self._logger.debug("Handling call_optional_binary response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalBinary' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalBinaryMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalBinary' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalBinary' method was already done!")

    def call_three_binaries(self, input1: bytes, input2: bytes, input3: bytes) -> futures.Future:
        """Calling this initiates a `callThreeBinaries` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_binaries_response, fut)
        payload = CallThreeBinariesMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'callThreeBinaries' method with payload %s", json_payload)
        self._conn.publish(
            "testAble/{}/method/callThreeBinaries".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/callThreeBinaries/response",
        )
        return fut

    def _handle_call_three_binaries_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callThreeBinaries` IPC method call."""
        self._logger.debug("Handling call_three_binaries response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callThreeBinaries' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallThreeBinariesMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callThreeBinaries' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callThreeBinaries' method was already done!")


class TestAbleClientBuilder:
    """Using decorators from TestAbleClient doesn't work if you are trying to create multiple instances of TestAbleClient.
    Instead, use this builder to create a registry of callbacks, and then build clients using the registry.

    When ready to create a TestAbleClient instance, call the `build(broker, service_instance_id)` method.
    """

    def __init__(self):
        """Creates a new TestAbleClientBuilder."""
        self._logger = logging.getLogger("TestAbleClientBuilder")
        self._signal_recv_callbacks_for_empty = []  # type: List[EmptySignalCallbackType]
        self._signal_recv_callbacks_for_single_int = []  # type: List[SingleIntSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_int = []  # type: List[SingleOptionalIntSignalCallbackType]
        self._signal_recv_callbacks_for_three_integers = []  # type: List[ThreeIntegersSignalCallbackType]
        self._signal_recv_callbacks_for_single_string = []  # type: List[SingleStringSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_string = []  # type: List[SingleOptionalStringSignalCallbackType]
        self._signal_recv_callbacks_for_three_strings = []  # type: List[ThreeStringsSignalCallbackType]
        self._signal_recv_callbacks_for_single_enum = []  # type: List[SingleEnumSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_enum = []  # type: List[SingleOptionalEnumSignalCallbackType]
        self._signal_recv_callbacks_for_three_enums = []  # type: List[ThreeEnumsSignalCallbackType]
        self._signal_recv_callbacks_for_single_struct = []  # type: List[SingleStructSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_struct = []  # type: List[SingleOptionalStructSignalCallbackType]
        self._signal_recv_callbacks_for_three_structs = []  # type: List[ThreeStructsSignalCallbackType]
        self._signal_recv_callbacks_for_single_date_time = []  # type: List[SingleDateTimeSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_datetime = []  # type: List[SingleOptionalDatetimeSignalCallbackType]
        self._signal_recv_callbacks_for_three_date_times = []  # type: List[ThreeDateTimesSignalCallbackType]
        self._signal_recv_callbacks_for_single_duration = []  # type: List[SingleDurationSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_duration = []  # type: List[SingleOptionalDurationSignalCallbackType]
        self._signal_recv_callbacks_for_three_durations = []  # type: List[ThreeDurationsSignalCallbackType]
        self._signal_recv_callbacks_for_single_binary = []  # type: List[SingleBinarySignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_binary = []  # type: List[SingleOptionalBinarySignalCallbackType]
        self._signal_recv_callbacks_for_three_binaries = []  # type: List[ThreeBinariesSignalCallbackType]
        self._property_updated_callbacks_for_read_write_integer: list[ReadWriteIntegerPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_only_integer: list[ReadOnlyIntegerPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_integer: list[ReadWriteOptionalIntegerPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_integers: list[ReadWriteTwoIntegersPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_only_string: list[ReadOnlyStringPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_string: list[ReadWriteStringPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_string: list[ReadWriteOptionalStringPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_strings: list[ReadWriteTwoStringsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_struct: list[ReadWriteStructPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_struct: list[ReadWriteOptionalStructPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_structs: list[ReadWriteTwoStructsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_only_enum: list[ReadOnlyEnumPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_enum: list[ReadWriteEnumPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_enum: list[ReadWriteOptionalEnumPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_enums: list[ReadWriteTwoEnumsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_datetime: list[ReadWriteDatetimePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_datetime: list[ReadWriteOptionalDatetimePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_datetimes: list[ReadWriteTwoDatetimesPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_duration: list[ReadWriteDurationPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_duration: list[ReadWriteOptionalDurationPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_durations: list[ReadWriteTwoDurationsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_binary: list[ReadWriteBinaryPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_binary: list[ReadWriteOptionalBinaryPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_binaries: list[ReadWriteTwoBinariesPropertyUpdatedCallbackType] = []

    def receive_empty(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_empty.append(handler)

    def receive_single_int(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_int.append(handler)

    def receive_single_optional_int(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_int.append(handler)

    def receive_three_integers(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_integers.append(handler)

    def receive_single_string(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_string.append(handler)

    def receive_single_optional_string(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_string.append(handler)

    def receive_three_strings(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_strings.append(handler)

    def receive_single_enum(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_enum.append(handler)

    def receive_single_optional_enum(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_enum.append(handler)

    def receive_three_enums(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_enums.append(handler)

    def receive_single_struct(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_struct.append(handler)

    def receive_single_optional_struct(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_struct.append(handler)

    def receive_three_structs(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_structs.append(handler)

    def receive_single_date_time(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_date_time.append(handler)

    def receive_single_optional_datetime(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_datetime.append(handler)

    def receive_three_date_times(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_date_times.append(handler)

    def receive_single_duration(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_duration.append(handler)

    def receive_single_optional_duration(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_duration.append(handler)

    def receive_three_durations(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_durations.append(handler)

    def receive_single_binary(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_binary.append(handler)

    def receive_single_optional_binary(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_binary.append(handler)

    def receive_three_binaries(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_binaries.append(handler)

    def read_write_integer_updated(self, handler: ReadWriteIntegerPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_integer.append(handler)

    def read_only_integer_updated(self, handler: ReadOnlyIntegerPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_only_integer.append(handler)

    def read_write_optional_integer_updated(self, handler: ReadWriteOptionalIntegerPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_integer.append(handler)

    def read_write_two_integers_updated(self, handler: ReadWriteTwoIntegersPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_integers.append(handler)

    def read_only_string_updated(self, handler: ReadOnlyStringPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_only_string.append(handler)

    def read_write_string_updated(self, handler: ReadWriteStringPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_string.append(handler)

    def read_write_optional_string_updated(self, handler: ReadWriteOptionalStringPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_string.append(handler)

    def read_write_two_strings_updated(self, handler: ReadWriteTwoStringsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_strings.append(handler)

    def read_write_struct_updated(self, handler: ReadWriteStructPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_struct.append(handler)

    def read_write_optional_struct_updated(self, handler: ReadWriteOptionalStructPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_struct.append(handler)

    def read_write_two_structs_updated(self, handler: ReadWriteTwoStructsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_structs.append(handler)

    def read_only_enum_updated(self, handler: ReadOnlyEnumPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_only_enum.append(handler)

    def read_write_enum_updated(self, handler: ReadWriteEnumPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_enum.append(handler)

    def read_write_optional_enum_updated(self, handler: ReadWriteOptionalEnumPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_enum.append(handler)

    def read_write_two_enums_updated(self, handler: ReadWriteTwoEnumsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_enums.append(handler)

    def read_write_datetime_updated(self, handler: ReadWriteDatetimePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_datetime.append(handler)

    def read_write_optional_datetime_updated(self, handler: ReadWriteOptionalDatetimePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_datetime.append(handler)

    def read_write_two_datetimes_updated(self, handler: ReadWriteTwoDatetimesPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_datetimes.append(handler)

    def read_write_duration_updated(self, handler: ReadWriteDurationPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_duration.append(handler)

    def read_write_optional_duration_updated(self, handler: ReadWriteOptionalDurationPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_duration.append(handler)

    def read_write_two_durations_updated(self, handler: ReadWriteTwoDurationsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_durations.append(handler)

    def read_write_binary_updated(self, handler: ReadWriteBinaryPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_binary.append(handler)

    def read_write_optional_binary_updated(self, handler: ReadWriteOptionalBinaryPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_optional_binary.append(handler)

    def read_write_two_binaries_updated(self, handler: ReadWriteTwoBinariesPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_read_write_two_binaries.append(handler)

    def build(self, broker: IBrokerConnection, service_instance_id: str) -> TestAbleClient:
        """Builds a new TestAbleClient."""
        self._logger.debug("Building TestAbleClient for service instance %s", service_instance_id)
        client = TestAbleClient(broker, service_instance_id)

        for cb in self._signal_recv_callbacks_for_empty:
            client.receive_empty(cb)

        for cb in self._signal_recv_callbacks_for_single_int:
            client.receive_single_int(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_int:
            client.receive_single_optional_int(cb)

        for cb in self._signal_recv_callbacks_for_three_integers:
            client.receive_three_integers(cb)

        for cb in self._signal_recv_callbacks_for_single_string:
            client.receive_single_string(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_string:
            client.receive_single_optional_string(cb)

        for cb in self._signal_recv_callbacks_for_three_strings:
            client.receive_three_strings(cb)

        for cb in self._signal_recv_callbacks_for_single_enum:
            client.receive_single_enum(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_enum:
            client.receive_single_optional_enum(cb)

        for cb in self._signal_recv_callbacks_for_three_enums:
            client.receive_three_enums(cb)

        for cb in self._signal_recv_callbacks_for_single_struct:
            client.receive_single_struct(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_struct:
            client.receive_single_optional_struct(cb)

        for cb in self._signal_recv_callbacks_for_three_structs:
            client.receive_three_structs(cb)

        for cb in self._signal_recv_callbacks_for_single_date_time:
            client.receive_single_date_time(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_datetime:
            client.receive_single_optional_datetime(cb)

        for cb in self._signal_recv_callbacks_for_three_date_times:
            client.receive_three_date_times(cb)

        for cb in self._signal_recv_callbacks_for_single_duration:
            client.receive_single_duration(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_duration:
            client.receive_single_optional_duration(cb)

        for cb in self._signal_recv_callbacks_for_three_durations:
            client.receive_three_durations(cb)

        for cb in self._signal_recv_callbacks_for_single_binary:
            client.receive_single_binary(cb)

        for cb in self._signal_recv_callbacks_for_single_optional_binary:
            client.receive_single_optional_binary(cb)

        for cb in self._signal_recv_callbacks_for_three_binaries:
            client.receive_three_binaries(cb)

        for cb in self._property_updated_callbacks_for_read_write_integer:
            client.read_write_integer_changed(cb)

        for cb in self._property_updated_callbacks_for_read_only_integer:
            client.read_only_integer_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_integer:
            client.read_write_optional_integer_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_integers:
            client.read_write_two_integers_changed(cb)

        for cb in self._property_updated_callbacks_for_read_only_string:
            client.read_only_string_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_string:
            client.read_write_string_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_string:
            client.read_write_optional_string_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_strings:
            client.read_write_two_strings_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_struct:
            client.read_write_struct_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_struct:
            client.read_write_optional_struct_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_structs:
            client.read_write_two_structs_changed(cb)

        for cb in self._property_updated_callbacks_for_read_only_enum:
            client.read_only_enum_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_enum:
            client.read_write_enum_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_enum:
            client.read_write_optional_enum_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_enums:
            client.read_write_two_enums_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_datetime:
            client.read_write_datetime_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_datetime:
            client.read_write_optional_datetime_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_datetimes:
            client.read_write_two_datetimes_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_duration:
            client.read_write_duration_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_duration:
            client.read_write_optional_duration_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_durations:
            client.read_write_two_durations_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_binary:
            client.read_write_binary_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_optional_binary:
            client.read_write_optional_binary_changed(cb)

        for cb in self._property_updated_callbacks_for_read_write_two_binaries:
            client.read_write_two_binaries_changed(cb)

        return client


class TestAbleClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[TestAbleClientBuilder] = None):
        """Creates a new TestAbleClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._logger = logging.getLogger("TestAbleClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "testAble/{}/interface".format("+")
        self._conn.subscribe(service_discovery_topic, self._process_service_discovery_message)
        self._mutex = threading.Lock()
        self._discovered_services: Dict[str, InterfaceInfo] = {}
        self._discovered_service_callbacks: List[Callable[[InterfaceInfo], None]] = []
        self._pending_futures: List[futures.Future] = []
        self._removed_service_callbacks: List[Callable[[str], None]] = []

    def add_discovered_service_callback(self, callback: Callable[[InterfaceInfo], None]):
        """Adds a callback to be called when a new service is discovered."""
        with self._mutex:
            self._discovered_service_callbacks.append(callback)

    def add_removed_service_callback(self, callback: Callable[[str], None]):
        """Adds a callback to be called when a service is removed."""
        with self._mutex:
            self._removed_service_callbacks.append(callback)

    def get_service_instance_ids(self) -> List[str]:
        """Returns a list of currently discovered service instance IDs."""
        with self._mutex:
            return list(self._discovered_services.keys())

    def get_singleton_client(self) -> futures.Future[TestAbleClient]:
        """Returns a TestAbleClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()
        with self._mutex:
            if len(self._discovered_services) > 0:
                service_instance_id = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(TestAbleClient(self._conn, service_instance_id))
                else:
                    new_client = self._builder.build(self._conn, service_instance_id)
                    fut.set_result(new_client)
            else:
                self._pending_futures.append(fut)
        return fut

    def _process_service_discovery_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a service discovery message."""
        self._logger.debug("Processing service discovery message on topic %s", topic)
        if len(payload) > 0:
            try:
                service_info = InterfaceInfo.model_validate_json(payload)
            except Exception as e:
                self._logger.warning("Failed to process service discovery message: %s", e)
            with self._mutex:
                self._discovered_services[service_info.instance] = service_info
                while self._pending_futures:
                    fut = self._pending_futures.pop(0)
                    if not fut.done():
                        if self._builder is not None:
                            fut.set_result(self._builder.build(self._conn, service_info.instance))
                        else:
                            fut.set_result(TestAbleClient(self._conn, service_info.instance))
                if not service_info.instance in self._discovered_services:
                    self._logger.info("Discovered service: %s.instance", service_info.instance)
                    for cb in self._discovered_service_callbacks:
                        cb(service_info)
                else:
                    self._logger.debug("Updated info for service: %s", service_info.instance)
        else:  # Empty payload means the service is going away
            instance_id = topic.split("/")[-2]
            with self._mutex:
                if instance_id in self._discovered_services:
                    self._logger.info("Service %s is going away", instance_id)
                    del self._discovered_services[instance_id]
                    for cb in self._removed_service_callbacks:
                        cb(instance_id)
