"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the testable interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from typing import Dict, Callable, List, Any, Optional, Union
from uuid import uuid4
from functools import partial, wraps
import json
import logging
from datetime import datetime, timedelta, UTC

from isodate import parse_duration
from stinger_python_utils.message_creator import MessageCreator
from stinger_python_utils.return_codes import *
from pyqttier.interface import IBrokerConnection
from pyqttier.message import Message
import concurrent.futures as futures

import asyncio
from stinger_python_utils.return_codes import (
    MethodReturnCode,
    ClientDeserializationErrorStingerMethodException,
    stinger_exception_factory,
)
from .interface_types import *
import threading


from .property import TestableInitialPropertyValues

from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)

EmptySignalCallbackType = Union[Callable[[], None], Callable[[Any], None]]
SingleIntSignalCallbackType = Union[Callable[[int], None], Callable[[Any, int], None]]
SingleOptionalIntSignalCallbackType = Union[Callable[[Optional[int]], None], Callable[[Any, Optional[int]], None]]
ThreeIntegersSignalCallbackType = Union[Callable[[int, int, Optional[int]], None], Callable[[Any, int, int, Optional[int]], None]]
SingleStringSignalCallbackType = Union[Callable[[str], None], Callable[[Any, str], None]]
SingleOptionalStringSignalCallbackType = Union[Callable[[Optional[str]], None], Callable[[Any, Optional[str]], None]]
ThreeStringsSignalCallbackType = Union[Callable[[str, str, Optional[str]], None], Callable[[Any, str, str, Optional[str]], None]]
SingleEnumSignalCallbackType = Union[Callable[[Numbers], None], Callable[[Any, Numbers], None]]
SingleOptionalEnumSignalCallbackType = Union[Callable[[Optional[Numbers]], None], Callable[[Any, Optional[Numbers]], None]]
ThreeEnumsSignalCallbackType = Union[Callable[[Numbers, Numbers, Optional[Numbers]], None], Callable[[Any, Numbers, Numbers, Optional[Numbers]], None]]
SingleStructSignalCallbackType = Union[Callable[[AllTypes], None], Callable[[Any, AllTypes], None]]
SingleOptionalStructSignalCallbackType = Union[Callable[[AllTypes], None], Callable[[Any, AllTypes], None]]
ThreeStructsSignalCallbackType = Union[Callable[[AllTypes, AllTypes, AllTypes], None], Callable[[Any, AllTypes, AllTypes, AllTypes], None]]
SingleDateTimeSignalCallbackType = Union[Callable[[datetime], None], Callable[[Any, datetime], None]]
SingleOptionalDatetimeSignalCallbackType = Union[Callable[[Optional[datetime]], None], Callable[[Any, Optional[datetime]], None]]
ThreeDateTimesSignalCallbackType = Union[Callable[[datetime, datetime, Optional[datetime]], None], Callable[[Any, datetime, datetime, Optional[datetime]], None]]
SingleDurationSignalCallbackType = Union[Callable[[timedelta], None], Callable[[Any, timedelta], None]]
SingleOptionalDurationSignalCallbackType = Union[Callable[[Optional[timedelta]], None], Callable[[Any, Optional[timedelta]], None]]
ThreeDurationsSignalCallbackType = Union[Callable[[timedelta, timedelta, Optional[timedelta]], None], Callable[[Any, timedelta, timedelta, Optional[timedelta]], None]]
SingleBinarySignalCallbackType = Union[Callable[[bytes], None], Callable[[Any, bytes], None]]
SingleOptionalBinarySignalCallbackType = Union[Callable[[bytes], None], Callable[[Any, bytes], None]]
ThreeBinariesSignalCallbackType = Union[Callable[[bytes, bytes, bytes], None], Callable[[Any, bytes, bytes, bytes], None]]
SingleArrayOfIntegersSignalCallbackType = Union[Callable[[List[int]], None], Callable[[Any, List[int]], None]]
SingleOptionalArrayOfStringsSignalCallbackType = Union[Callable[[List[str]], None], Callable[[Any, List[str]], None]]
ArrayOfEveryTypeSignalCallbackType = Union[
    Callable[[List[int], List[float], List[str], List[Numbers], List[Entry], List[datetime], List[timedelta], List[bytes]], None],
    Callable[[Any, List[int], List[float], List[str], List[Numbers], List[Entry], List[datetime], List[timedelta], List[bytes]], None],
]
CallWithNothingMethodResponseCallbackType = Union[Callable[[], None], Callable[[Any], None]]
CallOneIntegerMethodResponseCallbackType = Union[Callable[[int], None], Callable[[Any, int], None]]
CallOptionalIntegerMethodResponseCallbackType = Union[Callable[[Optional[int]], None], Callable[[Any, Optional[int]], None]]
CallThreeIntegersMethodResponseCallbackType = Union[Callable[[CallThreeIntegersMethodResponse], None], Callable[[Any, CallThreeIntegersMethodResponse], None]]
CallOneStringMethodResponseCallbackType = Union[Callable[[str], None], Callable[[Any, str], None]]
CallOptionalStringMethodResponseCallbackType = Union[Callable[[Optional[str]], None], Callable[[Any, Optional[str]], None]]
CallThreeStringsMethodResponseCallbackType = Union[Callable[[CallThreeStringsMethodResponse], None], Callable[[Any, CallThreeStringsMethodResponse], None]]
CallOneEnumMethodResponseCallbackType = Union[Callable[[Numbers], None], Callable[[Any, Numbers], None]]
CallOptionalEnumMethodResponseCallbackType = Union[Callable[[Optional[Numbers]], None], Callable[[Any, Optional[Numbers]], None]]
CallThreeEnumsMethodResponseCallbackType = Union[Callable[[CallThreeEnumsMethodResponse], None], Callable[[Any, CallThreeEnumsMethodResponse], None]]
CallOneStructMethodResponseCallbackType = Union[Callable[[AllTypes], None], Callable[[Any, AllTypes], None]]
CallOptionalStructMethodResponseCallbackType = Union[Callable[[AllTypes], None], Callable[[Any, AllTypes], None]]
CallThreeStructsMethodResponseCallbackType = Union[Callable[[CallThreeStructsMethodResponse], None], Callable[[Any, CallThreeStructsMethodResponse], None]]
CallOneDateTimeMethodResponseCallbackType = Union[Callable[[datetime], None], Callable[[Any, datetime], None]]
CallOptionalDateTimeMethodResponseCallbackType = Union[Callable[[Optional[datetime]], None], Callable[[Any, Optional[datetime]], None]]
CallThreeDateTimesMethodResponseCallbackType = Union[Callable[[CallThreeDateTimesMethodResponse], None], Callable[[Any, CallThreeDateTimesMethodResponse], None]]
CallOneDurationMethodResponseCallbackType = Union[Callable[[timedelta], None], Callable[[Any, timedelta], None]]
CallOptionalDurationMethodResponseCallbackType = Union[Callable[[Optional[timedelta]], None], Callable[[Any, Optional[timedelta]], None]]
CallThreeDurationsMethodResponseCallbackType = Union[Callable[[CallThreeDurationsMethodResponse], None], Callable[[Any, CallThreeDurationsMethodResponse], None]]
CallOneBinaryMethodResponseCallbackType = Union[Callable[[bytes], None], Callable[[Any, bytes], None]]
CallOptionalBinaryMethodResponseCallbackType = Union[Callable[[bytes], None], Callable[[Any, bytes], None]]
CallThreeBinariesMethodResponseCallbackType = Union[Callable[[CallThreeBinariesMethodResponse], None], Callable[[Any, CallThreeBinariesMethodResponse], None]]
CallOneListOfIntegersMethodResponseCallbackType = Union[Callable[[List[int]], None], Callable[[Any, List[int]], None]]
CallOptionalListOfFloatsMethodResponseCallbackType = Union[Callable[[List[float]], None], Callable[[Any, List[float]], None]]
CallTwoListsMethodResponseCallbackType = Union[Callable[[CallTwoListsMethodResponse], None], Callable[[Any, CallTwoListsMethodResponse], None]]

ReadWriteIntegerPropertyUpdatedCallbackType = Union[Callable[[int], None], Callable[[Any, int], None]]
ReadOnlyIntegerPropertyUpdatedCallbackType = Union[Callable[[int], None], Callable[[Any, int], None]]
ReadWriteOptionalIntegerPropertyUpdatedCallbackType = Union[Callable[[Optional[int]], None], Callable[[Any, Optional[int]], None]]
ReadWriteTwoIntegersPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoIntegersProperty], None], Callable[[Any, ReadWriteTwoIntegersProperty], None]]
ReadOnlyStringPropertyUpdatedCallbackType = Union[Callable[[str], None], Callable[[Any, str], None]]
ReadWriteStringPropertyUpdatedCallbackType = Union[Callable[[str], None], Callable[[Any, str], None]]
ReadWriteOptionalStringPropertyUpdatedCallbackType = Union[Callable[[Optional[str]], None], Callable[[Any, Optional[str]], None]]
ReadWriteTwoStringsPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoStringsProperty], None], Callable[[Any, ReadWriteTwoStringsProperty], None]]
ReadWriteStructPropertyUpdatedCallbackType = Union[Callable[[AllTypes], None], Callable[[Any, AllTypes], None]]
ReadWriteOptionalStructPropertyUpdatedCallbackType = Union[Callable[[AllTypes], None], Callable[[Any, AllTypes], None]]
ReadWriteTwoStructsPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoStructsProperty], None], Callable[[Any, ReadWriteTwoStructsProperty], None]]
ReadOnlyEnumPropertyUpdatedCallbackType = Union[Callable[[Numbers], None], Callable[[Any, Numbers], None]]
ReadWriteEnumPropertyUpdatedCallbackType = Union[Callable[[Numbers], None], Callable[[Any, Numbers], None]]
ReadWriteOptionalEnumPropertyUpdatedCallbackType = Union[Callable[[Optional[Numbers]], None], Callable[[Any, Optional[Numbers]], None]]
ReadWriteTwoEnumsPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoEnumsProperty], None], Callable[[Any, ReadWriteTwoEnumsProperty], None]]
ReadWriteDatetimePropertyUpdatedCallbackType = Union[Callable[[datetime], None], Callable[[Any, datetime], None]]
ReadWriteOptionalDatetimePropertyUpdatedCallbackType = Union[Callable[[Optional[datetime]], None], Callable[[Any, Optional[datetime]], None]]
ReadWriteTwoDatetimesPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoDatetimesProperty], None], Callable[[Any, ReadWriteTwoDatetimesProperty], None]]
ReadWriteDurationPropertyUpdatedCallbackType = Union[Callable[[timedelta], None], Callable[[Any, timedelta], None]]
ReadWriteOptionalDurationPropertyUpdatedCallbackType = Union[Callable[[Optional[timedelta]], None], Callable[[Any, Optional[timedelta]], None]]
ReadWriteTwoDurationsPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoDurationsProperty], None], Callable[[Any, ReadWriteTwoDurationsProperty], None]]
ReadWriteBinaryPropertyUpdatedCallbackType = Union[Callable[[bytes], None], Callable[[Any, bytes], None]]
ReadWriteOptionalBinaryPropertyUpdatedCallbackType = Union[Callable[[bytes], None], Callable[[Any, bytes], None]]
ReadWriteTwoBinariesPropertyUpdatedCallbackType = Union[Callable[[ReadWriteTwoBinariesProperty], None], Callable[[Any, ReadWriteTwoBinariesProperty], None]]
ReadWriteListOfStringsPropertyUpdatedCallbackType = Union[Callable[[List[str]], None], Callable[[Any, List[str]], None]]
ReadWriteListsPropertyUpdatedCallbackType = Union[Callable[[ReadWriteListsProperty], None], Callable[[Any, ReadWriteListsProperty], None]]


class DiscoveredInstance(BaseModel):
    instance_id: str
    initial_property_values: TestableInitialPropertyValues


class TestableClient:

    def __init__(self, connection: IBrokerConnection, instance_info: DiscoveredInstance):
        """Constructor for a `TestableClient` object."""
        self._logger = logging.getLogger("TestableClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing TestableClient with %s", instance_info.initial_property_values)
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = instance_info.instance_id

        self._pending_method_responses: Dict[str, Callable[..., None]] = {}

        self._property_read_write_integer = instance_info.initial_property_values.read_write_integer  # type: int
        self._property_read_write_integer_mutex = threading.Lock()
        self._property_read_write_integer_version = instance_info.initial_property_values.read_write_integer_version
        self._conn.subscribe("testable/{}/property/readWriteInteger/value".format(self._service_id), self._receive_read_write_integer_property_update_message)
        self._changed_value_callbacks_for_read_write_integer: List[ReadWriteIntegerPropertyUpdatedCallbackType] = []
        self._property_read_only_integer = instance_info.initial_property_values.read_only_integer  # type: int
        self._property_read_only_integer_mutex = threading.Lock()
        self._property_read_only_integer_version = instance_info.initial_property_values.read_only_integer_version
        self._conn.subscribe("testable/{}/property/readOnlyInteger/value".format(self._service_id), self._receive_read_only_integer_property_update_message)
        self._changed_value_callbacks_for_read_only_integer: List[ReadOnlyIntegerPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_integer = instance_info.initial_property_values.read_write_optional_integer  # type: Optional[int]
        self._property_read_write_optional_integer_mutex = threading.Lock()
        self._property_read_write_optional_integer_version = instance_info.initial_property_values.read_write_optional_integer_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalInteger/value".format(self._service_id), self._receive_read_write_optional_integer_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_integer: List[ReadWriteOptionalIntegerPropertyUpdatedCallbackType] = []
        self._property_read_write_two_integers = instance_info.initial_property_values.read_write_two_integers  # type: ReadWriteTwoIntegersProperty
        self._property_read_write_two_integers_mutex = threading.Lock()
        self._property_read_write_two_integers_version = instance_info.initial_property_values.read_write_two_integers_version
        self._conn.subscribe("testable/{}/property/readWriteTwoIntegers/value".format(self._service_id), self._receive_read_write_two_integers_property_update_message)
        self._changed_value_callbacks_for_read_write_two_integers: List[ReadWriteTwoIntegersPropertyUpdatedCallbackType] = []
        self._property_read_only_string = instance_info.initial_property_values.read_only_string  # type: str
        self._property_read_only_string_mutex = threading.Lock()
        self._property_read_only_string_version = instance_info.initial_property_values.read_only_string_version
        self._conn.subscribe("testable/{}/property/readOnlyString/value".format(self._service_id), self._receive_read_only_string_property_update_message)
        self._changed_value_callbacks_for_read_only_string: List[ReadOnlyStringPropertyUpdatedCallbackType] = []
        self._property_read_write_string = instance_info.initial_property_values.read_write_string  # type: str
        self._property_read_write_string_mutex = threading.Lock()
        self._property_read_write_string_version = instance_info.initial_property_values.read_write_string_version
        self._conn.subscribe("testable/{}/property/readWriteString/value".format(self._service_id), self._receive_read_write_string_property_update_message)
        self._changed_value_callbacks_for_read_write_string: List[ReadWriteStringPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_string = instance_info.initial_property_values.read_write_optional_string  # type: Optional[str]
        self._property_read_write_optional_string_mutex = threading.Lock()
        self._property_read_write_optional_string_version = instance_info.initial_property_values.read_write_optional_string_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalString/value".format(self._service_id), self._receive_read_write_optional_string_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_string: List[ReadWriteOptionalStringPropertyUpdatedCallbackType] = []
        self._property_read_write_two_strings = instance_info.initial_property_values.read_write_two_strings  # type: ReadWriteTwoStringsProperty
        self._property_read_write_two_strings_mutex = threading.Lock()
        self._property_read_write_two_strings_version = instance_info.initial_property_values.read_write_two_strings_version
        self._conn.subscribe("testable/{}/property/readWriteTwoStrings/value".format(self._service_id), self._receive_read_write_two_strings_property_update_message)
        self._changed_value_callbacks_for_read_write_two_strings: List[ReadWriteTwoStringsPropertyUpdatedCallbackType] = []
        self._property_read_write_struct = instance_info.initial_property_values.read_write_struct  # type: AllTypes
        self._property_read_write_struct_mutex = threading.Lock()
        self._property_read_write_struct_version = instance_info.initial_property_values.read_write_struct_version
        self._conn.subscribe("testable/{}/property/readWriteStruct/value".format(self._service_id), self._receive_read_write_struct_property_update_message)
        self._changed_value_callbacks_for_read_write_struct: List[ReadWriteStructPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_struct = instance_info.initial_property_values.read_write_optional_struct  # type: AllTypes
        self._property_read_write_optional_struct_mutex = threading.Lock()
        self._property_read_write_optional_struct_version = instance_info.initial_property_values.read_write_optional_struct_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalStruct/value".format(self._service_id), self._receive_read_write_optional_struct_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_struct: List[ReadWriteOptionalStructPropertyUpdatedCallbackType] = []
        self._property_read_write_two_structs = instance_info.initial_property_values.read_write_two_structs  # type: ReadWriteTwoStructsProperty
        self._property_read_write_two_structs_mutex = threading.Lock()
        self._property_read_write_two_structs_version = instance_info.initial_property_values.read_write_two_structs_version
        self._conn.subscribe("testable/{}/property/readWriteTwoStructs/value".format(self._service_id), self._receive_read_write_two_structs_property_update_message)
        self._changed_value_callbacks_for_read_write_two_structs: List[ReadWriteTwoStructsPropertyUpdatedCallbackType] = []
        self._property_read_only_enum = instance_info.initial_property_values.read_only_enum  # type: Numbers
        self._property_read_only_enum_mutex = threading.Lock()
        self._property_read_only_enum_version = instance_info.initial_property_values.read_only_enum_version
        self._conn.subscribe("testable/{}/property/readOnlyEnum/value".format(self._service_id), self._receive_read_only_enum_property_update_message)
        self._changed_value_callbacks_for_read_only_enum: List[ReadOnlyEnumPropertyUpdatedCallbackType] = []
        self._property_read_write_enum = instance_info.initial_property_values.read_write_enum  # type: Numbers
        self._property_read_write_enum_mutex = threading.Lock()
        self._property_read_write_enum_version = instance_info.initial_property_values.read_write_enum_version
        self._conn.subscribe("testable/{}/property/readWriteEnum/value".format(self._service_id), self._receive_read_write_enum_property_update_message)
        self._changed_value_callbacks_for_read_write_enum: List[ReadWriteEnumPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_enum = instance_info.initial_property_values.read_write_optional_enum  # type: Optional[Numbers]
        self._property_read_write_optional_enum_mutex = threading.Lock()
        self._property_read_write_optional_enum_version = instance_info.initial_property_values.read_write_optional_enum_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalEnum/value".format(self._service_id), self._receive_read_write_optional_enum_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_enum: List[ReadWriteOptionalEnumPropertyUpdatedCallbackType] = []
        self._property_read_write_two_enums = instance_info.initial_property_values.read_write_two_enums  # type: ReadWriteTwoEnumsProperty
        self._property_read_write_two_enums_mutex = threading.Lock()
        self._property_read_write_two_enums_version = instance_info.initial_property_values.read_write_two_enums_version
        self._conn.subscribe("testable/{}/property/readWriteTwoEnums/value".format(self._service_id), self._receive_read_write_two_enums_property_update_message)
        self._changed_value_callbacks_for_read_write_two_enums: List[ReadWriteTwoEnumsPropertyUpdatedCallbackType] = []
        self._property_read_write_datetime = instance_info.initial_property_values.read_write_datetime  # type: datetime
        self._property_read_write_datetime_mutex = threading.Lock()
        self._property_read_write_datetime_version = instance_info.initial_property_values.read_write_datetime_version
        self._conn.subscribe("testable/{}/property/readWriteDatetime/value".format(self._service_id), self._receive_read_write_datetime_property_update_message)
        self._changed_value_callbacks_for_read_write_datetime: List[ReadWriteDatetimePropertyUpdatedCallbackType] = []
        self._property_read_write_optional_datetime = instance_info.initial_property_values.read_write_optional_datetime  # type: Optional[datetime]
        self._property_read_write_optional_datetime_mutex = threading.Lock()
        self._property_read_write_optional_datetime_version = instance_info.initial_property_values.read_write_optional_datetime_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalDatetime/value".format(self._service_id), self._receive_read_write_optional_datetime_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_datetime: List[ReadWriteOptionalDatetimePropertyUpdatedCallbackType] = []
        self._property_read_write_two_datetimes = instance_info.initial_property_values.read_write_two_datetimes  # type: ReadWriteTwoDatetimesProperty
        self._property_read_write_two_datetimes_mutex = threading.Lock()
        self._property_read_write_two_datetimes_version = instance_info.initial_property_values.read_write_two_datetimes_version
        self._conn.subscribe("testable/{}/property/readWriteTwoDatetimes/value".format(self._service_id), self._receive_read_write_two_datetimes_property_update_message)
        self._changed_value_callbacks_for_read_write_two_datetimes: List[ReadWriteTwoDatetimesPropertyUpdatedCallbackType] = []
        self._property_read_write_duration = instance_info.initial_property_values.read_write_duration  # type: timedelta
        self._property_read_write_duration_mutex = threading.Lock()
        self._property_read_write_duration_version = instance_info.initial_property_values.read_write_duration_version
        self._conn.subscribe("testable/{}/property/readWriteDuration/value".format(self._service_id), self._receive_read_write_duration_property_update_message)
        self._changed_value_callbacks_for_read_write_duration: List[ReadWriteDurationPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_duration = instance_info.initial_property_values.read_write_optional_duration  # type: Optional[timedelta]
        self._property_read_write_optional_duration_mutex = threading.Lock()
        self._property_read_write_optional_duration_version = instance_info.initial_property_values.read_write_optional_duration_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalDuration/value".format(self._service_id), self._receive_read_write_optional_duration_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_duration: List[ReadWriteOptionalDurationPropertyUpdatedCallbackType] = []
        self._property_read_write_two_durations = instance_info.initial_property_values.read_write_two_durations  # type: ReadWriteTwoDurationsProperty
        self._property_read_write_two_durations_mutex = threading.Lock()
        self._property_read_write_two_durations_version = instance_info.initial_property_values.read_write_two_durations_version
        self._conn.subscribe("testable/{}/property/readWriteTwoDurations/value".format(self._service_id), self._receive_read_write_two_durations_property_update_message)
        self._changed_value_callbacks_for_read_write_two_durations: List[ReadWriteTwoDurationsPropertyUpdatedCallbackType] = []
        self._property_read_write_binary = instance_info.initial_property_values.read_write_binary  # type: bytes
        self._property_read_write_binary_mutex = threading.Lock()
        self._property_read_write_binary_version = instance_info.initial_property_values.read_write_binary_version
        self._conn.subscribe("testable/{}/property/readWriteBinary/value".format(self._service_id), self._receive_read_write_binary_property_update_message)
        self._changed_value_callbacks_for_read_write_binary: List[ReadWriteBinaryPropertyUpdatedCallbackType] = []
        self._property_read_write_optional_binary = instance_info.initial_property_values.read_write_optional_binary  # type: bytes
        self._property_read_write_optional_binary_mutex = threading.Lock()
        self._property_read_write_optional_binary_version = instance_info.initial_property_values.read_write_optional_binary_version
        self._conn.subscribe("testable/{}/property/readWriteOptionalBinary/value".format(self._service_id), self._receive_read_write_optional_binary_property_update_message)
        self._changed_value_callbacks_for_read_write_optional_binary: List[ReadWriteOptionalBinaryPropertyUpdatedCallbackType] = []
        self._property_read_write_two_binaries = instance_info.initial_property_values.read_write_two_binaries  # type: ReadWriteTwoBinariesProperty
        self._property_read_write_two_binaries_mutex = threading.Lock()
        self._property_read_write_two_binaries_version = instance_info.initial_property_values.read_write_two_binaries_version
        self._conn.subscribe("testable/{}/property/readWriteTwoBinaries/value".format(self._service_id), self._receive_read_write_two_binaries_property_update_message)
        self._changed_value_callbacks_for_read_write_two_binaries: List[ReadWriteTwoBinariesPropertyUpdatedCallbackType] = []
        self._property_read_write_list_of_strings = instance_info.initial_property_values.read_write_list_of_strings  # type: List[str]
        self._property_read_write_list_of_strings_mutex = threading.Lock()
        self._property_read_write_list_of_strings_version = instance_info.initial_property_values.read_write_list_of_strings_version
        self._conn.subscribe("testable/{}/property/readWriteListOfStrings/value".format(self._service_id), self._receive_read_write_list_of_strings_property_update_message)
        self._changed_value_callbacks_for_read_write_list_of_strings: List[ReadWriteListOfStringsPropertyUpdatedCallbackType] = []
        self._property_read_write_lists = instance_info.initial_property_values.read_write_lists  # type: ReadWriteListsProperty
        self._property_read_write_lists_mutex = threading.Lock()
        self._property_read_write_lists_version = instance_info.initial_property_values.read_write_lists_version
        self._conn.subscribe("testable/{}/property/readWriteLists/value".format(self._service_id), self._receive_read_write_lists_property_update_message)
        self._changed_value_callbacks_for_read_write_lists: List[ReadWriteListsPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_empty: List[EmptySignalCallbackType] = []
        self._signal_recv_callbacks_for_single_int: List[SingleIntSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_int: List[SingleOptionalIntSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_integers: List[ThreeIntegersSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_string: List[SingleStringSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_string: List[SingleOptionalStringSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_strings: List[ThreeStringsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_enum: List[SingleEnumSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_enum: List[SingleOptionalEnumSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_enums: List[ThreeEnumsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_struct: List[SingleStructSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_struct: List[SingleOptionalStructSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_structs: List[ThreeStructsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_date_time: List[SingleDateTimeSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_datetime: List[SingleOptionalDatetimeSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_date_times: List[ThreeDateTimesSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_duration: List[SingleDurationSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_duration: List[SingleOptionalDurationSignalCallbackType] = []
        self._signal_recv_callbacks_for_three_durations: List[ThreeDurationsSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_binary: List[SingleBinarySignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_binary: List[SingleOptionalBinarySignalCallbackType] = []
        self._signal_recv_callbacks_for_three_binaries: List[ThreeBinariesSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_array_of_integers: List[SingleArrayOfIntegersSignalCallbackType] = []
        self._signal_recv_callbacks_for_single_optional_array_of_strings: List[SingleOptionalArrayOfStringsSignalCallbackType] = []
        self._signal_recv_callbacks_for_array_of_every_type: List[ArrayOfEveryTypeSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/testable/methodResponse", self._receive_any_method_response_message)

        self._property_response_topic = f"client/{self._conn.client_id}/testable/propertyUpdateResponse"
        self._conn.subscribe(self._property_response_topic, self._receive_any_property_response_message)

    @property
    def service_id(self) -> str:
        """The service ID of the connected service instance."""
        return self._service_id

    @property
    def read_write_integer(self) -> int:
        """Property 'read_write_integer' getter."""
        with self._property_read_write_integer_mutex:
            return self._property_read_write_integer

    @read_write_integer.setter
    def read_write_integer(self, value: int):
        """Serializes and publishes the 'read_write_integer' property."""
        if not isinstance(value, int):
            raise ValueError("The 'read_write_integer' property must be a int")
        property_obj = ReadWriteIntegerProperty(value=value)
        self._logger.debug("Setting 'read_write_integer' property to %s", property_obj)
        with self._property_read_write_integer_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteInteger/setValue".format(self._service_id), property_obj, str(self._property_read_write_integer_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_integer_changed(self, handler: ReadWriteIntegerPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_integer' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_integer_mutex:
            self._changed_value_callbacks_for_read_write_integer.append(handler)
            if call_immediately and self._property_read_write_integer is not None:
                handler(self._property_read_write_integer)  # type: ignore[call-arg]
        return handler

    @property
    def read_only_integer(self) -> int:
        """Property 'read_only_integer' getter."""
        with self._property_read_only_integer_mutex:
            return self._property_read_only_integer

    def read_only_integer_changed(self, handler: ReadOnlyIntegerPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_only_integer' property changes.
        Can be used as a decorator.
        """
        with self._property_read_only_integer_mutex:
            self._changed_value_callbacks_for_read_only_integer.append(handler)
            if call_immediately and self._property_read_only_integer is not None:
                handler(self._property_read_only_integer)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_integer(self) -> Optional[int]:
        """Property 'read_write_optional_integer' getter."""
        with self._property_read_write_optional_integer_mutex:
            return self._property_read_write_optional_integer

    @read_write_optional_integer.setter
    def read_write_optional_integer(self, value: Optional[int]):
        """Serializes and publishes the 'read_write_optional_integer' property."""
        if not isinstance(value, int):
            raise ValueError("The 'read_write_optional_integer' property must be a int")
        property_obj = ReadWriteOptionalIntegerProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_integer' property to %s", property_obj)
        with self._property_read_write_optional_integer_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalInteger/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_integer_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_integer_changed(self, handler: ReadWriteOptionalIntegerPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_integer' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_integer_mutex:
            self._changed_value_callbacks_for_read_write_optional_integer.append(handler)
            if call_immediately and self._property_read_write_optional_integer is not None:
                handler(self._property_read_write_optional_integer)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_integers(self) -> ReadWriteTwoIntegersProperty:
        """Property 'read_write_two_integers' getter."""
        with self._property_read_write_two_integers_mutex:
            return self._property_read_write_two_integers

    @read_write_two_integers.setter
    def read_write_two_integers(self, value: ReadWriteTwoIntegersProperty):
        """Serializes and publishes the 'read_write_two_integers' property."""
        if not isinstance(value, ReadWriteTwoIntegersProperty):
            raise ValueError("The 'read_write_two_integers' property must be a ReadWriteTwoIntegersProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_integers' property to %s", property_obj)
        with self._property_read_write_two_integers_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoIntegers/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_two_integers_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_two_integers_changed(self, handler: ReadWriteTwoIntegersPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_integers' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_integers_mutex:
            self._changed_value_callbacks_for_read_write_two_integers.append(handler)
            if call_immediately and self._property_read_write_two_integers is not None:
                handler(self._property_read_write_two_integers)  # type: ignore[call-arg]
        return handler

    @property
    def read_only_string(self) -> str:
        """Property 'read_only_string' getter."""
        with self._property_read_only_string_mutex:
            return self._property_read_only_string

    def read_only_string_changed(self, handler: ReadOnlyStringPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_only_string' property changes.
        Can be used as a decorator.
        """
        with self._property_read_only_string_mutex:
            self._changed_value_callbacks_for_read_only_string.append(handler)
            if call_immediately and self._property_read_only_string is not None:
                handler(self._property_read_only_string)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_string(self) -> str:
        """Property 'read_write_string' getter."""
        with self._property_read_write_string_mutex:
            return self._property_read_write_string

    @read_write_string.setter
    def read_write_string(self, value: str):
        """Serializes and publishes the 'read_write_string' property."""
        if not isinstance(value, str):
            raise ValueError("The 'read_write_string' property must be a str")
        property_obj = ReadWriteStringProperty(value=value)
        self._logger.debug("Setting 'read_write_string' property to %s", property_obj)
        with self._property_read_write_string_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteString/setValue".format(self._service_id), property_obj, str(self._property_read_write_string_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_string_changed(self, handler: ReadWriteStringPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_string' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_string_mutex:
            self._changed_value_callbacks_for_read_write_string.append(handler)
            if call_immediately and self._property_read_write_string is not None:
                handler(self._property_read_write_string)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_string(self) -> Optional[str]:
        """Property 'read_write_optional_string' getter."""
        with self._property_read_write_optional_string_mutex:
            return self._property_read_write_optional_string

    @read_write_optional_string.setter
    def read_write_optional_string(self, value: Optional[str]):
        """Serializes and publishes the 'read_write_optional_string' property."""
        if not isinstance(value, str):
            raise ValueError("The 'read_write_optional_string' property must be a str")
        property_obj = ReadWriteOptionalStringProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_string' property to %s", property_obj)
        with self._property_read_write_optional_string_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalString/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_string_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_string_changed(self, handler: ReadWriteOptionalStringPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_string' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_string_mutex:
            self._changed_value_callbacks_for_read_write_optional_string.append(handler)
            if call_immediately and self._property_read_write_optional_string is not None:
                handler(self._property_read_write_optional_string)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_strings(self) -> ReadWriteTwoStringsProperty:
        """Property 'read_write_two_strings' getter."""
        with self._property_read_write_two_strings_mutex:
            return self._property_read_write_two_strings

    @read_write_two_strings.setter
    def read_write_two_strings(self, value: ReadWriteTwoStringsProperty):
        """Serializes and publishes the 'read_write_two_strings' property."""
        if not isinstance(value, ReadWriteTwoStringsProperty):
            raise ValueError("The 'read_write_two_strings' property must be a ReadWriteTwoStringsProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_strings' property to %s", property_obj)
        with self._property_read_write_two_strings_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoStrings/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_two_strings_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_two_strings_changed(self, handler: ReadWriteTwoStringsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_strings' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_strings_mutex:
            self._changed_value_callbacks_for_read_write_two_strings.append(handler)
            if call_immediately and self._property_read_write_two_strings is not None:
                handler(self._property_read_write_two_strings)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_struct(self) -> AllTypes:
        """Property 'read_write_struct' getter."""
        with self._property_read_write_struct_mutex:
            return self._property_read_write_struct

    @read_write_struct.setter
    def read_write_struct(self, value: AllTypes):
        """Serializes and publishes the 'read_write_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError("The 'read_write_struct' property must be a AllTypes")
        property_obj = ReadWriteStructProperty(value=value)
        self._logger.debug("Setting 'read_write_struct' property to %s", property_obj)
        with self._property_read_write_struct_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteStruct/setValue".format(self._service_id), property_obj, str(self._property_read_write_struct_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_struct_changed(self, handler: ReadWriteStructPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_struct' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_struct_mutex:
            self._changed_value_callbacks_for_read_write_struct.append(handler)
            if call_immediately and self._property_read_write_struct is not None:
                handler(self._property_read_write_struct)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_struct(self) -> AllTypes:
        """Property 'read_write_optional_struct' getter."""
        with self._property_read_write_optional_struct_mutex:
            return self._property_read_write_optional_struct

    @read_write_optional_struct.setter
    def read_write_optional_struct(self, value: AllTypes):
        """Serializes and publishes the 'read_write_optional_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError("The 'read_write_optional_struct' property must be a AllTypes")
        property_obj = ReadWriteOptionalStructProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_struct' property to %s", property_obj)
        with self._property_read_write_optional_struct_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalStruct/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_struct_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_struct_changed(self, handler: ReadWriteOptionalStructPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_struct' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_struct_mutex:
            self._changed_value_callbacks_for_read_write_optional_struct.append(handler)
            if call_immediately and self._property_read_write_optional_struct is not None:
                handler(self._property_read_write_optional_struct)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_structs(self) -> ReadWriteTwoStructsProperty:
        """Property 'read_write_two_structs' getter."""
        with self._property_read_write_two_structs_mutex:
            return self._property_read_write_two_structs

    @read_write_two_structs.setter
    def read_write_two_structs(self, value: ReadWriteTwoStructsProperty):
        """Serializes and publishes the 'read_write_two_structs' property."""
        if not isinstance(value, ReadWriteTwoStructsProperty):
            raise ValueError("The 'read_write_two_structs' property must be a ReadWriteTwoStructsProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_structs' property to %s", property_obj)
        with self._property_read_write_two_structs_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoStructs/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_two_structs_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_two_structs_changed(self, handler: ReadWriteTwoStructsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_structs' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_structs_mutex:
            self._changed_value_callbacks_for_read_write_two_structs.append(handler)
            if call_immediately and self._property_read_write_two_structs is not None:
                handler(self._property_read_write_two_structs)  # type: ignore[call-arg]
        return handler

    @property
    def read_only_enum(self) -> Numbers:
        """Property 'read_only_enum' getter."""
        with self._property_read_only_enum_mutex:
            return self._property_read_only_enum

    def read_only_enum_changed(self, handler: ReadOnlyEnumPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_only_enum' property changes.
        Can be used as a decorator.
        """
        with self._property_read_only_enum_mutex:
            self._changed_value_callbacks_for_read_only_enum.append(handler)
            if call_immediately and self._property_read_only_enum is not None:
                handler(self._property_read_only_enum)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_enum(self) -> Numbers:
        """Property 'read_write_enum' getter."""
        with self._property_read_write_enum_mutex:
            return self._property_read_write_enum

    @read_write_enum.setter
    def read_write_enum(self, value: Numbers):
        """Serializes and publishes the 'read_write_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError("The 'read_write_enum' property must be a Numbers")
        property_obj = ReadWriteEnumProperty(value=value)
        self._logger.debug("Setting 'read_write_enum' property to %s", property_obj)
        with self._property_read_write_enum_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteEnum/setValue".format(self._service_id), property_obj, str(self._property_read_write_enum_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_enum_changed(self, handler: ReadWriteEnumPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_enum' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_enum_mutex:
            self._changed_value_callbacks_for_read_write_enum.append(handler)
            if call_immediately and self._property_read_write_enum is not None:
                handler(self._property_read_write_enum)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_enum(self) -> Optional[Numbers]:
        """Property 'read_write_optional_enum' getter."""
        with self._property_read_write_optional_enum_mutex:
            return self._property_read_write_optional_enum

    @read_write_optional_enum.setter
    def read_write_optional_enum(self, value: Optional[Numbers]):
        """Serializes and publishes the 'read_write_optional_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError("The 'read_write_optional_enum' property must be a Numbers")
        property_obj = ReadWriteOptionalEnumProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_enum' property to %s", property_obj)
        with self._property_read_write_optional_enum_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalEnum/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_enum_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_enum_changed(self, handler: ReadWriteOptionalEnumPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_enum' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_enum_mutex:
            self._changed_value_callbacks_for_read_write_optional_enum.append(handler)
            if call_immediately and self._property_read_write_optional_enum is not None:
                handler(self._property_read_write_optional_enum)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_enums(self) -> ReadWriteTwoEnumsProperty:
        """Property 'read_write_two_enums' getter."""
        with self._property_read_write_two_enums_mutex:
            return self._property_read_write_two_enums

    @read_write_two_enums.setter
    def read_write_two_enums(self, value: ReadWriteTwoEnumsProperty):
        """Serializes and publishes the 'read_write_two_enums' property."""
        if not isinstance(value, ReadWriteTwoEnumsProperty):
            raise ValueError("The 'read_write_two_enums' property must be a ReadWriteTwoEnumsProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_enums' property to %s", property_obj)
        with self._property_read_write_two_enums_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoEnums/setValue".format(self._service_id), property_obj, str(self._property_read_write_two_enums_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_two_enums_changed(self, handler: ReadWriteTwoEnumsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_enums' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_enums_mutex:
            self._changed_value_callbacks_for_read_write_two_enums.append(handler)
            if call_immediately and self._property_read_write_two_enums is not None:
                handler(self._property_read_write_two_enums)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_datetime(self) -> datetime:
        """Property 'read_write_datetime' getter."""
        with self._property_read_write_datetime_mutex:
            return self._property_read_write_datetime

    @read_write_datetime.setter
    def read_write_datetime(self, value: datetime):
        """Serializes and publishes the 'read_write_datetime' property."""
        if not isinstance(value, datetime):
            raise ValueError("The 'read_write_datetime' property must be a datetime")
        property_obj = ReadWriteDatetimeProperty(value=value)
        self._logger.debug("Setting 'read_write_datetime' property to %s", property_obj)
        with self._property_read_write_datetime_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteDatetime/setValue".format(self._service_id), property_obj, str(self._property_read_write_datetime_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_datetime_changed(self, handler: ReadWriteDatetimePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_datetime' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_datetime_mutex:
            self._changed_value_callbacks_for_read_write_datetime.append(handler)
            if call_immediately and self._property_read_write_datetime is not None:
                handler(self._property_read_write_datetime)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_datetime(self) -> Optional[datetime]:
        """Property 'read_write_optional_datetime' getter."""
        with self._property_read_write_optional_datetime_mutex:
            return self._property_read_write_optional_datetime

    @read_write_optional_datetime.setter
    def read_write_optional_datetime(self, value: Optional[datetime]):
        """Serializes and publishes the 'read_write_optional_datetime' property."""
        if not isinstance(value, datetime):
            raise ValueError("The 'read_write_optional_datetime' property must be a datetime")
        property_obj = ReadWriteOptionalDatetimeProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_datetime' property to %s", property_obj)
        with self._property_read_write_optional_datetime_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalDatetime/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_datetime_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_datetime_changed(self, handler: ReadWriteOptionalDatetimePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_datetime' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_datetime_mutex:
            self._changed_value_callbacks_for_read_write_optional_datetime.append(handler)
            if call_immediately and self._property_read_write_optional_datetime is not None:
                handler(self._property_read_write_optional_datetime)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_datetimes(self) -> ReadWriteTwoDatetimesProperty:
        """Property 'read_write_two_datetimes' getter."""
        with self._property_read_write_two_datetimes_mutex:
            return self._property_read_write_two_datetimes

    @read_write_two_datetimes.setter
    def read_write_two_datetimes(self, value: ReadWriteTwoDatetimesProperty):
        """Serializes and publishes the 'read_write_two_datetimes' property."""
        if not isinstance(value, ReadWriteTwoDatetimesProperty):
            raise ValueError("The 'read_write_two_datetimes' property must be a ReadWriteTwoDatetimesProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_datetimes' property to %s", property_obj)
        with self._property_read_write_two_datetimes_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoDatetimes/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_two_datetimes_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_two_datetimes_changed(self, handler: ReadWriteTwoDatetimesPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_datetimes' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_datetimes_mutex:
            self._changed_value_callbacks_for_read_write_two_datetimes.append(handler)
            if call_immediately and self._property_read_write_two_datetimes is not None:
                handler(self._property_read_write_two_datetimes)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_duration(self) -> timedelta:
        """Property 'read_write_duration' getter."""
        with self._property_read_write_duration_mutex:
            return self._property_read_write_duration

    @read_write_duration.setter
    def read_write_duration(self, value: timedelta):
        """Serializes and publishes the 'read_write_duration' property."""
        if not isinstance(value, timedelta):
            raise ValueError("The 'read_write_duration' property must be a timedelta")
        property_obj = ReadWriteDurationProperty(value=value)
        self._logger.debug("Setting 'read_write_duration' property to %s", property_obj)
        with self._property_read_write_duration_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteDuration/setValue".format(self._service_id), property_obj, str(self._property_read_write_duration_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_duration_changed(self, handler: ReadWriteDurationPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_duration' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_duration_mutex:
            self._changed_value_callbacks_for_read_write_duration.append(handler)
            if call_immediately and self._property_read_write_duration is not None:
                handler(self._property_read_write_duration)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_duration(self) -> Optional[timedelta]:
        """Property 'read_write_optional_duration' getter."""
        with self._property_read_write_optional_duration_mutex:
            return self._property_read_write_optional_duration

    @read_write_optional_duration.setter
    def read_write_optional_duration(self, value: Optional[timedelta]):
        """Serializes and publishes the 'read_write_optional_duration' property."""
        if not isinstance(value, timedelta):
            raise ValueError("The 'read_write_optional_duration' property must be a timedelta")
        property_obj = ReadWriteOptionalDurationProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_duration' property to %s", property_obj)
        with self._property_read_write_optional_duration_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalDuration/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_duration_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_duration_changed(self, handler: ReadWriteOptionalDurationPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_duration' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_duration_mutex:
            self._changed_value_callbacks_for_read_write_optional_duration.append(handler)
            if call_immediately and self._property_read_write_optional_duration is not None:
                handler(self._property_read_write_optional_duration)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_durations(self) -> ReadWriteTwoDurationsProperty:
        """Property 'read_write_two_durations' getter."""
        with self._property_read_write_two_durations_mutex:
            return self._property_read_write_two_durations

    @read_write_two_durations.setter
    def read_write_two_durations(self, value: ReadWriteTwoDurationsProperty):
        """Serializes and publishes the 'read_write_two_durations' property."""
        if not isinstance(value, ReadWriteTwoDurationsProperty):
            raise ValueError("The 'read_write_two_durations' property must be a ReadWriteTwoDurationsProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_durations' property to %s", property_obj)
        with self._property_read_write_two_durations_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoDurations/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_two_durations_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_two_durations_changed(self, handler: ReadWriteTwoDurationsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_durations' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_durations_mutex:
            self._changed_value_callbacks_for_read_write_two_durations.append(handler)
            if call_immediately and self._property_read_write_two_durations is not None:
                handler(self._property_read_write_two_durations)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_binary(self) -> bytes:
        """Property 'read_write_binary' getter."""
        with self._property_read_write_binary_mutex:
            return self._property_read_write_binary

    @read_write_binary.setter
    def read_write_binary(self, value: bytes):
        """Serializes and publishes the 'read_write_binary' property."""
        if not isinstance(value, bytes):
            raise ValueError("The 'read_write_binary' property must be a bytes")
        property_obj = ReadWriteBinaryProperty(value=value)
        self._logger.debug("Setting 'read_write_binary' property to %s", property_obj)
        with self._property_read_write_binary_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteBinary/setValue".format(self._service_id), property_obj, str(self._property_read_write_binary_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_binary_changed(self, handler: ReadWriteBinaryPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_binary' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_binary_mutex:
            self._changed_value_callbacks_for_read_write_binary.append(handler)
            if call_immediately and self._property_read_write_binary is not None:
                handler(self._property_read_write_binary)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_optional_binary(self) -> bytes:
        """Property 'read_write_optional_binary' getter."""
        with self._property_read_write_optional_binary_mutex:
            return self._property_read_write_optional_binary

    @read_write_optional_binary.setter
    def read_write_optional_binary(self, value: bytes):
        """Serializes and publishes the 'read_write_optional_binary' property."""
        if not isinstance(value, bytes):
            raise ValueError("The 'read_write_optional_binary' property must be a bytes")
        property_obj = ReadWriteOptionalBinaryProperty(value=value)
        self._logger.debug("Setting 'read_write_optional_binary' property to %s", property_obj)
        with self._property_read_write_optional_binary_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteOptionalBinary/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_optional_binary_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_optional_binary_changed(self, handler: ReadWriteOptionalBinaryPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_optional_binary' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_optional_binary_mutex:
            self._changed_value_callbacks_for_read_write_optional_binary.append(handler)
            if call_immediately and self._property_read_write_optional_binary is not None:
                handler(self._property_read_write_optional_binary)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_two_binaries(self) -> ReadWriteTwoBinariesProperty:
        """Property 'read_write_two_binaries' getter."""
        with self._property_read_write_two_binaries_mutex:
            return self._property_read_write_two_binaries

    @read_write_two_binaries.setter
    def read_write_two_binaries(self, value: ReadWriteTwoBinariesProperty):
        """Serializes and publishes the 'read_write_two_binaries' property."""
        if not isinstance(value, ReadWriteTwoBinariesProperty):
            raise ValueError("The 'read_write_two_binaries' property must be a ReadWriteTwoBinariesProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_two_binaries' property to %s", property_obj)
        with self._property_read_write_two_binaries_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteTwoBinaries/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_two_binaries_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_two_binaries_changed(self, handler: ReadWriteTwoBinariesPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_two_binaries' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_two_binaries_mutex:
            self._changed_value_callbacks_for_read_write_two_binaries.append(handler)
            if call_immediately and self._property_read_write_two_binaries is not None:
                handler(self._property_read_write_two_binaries)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_list_of_strings(self) -> List[str]:
        """Property 'read_write_list_of_strings' getter."""
        with self._property_read_write_list_of_strings_mutex:
            return self._property_read_write_list_of_strings

    @read_write_list_of_strings.setter
    def read_write_list_of_strings(self, value: List[str]):
        """Serializes and publishes the 'read_write_list_of_strings' property."""
        if not isinstance(value, list):
            raise ValueError("The 'read_write_list_of_strings' property must be a list")
        property_obj = ReadWriteListOfStringsProperty(value=value)
        self._logger.debug("Setting 'read_write_list_of_strings' property to %s", property_obj)
        with self._property_read_write_list_of_strings_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteListOfStrings/setValue".format(self._service_id),
                property_obj,
                str(self._property_read_write_list_of_strings_version),
                self._property_response_topic,
                str(uuid4()),
            )
            self._conn.publish(req_msg)

    def read_write_list_of_strings_changed(self, handler: ReadWriteListOfStringsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_list_of_strings' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_list_of_strings_mutex:
            self._changed_value_callbacks_for_read_write_list_of_strings.append(handler)
            if call_immediately and self._property_read_write_list_of_strings is not None:
                handler(self._property_read_write_list_of_strings)  # type: ignore[call-arg]
        return handler

    @property
    def read_write_lists(self) -> ReadWriteListsProperty:
        """Property 'read_write_lists' getter."""
        with self._property_read_write_lists_mutex:
            return self._property_read_write_lists

    @read_write_lists.setter
    def read_write_lists(self, value: ReadWriteListsProperty):
        """Serializes and publishes the 'read_write_lists' property."""
        if not isinstance(value, ReadWriteListsProperty):
            raise ValueError("The 'read_write_lists' property must be a ReadWriteListsProperty")
        property_obj = value
        self._logger.debug("Setting 'read_write_lists' property to %s", property_obj)
        with self._property_read_write_lists_mutex:
            req_msg = MessageCreator.property_update_request_message(
                "testable/{}/property/readWriteLists/setValue".format(self._service_id), property_obj, str(self._property_read_write_lists_version), self._property_response_topic, str(uuid4())
            )
            self._conn.publish(req_msg)

    def read_write_lists_changed(self, handler: ReadWriteListsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'read_write_lists' property changes.
        Can be used as a decorator.
        """
        with self._property_read_write_lists_mutex:
            self._changed_value_callbacks_for_read_write_lists.append(handler)
            if call_immediately and self._property_read_write_lists is not None:
                handler(self._property_read_write_lists)  # type: ignore[call-arg]
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

    def _receive_empty_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'empty' signal with non-JSON content type")
            return

        model = EmptySignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_empty, **kwargs)

    def _receive_single_int_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleInt' signal with non-JSON content type")
            return

        model = SingleIntSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_int, **kwargs)

    def _receive_single_optional_int_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalInt' signal with non-JSON content type")
            return

        model = SingleOptionalIntSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_int, **kwargs)

    def _receive_three_integers_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeIntegers' signal with non-JSON content type")
            return

        model = ThreeIntegersSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_integers, **kwargs)

    def _receive_single_string_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleString' signal with non-JSON content type")
            return

        model = SingleStringSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_string, **kwargs)

    def _receive_single_optional_string_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalString' signal with non-JSON content type")
            return

        model = SingleOptionalStringSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_string, **kwargs)

    def _receive_three_strings_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeStrings' signal with non-JSON content type")
            return

        model = ThreeStringsSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_strings, **kwargs)

    def _receive_single_enum_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleEnum' signal with non-JSON content type")
            return

        model = SingleEnumSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_enum, **kwargs)

    def _receive_single_optional_enum_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalEnum' signal with non-JSON content type")
            return

        model = SingleOptionalEnumSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_enum, **kwargs)

    def _receive_three_enums_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeEnums' signal with non-JSON content type")
            return

        model = ThreeEnumsSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_enums, **kwargs)

    def _receive_single_struct_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleStruct' signal with non-JSON content type")
            return

        model = SingleStructSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_struct, **kwargs)

    def _receive_single_optional_struct_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalStruct' signal with non-JSON content type")
            return

        model = SingleOptionalStructSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_struct, **kwargs)

    def _receive_three_structs_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeStructs' signal with non-JSON content type")
            return

        model = ThreeStructsSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_structs, **kwargs)

    def _receive_single_date_time_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleDateTime' signal with non-JSON content type")
            return

        model = SingleDateTimeSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_date_time, **kwargs)

    def _receive_single_optional_datetime_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalDatetime' signal with non-JSON content type")
            return

        model = SingleOptionalDatetimeSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_datetime, **kwargs)

    def _receive_three_date_times_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeDateTimes' signal with non-JSON content type")
            return

        model = ThreeDateTimesSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_date_times, **kwargs)

    def _receive_single_duration_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleDuration' signal with non-JSON content type")
            return

        model = SingleDurationSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_duration, **kwargs)

    def _receive_single_optional_duration_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalDuration' signal with non-JSON content type")
            return

        model = SingleOptionalDurationSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_duration, **kwargs)

    def _receive_three_durations_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeDurations' signal with non-JSON content type")
            return

        model = ThreeDurationsSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_durations, **kwargs)

    def _receive_single_binary_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleBinary' signal with non-JSON content type")
            return

        model = SingleBinarySignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_binary, **kwargs)

    def _receive_single_optional_binary_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalBinary' signal with non-JSON content type")
            return

        model = SingleOptionalBinarySignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_binary, **kwargs)

    def _receive_three_binaries_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'threeBinaries' signal with non-JSON content type")
            return

        model = ThreeBinariesSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_three_binaries, **kwargs)

    def _receive_single_array_of_integers_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleArrayOfIntegers' signal with non-JSON content type")
            return

        model = SingleArrayOfIntegersSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_array_of_integers, **kwargs)

    def _receive_single_optional_array_of_strings_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'singleOptionalArrayOfStrings' signal with non-JSON content type")
            return

        model = SingleOptionalArrayOfStringsSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_single_optional_array_of_strings, **kwargs)

    def _receive_array_of_every_type_signal_message(self, message: Message):
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'arrayOfEveryType' signal with non-JSON content type")
            return

        model = ArrayOfEveryTypeSignalPayload.model_validate_json(message.payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_array_of_every_type, **kwargs)

    def _receive_any_method_response_message(self, message: Message):
        # Handle '' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if message.user_properties:
            user_properties = message.user_properties or {}
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", message.topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if message.correlation_data is not None:
            correlation_id = message.correlation_data.decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(message.payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s.", message.topic)

    def _receive_any_property_response_message(self, message: Message):
        user_properties = message.user_properties or {}
        return_code = user_properties.get("ReturnCode")
        if return_code is not None and int(return_code) != MethodReturnCode.SUCCESS.value:
            debug_info = user_properties.get("DebugInfo", "")
            self._logger.warning("Received error return value %s from property update: %s", return_code, debug_info)

    def _receive_read_write_integer_property_update_message(self, message: Message):
        # Handle 'read_write_integer' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_integer' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteIntegerProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_integer_mutex:
                self._property_read_write_integer = prop_obj.value
                self._property_read_write_integer_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_integer, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_integer' property change: %s", exc_info=e)

    def _receive_read_only_integer_property_update_message(self, message: Message):
        # Handle 'read_only_integer' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_only_integer' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadOnlyIntegerProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_only_integer_mutex:
                self._property_read_only_integer = prop_obj.value
                self._property_read_only_integer_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_only_integer, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_only_integer' property change: %s", exc_info=e)

    def _receive_read_write_optional_integer_property_update_message(self, message: Message):
        # Handle 'read_write_optional_integer' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_integer' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalIntegerProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_integer_mutex:
                self._property_read_write_optional_integer = prop_obj.value
                self._property_read_write_optional_integer_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_integer, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_integer' property change: %s", exc_info=e)

    def _receive_read_write_two_integers_property_update_message(self, message: Message):
        # Handle 'read_write_two_integers' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_integers' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoIntegersProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_integers_mutex:
                self._property_read_write_two_integers = prop_obj
                self._property_read_write_two_integers_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_integers, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_integers' property change: %s", exc_info=e)

    def _receive_read_only_string_property_update_message(self, message: Message):
        # Handle 'read_only_string' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_only_string' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadOnlyStringProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_only_string_mutex:
                self._property_read_only_string = prop_obj.value
                self._property_read_only_string_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_only_string, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_only_string' property change: %s", exc_info=e)

    def _receive_read_write_string_property_update_message(self, message: Message):
        # Handle 'read_write_string' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_string' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteStringProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_string_mutex:
                self._property_read_write_string = prop_obj.value
                self._property_read_write_string_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_string, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_string' property change: %s", exc_info=e)

    def _receive_read_write_optional_string_property_update_message(self, message: Message):
        # Handle 'read_write_optional_string' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_string' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalStringProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_string_mutex:
                self._property_read_write_optional_string = prop_obj.value
                self._property_read_write_optional_string_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_string, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_string' property change: %s", exc_info=e)

    def _receive_read_write_two_strings_property_update_message(self, message: Message):
        # Handle 'read_write_two_strings' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_strings' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoStringsProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_strings_mutex:
                self._property_read_write_two_strings = prop_obj
                self._property_read_write_two_strings_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_strings, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_strings' property change: %s", exc_info=e)

    def _receive_read_write_struct_property_update_message(self, message: Message):
        # Handle 'read_write_struct' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_struct' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteStructProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_struct_mutex:
                self._property_read_write_struct = prop_obj.value
                self._property_read_write_struct_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_struct, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_struct' property change: %s", exc_info=e)

    def _receive_read_write_optional_struct_property_update_message(self, message: Message):
        # Handle 'read_write_optional_struct' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_struct' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalStructProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_struct_mutex:
                self._property_read_write_optional_struct = prop_obj.value
                self._property_read_write_optional_struct_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_struct, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_struct' property change: %s", exc_info=e)

    def _receive_read_write_two_structs_property_update_message(self, message: Message):
        # Handle 'read_write_two_structs' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_structs' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoStructsProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_structs_mutex:
                self._property_read_write_two_structs = prop_obj
                self._property_read_write_two_structs_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_structs, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_structs' property change: %s", exc_info=e)

    def _receive_read_only_enum_property_update_message(self, message: Message):
        # Handle 'read_only_enum' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_only_enum' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadOnlyEnumProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_only_enum_mutex:
                self._property_read_only_enum = prop_obj.value
                self._property_read_only_enum_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_only_enum, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_only_enum' property change: %s", exc_info=e)

    def _receive_read_write_enum_property_update_message(self, message: Message):
        # Handle 'read_write_enum' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_enum' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteEnumProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_enum_mutex:
                self._property_read_write_enum = prop_obj.value
                self._property_read_write_enum_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_enum, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_enum' property change: %s", exc_info=e)

    def _receive_read_write_optional_enum_property_update_message(self, message: Message):
        # Handle 'read_write_optional_enum' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_enum' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalEnumProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_enum_mutex:
                self._property_read_write_optional_enum = prop_obj.value
                self._property_read_write_optional_enum_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_enum, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_enum' property change: %s", exc_info=e)

    def _receive_read_write_two_enums_property_update_message(self, message: Message):
        # Handle 'read_write_two_enums' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_enums' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoEnumsProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_enums_mutex:
                self._property_read_write_two_enums = prop_obj
                self._property_read_write_two_enums_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_enums, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_enums' property change: %s", exc_info=e)

    def _receive_read_write_datetime_property_update_message(self, message: Message):
        # Handle 'read_write_datetime' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_datetime' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteDatetimeProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_datetime_mutex:
                self._property_read_write_datetime = prop_obj.value
                self._property_read_write_datetime_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_datetime, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_datetime' property change: %s", exc_info=e)

    def _receive_read_write_optional_datetime_property_update_message(self, message: Message):
        # Handle 'read_write_optional_datetime' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_datetime' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalDatetimeProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_datetime_mutex:
                self._property_read_write_optional_datetime = prop_obj.value
                self._property_read_write_optional_datetime_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_datetime, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_datetime' property change: %s", exc_info=e)

    def _receive_read_write_two_datetimes_property_update_message(self, message: Message):
        # Handle 'read_write_two_datetimes' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_datetimes' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoDatetimesProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_datetimes_mutex:
                self._property_read_write_two_datetimes = prop_obj
                self._property_read_write_two_datetimes_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_datetimes, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_datetimes' property change: %s", exc_info=e)

    def _receive_read_write_duration_property_update_message(self, message: Message):
        # Handle 'read_write_duration' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_duration' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteDurationProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_duration_mutex:
                self._property_read_write_duration = prop_obj.value
                self._property_read_write_duration_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_duration, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_duration' property change: %s", exc_info=e)

    def _receive_read_write_optional_duration_property_update_message(self, message: Message):
        # Handle 'read_write_optional_duration' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_duration' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalDurationProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_duration_mutex:
                self._property_read_write_optional_duration = prop_obj.value
                self._property_read_write_optional_duration_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_duration, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_duration' property change: %s", exc_info=e)

    def _receive_read_write_two_durations_property_update_message(self, message: Message):
        # Handle 'read_write_two_durations' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_durations' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoDurationsProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_durations_mutex:
                self._property_read_write_two_durations = prop_obj
                self._property_read_write_two_durations_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_durations, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_durations' property change: %s", exc_info=e)

    def _receive_read_write_binary_property_update_message(self, message: Message):
        # Handle 'read_write_binary' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_binary' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteBinaryProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_binary_mutex:
                self._property_read_write_binary = prop_obj.value
                self._property_read_write_binary_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_binary, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_binary' property change: %s", exc_info=e)

    def _receive_read_write_optional_binary_property_update_message(self, message: Message):
        # Handle 'read_write_optional_binary' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_optional_binary' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteOptionalBinaryProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_optional_binary_mutex:
                self._property_read_write_optional_binary = prop_obj.value
                self._property_read_write_optional_binary_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_optional_binary, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_optional_binary' property change: %s", exc_info=e)

    def _receive_read_write_two_binaries_property_update_message(self, message: Message):
        # Handle 'read_write_two_binaries' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_two_binaries' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteTwoBinariesProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_two_binaries_mutex:
                self._property_read_write_two_binaries = prop_obj
                self._property_read_write_two_binaries_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_two_binaries, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_two_binaries' property change: %s", exc_info=e)

    def _receive_read_write_list_of_strings_property_update_message(self, message: Message):
        # Handle 'read_write_list_of_strings' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_list_of_strings' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteListOfStringsProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_list_of_strings_mutex:
                self._property_read_write_list_of_strings = prop_obj.value
                self._property_read_write_list_of_strings_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_list_of_strings, value=prop_obj.value)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_list_of_strings' property change: %s", exc_info=e)

    def _receive_read_write_lists_property_update_message(self, message: Message):
        # Handle 'read_write_lists' property change.
        if message.content_type is None or message.content_type != "application/json":
            self._logger.warning("Received 'read_write_lists' property change with non-JSON content type")
            return
        try:
            prop_obj = ReadWriteListsProperty.model_validate_json(message.payload)
            user_properties = message.user_properties or {}
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_read_write_lists_mutex:
                self._property_read_write_lists = prop_obj
                self._property_read_write_lists_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_read_write_lists, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'read_write_lists' property change: %s", exc_info=e)

    def _receive_message(self, message: Message):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.warning("Receiving message %s, but without a handler", message)

    def receive_empty(self, handler: EmptySignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_empty.append(handler)
        if len(self._signal_recv_callbacks_for_empty) == 1:
            self._conn.subscribe("testable/{}/signal/empty".format(self._service_id), self._receive_empty_signal_message)
        return handler

    def receive_single_int(self, handler: SingleIntSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_int.append(handler)
        if len(self._signal_recv_callbacks_for_single_int) == 1:
            self._conn.subscribe("testable/{}/signal/singleInt".format(self._service_id), self._receive_single_int_signal_message)
        return handler

    def receive_single_optional_int(self, handler: SingleOptionalIntSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_int.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_int) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalInt".format(self._service_id), self._receive_single_optional_int_signal_message)
        return handler

    def receive_three_integers(self, handler: ThreeIntegersSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_integers.append(handler)
        if len(self._signal_recv_callbacks_for_three_integers) == 1:
            self._conn.subscribe("testable/{}/signal/threeIntegers".format(self._service_id), self._receive_three_integers_signal_message)
        return handler

    def receive_single_string(self, handler: SingleStringSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_string.append(handler)
        if len(self._signal_recv_callbacks_for_single_string) == 1:
            self._conn.subscribe("testable/{}/signal/singleString".format(self._service_id), self._receive_single_string_signal_message)
        return handler

    def receive_single_optional_string(self, handler: SingleOptionalStringSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_string.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_string) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalString".format(self._service_id), self._receive_single_optional_string_signal_message)
        return handler

    def receive_three_strings(self, handler: ThreeStringsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_strings.append(handler)
        if len(self._signal_recv_callbacks_for_three_strings) == 1:
            self._conn.subscribe("testable/{}/signal/threeStrings".format(self._service_id), self._receive_three_strings_signal_message)
        return handler

    def receive_single_enum(self, handler: SingleEnumSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_enum.append(handler)
        if len(self._signal_recv_callbacks_for_single_enum) == 1:
            self._conn.subscribe("testable/{}/signal/singleEnum".format(self._service_id), self._receive_single_enum_signal_message)
        return handler

    def receive_single_optional_enum(self, handler: SingleOptionalEnumSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_enum.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_enum) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalEnum".format(self._service_id), self._receive_single_optional_enum_signal_message)
        return handler

    def receive_three_enums(self, handler: ThreeEnumsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_enums.append(handler)
        if len(self._signal_recv_callbacks_for_three_enums) == 1:
            self._conn.subscribe("testable/{}/signal/threeEnums".format(self._service_id), self._receive_three_enums_signal_message)
        return handler

    def receive_single_struct(self, handler: SingleStructSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_struct.append(handler)
        if len(self._signal_recv_callbacks_for_single_struct) == 1:
            self._conn.subscribe("testable/{}/signal/singleStruct".format(self._service_id), self._receive_single_struct_signal_message)
        return handler

    def receive_single_optional_struct(self, handler: SingleOptionalStructSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_struct.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_struct) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalStruct".format(self._service_id), self._receive_single_optional_struct_signal_message)
        return handler

    def receive_three_structs(self, handler: ThreeStructsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_structs.append(handler)
        if len(self._signal_recv_callbacks_for_three_structs) == 1:
            self._conn.subscribe("testable/{}/signal/threeStructs".format(self._service_id), self._receive_three_structs_signal_message)
        return handler

    def receive_single_date_time(self, handler: SingleDateTimeSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_date_time.append(handler)
        if len(self._signal_recv_callbacks_for_single_date_time) == 1:
            self._conn.subscribe("testable/{}/signal/singleDateTime".format(self._service_id), self._receive_single_date_time_signal_message)
        return handler

    def receive_single_optional_datetime(self, handler: SingleOptionalDatetimeSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_datetime.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_datetime) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalDatetime".format(self._service_id), self._receive_single_optional_datetime_signal_message)
        return handler

    def receive_three_date_times(self, handler: ThreeDateTimesSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_date_times.append(handler)
        if len(self._signal_recv_callbacks_for_three_date_times) == 1:
            self._conn.subscribe("testable/{}/signal/threeDateTimes".format(self._service_id), self._receive_three_date_times_signal_message)
        return handler

    def receive_single_duration(self, handler: SingleDurationSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_duration.append(handler)
        if len(self._signal_recv_callbacks_for_single_duration) == 1:
            self._conn.subscribe("testable/{}/signal/singleDuration".format(self._service_id), self._receive_single_duration_signal_message)
        return handler

    def receive_single_optional_duration(self, handler: SingleOptionalDurationSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_duration.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_duration) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalDuration".format(self._service_id), self._receive_single_optional_duration_signal_message)
        return handler

    def receive_three_durations(self, handler: ThreeDurationsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_durations.append(handler)
        if len(self._signal_recv_callbacks_for_three_durations) == 1:
            self._conn.subscribe("testable/{}/signal/threeDurations".format(self._service_id), self._receive_three_durations_signal_message)
        return handler

    def receive_single_binary(self, handler: SingleBinarySignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_binary.append(handler)
        if len(self._signal_recv_callbacks_for_single_binary) == 1:
            self._conn.subscribe("testable/{}/signal/singleBinary".format(self._service_id), self._receive_single_binary_signal_message)
        return handler

    def receive_single_optional_binary(self, handler: SingleOptionalBinarySignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_binary.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_binary) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalBinary".format(self._service_id), self._receive_single_optional_binary_signal_message)
        return handler

    def receive_three_binaries(self, handler: ThreeBinariesSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_three_binaries.append(handler)
        if len(self._signal_recv_callbacks_for_three_binaries) == 1:
            self._conn.subscribe("testable/{}/signal/threeBinaries".format(self._service_id), self._receive_three_binaries_signal_message)
        return handler

    def receive_single_array_of_integers(self, handler: SingleArrayOfIntegersSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_array_of_integers.append(handler)
        if len(self._signal_recv_callbacks_for_single_array_of_integers) == 1:
            self._conn.subscribe("testable/{}/signal/singleArrayOfIntegers".format(self._service_id), self._receive_single_array_of_integers_signal_message)
        return handler

    def receive_single_optional_array_of_strings(self, handler: SingleOptionalArrayOfStringsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_single_optional_array_of_strings.append(handler)
        if len(self._signal_recv_callbacks_for_single_optional_array_of_strings) == 1:
            self._conn.subscribe("testable/{}/signal/singleOptionalArrayOfStrings".format(self._service_id), self._receive_single_optional_array_of_strings_signal_message)
        return handler

    def receive_array_of_every_type(self, handler: ArrayOfEveryTypeSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_array_of_every_type.append(handler)
        if len(self._signal_recv_callbacks_for_array_of_every_type) == 1:
            self._conn.subscribe("testable/{}/signal/arrayOfEveryType".format(self._service_id), self._receive_array_of_every_type_signal_message)
        return handler

    def call_with_nothing(
        self,
    ) -> futures.Future:
        """Calling this initiates a `callWithNothing` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_with_nothing_response, fut)
        payload = CallWithNothingMethodRequest()
        self._logger.debug("Calling 'callWithNothing' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callWithNothing".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOneInteger' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneInteger".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOptionalInteger' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalInteger".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callThreeIntegers' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeIntegers".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOneString' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneString".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOptionalString' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalString".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callThreeStrings' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeStrings".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_one_enum(self, input1: Numbers) -> futures.Future:
        """Calling this initiates a `callOneEnum` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_enum_response, fut)
        payload = CallOneEnumMethodRequest(
            input1=input1,
        )
        self._logger.debug("Calling 'callOneEnum' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneEnum".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_optional_enum(self, input1: Optional[Numbers]) -> futures.Future:
        """Calling this initiates a `callOptionalEnum` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_enum_response, fut)
        payload = CallOptionalEnumMethodRequest(
            input1=input1,
        )
        self._logger.debug("Calling 'callOptionalEnum' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalEnum".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_three_enums(self, input1: Numbers, input2: Numbers, input3: Optional[Numbers]) -> futures.Future:
        """Calling this initiates a `callThreeEnums` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_enums_response, fut)
        payload = CallThreeEnumsMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        self._logger.debug("Calling 'callThreeEnums' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeEnums".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_one_struct(self, input1: AllTypes) -> futures.Future:
        """Calling this initiates a `callOneStruct` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_struct_response, fut)
        payload = CallOneStructMethodRequest(
            input1=input1,
        )
        self._logger.debug("Calling 'callOneStruct' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneStruct".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_optional_struct(self, input1: AllTypes) -> futures.Future:
        """Calling this initiates a `callOptionalStruct` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_struct_response, fut)
        payload = CallOptionalStructMethodRequest(
            input1=input1,
        )
        self._logger.debug("Calling 'callOptionalStruct' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalStruct".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_three_structs(self, input1: AllTypes, input2: AllTypes, input3: AllTypes) -> futures.Future:
        """Calling this initiates a `callThreeStructs` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_three_structs_response, fut)
        payload = CallThreeStructsMethodRequest(
            input1=input1,
            input2=input2,
            input3=input3,
        )
        self._logger.debug("Calling 'callThreeStructs' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeStructs".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOneDateTime' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneDateTime".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOptionalDateTime' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalDateTime".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callThreeDateTimes' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeDateTimes".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOneDuration' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneDuration".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOptionalDuration' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalDuration".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callThreeDurations' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeDurations".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOneBinary' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneBinary".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callOptionalBinary' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalBinary".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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
        self._logger.debug("Calling 'callThreeBinaries' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callThreeBinaries".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
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

    def call_one_list_of_integers(self, input1: List[int]) -> futures.Future:
        """Calling this initiates a `callOneListOfIntegers` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_one_list_of_integers_response, fut)
        payload = CallOneListOfIntegersMethodRequest(
            input1=input1,
        )
        self._logger.debug("Calling 'callOneListOfIntegers' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOneListOfIntegers".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
        return fut

    def _handle_call_one_list_of_integers_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOneListOfIntegers` IPC method call."""
        self._logger.debug("Handling call_one_list_of_integers response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOneListOfIntegers' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOneListOfIntegersMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOneListOfIntegers' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOneListOfIntegers' method was already done!")

    def call_optional_list_of_floats(self, input1: List[float]) -> futures.Future:
        """Calling this initiates a `callOptionalListOfFloats` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_optional_list_of_floats_response, fut)
        payload = CallOptionalListOfFloatsMethodRequest(
            input1=input1,
        )
        self._logger.debug("Calling 'callOptionalListOfFloats' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callOptionalListOfFloats".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
        return fut

    def _handle_call_optional_list_of_floats_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callOptionalListOfFloats` IPC method call."""
        self._logger.debug("Handling call_optional_list_of_floats response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callOptionalListOfFloats' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallOptionalListOfFloatsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callOptionalListOfFloats' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.output1)
        else:
            self._logger.warning("Future for 'callOptionalListOfFloats' method was already done!")

    def call_two_lists(self, input1: List[Numbers], input2: List[str]) -> futures.Future:
        """Calling this initiates a `callTwoLists` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_call_two_lists_response, fut)
        payload = CallTwoListsMethodRequest(
            input1=input1,
            input2=input2,
        )
        self._logger.debug("Calling 'callTwoLists' method with payload %s", payload)
        response_topic = f"client/{self._conn.client_id}/testable/methodResponse"
        req_msg = MessageCreator.request_message("testable/{}/method/callTwoLists".format(self._service_id), payload, response_topic, correlation_id)
        self._conn.publish(req_msg)
        return fut

    def _handle_call_two_lists_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `callTwoLists` IPC method call."""
        self._logger.debug("Handling call_two_lists response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'callTwoLists' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = CallTwoListsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'callTwoLists' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'callTwoLists' method was already done!")


class TestableClientBuilder:
    """Using decorators from TestableClient doesn't work if you are trying to create multiple instances of TestableClient.
    Instead, use this builder to create a registry of callbacks, and then build clients using the registry.

    When ready to create a TestableClient instance, call the `build(broker, service_instance_id)` method.
    """

    def __init__(self):
        """Creates a new TestableClientBuilder."""
        self._logger = logging.getLogger("TestableClientBuilder")
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
        self._signal_recv_callbacks_for_single_array_of_integers = []  # type: List[SingleArrayOfIntegersSignalCallbackType]
        self._signal_recv_callbacks_for_single_optional_array_of_strings = []  # type: List[SingleOptionalArrayOfStringsSignalCallbackType]
        self._signal_recv_callbacks_for_array_of_every_type = []  # type: List[ArrayOfEveryTypeSignalCallbackType]
        self._property_updated_callbacks_for_read_write_integer: List[ReadWriteIntegerPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_only_integer: List[ReadOnlyIntegerPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_integer: List[ReadWriteOptionalIntegerPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_integers: List[ReadWriteTwoIntegersPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_only_string: List[ReadOnlyStringPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_string: List[ReadWriteStringPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_string: List[ReadWriteOptionalStringPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_strings: List[ReadWriteTwoStringsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_struct: List[ReadWriteStructPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_struct: List[ReadWriteOptionalStructPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_structs: List[ReadWriteTwoStructsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_only_enum: List[ReadOnlyEnumPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_enum: List[ReadWriteEnumPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_enum: List[ReadWriteOptionalEnumPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_enums: List[ReadWriteTwoEnumsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_datetime: List[ReadWriteDatetimePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_datetime: List[ReadWriteOptionalDatetimePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_datetimes: List[ReadWriteTwoDatetimesPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_duration: List[ReadWriteDurationPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_duration: List[ReadWriteOptionalDurationPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_durations: List[ReadWriteTwoDurationsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_binary: List[ReadWriteBinaryPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_optional_binary: List[ReadWriteOptionalBinaryPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_two_binaries: List[ReadWriteTwoBinariesPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_list_of_strings: List[ReadWriteListOfStringsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_read_write_lists: List[ReadWriteListsPropertyUpdatedCallbackType] = []

    def receive_empty(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_empty.append(wrapper)
        return wrapper

    def receive_single_int(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_int.append(wrapper)
        return wrapper

    def receive_single_optional_int(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_int.append(wrapper)
        return wrapper

    def receive_three_integers(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_integers.append(wrapper)
        return wrapper

    def receive_single_string(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_string.append(wrapper)
        return wrapper

    def receive_single_optional_string(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_string.append(wrapper)
        return wrapper

    def receive_three_strings(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_strings.append(wrapper)
        return wrapper

    def receive_single_enum(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_enum.append(wrapper)
        return wrapper

    def receive_single_optional_enum(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_enum.append(wrapper)
        return wrapper

    def receive_three_enums(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_enums.append(wrapper)
        return wrapper

    def receive_single_struct(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_struct.append(wrapper)
        return wrapper

    def receive_single_optional_struct(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_struct.append(wrapper)
        return wrapper

    def receive_three_structs(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_structs.append(wrapper)
        return wrapper

    def receive_single_date_time(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_date_time.append(wrapper)
        return wrapper

    def receive_single_optional_datetime(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_datetime.append(wrapper)
        return wrapper

    def receive_three_date_times(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_date_times.append(wrapper)
        return wrapper

    def receive_single_duration(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_duration.append(wrapper)
        return wrapper

    def receive_single_optional_duration(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_duration.append(wrapper)
        return wrapper

    def receive_three_durations(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_durations.append(wrapper)
        return wrapper

    def receive_single_binary(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_binary.append(wrapper)
        return wrapper

    def receive_single_optional_binary(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_binary.append(wrapper)
        return wrapper

    def receive_three_binaries(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_three_binaries.append(wrapper)
        return wrapper

    def receive_single_array_of_integers(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_array_of_integers.append(wrapper)
        return wrapper

    def receive_single_optional_array_of_strings(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_single_optional_array_of_strings.append(wrapper)
        return wrapper

    def receive_array_of_every_type(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_array_of_every_type.append(wrapper)
        return wrapper

    def read_write_integer_updated(self, handler: ReadWriteIntegerPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_integer.append(wrapper)
        return wrapper

    def read_only_integer_updated(self, handler: ReadOnlyIntegerPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_only_integer.append(wrapper)
        return wrapper

    def read_write_optional_integer_updated(self, handler: ReadWriteOptionalIntegerPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_integer.append(wrapper)
        return wrapper

    def read_write_two_integers_updated(self, handler: ReadWriteTwoIntegersPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_integers.append(wrapper)
        return wrapper

    def read_only_string_updated(self, handler: ReadOnlyStringPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_only_string.append(wrapper)
        return wrapper

    def read_write_string_updated(self, handler: ReadWriteStringPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_string.append(wrapper)
        return wrapper

    def read_write_optional_string_updated(self, handler: ReadWriteOptionalStringPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_string.append(wrapper)
        return wrapper

    def read_write_two_strings_updated(self, handler: ReadWriteTwoStringsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_strings.append(wrapper)
        return wrapper

    def read_write_struct_updated(self, handler: ReadWriteStructPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_struct.append(wrapper)
        return wrapper

    def read_write_optional_struct_updated(self, handler: ReadWriteOptionalStructPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_struct.append(wrapper)
        return wrapper

    def read_write_two_structs_updated(self, handler: ReadWriteTwoStructsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_structs.append(wrapper)
        return wrapper

    def read_only_enum_updated(self, handler: ReadOnlyEnumPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_only_enum.append(wrapper)
        return wrapper

    def read_write_enum_updated(self, handler: ReadWriteEnumPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_enum.append(wrapper)
        return wrapper

    def read_write_optional_enum_updated(self, handler: ReadWriteOptionalEnumPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_enum.append(wrapper)
        return wrapper

    def read_write_two_enums_updated(self, handler: ReadWriteTwoEnumsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_enums.append(wrapper)
        return wrapper

    def read_write_datetime_updated(self, handler: ReadWriteDatetimePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_datetime.append(wrapper)
        return wrapper

    def read_write_optional_datetime_updated(self, handler: ReadWriteOptionalDatetimePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_datetime.append(wrapper)
        return wrapper

    def read_write_two_datetimes_updated(self, handler: ReadWriteTwoDatetimesPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_datetimes.append(wrapper)
        return wrapper

    def read_write_duration_updated(self, handler: ReadWriteDurationPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_duration.append(wrapper)
        return wrapper

    def read_write_optional_duration_updated(self, handler: ReadWriteOptionalDurationPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_duration.append(wrapper)
        return wrapper

    def read_write_two_durations_updated(self, handler: ReadWriteTwoDurationsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_durations.append(wrapper)
        return wrapper

    def read_write_binary_updated(self, handler: ReadWriteBinaryPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_binary.append(wrapper)
        return wrapper

    def read_write_optional_binary_updated(self, handler: ReadWriteOptionalBinaryPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_optional_binary.append(wrapper)
        return wrapper

    def read_write_two_binaries_updated(self, handler: ReadWriteTwoBinariesPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_two_binaries.append(wrapper)
        return wrapper

    def read_write_list_of_strings_updated(self, handler: ReadWriteListOfStringsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_list_of_strings.append(wrapper)
        return wrapper

    def read_write_lists_updated(self, handler: ReadWriteListsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_read_write_lists.append(wrapper)
        return wrapper

    def build(self, broker: IBrokerConnection, instance_info: DiscoveredInstance, binding: Optional[Any] = None) -> TestableClient:
        """Builds a new TestableClient."""
        self._logger.debug("Building TestableClient for service instance %s", instance_info.instance_id)
        client = TestableClient(broker, instance_info)

        for empty_cb in self._signal_recv_callbacks_for_empty:
            if binding:
                client.receive_empty(empty_cb.__get__(binding, binding.__class__))
            else:
                client.receive_empty(empty_cb)

        for single_int_cb in self._signal_recv_callbacks_for_single_int:
            if binding:
                client.receive_single_int(single_int_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_int(single_int_cb)

        for single_optional_int_cb in self._signal_recv_callbacks_for_single_optional_int:
            if binding:
                client.receive_single_optional_int(single_optional_int_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_int(single_optional_int_cb)

        for three_integers_cb in self._signal_recv_callbacks_for_three_integers:
            if binding:
                client.receive_three_integers(three_integers_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_integers(three_integers_cb)

        for single_string_cb in self._signal_recv_callbacks_for_single_string:
            if binding:
                client.receive_single_string(single_string_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_string(single_string_cb)

        for single_optional_string_cb in self._signal_recv_callbacks_for_single_optional_string:
            if binding:
                client.receive_single_optional_string(single_optional_string_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_string(single_optional_string_cb)

        for three_strings_cb in self._signal_recv_callbacks_for_three_strings:
            if binding:
                client.receive_three_strings(three_strings_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_strings(three_strings_cb)

        for single_enum_cb in self._signal_recv_callbacks_for_single_enum:
            if binding:
                client.receive_single_enum(single_enum_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_enum(single_enum_cb)

        for single_optional_enum_cb in self._signal_recv_callbacks_for_single_optional_enum:
            if binding:
                client.receive_single_optional_enum(single_optional_enum_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_enum(single_optional_enum_cb)

        for three_enums_cb in self._signal_recv_callbacks_for_three_enums:
            if binding:
                client.receive_three_enums(three_enums_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_enums(three_enums_cb)

        for single_struct_cb in self._signal_recv_callbacks_for_single_struct:
            if binding:
                client.receive_single_struct(single_struct_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_struct(single_struct_cb)

        for single_optional_struct_cb in self._signal_recv_callbacks_for_single_optional_struct:
            if binding:
                client.receive_single_optional_struct(single_optional_struct_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_struct(single_optional_struct_cb)

        for three_structs_cb in self._signal_recv_callbacks_for_three_structs:
            if binding:
                client.receive_three_structs(three_structs_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_structs(three_structs_cb)

        for single_date_time_cb in self._signal_recv_callbacks_for_single_date_time:
            if binding:
                client.receive_single_date_time(single_date_time_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_date_time(single_date_time_cb)

        for single_optional_datetime_cb in self._signal_recv_callbacks_for_single_optional_datetime:
            if binding:
                client.receive_single_optional_datetime(single_optional_datetime_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_datetime(single_optional_datetime_cb)

        for three_date_times_cb in self._signal_recv_callbacks_for_three_date_times:
            if binding:
                client.receive_three_date_times(three_date_times_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_date_times(three_date_times_cb)

        for single_duration_cb in self._signal_recv_callbacks_for_single_duration:
            if binding:
                client.receive_single_duration(single_duration_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_duration(single_duration_cb)

        for single_optional_duration_cb in self._signal_recv_callbacks_for_single_optional_duration:
            if binding:
                client.receive_single_optional_duration(single_optional_duration_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_duration(single_optional_duration_cb)

        for three_durations_cb in self._signal_recv_callbacks_for_three_durations:
            if binding:
                client.receive_three_durations(three_durations_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_durations(three_durations_cb)

        for single_binary_cb in self._signal_recv_callbacks_for_single_binary:
            if binding:
                client.receive_single_binary(single_binary_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_binary(single_binary_cb)

        for single_optional_binary_cb in self._signal_recv_callbacks_for_single_optional_binary:
            if binding:
                client.receive_single_optional_binary(single_optional_binary_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_binary(single_optional_binary_cb)

        for three_binaries_cb in self._signal_recv_callbacks_for_three_binaries:
            if binding:
                client.receive_three_binaries(three_binaries_cb.__get__(binding, binding.__class__))
            else:
                client.receive_three_binaries(three_binaries_cb)

        for single_array_of_integers_cb in self._signal_recv_callbacks_for_single_array_of_integers:
            if binding:
                client.receive_single_array_of_integers(single_array_of_integers_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_array_of_integers(single_array_of_integers_cb)

        for single_optional_array_of_strings_cb in self._signal_recv_callbacks_for_single_optional_array_of_strings:
            if binding:
                client.receive_single_optional_array_of_strings(single_optional_array_of_strings_cb.__get__(binding, binding.__class__))
            else:
                client.receive_single_optional_array_of_strings(single_optional_array_of_strings_cb)

        for array_of_every_type_cb in self._signal_recv_callbacks_for_array_of_every_type:
            if binding:
                client.receive_array_of_every_type(array_of_every_type_cb.__get__(binding, binding.__class__))
            else:
                client.receive_array_of_every_type(array_of_every_type_cb)

        for read_write_integer_cb in self._property_updated_callbacks_for_read_write_integer:
            if binding:
                client.read_write_integer_changed(read_write_integer_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_integer_changed(read_write_integer_cb)

        for read_only_integer_cb in self._property_updated_callbacks_for_read_only_integer:
            if binding:
                client.read_only_integer_changed(read_only_integer_cb.__get__(binding, binding.__class__))
            else:
                client.read_only_integer_changed(read_only_integer_cb)

        for read_write_optional_integer_cb in self._property_updated_callbacks_for_read_write_optional_integer:
            if binding:
                client.read_write_optional_integer_changed(read_write_optional_integer_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_integer_changed(read_write_optional_integer_cb)

        for read_write_two_integers_cb in self._property_updated_callbacks_for_read_write_two_integers:
            if binding:
                client.read_write_two_integers_changed(read_write_two_integers_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_integers_changed(read_write_two_integers_cb)

        for read_only_string_cb in self._property_updated_callbacks_for_read_only_string:
            if binding:
                client.read_only_string_changed(read_only_string_cb.__get__(binding, binding.__class__))
            else:
                client.read_only_string_changed(read_only_string_cb)

        for read_write_string_cb in self._property_updated_callbacks_for_read_write_string:
            if binding:
                client.read_write_string_changed(read_write_string_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_string_changed(read_write_string_cb)

        for read_write_optional_string_cb in self._property_updated_callbacks_for_read_write_optional_string:
            if binding:
                client.read_write_optional_string_changed(read_write_optional_string_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_string_changed(read_write_optional_string_cb)

        for read_write_two_strings_cb in self._property_updated_callbacks_for_read_write_two_strings:
            if binding:
                client.read_write_two_strings_changed(read_write_two_strings_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_strings_changed(read_write_two_strings_cb)

        for read_write_struct_cb in self._property_updated_callbacks_for_read_write_struct:
            if binding:
                client.read_write_struct_changed(read_write_struct_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_struct_changed(read_write_struct_cb)

        for read_write_optional_struct_cb in self._property_updated_callbacks_for_read_write_optional_struct:
            if binding:
                client.read_write_optional_struct_changed(read_write_optional_struct_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_struct_changed(read_write_optional_struct_cb)

        for read_write_two_structs_cb in self._property_updated_callbacks_for_read_write_two_structs:
            if binding:
                client.read_write_two_structs_changed(read_write_two_structs_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_structs_changed(read_write_two_structs_cb)

        for read_only_enum_cb in self._property_updated_callbacks_for_read_only_enum:
            if binding:
                client.read_only_enum_changed(read_only_enum_cb.__get__(binding, binding.__class__))
            else:
                client.read_only_enum_changed(read_only_enum_cb)

        for read_write_enum_cb in self._property_updated_callbacks_for_read_write_enum:
            if binding:
                client.read_write_enum_changed(read_write_enum_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_enum_changed(read_write_enum_cb)

        for read_write_optional_enum_cb in self._property_updated_callbacks_for_read_write_optional_enum:
            if binding:
                client.read_write_optional_enum_changed(read_write_optional_enum_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_enum_changed(read_write_optional_enum_cb)

        for read_write_two_enums_cb in self._property_updated_callbacks_for_read_write_two_enums:
            if binding:
                client.read_write_two_enums_changed(read_write_two_enums_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_enums_changed(read_write_two_enums_cb)

        for read_write_datetime_cb in self._property_updated_callbacks_for_read_write_datetime:
            if binding:
                client.read_write_datetime_changed(read_write_datetime_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_datetime_changed(read_write_datetime_cb)

        for read_write_optional_datetime_cb in self._property_updated_callbacks_for_read_write_optional_datetime:
            if binding:
                client.read_write_optional_datetime_changed(read_write_optional_datetime_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_datetime_changed(read_write_optional_datetime_cb)

        for read_write_two_datetimes_cb in self._property_updated_callbacks_for_read_write_two_datetimes:
            if binding:
                client.read_write_two_datetimes_changed(read_write_two_datetimes_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_datetimes_changed(read_write_two_datetimes_cb)

        for read_write_duration_cb in self._property_updated_callbacks_for_read_write_duration:
            if binding:
                client.read_write_duration_changed(read_write_duration_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_duration_changed(read_write_duration_cb)

        for read_write_optional_duration_cb in self._property_updated_callbacks_for_read_write_optional_duration:
            if binding:
                client.read_write_optional_duration_changed(read_write_optional_duration_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_duration_changed(read_write_optional_duration_cb)

        for read_write_two_durations_cb in self._property_updated_callbacks_for_read_write_two_durations:
            if binding:
                client.read_write_two_durations_changed(read_write_two_durations_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_durations_changed(read_write_two_durations_cb)

        for read_write_binary_cb in self._property_updated_callbacks_for_read_write_binary:
            if binding:
                client.read_write_binary_changed(read_write_binary_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_binary_changed(read_write_binary_cb)

        for read_write_optional_binary_cb in self._property_updated_callbacks_for_read_write_optional_binary:
            if binding:
                client.read_write_optional_binary_changed(read_write_optional_binary_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_optional_binary_changed(read_write_optional_binary_cb)

        for read_write_two_binaries_cb in self._property_updated_callbacks_for_read_write_two_binaries:
            if binding:
                client.read_write_two_binaries_changed(read_write_two_binaries_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_two_binaries_changed(read_write_two_binaries_cb)

        for read_write_list_of_strings_cb in self._property_updated_callbacks_for_read_write_list_of_strings:
            if binding:
                client.read_write_list_of_strings_changed(read_write_list_of_strings_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_list_of_strings_changed(read_write_list_of_strings_cb)

        for read_write_lists_cb in self._property_updated_callbacks_for_read_write_lists:
            if binding:
                client.read_write_lists_changed(read_write_lists_cb.__get__(binding, binding.__class__))
            else:
                client.read_write_lists_changed(read_write_lists_cb)

        return client


class TestableClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[TestableClientBuilder] = None, build_binding: Optional[Any] = None):
        """Creates a new TestableClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._build_binding = build_binding
        self._logger = logging.getLogger("TestableClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "testable/{}/interface".format("+")
        self._conn.subscribe(service_discovery_topic, self._process_service_discovery_message)
        self._conn.subscribe("testable/+/property/+/value", self._process_property_value_message)
        self._mutex = threading.Lock()
        self._pending_futures: List[futures.Future] = []
        self._removed_service_callbacks: List[Callable[[str], None]] = []

        # For partially discovered services
        self._discovered_interface_infos = dict()  # type: Dict[str, InterfaceInfo]
        self._discovered_properties = dict()  # type: Dict[str, Dict[str, Any]]

        # For fully discovered services
        self._discovered_services: Dict[str, DiscoveredInstance] = {}
        self._discovered_service_callbacks: List[Callable[[DiscoveredInstance], None]] = []

    def add_discovered_service_callback(self, callback: Callable[[DiscoveredInstance], None]):
        """Adds a callback to be called when a new service is discovered."""
        with self._mutex:
            for instance in self._discovered_services.values():
                callback(instance)
            self._discovered_service_callbacks.append(callback)

    def add_removed_service_callback(self, callback: Callable[[str], None]):
        """Adds a callback to be called when a service is removed."""
        with self._mutex:
            self._removed_service_callbacks.append(callback)

    def get_service_instance_ids(self) -> List[str]:
        """Returns a list of currently discovered service instance IDs."""
        with self._mutex:
            return list(self._discovered_services.keys())

    def get_discovery_info(self, instance_id: str) -> Optional[DiscoveredInstance]:
        """Returns the DiscoveredInstance for a discovered service instance ID, or None if not found."""
        with self._mutex:
            return self._discovered_services.get(instance_id, None)

    def get_singleton_client(self) -> futures.Future[TestableClient]:
        """Returns a TestableClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()  # type: futures.Future[TestableClient]
        with self._mutex:
            if len(self._discovered_services) > 0:
                instance_info = next(iter(self._discovered_services.values()))
                if self._builder is None:
                    fut.set_result(TestableClient(self._conn, instance_info))
                else:
                    new_client = self._builder.build(self._conn, instance_info, self._build_binding)
                    fut.set_result(new_client)
            else:
                self._pending_futures.append(fut)
        return fut

    def _check_for_fully_discovered(self, instance_id: str):
        """Checks if all properties have been discovered for the given instance ID."""
        with self._mutex:
            if instance_id in self._discovered_properties and len(self._discovered_properties[instance_id]) == 52 and instance_id in self._discovered_interface_infos:

                entry = DiscoveredInstance(instance_id=instance_id, initial_property_values=TestableInitialPropertyValues(**self._discovered_properties[instance_id]))
                is_new_entry = not instance_id in self._discovered_services

                self._discovered_services[instance_id] = entry
                while self._pending_futures:
                    self._logger.info("Creating a client object id=%s and returning as future result", instance_id)
                    fut = self._pending_futures.pop(0)
                    if not fut.done():
                        if self._builder is not None:
                            fut.set_result(self._builder.build(self._conn, entry, self._build_binding))
                        else:
                            fut.set_result(TestableClient(self._conn, entry))
                if is_new_entry:
                    self._logger.info("Discovered service: %s", instance_id)
                    for cb in self._discovered_service_callbacks:
                        cb(entry)
                else:
                    self._logger.debug("Updated info for service: %s", instance_id)

    def _process_service_discovery_message(self, message: Message):
        """Processes a service discovery message."""
        self._logger.debug("Processing service discovery message on topic %s", message.topic)
        if len(message.payload) > 0:
            try:
                service_info = InterfaceInfo.model_validate_json(message.payload)
                with self._mutex:
                    self._discovered_interface_infos[service_info.instance] = service_info
            except Exception as e:
                self._logger.warning("Failed to process service discovery message: %s", e)
            self._check_for_fully_discovered(service_info.instance)

        else:  # Empty payload means the service is going away
            instance_id = message.topic.split("/")[-2]
            with self._mutex:
                if instance_id in self._discovered_services:
                    self._logger.info("Service %s is going away", instance_id)
                    if instance_id in self._discovered_services:
                        del self._discovered_services[instance_id]
                    if instance_id in self._discovered_interface_infos:
                        del self._discovered_interface_infos[instance_id]
                    if instance_id in self._discovered_properties:
                        del self._discovered_properties[instance_id]
                    for cb in self._removed_service_callbacks:
                        cb(instance_id)

    def _process_property_value_message(self, message: Message):
        """Processes a property value message for discovery purposes."""
        self._logger.debug("Processing property value message on topic %s", message.topic)
        instance_id = message.topic.split("/")[1]
        property_name = message.topic.split("/")[3]
        user_properties = message.user_properties or {}
        prop_version = user_properties.get("PropertyVersion", "-1")
        try:
            prop_obj = json.loads(message.payload)
            with self._mutex:
                if instance_id not in self._discovered_properties:
                    self._discovered_properties[instance_id] = dict()

                if property_name == "readWriteInteger":

                    self._discovered_properties[instance_id]["read_write_integer"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_integer_version"] = prop_version

                elif property_name == "readOnlyInteger":

                    self._discovered_properties[instance_id]["read_only_integer"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_only_integer_version"] = prop_version

                elif property_name == "readWriteOptionalInteger":

                    self._discovered_properties[instance_id]["read_write_optional_integer"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_integer_version"] = prop_version

                elif property_name == "readWriteTwoIntegers":

                    self._discovered_properties[instance_id]["read_write_two_integers"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_integers_version"] = prop_version

                elif property_name == "readOnlyString":

                    self._discovered_properties[instance_id]["read_only_string"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_only_string_version"] = prop_version

                elif property_name == "readWriteString":

                    self._discovered_properties[instance_id]["read_write_string"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_string_version"] = prop_version

                elif property_name == "readWriteOptionalString":

                    self._discovered_properties[instance_id]["read_write_optional_string"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_string_version"] = prop_version

                elif property_name == "readWriteTwoStrings":

                    self._discovered_properties[instance_id]["read_write_two_strings"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_strings_version"] = prop_version

                elif property_name == "readWriteStruct":

                    self._discovered_properties[instance_id]["read_write_struct"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_struct_version"] = prop_version

                elif property_name == "readWriteOptionalStruct":

                    self._discovered_properties[instance_id]["read_write_optional_struct"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_struct_version"] = prop_version

                elif property_name == "readWriteTwoStructs":

                    self._discovered_properties[instance_id]["read_write_two_structs"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_structs_version"] = prop_version

                elif property_name == "readOnlyEnum":

                    self._discovered_properties[instance_id]["read_only_enum"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_only_enum_version"] = prop_version

                elif property_name == "readWriteEnum":

                    self._discovered_properties[instance_id]["read_write_enum"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_enum_version"] = prop_version

                elif property_name == "readWriteOptionalEnum":

                    self._discovered_properties[instance_id]["read_write_optional_enum"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_enum_version"] = prop_version

                elif property_name == "readWriteTwoEnums":

                    self._discovered_properties[instance_id]["read_write_two_enums"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_enums_version"] = prop_version

                elif property_name == "readWriteDatetime":

                    self._discovered_properties[instance_id]["read_write_datetime"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_datetime_version"] = prop_version

                elif property_name == "readWriteOptionalDatetime":

                    self._discovered_properties[instance_id]["read_write_optional_datetime"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_datetime_version"] = prop_version

                elif property_name == "readWriteTwoDatetimes":

                    self._discovered_properties[instance_id]["read_write_two_datetimes"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_datetimes_version"] = prop_version

                elif property_name == "readWriteDuration":

                    self._discovered_properties[instance_id]["read_write_duration"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_duration_version"] = prop_version

                elif property_name == "readWriteOptionalDuration":

                    self._discovered_properties[instance_id]["read_write_optional_duration"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_duration_version"] = prop_version

                elif property_name == "readWriteTwoDurations":

                    self._discovered_properties[instance_id]["read_write_two_durations"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_durations_version"] = prop_version

                elif property_name == "readWriteBinary":

                    self._discovered_properties[instance_id]["read_write_binary"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_binary_version"] = prop_version

                elif property_name == "readWriteOptionalBinary":

                    self._discovered_properties[instance_id]["read_write_optional_binary"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_optional_binary_version"] = prop_version

                elif property_name == "readWriteTwoBinaries":

                    self._discovered_properties[instance_id]["read_write_two_binaries"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_two_binaries_version"] = prop_version

                elif property_name == "readWriteListOfStrings":

                    self._discovered_properties[instance_id]["read_write_list_of_strings"] = prop_obj.get("value")

                    self._discovered_properties[instance_id]["read_write_list_of_strings_version"] = prop_version

                elif property_name == "readWriteLists":

                    self._discovered_properties[instance_id]["read_write_lists"] = prop_obj

                    self._discovered_properties[instance_id]["read_write_lists_version"] = prop_version

            self._check_for_fully_discovered(instance_id)

        except Exception as e:
            self._logger.warning("Failed to process property value message: %s", e)
