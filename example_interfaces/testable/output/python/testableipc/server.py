"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Test Able interface.
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
import isodate

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from connection import IBrokerConnection
from method_codes import *
from interface_types import *
import interface_types as stinger_types


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T | None = None
    mutex = threading.Lock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
    callback: Optional[Callable] = None


class TestAbleServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str):
        self._logger = logging.getLogger(f"TestAbleServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing TestAbleServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_read_write_integer: PropertyControls[int, int] = PropertyControls()
        self._property_read_write_integer.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteInteger/setValue".format(self._instance_id), self._receive_read_write_integer_update_request_message
        )

        self._property_read_only_integer: PropertyControls[int, int] = PropertyControls()
        self._property_read_only_integer.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readOnlyInteger/setValue".format(self._instance_id), self._receive_read_only_integer_update_request_message
        )

        self._property_read_write_optional_integer: PropertyControls[int, Optional[int]] = PropertyControls()
        self._property_read_write_optional_integer.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalInteger/setValue".format(self._instance_id), self._receive_read_write_optional_integer_update_request_message
        )

        self._property_read_write_two_integers: PropertyControls[stinger_types.ReadWriteTwoIntegersProperty, int, Optional[int]] = PropertyControls()
        self._property_read_write_two_integers.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoIntegers/setValue".format(self._instance_id), self._receive_read_write_two_integers_update_request_message
        )

        self._property_read_only_string: PropertyControls[str, str] = PropertyControls()
        self._property_read_only_string.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readOnlyString/setValue".format(self._instance_id), self._receive_read_only_string_update_request_message
        )

        self._property_read_write_string: PropertyControls[str, str] = PropertyControls()
        self._property_read_write_string.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteString/setValue".format(self._instance_id), self._receive_read_write_string_update_request_message
        )

        self._property_read_write_optional_string: PropertyControls[str, Optional[str]] = PropertyControls()
        self._property_read_write_optional_string.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalString/setValue".format(self._instance_id), self._receive_read_write_optional_string_update_request_message
        )

        self._property_read_write_two_strings: PropertyControls[stinger_types.ReadWriteTwoStringsProperty, str, Optional[str]] = PropertyControls()
        self._property_read_write_two_strings.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoStrings/setValue".format(self._instance_id), self._receive_read_write_two_strings_update_request_message
        )

        self._property_read_write_struct: PropertyControls[stinger_types.AllTypes, stinger_types.AllTypes] = PropertyControls()
        self._property_read_write_struct.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteStruct/setValue".format(self._instance_id), self._receive_read_write_struct_update_request_message
        )

        self._property_read_write_optional_struct: PropertyControls[stinger_types.AllTypes, stinger_types.AllTypes] = PropertyControls()
        self._property_read_write_optional_struct.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalStruct/setValue".format(self._instance_id), self._receive_read_write_optional_struct_update_request_message
        )

        self._property_read_write_two_structs: PropertyControls[stinger_types.ReadWriteTwoStructsProperty, stinger_types.AllTypes, stinger_types.AllTypes] = PropertyControls()
        self._property_read_write_two_structs.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoStructs/setValue".format(self._instance_id), self._receive_read_write_two_structs_update_request_message
        )

        self._property_read_only_enum: PropertyControls[stinger_types.Numbers, stinger_types.Numbers] = PropertyControls()
        self._property_read_only_enum.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readOnlyEnum/setValue".format(self._instance_id), self._receive_read_only_enum_update_request_message
        )

        self._property_read_write_enum: PropertyControls[stinger_types.Numbers, stinger_types.Numbers] = PropertyControls()
        self._property_read_write_enum.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteEnum/setValue".format(self._instance_id), self._receive_read_write_enum_update_request_message
        )

        self._property_read_write_optional_enum: PropertyControls[stinger_types.Numbers, Optional[stinger_types.Numbers]] = PropertyControls()
        self._property_read_write_optional_enum.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalEnum/setValue".format(self._instance_id), self._receive_read_write_optional_enum_update_request_message
        )

        self._property_read_write_two_enums: PropertyControls[stinger_types.ReadWriteTwoEnumsProperty, stinger_types.Numbers, Optional[stinger_types.Numbers]] = PropertyControls()
        self._property_read_write_two_enums.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoEnums/setValue".format(self._instance_id), self._receive_read_write_two_enums_update_request_message
        )

        self._property_read_write_datetime: PropertyControls[datetime.datetime, datetime] = PropertyControls()
        self._property_read_write_datetime.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteDatetime/setValue".format(self._instance_id), self._receive_read_write_datetime_update_request_message
        )

        self._property_read_write_optional_datetime: PropertyControls[datetime.datetime, Optional[datetime]] = PropertyControls()
        self._property_read_write_optional_datetime.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalDatetime/setValue".format(self._instance_id), self._receive_read_write_optional_datetime_update_request_message
        )

        self._property_read_write_two_datetimes: PropertyControls[stinger_types.ReadWriteTwoDatetimesProperty, datetime, Optional[datetime]] = PropertyControls()
        self._property_read_write_two_datetimes.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoDatetimes/setValue".format(self._instance_id), self._receive_read_write_two_datetimes_update_request_message
        )

        self._property_read_write_duration: PropertyControls[datetime.timedelta, timedelta] = PropertyControls()
        self._property_read_write_duration.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteDuration/setValue".format(self._instance_id), self._receive_read_write_duration_update_request_message
        )

        self._property_read_write_optional_duration: PropertyControls[datetime.timedelta, Optional[timedelta]] = PropertyControls()
        self._property_read_write_optional_duration.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalDuration/setValue".format(self._instance_id), self._receive_read_write_optional_duration_update_request_message
        )

        self._property_read_write_two_durations: PropertyControls[stinger_types.ReadWriteTwoDurationsProperty, timedelta, Optional[timedelta]] = PropertyControls()
        self._property_read_write_two_durations.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoDurations/setValue".format(self._instance_id), self._receive_read_write_two_durations_update_request_message
        )

        self._property_read_write_binary: PropertyControls[bytes, bytes] = PropertyControls()
        self._property_read_write_binary.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteBinary/setValue".format(self._instance_id), self._receive_read_write_binary_update_request_message
        )

        self._property_read_write_optional_binary: PropertyControls[bytes, bytes] = PropertyControls()
        self._property_read_write_optional_binary.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteOptionalBinary/setValue".format(self._instance_id), self._receive_read_write_optional_binary_update_request_message
        )

        self._property_read_write_two_binaries: PropertyControls[stinger_types.ReadWriteTwoBinariesProperty, bytes, bytes] = PropertyControls()
        self._property_read_write_two_binaries.subscription_id = self._conn.subscribe(
            "testAble/{}/property/readWriteTwoBinaries/setValue".format(self._instance_id), self._receive_read_write_two_binaries_update_request_message
        )

        self._method_call_with_nothing = MethodControls()
        self._method_call_with_nothing.subscription_id = self._conn.subscribe("testAble/{}/method/callWithNothing".format(self._instance_id), self._process_call_with_nothing_call)

        self._method_call_one_integer = MethodControls()
        self._method_call_one_integer.subscription_id = self._conn.subscribe("testAble/{}/method/callOneInteger".format(self._instance_id), self._process_call_one_integer_call)

        self._method_call_optional_integer = MethodControls()
        self._method_call_optional_integer.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalInteger".format(self._instance_id), self._process_call_optional_integer_call)

        self._method_call_three_integers = MethodControls()
        self._method_call_three_integers.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeIntegers".format(self._instance_id), self._process_call_three_integers_call)

        self._method_call_one_string = MethodControls()
        self._method_call_one_string.subscription_id = self._conn.subscribe("testAble/{}/method/callOneString".format(self._instance_id), self._process_call_one_string_call)

        self._method_call_optional_string = MethodControls()
        self._method_call_optional_string.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalString".format(self._instance_id), self._process_call_optional_string_call)

        self._method_call_three_strings = MethodControls()
        self._method_call_three_strings.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeStrings".format(self._instance_id), self._process_call_three_strings_call)

        self._method_call_one_enum = MethodControls()
        self._method_call_one_enum.subscription_id = self._conn.subscribe("testAble/{}/method/callOneEnum".format(self._instance_id), self._process_call_one_enum_call)

        self._method_call_optional_enum = MethodControls()
        self._method_call_optional_enum.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalEnum".format(self._instance_id), self._process_call_optional_enum_call)

        self._method_call_three_enums = MethodControls()
        self._method_call_three_enums.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeEnums".format(self._instance_id), self._process_call_three_enums_call)

        self._method_call_one_struct = MethodControls()
        self._method_call_one_struct.subscription_id = self._conn.subscribe("testAble/{}/method/callOneStruct".format(self._instance_id), self._process_call_one_struct_call)

        self._method_call_optional_struct = MethodControls()
        self._method_call_optional_struct.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalStruct".format(self._instance_id), self._process_call_optional_struct_call)

        self._method_call_three_structs = MethodControls()
        self._method_call_three_structs.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeStructs".format(self._instance_id), self._process_call_three_structs_call)

        self._method_call_one_date_time = MethodControls()
        self._method_call_one_date_time.subscription_id = self._conn.subscribe("testAble/{}/method/callOneDateTime".format(self._instance_id), self._process_call_one_date_time_call)

        self._method_call_optional_date_time = MethodControls()
        self._method_call_optional_date_time.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalDateTime".format(self._instance_id), self._process_call_optional_date_time_call)

        self._method_call_three_date_times = MethodControls()
        self._method_call_three_date_times.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeDateTimes".format(self._instance_id), self._process_call_three_date_times_call)

        self._method_call_one_duration = MethodControls()
        self._method_call_one_duration.subscription_id = self._conn.subscribe("testAble/{}/method/callOneDuration".format(self._instance_id), self._process_call_one_duration_call)

        self._method_call_optional_duration = MethodControls()
        self._method_call_optional_duration.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalDuration".format(self._instance_id), self._process_call_optional_duration_call)

        self._method_call_three_durations = MethodControls()
        self._method_call_three_durations.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeDurations".format(self._instance_id), self._process_call_three_durations_call)

        self._method_call_one_binary = MethodControls()
        self._method_call_one_binary.subscription_id = self._conn.subscribe("testAble/{}/method/callOneBinary".format(self._instance_id), self._process_call_one_binary_call)

        self._method_call_optional_binary = MethodControls()
        self._method_call_optional_binary.subscription_id = self._conn.subscribe("testAble/{}/method/callOptionalBinary".format(self._instance_id), self._process_call_optional_binary_call)

        self._method_call_three_binaries = MethodControls()
        self._method_call_three_binaries.subscription_id = self._conn.subscribe("testAble/{}/method/callThreeBinaries".format(self._instance_id), self._process_call_three_binaries_call)

        self._advertise_thread = threading.Thread(target=self.loop_publishing_interface_info)
        self._advertise_thread.start()

    def __del__(self):
        self._running = False
        self._conn.unpublish_retained(self._conn.online_topic)
        self._advertise_thread.join()

    def loop_publishing_interface_info(self):
        while self._conn.is_connected() and self._running:
            self._publish_interface_info()
            sleep(self._re_advertise_server_interval_seconds)

    def _publish_interface_info(self):
        data = InterfaceInfo(instance=self._instance_id, connection_topic=self._conn.online_topic, timestamp=datetime.now(UTC).isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = "testAble/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json())
        self._conn.publish_status(topic, data, expiry)

    def _send_reply_error_message(self, return_code: MethodReturnCode, request_properties: Dict[str, Any], debug_info: Optional[str] = None):
        correlation_id = request_properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = request_properties.get("ResponseTopic")  # type: Optional[str]
        if response_topic is not None:
            self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_info)

    def _receive_read_write_integer_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["value"])
        with self._property_read_write_integer.mutex:
            self._property_read_write_integer.value = prop_value
            self._property_read_write_integer.version += 1
        for callback in self._property_read_write_integer.callbacks:
            callback(prop_value)

    def _receive_read_only_integer_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["value"])
        with self._property_read_only_integer.mutex:
            self._property_read_only_integer.value = prop_value
            self._property_read_only_integer.version += 1
        for callback in self._property_read_only_integer.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_integer_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["value"])
        with self._property_read_write_optional_integer.mutex:
            self._property_read_write_optional_integer.value = prop_value
            self._property_read_write_optional_integer.version += 1
        for callback in self._property_read_write_optional_integer.callbacks:
            callback(prop_value)

    def _receive_read_write_two_integers_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoIntegersProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_integers.mutex:
            self._property_read_write_two_integers.value = prop_value
            self._property_read_write_two_integers.version += 1
        for callback in self._property_read_write_two_integers.callbacks:
            callback(prop_value.first, prop_value.second)

    def _receive_read_only_string_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = str(payload_obj["value"])
        with self._property_read_only_string.mutex:
            self._property_read_only_string.value = prop_value
            self._property_read_only_string.version += 1
        for callback in self._property_read_only_string.callbacks:
            callback(prop_value)

    def _receive_read_write_string_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = str(payload_obj["value"])
        with self._property_read_write_string.mutex:
            self._property_read_write_string.value = prop_value
            self._property_read_write_string.version += 1
        for callback in self._property_read_write_string.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_string_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = str(payload_obj["value"])
        with self._property_read_write_optional_string.mutex:
            self._property_read_write_optional_string.value = prop_value
            self._property_read_write_optional_string.version += 1
        for callback in self._property_read_write_optional_string.callbacks:
            callback(prop_value)

    def _receive_read_write_two_strings_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoStringsProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_strings.mutex:
            self._property_read_write_two_strings.value = prop_value
            self._property_read_write_two_strings.version += 1
        for callback in self._property_read_write_two_strings.callbacks:
            callback(prop_value.first, prop_value.second)

    def _receive_read_write_struct_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = stinger_types.AllTypes(payload_obj["value"])
        with self._property_read_write_struct.mutex:
            self._property_read_write_struct.value = prop_value
            self._property_read_write_struct.version += 1
        for callback in self._property_read_write_struct.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_struct_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = stinger_types.AllTypes(payload_obj["value"])
        with self._property_read_write_optional_struct.mutex:
            self._property_read_write_optional_struct.value = prop_value
            self._property_read_write_optional_struct.version += 1
        for callback in self._property_read_write_optional_struct.callbacks:
            callback(prop_value)

    def _receive_read_write_two_structs_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoStructsProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_structs.mutex:
            self._property_read_write_two_structs.value = prop_value
            self._property_read_write_two_structs.version += 1
        for callback in self._property_read_write_two_structs.callbacks:
            callback(prop_value.first, prop_value.second)

    def _receive_read_only_enum_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = stinger_types.Numbers(payload_obj["value"])
        with self._property_read_only_enum.mutex:
            self._property_read_only_enum.value = prop_value
            self._property_read_only_enum.version += 1
        for callback in self._property_read_only_enum.callbacks:
            callback(prop_value)

    def _receive_read_write_enum_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = stinger_types.Numbers(payload_obj["value"])
        with self._property_read_write_enum.mutex:
            self._property_read_write_enum.value = prop_value
            self._property_read_write_enum.version += 1
        for callback in self._property_read_write_enum.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_enum_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = stinger_types.Numbers(payload_obj["value"])
        with self._property_read_write_optional_enum.mutex:
            self._property_read_write_optional_enum.value = prop_value
            self._property_read_write_optional_enum.version += 1
        for callback in self._property_read_write_optional_enum.callbacks:
            callback(prop_value)

    def _receive_read_write_two_enums_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoEnumsProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_enums.mutex:
            self._property_read_write_two_enums.value = prop_value
            self._property_read_write_two_enums.version += 1
        for callback in self._property_read_write_two_enums.callbacks:
            callback(prop_value.first, prop_value.second)

    def _receive_read_write_datetime_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = datetime.datetime(payload_obj["value"])
        with self._property_read_write_datetime.mutex:
            self._property_read_write_datetime.value = prop_value
            self._property_read_write_datetime.version += 1
        for callback in self._property_read_write_datetime.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_datetime_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = datetime.datetime(payload_obj["value"])
        with self._property_read_write_optional_datetime.mutex:
            self._property_read_write_optional_datetime.value = prop_value
            self._property_read_write_optional_datetime.version += 1
        for callback in self._property_read_write_optional_datetime.callbacks:
            callback(prop_value)

    def _receive_read_write_two_datetimes_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoDatetimesProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_datetimes.mutex:
            self._property_read_write_two_datetimes.value = prop_value
            self._property_read_write_two_datetimes.version += 1
        for callback in self._property_read_write_two_datetimes.callbacks:
            callback(prop_value.first, prop_value.second)

    def _receive_read_write_duration_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = datetime.timedelta(payload_obj["value"])
        with self._property_read_write_duration.mutex:
            self._property_read_write_duration.value = prop_value
            self._property_read_write_duration.version += 1
        for callback in self._property_read_write_duration.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_duration_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = datetime.timedelta(payload_obj["value"])
        with self._property_read_write_optional_duration.mutex:
            self._property_read_write_optional_duration.value = prop_value
            self._property_read_write_optional_duration.version += 1
        for callback in self._property_read_write_optional_duration.callbacks:
            callback(prop_value)

    def _receive_read_write_two_durations_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoDurationsProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_durations.mutex:
            self._property_read_write_two_durations.value = prop_value
            self._property_read_write_two_durations.version += 1
        for callback in self._property_read_write_two_durations.callbacks:
            callback(prop_value.first, prop_value.second)

    def _receive_read_write_binary_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = bytes(payload_obj["value"])
        with self._property_read_write_binary.mutex:
            self._property_read_write_binary.value = prop_value
            self._property_read_write_binary.version += 1
        for callback in self._property_read_write_binary.callbacks:
            callback(prop_value)

    def _receive_read_write_optional_binary_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = bytes(payload_obj["value"])
        with self._property_read_write_optional_binary.mutex:
            self._property_read_write_optional_binary.value = prop_value
            self._property_read_write_optional_binary.version += 1
        for callback in self._property_read_write_optional_binary.callbacks:
            callback(prop_value)

    def _receive_read_write_two_binaries_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = stinger_types.ReadWriteTwoBinariesProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_read_write_two_binaries.mutex:
            self._property_read_write_two_binaries.value = prop_value
            self._property_read_write_two_binaries.version += 1
        for callback in self._property_read_write_two_binaries.callbacks:
            callback(prop_value.first, prop_value.second)

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
        self._conn.publish("testAble/{}/signal/empty".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_int(self, value: int):
        """Server application code should call this method to emit the 'singleInt' signal.

        SingleIntSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleIntSignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleInt".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_int(self, value: Optional[int]):
        """Server application code should call this method to emit the 'singleOptionalInt' signal.

        SingleOptionalIntSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalIntSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalInt".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_integers(self, first: int, second: int, third: Optional[int]):
        """Server application code should call this method to emit the 'threeIntegers' signal.

        ThreeIntegersSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeIntegersSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeIntegers".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_string(self, value: str):
        """Server application code should call this method to emit the 'singleString' signal.

        SingleStringSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleStringSignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleString".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_string(self, value: Optional[str]):
        """Server application code should call this method to emit the 'singleOptionalString' signal.

        SingleOptionalStringSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalStringSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalString".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_strings(self, first: str, second: str, third: Optional[str]):
        """Server application code should call this method to emit the 'threeStrings' signal.

        ThreeStringsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeStringsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeStrings".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_enum(self, value: stinger_types.Numbers):
        """Server application code should call this method to emit the 'singleEnum' signal.

        SingleEnumSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleEnumSignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleEnum".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_enum(self, value: Optional[stinger_types.Numbers]):
        """Server application code should call this method to emit the 'singleOptionalEnum' signal.

        SingleOptionalEnumSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalEnumSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalEnum".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_enums(self, first: stinger_types.Numbers, second: stinger_types.Numbers, third: Optional[stinger_types.Numbers]):
        """Server application code should call this method to emit the 'threeEnums' signal.

        ThreeEnumsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeEnumsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeEnums".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_struct(self, value: stinger_types.AllTypes):
        """Server application code should call this method to emit the 'singleStruct' signal.

        SingleStructSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleStructSignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleStruct".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_struct(self, value: stinger_types.AllTypes):
        """Server application code should call this method to emit the 'singleOptionalStruct' signal.

        SingleOptionalStructSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalStructSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalStruct".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_structs(self, first: stinger_types.AllTypes, second: stinger_types.AllTypes, third: stinger_types.AllTypes):
        """Server application code should call this method to emit the 'threeStructs' signal.

        ThreeStructsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeStructsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeStructs".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_date_time(self, value: datetime):
        """Server application code should call this method to emit the 'singleDateTime' signal.

        SingleDateTimeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleDateTimeSignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleDateTime".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_datetime(self, value: Optional[datetime]):
        """Server application code should call this method to emit the 'singleOptionalDatetime' signal.

        SingleOptionalDatetimeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalDatetimeSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalDatetime".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_date_times(self, first: datetime, second: datetime, third: Optional[datetime]):
        """Server application code should call this method to emit the 'threeDateTimes' signal.

        ThreeDateTimesSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeDateTimesSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeDateTimes".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_duration(self, value: timedelta):
        """Server application code should call this method to emit the 'singleDuration' signal.

        SingleDurationSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleDurationSignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleDuration".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_duration(self, value: Optional[timedelta]):
        """Server application code should call this method to emit the 'singleOptionalDuration' signal.

        SingleOptionalDurationSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalDurationSignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalDuration".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_durations(self, first: timedelta, second: timedelta, third: Optional[timedelta]):
        """Server application code should call this method to emit the 'threeDurations' signal.

        ThreeDurationsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeDurationsSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeDurations".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_binary(self, value: bytes):
        """Server application code should call this method to emit the 'singleBinary' signal.

        SingleBinarySignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleBinarySignalPayload(
            value=value,
        )
        self._conn.publish("testAble/{}/signal/singleBinary".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_single_optional_binary(self, value: bytes):
        """Server application code should call this method to emit the 'singleOptionalBinary' signal.

        SingleOptionalBinarySignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = SingleOptionalBinarySignalPayload(
            value=value if value is not None else None,
        )
        self._conn.publish("testAble/{}/signal/singleOptionalBinary".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_three_binaries(self, first: bytes, second: bytes, third: bytes):
        """Server application code should call this method to emit the 'threeBinaries' signal.

        ThreeBinariesSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = ThreeBinariesSignalPayload(
            first=first,
            second=second,
            third=third if third is not None else None,
        )
        self._conn.publish("testAble/{}/signal/threeBinaries".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

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
                    return_struct = self._method_call_with_nothing.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

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
                    return_struct = self._method_call_one_integer.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct})
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
                    return_struct = self._method_call_optional_integer.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct})
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalInteger", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_integers(self, handler: Callable[[int, int, Optional[int]], stinger_types.CallThreeIntegersReturnValues]):
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
                    return_struct = self._method_call_three_integers.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

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
                    return_struct = self._method_call_one_string.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct})
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
                    return_struct = self._method_call_optional_string.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct})
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalString", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_strings(self, handler: Callable[[str, Optional[str], str], stinger_types.CallThreeStringsReturnValues]):
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
                    return_struct = self._method_call_three_strings.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling callThreeStrings", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_enum(self, handler: Callable[[stinger_types.Numbers], stinger_types.Numbers]):
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
                    return_struct = self._method_call_one_enum.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct.value})
                except Exception as e:
                    self._logger.exception("Exception while handling callOneEnum", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_enum(self, handler: Callable[[Optional[stinger_types.Numbers]], Optional[stinger_types.Numbers]]):
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
                    return_struct = self._method_call_optional_enum.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct.value})
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalEnum", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_enums(self, handler: Callable[[stinger_types.Numbers, stinger_types.Numbers, Optional[stinger_types.Numbers]], stinger_types.CallThreeEnumsReturnValues]):
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
                    return_struct = self._method_call_three_enums.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling callThreeEnums", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_one_struct(self, handler: Callable[[stinger_types.AllTypes], stinger_types.AllTypes]):
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
                    return_struct = self._method_call_one_struct.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling callOneStruct", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_optional_struct(self, handler: Callable[[stinger_types.AllTypes], stinger_types.AllTypes]):
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
                    return_struct = self._method_call_optional_struct.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalStruct", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_structs(self, handler: Callable[[stinger_types.AllTypes, stinger_types.AllTypes, stinger_types.AllTypes], stinger_types.CallThreeStructsReturnValues]):
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
                    return_struct = self._method_call_three_structs.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

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
                    return_struct = self._method_call_one_date_time.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct.isoformat()})
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
                    return_struct = self._method_call_optional_date_time.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": return_struct.isoformat()})
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalDateTime", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_date_times(self, handler: Callable[[datetime, datetime, Optional[datetime]], stinger_types.CallThreeDateTimesReturnValues]):
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
                    return_struct = self._method_call_three_date_times.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

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
                    return_struct = self._method_call_one_duration.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": isodate.duration_isoformat(return_struct)})
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
                    return_struct = self._method_call_optional_duration.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"output1": isodate.duration_isoformat(return_struct)})
                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalDuration", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_durations(self, handler: Callable[[timedelta, timedelta, Optional[timedelta]], stinger_types.CallThreeDurationsReturnValues]):
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
                    return_struct = self._method_call_three_durations.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

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
                    return_struct = self._method_call_one_binary.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        import base64

                        return_json = json.dumps({"output1": base64.b64encode(return_struct).decode("utf-8")})

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
                    return_struct = self._method_call_optional_binary.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        import base64

                        return_json = json.dumps({"output1": base64.b64encode(return_struct).decode("utf-8")})

                except Exception as e:
                    self._logger.exception("Exception while handling callOptionalBinary", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_call_three_binaries(self, handler: Callable[[bytes, bytes, bytes], stinger_types.CallThreeBinariesReturnValues]):
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
                    return_struct = self._method_call_three_binaries.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling callThreeBinaries", exc_info=e)
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
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_integer.value:
            with self._property_read_write_integer.mutex:
                self._property_read_write_integer.value = value
                self._property_read_write_integer.version += 1
            self._conn.publish("testAble/{}/property/readWriteInteger/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_integer.callbacks:
                callback(value)

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
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"value": value})

        if value != self._property_read_only_integer.value:
            with self._property_read_only_integer.mutex:
                self._property_read_only_integer.value = value
                self._property_read_only_integer.version += 1
            self._conn.publish("testAble/{}/property/readOnlyInteger/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_only_integer.callbacks:
                callback(value)

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
    def read_write_optional_integer(self) -> Optional[Optional[int]]:
        """This property returns the last received value for the 'read_write_optional_integer' property."""
        with self._property_read_write_optional_integer_mutex:
            return self._property_read_write_optional_integer

    @read_write_optional_integer.setter
    def read_write_optional_integer(self, value: Optional[int]):
        """This property sets (publishes) a new value for the 'read_write_optional_integer' property."""
        if not isinstance(value, int):
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_optional_integer.value:
            with self._property_read_write_optional_integer.mutex:
                self._property_read_write_optional_integer.value = value
                self._property_read_write_optional_integer.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalInteger/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_integer.callbacks:
                callback(value)

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
    def read_write_two_integers(self) -> Optional[stinger_types.ReadWriteTwoIntegersProperty]:
        """This property returns the last received value for the 'read_write_two_integers' property."""
        with self._property_read_write_two_integers_mutex:
            return self._property_read_write_two_integers

    @read_write_two_integers.setter
    def read_write_two_integers(self, value: stinger_types.ReadWriteTwoIntegersProperty):
        """This property sets (publishes) a new value for the 'read_write_two_integers' property."""
        if not isinstance(value, ReadWriteTwoIntegersProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoIntegersProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_integers.value:
            with self._property_read_write_two_integers.mutex:
                self._property_read_write_two_integers.value = value
                self._property_read_write_two_integers.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoIntegers/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_integers.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_integers(self, first: int, second: Optional[int]):
        """This method sets (publishes) a new value for the 'read_write_two_integers' property."""
        if not isinstance(first, int):
            raise ValueError(f"The 'first' value must be int.")
        if not isinstance(second, int) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[int].")

        obj = stinger_types.ReadWriteTwoIntegersProperty(
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
            raise ValueError(f"The value must be str.")

        payload = json.dumps({"value": value})

        if value != self._property_read_only_string.value:
            with self._property_read_only_string.mutex:
                self._property_read_only_string.value = value
                self._property_read_only_string.version += 1
            self._conn.publish("testAble/{}/property/readOnlyString/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_only_string.callbacks:
                callback(value)

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
            raise ValueError(f"The value must be str.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_string.value:
            with self._property_read_write_string.mutex:
                self._property_read_write_string.value = value
                self._property_read_write_string.version += 1
            self._conn.publish("testAble/{}/property/readWriteString/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_string.callbacks:
                callback(value)

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
    def read_write_optional_string(self) -> Optional[Optional[str]]:
        """This property returns the last received value for the 'read_write_optional_string' property."""
        with self._property_read_write_optional_string_mutex:
            return self._property_read_write_optional_string

    @read_write_optional_string.setter
    def read_write_optional_string(self, value: Optional[str]):
        """This property sets (publishes) a new value for the 'read_write_optional_string' property."""
        if not isinstance(value, str):
            raise ValueError(f"The value must be str.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_optional_string.value:
            with self._property_read_write_optional_string.mutex:
                self._property_read_write_optional_string.value = value
                self._property_read_write_optional_string.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalString/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_string.callbacks:
                callback(value)

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
    def read_write_two_strings(self) -> Optional[stinger_types.ReadWriteTwoStringsProperty]:
        """This property returns the last received value for the 'read_write_two_strings' property."""
        with self._property_read_write_two_strings_mutex:
            return self._property_read_write_two_strings

    @read_write_two_strings.setter
    def read_write_two_strings(self, value: stinger_types.ReadWriteTwoStringsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_strings' property."""
        if not isinstance(value, ReadWriteTwoStringsProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoStringsProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_strings.value:
            with self._property_read_write_two_strings.mutex:
                self._property_read_write_two_strings.value = value
                self._property_read_write_two_strings.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoStrings/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_strings.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_strings(self, first: str, second: Optional[str]):
        """This method sets (publishes) a new value for the 'read_write_two_strings' property."""
        if not isinstance(first, str):
            raise ValueError(f"The 'first' value must be str.")
        if not isinstance(second, str) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[str].")

        obj = stinger_types.ReadWriteTwoStringsProperty(
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
    def read_write_struct(self) -> Optional[stinger_types.AllTypes]:
        """This property returns the last received value for the 'read_write_struct' property."""
        with self._property_read_write_struct_mutex:
            return self._property_read_write_struct

    @read_write_struct.setter
    def read_write_struct(self, value: stinger_types.AllTypes):
        """This property sets (publishes) a new value for the 'read_write_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError(f"The value must be stinger_types.AllTypes.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_struct.value:
            with self._property_read_write_struct.mutex:
                self._property_read_write_struct.value = value
                self._property_read_write_struct.version += 1
            self._conn.publish("testAble/{}/property/readWriteStruct/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_struct.callbacks:
                callback(value)

    def set_read_write_struct(self, value: stinger_types.AllTypes):
        """This method sets (publishes) a new value for the 'read_write_struct' property."""
        if not isinstance(value, stinger_types.AllTypes):
            raise ValueError(f"The 'value' value must be stinger_types.AllTypes.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_struct = obj

    def on_read_write_struct_updates(self, handler: Callable[[stinger_types.AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_struct' property update is received."""
        if handler is not None:
            self._property_read_write_struct.callbacks.append(handler)

    @property
    def read_write_optional_struct(self) -> Optional[stinger_types.AllTypes]:
        """This property returns the last received value for the 'read_write_optional_struct' property."""
        with self._property_read_write_optional_struct_mutex:
            return self._property_read_write_optional_struct

    @read_write_optional_struct.setter
    def read_write_optional_struct(self, value: stinger_types.AllTypes):
        """This property sets (publishes) a new value for the 'read_write_optional_struct' property."""
        if not isinstance(value, AllTypes):
            raise ValueError(f"The value must be stinger_types.AllTypes.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_optional_struct.value:
            with self._property_read_write_optional_struct.mutex:
                self._property_read_write_optional_struct.value = value
                self._property_read_write_optional_struct.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalStruct/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_struct.callbacks:
                callback(value)

    def set_read_write_optional_struct(self, value: stinger_types.AllTypes):
        """This method sets (publishes) a new value for the 'read_write_optional_struct' property."""
        if not isinstance(value, stinger_types.AllTypes) and value is not None:
            raise ValueError(f"The 'value' value must be stinger_types.AllTypes.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_struct = obj

    def on_read_write_optional_struct_updates(self, handler: Callable[[stinger_types.AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_struct' property update is received."""
        if handler is not None:
            self._property_read_write_optional_struct.callbacks.append(handler)

    @property
    def read_write_two_structs(self) -> Optional[stinger_types.ReadWriteTwoStructsProperty]:
        """This property returns the last received value for the 'read_write_two_structs' property."""
        with self._property_read_write_two_structs_mutex:
            return self._property_read_write_two_structs

    @read_write_two_structs.setter
    def read_write_two_structs(self, value: stinger_types.ReadWriteTwoStructsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_structs' property."""
        if not isinstance(value, ReadWriteTwoStructsProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoStructsProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_structs.value:
            with self._property_read_write_two_structs.mutex:
                self._property_read_write_two_structs.value = value
                self._property_read_write_two_structs.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoStructs/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_structs.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_structs(self, first: stinger_types.AllTypes, second: stinger_types.AllTypes):
        """This method sets (publishes) a new value for the 'read_write_two_structs' property."""
        if not isinstance(first, stinger_types.AllTypes):
            raise ValueError(f"The 'first' value must be stinger_types.AllTypes.")
        if not isinstance(second, stinger_types.AllTypes) and second is not None:
            raise ValueError(f"The 'second' value must be stinger_types.AllTypes.")

        obj = stinger_types.ReadWriteTwoStructsProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_structs = obj

    def on_read_write_two_structs_updates(self, handler: Callable[[stinger_types.AllTypes, stinger_types.AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_structs' property update is received."""
        if handler is not None:
            self._property_read_write_two_structs.callbacks.append(handler)

    @property
    def read_only_enum(self) -> Optional[stinger_types.Numbers]:
        """This property returns the last received value for the 'read_only_enum' property."""
        with self._property_read_only_enum_mutex:
            return self._property_read_only_enum

    @read_only_enum.setter
    def read_only_enum(self, value: stinger_types.Numbers):
        """This property sets (publishes) a new value for the 'read_only_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError(f"The value must be stinger_types.Numbers.")

        payload = json.dumps({"value": value})

        if value != self._property_read_only_enum.value:
            with self._property_read_only_enum.mutex:
                self._property_read_only_enum.value = value
                self._property_read_only_enum.version += 1
            self._conn.publish("testAble/{}/property/readOnlyEnum/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_only_enum.callbacks:
                callback(value)

    def set_read_only_enum(self, value: stinger_types.Numbers):
        """This method sets (publishes) a new value for the 'read_only_enum' property."""
        if not isinstance(value, stinger_types.Numbers):
            raise ValueError(f"The 'value' value must be stinger_types.Numbers.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_only_enum = obj

    def on_read_only_enum_updates(self, handler: Callable[[stinger_types.Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_only_enum' property update is received."""
        if handler is not None:
            self._property_read_only_enum.callbacks.append(handler)

    @property
    def read_write_enum(self) -> Optional[stinger_types.Numbers]:
        """This property returns the last received value for the 'read_write_enum' property."""
        with self._property_read_write_enum_mutex:
            return self._property_read_write_enum

    @read_write_enum.setter
    def read_write_enum(self, value: stinger_types.Numbers):
        """This property sets (publishes) a new value for the 'read_write_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError(f"The value must be stinger_types.Numbers.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_enum.value:
            with self._property_read_write_enum.mutex:
                self._property_read_write_enum.value = value
                self._property_read_write_enum.version += 1
            self._conn.publish("testAble/{}/property/readWriteEnum/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_enum.callbacks:
                callback(value)

    def set_read_write_enum(self, value: stinger_types.Numbers):
        """This method sets (publishes) a new value for the 'read_write_enum' property."""
        if not isinstance(value, stinger_types.Numbers):
            raise ValueError(f"The 'value' value must be stinger_types.Numbers.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_enum = obj

    def on_read_write_enum_updates(self, handler: Callable[[stinger_types.Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_write_enum' property update is received."""
        if handler is not None:
            self._property_read_write_enum.callbacks.append(handler)

    @property
    def read_write_optional_enum(self) -> Optional[Optional[stinger_types.Numbers]]:
        """This property returns the last received value for the 'read_write_optional_enum' property."""
        with self._property_read_write_optional_enum_mutex:
            return self._property_read_write_optional_enum

    @read_write_optional_enum.setter
    def read_write_optional_enum(self, value: Optional[stinger_types.Numbers]):
        """This property sets (publishes) a new value for the 'read_write_optional_enum' property."""
        if not isinstance(value, Numbers):
            raise ValueError(f"The value must be stinger_types.Numbers.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_optional_enum.value:
            with self._property_read_write_optional_enum.mutex:
                self._property_read_write_optional_enum.value = value
                self._property_read_write_optional_enum.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalEnum/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_enum.callbacks:
                callback(value)

    def set_read_write_optional_enum(self, value: Optional[stinger_types.Numbers]):
        """This method sets (publishes) a new value for the 'read_write_optional_enum' property."""
        if not isinstance(value, stinger_types.Numbers) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[stinger_types.Numbers].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_enum = obj

    def on_read_write_optional_enum_updates(self, handler: Callable[[Optional[stinger_types.Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_enum' property update is received."""
        if handler is not None:
            self._property_read_write_optional_enum.callbacks.append(handler)

    @property
    def read_write_two_enums(self) -> Optional[stinger_types.ReadWriteTwoEnumsProperty]:
        """This property returns the last received value for the 'read_write_two_enums' property."""
        with self._property_read_write_two_enums_mutex:
            return self._property_read_write_two_enums

    @read_write_two_enums.setter
    def read_write_two_enums(self, value: stinger_types.ReadWriteTwoEnumsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_enums' property."""
        if not isinstance(value, ReadWriteTwoEnumsProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoEnumsProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_enums.value:
            with self._property_read_write_two_enums.mutex:
                self._property_read_write_two_enums.value = value
                self._property_read_write_two_enums.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoEnums/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_enums.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_enums(self, first: stinger_types.Numbers, second: Optional[stinger_types.Numbers]):
        """This method sets (publishes) a new value for the 'read_write_two_enums' property."""
        if not isinstance(first, stinger_types.Numbers):
            raise ValueError(f"The 'first' value must be stinger_types.Numbers.")
        if not isinstance(second, stinger_types.Numbers) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[stinger_types.Numbers].")

        obj = stinger_types.ReadWriteTwoEnumsProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_enums = obj

    def on_read_write_two_enums_updates(self, handler: Callable[[stinger_types.Numbers, Optional[stinger_types.Numbers]], None]):
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
            raise ValueError(f"The value must be datetime.datetime.")

        payload = json.dumps({"value": value.isoformat()})

        if value != self._property_read_write_datetime.value:
            with self._property_read_write_datetime.mutex:
                self._property_read_write_datetime.value = value
                self._property_read_write_datetime.version += 1
            self._conn.publish("testAble/{}/property/readWriteDatetime/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_datetime.callbacks:
                callback(value)

    def set_read_write_datetime(self, value: datetime):
        """This method sets (publishes) a new value for the 'read_write_datetime' property."""
        if not isinstance(value, datetime.datetime):
            raise ValueError(f"The 'value' value must be datetime.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_datetime = obj

    def on_read_write_datetime_updates(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'read_write_datetime' property update is received."""
        if handler is not None:
            self._property_read_write_datetime.callbacks.append(handler)

    @property
    def read_write_optional_datetime(self) -> Optional[Optional[datetime]]:
        """This property returns the last received value for the 'read_write_optional_datetime' property."""
        with self._property_read_write_optional_datetime_mutex:
            return self._property_read_write_optional_datetime

    @read_write_optional_datetime.setter
    def read_write_optional_datetime(self, value: Optional[datetime]):
        """This property sets (publishes) a new value for the 'read_write_optional_datetime' property."""
        if not isinstance(value, datetime):
            raise ValueError(f"The value must be datetime.datetime.")

        payload = json.dumps({"value": value.isoformat()})

        if value != self._property_read_write_optional_datetime.value:
            with self._property_read_write_optional_datetime.mutex:
                self._property_read_write_optional_datetime.value = value
                self._property_read_write_optional_datetime.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalDatetime/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_datetime.callbacks:
                callback(value)

    def set_read_write_optional_datetime(self, value: Optional[datetime]):
        """This method sets (publishes) a new value for the 'read_write_optional_datetime' property."""
        if not isinstance(value, datetime.datetime) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[datetime].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_datetime = obj

    def on_read_write_optional_datetime_updates(self, handler: Callable[[Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_datetime' property update is received."""
        if handler is not None:
            self._property_read_write_optional_datetime.callbacks.append(handler)

    @property
    def read_write_two_datetimes(self) -> Optional[stinger_types.ReadWriteTwoDatetimesProperty]:
        """This property returns the last received value for the 'read_write_two_datetimes' property."""
        with self._property_read_write_two_datetimes_mutex:
            return self._property_read_write_two_datetimes

    @read_write_two_datetimes.setter
    def read_write_two_datetimes(self, value: stinger_types.ReadWriteTwoDatetimesProperty):
        """This property sets (publishes) a new value for the 'read_write_two_datetimes' property."""
        if not isinstance(value, ReadWriteTwoDatetimesProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoDatetimesProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_datetimes.value:
            with self._property_read_write_two_datetimes.mutex:
                self._property_read_write_two_datetimes.value = value
                self._property_read_write_two_datetimes.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoDatetimes/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_datetimes.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_datetimes(self, first: datetime, second: Optional[datetime]):
        """This method sets (publishes) a new value for the 'read_write_two_datetimes' property."""
        if not isinstance(first, datetime.datetime):
            raise ValueError(f"The 'first' value must be datetime.")
        if not isinstance(second, datetime.datetime) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[datetime].")

        obj = stinger_types.ReadWriteTwoDatetimesProperty(
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
            raise ValueError(f"The value must be datetime.timedelta.")

        payload = json.dumps({"value": isodate.duration_isoformat(value)})

        if value != self._property_read_write_duration.value:
            with self._property_read_write_duration.mutex:
                self._property_read_write_duration.value = value
                self._property_read_write_duration.version += 1
            self._conn.publish("testAble/{}/property/readWriteDuration/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_duration.callbacks:
                callback(value)

    def set_read_write_duration(self, value: timedelta):
        """This method sets (publishes) a new value for the 'read_write_duration' property."""
        if not isinstance(value, datetime.timedelta):
            raise ValueError(f"The 'value' value must be timedelta.")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_duration = obj

    def on_read_write_duration_updates(self, handler: Callable[[timedelta], None]):
        """This method registers a callback to be called whenever a new 'read_write_duration' property update is received."""
        if handler is not None:
            self._property_read_write_duration.callbacks.append(handler)

    @property
    def read_write_optional_duration(self) -> Optional[Optional[timedelta]]:
        """This property returns the last received value for the 'read_write_optional_duration' property."""
        with self._property_read_write_optional_duration_mutex:
            return self._property_read_write_optional_duration

    @read_write_optional_duration.setter
    def read_write_optional_duration(self, value: Optional[timedelta]):
        """This property sets (publishes) a new value for the 'read_write_optional_duration' property."""
        if not isinstance(value, timedelta):
            raise ValueError(f"The value must be datetime.timedelta.")

        payload = json.dumps({"value": isodate.duration_isoformat(value)})

        if value != self._property_read_write_optional_duration.value:
            with self._property_read_write_optional_duration.mutex:
                self._property_read_write_optional_duration.value = value
                self._property_read_write_optional_duration.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalDuration/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_duration.callbacks:
                callback(value)

    def set_read_write_optional_duration(self, value: Optional[timedelta]):
        """This method sets (publishes) a new value for the 'read_write_optional_duration' property."""
        if not isinstance(value, datetime.timedelta) and value is not None:
            raise ValueError(f"The 'value' value must be Optional[timedelta].")

        obj = value

        # Use the property.setter to do that actual work.
        self.read_write_optional_duration = obj

    def on_read_write_optional_duration_updates(self, handler: Callable[[Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_duration' property update is received."""
        if handler is not None:
            self._property_read_write_optional_duration.callbacks.append(handler)

    @property
    def read_write_two_durations(self) -> Optional[stinger_types.ReadWriteTwoDurationsProperty]:
        """This property returns the last received value for the 'read_write_two_durations' property."""
        with self._property_read_write_two_durations_mutex:
            return self._property_read_write_two_durations

    @read_write_two_durations.setter
    def read_write_two_durations(self, value: stinger_types.ReadWriteTwoDurationsProperty):
        """This property sets (publishes) a new value for the 'read_write_two_durations' property."""
        if not isinstance(value, ReadWriteTwoDurationsProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoDurationsProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_durations.value:
            with self._property_read_write_two_durations.mutex:
                self._property_read_write_two_durations.value = value
                self._property_read_write_two_durations.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoDurations/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_durations.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_durations(self, first: timedelta, second: Optional[timedelta]):
        """This method sets (publishes) a new value for the 'read_write_two_durations' property."""
        if not isinstance(first, datetime.timedelta):
            raise ValueError(f"The 'first' value must be timedelta.")
        if not isinstance(second, datetime.timedelta) and second is not None:
            raise ValueError(f"The 'second' value must be Optional[timedelta].")

        obj = stinger_types.ReadWriteTwoDurationsProperty(
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
            raise ValueError(f"The value must be bytes.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_binary.value:
            with self._property_read_write_binary.mutex:
                self._property_read_write_binary.value = value
                self._property_read_write_binary.version += 1
            self._conn.publish("testAble/{}/property/readWriteBinary/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_binary.callbacks:
                callback(value)

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
    def read_write_optional_binary(self) -> Optional[bytes]:
        """This property returns the last received value for the 'read_write_optional_binary' property."""
        with self._property_read_write_optional_binary_mutex:
            return self._property_read_write_optional_binary

    @read_write_optional_binary.setter
    def read_write_optional_binary(self, value: bytes):
        """This property sets (publishes) a new value for the 'read_write_optional_binary' property."""
        if not isinstance(value, bytes):
            raise ValueError(f"The value must be bytes.")

        payload = json.dumps({"value": value})

        if value != self._property_read_write_optional_binary.value:
            with self._property_read_write_optional_binary.mutex:
                self._property_read_write_optional_binary.value = value
                self._property_read_write_optional_binary.version += 1
            self._conn.publish("testAble/{}/property/readWriteOptionalBinary/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_optional_binary.callbacks:
                callback(value)

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
    def read_write_two_binaries(self) -> Optional[stinger_types.ReadWriteTwoBinariesProperty]:
        """This property returns the last received value for the 'read_write_two_binaries' property."""
        with self._property_read_write_two_binaries_mutex:
            return self._property_read_write_two_binaries

    @read_write_two_binaries.setter
    def read_write_two_binaries(self, value: stinger_types.ReadWriteTwoBinariesProperty):
        """This property sets (publishes) a new value for the 'read_write_two_binaries' property."""
        if not isinstance(value, ReadWriteTwoBinariesProperty):
            raise ValueError(f"The value must be stinger_types.ReadWriteTwoBinariesProperty.")

        payload = value.model_dump_json()

        if value != self._property_read_write_two_binaries.value:
            with self._property_read_write_two_binaries.mutex:
                self._property_read_write_two_binaries.value = value
                self._property_read_write_two_binaries.version += 1
            self._conn.publish("testAble/{}/property/readWriteTwoBinaries/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_read_write_two_binaries.callbacks:
                callback(value.first, value.second)

    def set_read_write_two_binaries(self, first: bytes, second: bytes):
        """This method sets (publishes) a new value for the 'read_write_two_binaries' property."""
        if not isinstance(first, bytes):
            raise ValueError(f"The 'first' value must be bytes.")
        if not isinstance(second, bytes) and second is not None:
            raise ValueError(f"The 'second' value must be bytes.")

        obj = stinger_types.ReadWriteTwoBinariesProperty(
            first=first,
            second=second,
        )

        # Use the property.setter to do that actual work.
        self.read_write_two_binaries = obj

    def on_read_write_two_binaries_updates(self, handler: Callable[[bytes, bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_binaries' property update is received."""
        if handler is not None:
            self._property_read_write_two_binaries.callbacks.append(handler)


class TestAbleServerBuilder:
    """
    This is a builder for the TestAbleServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._call_with_nothing_method_handler: Optional[Callable[[None], None]] = None
        self._call_one_integer_method_handler: Optional[Callable[[int], int]] = None
        self._call_optional_integer_method_handler: Optional[Callable[[Optional[int]], Optional[int]]] = None
        self._call_three_integers_method_handler: Optional[Callable[[int, int, Optional[int]], stinger_types.CallThreeIntegersReturnValues]] = None
        self._call_one_string_method_handler: Optional[Callable[[str], str]] = None
        self._call_optional_string_method_handler: Optional[Callable[[Optional[str]], Optional[str]]] = None
        self._call_three_strings_method_handler: Optional[Callable[[str, Optional[str], str], stinger_types.CallThreeStringsReturnValues]] = None
        self._call_one_enum_method_handler: Optional[Callable[[stinger_types.Numbers], stinger_types.Numbers]] = None
        self._call_optional_enum_method_handler: Optional[Callable[[Optional[stinger_types.Numbers]], Optional[stinger_types.Numbers]]] = None
        self._call_three_enums_method_handler: Optional[Callable[[stinger_types.Numbers, stinger_types.Numbers, Optional[stinger_types.Numbers]], stinger_types.CallThreeEnumsReturnValues]] = None
        self._call_one_struct_method_handler: Optional[Callable[[stinger_types.AllTypes], stinger_types.AllTypes]] = None
        self._call_optional_struct_method_handler: Optional[Callable[[stinger_types.AllTypes], stinger_types.AllTypes]] = None
        self._call_three_structs_method_handler: Optional[Callable[[stinger_types.AllTypes, stinger_types.AllTypes, stinger_types.AllTypes], stinger_types.CallThreeStructsReturnValues]] = None
        self._call_one_date_time_method_handler: Optional[Callable[[datetime], datetime]] = None
        self._call_optional_date_time_method_handler: Optional[Callable[[Optional[datetime]], Optional[datetime]]] = None
        self._call_three_date_times_method_handler: Optional[Callable[[datetime, datetime, Optional[datetime]], stinger_types.CallThreeDateTimesReturnValues]] = None
        self._call_one_duration_method_handler: Optional[Callable[[timedelta], timedelta]] = None
        self._call_optional_duration_method_handler: Optional[Callable[[Optional[timedelta]], Optional[timedelta]]] = None
        self._call_three_durations_method_handler: Optional[Callable[[timedelta, timedelta, Optional[timedelta]], stinger_types.CallThreeDurationsReturnValues]] = None
        self._call_one_binary_method_handler: Optional[Callable[[bytes], bytes]] = None
        self._call_optional_binary_method_handler: Optional[Callable[[bytes], bytes]] = None
        self._call_three_binaries_method_handler: Optional[Callable[[bytes, bytes, bytes], stinger_types.CallThreeBinariesReturnValues]] = None

        self._read_write_integer_property_callbacks: List[Callable[[int], None]] = []
        self._read_only_integer_property_callbacks: List[Callable[[int], None]] = []
        self._read_write_optional_integer_property_callbacks: List[Callable[[Optional[int]], None]] = []
        self._read_write_two_integers_property_callbacks: List[Callable[[int, Optional[int]], None]] = []
        self._read_only_string_property_callbacks: List[Callable[[str], None]] = []
        self._read_write_string_property_callbacks: List[Callable[[str], None]] = []
        self._read_write_optional_string_property_callbacks: List[Callable[[Optional[str]], None]] = []
        self._read_write_two_strings_property_callbacks: List[Callable[[str, Optional[str]], None]] = []
        self._read_write_struct_property_callbacks: List[Callable[[stinger_types.AllTypes], None]] = []
        self._read_write_optional_struct_property_callbacks: List[Callable[[stinger_types.AllTypes], None]] = []
        self._read_write_two_structs_property_callbacks: List[Callable[[stinger_types.AllTypes, stinger_types.AllTypes], None]] = []
        self._read_only_enum_property_callbacks: List[Callable[[stinger_types.Numbers], None]] = []
        self._read_write_enum_property_callbacks: List[Callable[[stinger_types.Numbers], None]] = []
        self._read_write_optional_enum_property_callbacks: List[Callable[[Optional[stinger_types.Numbers]], None]] = []
        self._read_write_two_enums_property_callbacks: List[Callable[[stinger_types.Numbers, Optional[stinger_types.Numbers]], None]] = []
        self._read_write_datetime_property_callbacks: List[Callable[[datetime], None]] = []
        self._read_write_optional_datetime_property_callbacks: List[Callable[[Optional[datetime]], None]] = []
        self._read_write_two_datetimes_property_callbacks: List[Callable[[datetime, Optional[datetime]], None]] = []
        self._read_write_duration_property_callbacks: List[Callable[[timedelta], None]] = []
        self._read_write_optional_duration_property_callbacks: List[Callable[[Optional[timedelta]], None]] = []
        self._read_write_two_durations_property_callbacks: List[Callable[[timedelta, Optional[timedelta]], None]] = []
        self._read_write_binary_property_callbacks: List[Callable[[bytes], None]] = []
        self._read_write_optional_binary_property_callbacks: List[Callable[[bytes], None]] = []
        self._read_write_two_binaries_property_callbacks: List[Callable[[bytes, bytes], None]] = []

    def handle_call_with_nothing(self, handler: Callable[[None], None]):
        if self._call_with_nothing_method_handler is None and handler is not None:
            self._call_with_nothing_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_integer(self, handler: Callable[[int], int]):
        if self._call_one_integer_method_handler is None and handler is not None:
            self._call_one_integer_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_integer(self, handler: Callable[[Optional[int]], Optional[int]]):
        if self._call_optional_integer_method_handler is None and handler is not None:
            self._call_optional_integer_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_integers(self, handler: Callable[[int, int, Optional[int]], stinger_types.CallThreeIntegersReturnValues]):
        if self._call_three_integers_method_handler is None and handler is not None:
            self._call_three_integers_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_string(self, handler: Callable[[str], str]):
        if self._call_one_string_method_handler is None and handler is not None:
            self._call_one_string_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_string(self, handler: Callable[[Optional[str]], Optional[str]]):
        if self._call_optional_string_method_handler is None and handler is not None:
            self._call_optional_string_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_strings(self, handler: Callable[[str, Optional[str], str], stinger_types.CallThreeStringsReturnValues]):
        if self._call_three_strings_method_handler is None and handler is not None:
            self._call_three_strings_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_enum(self, handler: Callable[[stinger_types.Numbers], stinger_types.Numbers]):
        if self._call_one_enum_method_handler is None and handler is not None:
            self._call_one_enum_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_enum(self, handler: Callable[[Optional[stinger_types.Numbers]], Optional[stinger_types.Numbers]]):
        if self._call_optional_enum_method_handler is None and handler is not None:
            self._call_optional_enum_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_enums(self, handler: Callable[[stinger_types.Numbers, stinger_types.Numbers, Optional[stinger_types.Numbers]], stinger_types.CallThreeEnumsReturnValues]):
        if self._call_three_enums_method_handler is None and handler is not None:
            self._call_three_enums_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_struct(self, handler: Callable[[stinger_types.AllTypes], stinger_types.AllTypes]):
        if self._call_one_struct_method_handler is None and handler is not None:
            self._call_one_struct_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_struct(self, handler: Callable[[stinger_types.AllTypes], stinger_types.AllTypes]):
        if self._call_optional_struct_method_handler is None and handler is not None:
            self._call_optional_struct_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_structs(self, handler: Callable[[stinger_types.AllTypes, stinger_types.AllTypes, stinger_types.AllTypes], stinger_types.CallThreeStructsReturnValues]):
        if self._call_three_structs_method_handler is None and handler is not None:
            self._call_three_structs_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_date_time(self, handler: Callable[[datetime], datetime]):
        if self._call_one_date_time_method_handler is None and handler is not None:
            self._call_one_date_time_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_date_time(self, handler: Callable[[Optional[datetime]], Optional[datetime]]):
        if self._call_optional_date_time_method_handler is None and handler is not None:
            self._call_optional_date_time_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_date_times(self, handler: Callable[[datetime, datetime, Optional[datetime]], stinger_types.CallThreeDateTimesReturnValues]):
        if self._call_three_date_times_method_handler is None and handler is not None:
            self._call_three_date_times_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_duration(self, handler: Callable[[timedelta], timedelta]):
        if self._call_one_duration_method_handler is None and handler is not None:
            self._call_one_duration_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_duration(self, handler: Callable[[Optional[timedelta]], Optional[timedelta]]):
        if self._call_optional_duration_method_handler is None and handler is not None:
            self._call_optional_duration_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_durations(self, handler: Callable[[timedelta, timedelta, Optional[timedelta]], stinger_types.CallThreeDurationsReturnValues]):
        if self._call_three_durations_method_handler is None and handler is not None:
            self._call_three_durations_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_one_binary(self, handler: Callable[[bytes], bytes]):
        if self._call_one_binary_method_handler is None and handler is not None:
            self._call_one_binary_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_optional_binary(self, handler: Callable[[bytes], bytes]):
        if self._call_optional_binary_method_handler is None and handler is not None:
            self._call_optional_binary_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_call_three_binaries(self, handler: Callable[[bytes, bytes, bytes], stinger_types.CallThreeBinariesReturnValues]):
        if self._call_three_binaries_method_handler is None and handler is not None:
            self._call_three_binaries_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def on_read_write_integer_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'read_write_integer' property update is received."""
        self._read_write_integer_property_callbacks.append(handler)

    def on_read_only_integer_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'read_only_integer' property update is received."""
        self._read_only_integer_property_callbacks.append(handler)

    def on_read_write_optional_integer_updates(self, handler: Callable[[Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_integer' property update is received."""
        self._read_write_optional_integer_property_callbacks.append(handler)

    def on_read_write_two_integers_updates(self, handler: Callable[[int, Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_integers' property update is received."""
        self._read_write_two_integers_property_callbacks.append(handler)

    def on_read_only_string_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'read_only_string' property update is received."""
        self._read_only_string_property_callbacks.append(handler)

    def on_read_write_string_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'read_write_string' property update is received."""
        self._read_write_string_property_callbacks.append(handler)

    def on_read_write_optional_string_updates(self, handler: Callable[[Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_string' property update is received."""
        self._read_write_optional_string_property_callbacks.append(handler)

    def on_read_write_two_strings_updates(self, handler: Callable[[str, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_strings' property update is received."""
        self._read_write_two_strings_property_callbacks.append(handler)

    def on_read_write_struct_updates(self, handler: Callable[[stinger_types.AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_struct' property update is received."""
        self._read_write_struct_property_callbacks.append(handler)

    def on_read_write_optional_struct_updates(self, handler: Callable[[stinger_types.AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_struct' property update is received."""
        self._read_write_optional_struct_property_callbacks.append(handler)

    def on_read_write_two_structs_updates(self, handler: Callable[[stinger_types.AllTypes, stinger_types.AllTypes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_structs' property update is received."""
        self._read_write_two_structs_property_callbacks.append(handler)

    def on_read_only_enum_updates(self, handler: Callable[[stinger_types.Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_only_enum' property update is received."""
        self._read_only_enum_property_callbacks.append(handler)

    def on_read_write_enum_updates(self, handler: Callable[[stinger_types.Numbers], None]):
        """This method registers a callback to be called whenever a new 'read_write_enum' property update is received."""
        self._read_write_enum_property_callbacks.append(handler)

    def on_read_write_optional_enum_updates(self, handler: Callable[[Optional[stinger_types.Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_enum' property update is received."""
        self._read_write_optional_enum_property_callbacks.append(handler)

    def on_read_write_two_enums_updates(self, handler: Callable[[stinger_types.Numbers, Optional[stinger_types.Numbers]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_enums' property update is received."""
        self._read_write_two_enums_property_callbacks.append(handler)

    def on_read_write_datetime_updates(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'read_write_datetime' property update is received."""
        self._read_write_datetime_property_callbacks.append(handler)

    def on_read_write_optional_datetime_updates(self, handler: Callable[[Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_datetime' property update is received."""
        self._read_write_optional_datetime_property_callbacks.append(handler)

    def on_read_write_two_datetimes_updates(self, handler: Callable[[datetime, Optional[datetime]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_datetimes' property update is received."""
        self._read_write_two_datetimes_property_callbacks.append(handler)

    def on_read_write_duration_updates(self, handler: Callable[[timedelta], None]):
        """This method registers a callback to be called whenever a new 'read_write_duration' property update is received."""
        self._read_write_duration_property_callbacks.append(handler)

    def on_read_write_optional_duration_updates(self, handler: Callable[[Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_duration' property update is received."""
        self._read_write_optional_duration_property_callbacks.append(handler)

    def on_read_write_two_durations_updates(self, handler: Callable[[timedelta, Optional[timedelta]], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_durations' property update is received."""
        self._read_write_two_durations_property_callbacks.append(handler)

    def on_read_write_binary_updates(self, handler: Callable[[bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_binary' property update is received."""
        self._read_write_binary_property_callbacks.append(handler)

    def on_read_write_optional_binary_updates(self, handler: Callable[[bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_optional_binary' property update is received."""
        self._read_write_optional_binary_property_callbacks.append(handler)

    def on_read_write_two_binaries_updates(self, handler: Callable[[bytes, bytes], None]):
        """This method registers a callback to be called whenever a new 'read_write_two_binaries' property update is received."""
        self._read_write_two_binaries_property_callbacks.append(handler)

    def build(self, connection: IBrokerConnection) -> TestAbleServer:
        new_server = TestAbleServer(connection)

        if self._call_with_nothing_method_handler is not None:
            new_server.handle_call_with_nothing(self._call_with_nothing_method_handler)
        if self._call_one_integer_method_handler is not None:
            new_server.handle_call_one_integer(self._call_one_integer_method_handler)
        if self._call_optional_integer_method_handler is not None:
            new_server.handle_call_optional_integer(self._call_optional_integer_method_handler)
        if self._call_three_integers_method_handler is not None:
            new_server.handle_call_three_integers(self._call_three_integers_method_handler)
        if self._call_one_string_method_handler is not None:
            new_server.handle_call_one_string(self._call_one_string_method_handler)
        if self._call_optional_string_method_handler is not None:
            new_server.handle_call_optional_string(self._call_optional_string_method_handler)
        if self._call_three_strings_method_handler is not None:
            new_server.handle_call_three_strings(self._call_three_strings_method_handler)
        if self._call_one_enum_method_handler is not None:
            new_server.handle_call_one_enum(self._call_one_enum_method_handler)
        if self._call_optional_enum_method_handler is not None:
            new_server.handle_call_optional_enum(self._call_optional_enum_method_handler)
        if self._call_three_enums_method_handler is not None:
            new_server.handle_call_three_enums(self._call_three_enums_method_handler)
        if self._call_one_struct_method_handler is not None:
            new_server.handle_call_one_struct(self._call_one_struct_method_handler)
        if self._call_optional_struct_method_handler is not None:
            new_server.handle_call_optional_struct(self._call_optional_struct_method_handler)
        if self._call_three_structs_method_handler is not None:
            new_server.handle_call_three_structs(self._call_three_structs_method_handler)
        if self._call_one_date_time_method_handler is not None:
            new_server.handle_call_one_date_time(self._call_one_date_time_method_handler)
        if self._call_optional_date_time_method_handler is not None:
            new_server.handle_call_optional_date_time(self._call_optional_date_time_method_handler)
        if self._call_three_date_times_method_handler is not None:
            new_server.handle_call_three_date_times(self._call_three_date_times_method_handler)
        if self._call_one_duration_method_handler is not None:
            new_server.handle_call_one_duration(self._call_one_duration_method_handler)
        if self._call_optional_duration_method_handler is not None:
            new_server.handle_call_optional_duration(self._call_optional_duration_method_handler)
        if self._call_three_durations_method_handler is not None:
            new_server.handle_call_three_durations(self._call_three_durations_method_handler)
        if self._call_one_binary_method_handler is not None:
            new_server.handle_call_one_binary(self._call_one_binary_method_handler)
        if self._call_optional_binary_method_handler is not None:
            new_server.handle_call_optional_binary(self._call_optional_binary_method_handler)
        if self._call_three_binaries_method_handler is not None:
            new_server.handle_call_three_binaries(self._call_three_binaries_method_handler)

        for callback in self._read_write_integer_property_callbacks:
            new_server.on_read_write_integer_updates(callback)

        for callback in self._read_only_integer_property_callbacks:
            new_server.on_read_only_integer_updates(callback)

        for callback in self._read_write_optional_integer_property_callbacks:
            new_server.on_read_write_optional_integer_updates(callback)

        for callback in self._read_write_two_integers_property_callbacks:
            new_server.on_read_write_two_integers_updates(callback)

        for callback in self._read_only_string_property_callbacks:
            new_server.on_read_only_string_updates(callback)

        for callback in self._read_write_string_property_callbacks:
            new_server.on_read_write_string_updates(callback)

        for callback in self._read_write_optional_string_property_callbacks:
            new_server.on_read_write_optional_string_updates(callback)

        for callback in self._read_write_two_strings_property_callbacks:
            new_server.on_read_write_two_strings_updates(callback)

        for callback in self._read_write_struct_property_callbacks:
            new_server.on_read_write_struct_updates(callback)

        for callback in self._read_write_optional_struct_property_callbacks:
            new_server.on_read_write_optional_struct_updates(callback)

        for callback in self._read_write_two_structs_property_callbacks:
            new_server.on_read_write_two_structs_updates(callback)

        for callback in self._read_only_enum_property_callbacks:
            new_server.on_read_only_enum_updates(callback)

        for callback in self._read_write_enum_property_callbacks:
            new_server.on_read_write_enum_updates(callback)

        for callback in self._read_write_optional_enum_property_callbacks:
            new_server.on_read_write_optional_enum_updates(callback)

        for callback in self._read_write_two_enums_property_callbacks:
            new_server.on_read_write_two_enums_updates(callback)

        for callback in self._read_write_datetime_property_callbacks:
            new_server.on_read_write_datetime_updates(callback)

        for callback in self._read_write_optional_datetime_property_callbacks:
            new_server.on_read_write_optional_datetime_updates(callback)

        for callback in self._read_write_two_datetimes_property_callbacks:
            new_server.on_read_write_two_datetimes_updates(callback)

        for callback in self._read_write_duration_property_callbacks:
            new_server.on_read_write_duration_updates(callback)

        for callback in self._read_write_optional_duration_property_callbacks:
            new_server.on_read_write_optional_duration_updates(callback)

        for callback in self._read_write_two_durations_property_callbacks:
            new_server.on_read_write_two_durations_updates(callback)

        for callback in self._read_write_binary_property_callbacks:
            new_server.on_read_write_binary_updates(callback)

        for callback in self._read_write_optional_binary_property_callbacks:
            new_server.on_read_write_optional_binary_updates(callback)

        for callback in self._read_write_two_binaries_property_callbacks:
            new_server.on_read_write_two_binaries_updates(callback)

        return new_server


if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    from connection import MqttBrokerConnection, MqttTransport, MqttTransportType

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = TestAbleServer(conn, "py-server-demo:1")

    server.read_write_integer = 42

    server.read_only_integer = 42

    server.read_write_optional_integer = 42

    server.read_write_two_integers = stinger_types.ReadWriteTwoIntegersProperty(
        first=42,
        second=42,
    )

    server.read_only_string = "apples"

    server.read_write_string = "apples"

    server.read_write_optional_string = "apples"

    server.read_write_two_strings = stinger_types.ReadWriteTwoStringsProperty(
        first="apples",
        second="apples",
    )

    server.read_write_struct = stinger_types.AllTypes(
        the_bool=True,
        the_int=42,
        the_number=3.14,
        the_str="apples",
        the_enum=stinger_types.Numbers.ONE,
        date_and_time=datetime.now(),
        time_duration=timedelta(seconds=3536),
        data=b"example binary data",
        OptionalInteger=42,
        OptionalString="apples",
        OptionalEnum=stinger_types.Numbers.ONE,
        OptionalDateTime=None,
        OptionalDuration=None,
        OptionalBinary=b"example binary data",
    )

    server.read_write_optional_struct = stinger_types.AllTypes(
        the_bool=True,
        the_int=42,
        the_number=3.14,
        the_str="apples",
        the_enum=stinger_types.Numbers.ONE,
        date_and_time=datetime.now(),
        time_duration=timedelta(seconds=3536),
        data=b"example binary data",
        OptionalInteger=42,
        OptionalString="apples",
        OptionalEnum=stinger_types.Numbers.ONE,
        OptionalDateTime=datetime.now(),
        OptionalDuration=None,
        OptionalBinary=b"example binary data",
    )

    server.read_write_two_structs = stinger_types.ReadWriteTwoStructsProperty(
        first=stinger_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=stinger_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            OptionalInteger=42,
            OptionalString="apples",
            OptionalEnum=stinger_types.Numbers.ONE,
            OptionalDateTime=None,
            OptionalDuration=None,
            OptionalBinary=b"example binary data",
        ),
        second=stinger_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=stinger_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            OptionalInteger=42,
            OptionalString="apples",
            OptionalEnum=stinger_types.Numbers.ONE,
            OptionalDateTime=datetime.now(),
            OptionalDuration=None,
            OptionalBinary=b"example binary data",
        ),
    )

    server.read_only_enum = stinger_types.Numbers.ONE

    server.read_write_enum = stinger_types.Numbers.ONE

    server.read_write_optional_enum = stinger_types.Numbers.ONE

    server.read_write_two_enums = stinger_types.ReadWriteTwoEnumsProperty(
        first=stinger_types.Numbers.ONE,
        second=stinger_types.Numbers.ONE,
    )

    server.read_write_datetime = datetime.now()

    server.read_write_optional_datetime = None

    server.read_write_two_datetimes = stinger_types.ReadWriteTwoDatetimesProperty(
        first=datetime.now(),
        second=None,
    )

    server.read_write_duration = timedelta(seconds=3536)

    server.read_write_optional_duration = None

    server.read_write_two_durations = stinger_types.ReadWriteTwoDurationsProperty(
        first=timedelta(seconds=3536),
        second=None,
    )

    server.read_write_binary = b"example binary data"

    server.read_write_optional_binary = b"example binary data"

    server.read_write_two_binaries = stinger_types.ReadWriteTwoBinariesProperty(
        first=b"example binary data",
        second=b"example binary data",
    )

    @server.handle_call_with_nothing
    def call_with_nothing() -> None:
        """This is an example handler for the 'callWithNothing' method."""
        print(f"Running call_with_nothing'()'")
        return None

    @server.handle_call_one_integer
    def call_one_integer(input1: int) -> int:
        """This is an example handler for the 'callOneInteger' method."""
        print(f"Running call_one_integer'({input1})'")
        return 42

    @server.handle_call_optional_integer
    def call_optional_integer(input1: Optional[int]) -> Optional[int]:
        """This is an example handler for the 'callOptionalInteger' method."""
        print(f"Running call_optional_integer'({input1})'")
        return 42

    @server.handle_call_three_integers
    def call_three_integers(input1: int, input2: int, input3: Optional[int]) -> stinger_types.CallThreeIntegersReturnValues:
        """This is an example handler for the 'callThreeIntegers' method."""
        print(f"Running call_three_integers'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeIntegersReturnValues(output1=42, output2=42, output3=42)

    @server.handle_call_one_string
    def call_one_string(input1: str) -> str:
        """This is an example handler for the 'callOneString' method."""
        print(f"Running call_one_string'({input1})'")
        return "apples"

    @server.handle_call_optional_string
    def call_optional_string(input1: Optional[str]) -> Optional[str]:
        """This is an example handler for the 'callOptionalString' method."""
        print(f"Running call_optional_string'({input1})'")
        return "apples"

    @server.handle_call_three_strings
    def call_three_strings(input1: str, input2: Optional[str], input3: str) -> stinger_types.CallThreeStringsReturnValues:
        """This is an example handler for the 'callThreeStrings' method."""
        print(f"Running call_three_strings'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeStringsReturnValues(output1="apples", output2="apples", output3="apples")

    @server.handle_call_one_enum
    def call_one_enum(input1: stinger_types.Numbers) -> stinger_types.Numbers:
        """This is an example handler for the 'callOneEnum' method."""
        print(f"Running call_one_enum'({input1})'")
        return stinger_types.Numbers.ONE

    @server.handle_call_optional_enum
    def call_optional_enum(input1: Optional[stinger_types.Numbers]) -> Optional[stinger_types.Numbers]:
        """This is an example handler for the 'callOptionalEnum' method."""
        print(f"Running call_optional_enum'({input1})'")
        return stinger_types.Numbers.ONE

    @server.handle_call_three_enums
    def call_three_enums(input1: stinger_types.Numbers, input2: stinger_types.Numbers, input3: Optional[stinger_types.Numbers]) -> stinger_types.CallThreeEnumsReturnValues:
        """This is an example handler for the 'callThreeEnums' method."""
        print(f"Running call_three_enums'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeEnumsReturnValues(output1=stinger_types.Numbers.ONE, output2=stinger_types.Numbers.ONE, output3=stinger_types.Numbers.ONE)

    @server.handle_call_one_struct
    def call_one_struct(input1: stinger_types.AllTypes) -> stinger_types.AllTypes:
        """This is an example handler for the 'callOneStruct' method."""
        print(f"Running call_one_struct'({input1})'")
        return stinger_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=stinger_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            OptionalInteger=42,
            OptionalString="apples",
            OptionalEnum=stinger_types.Numbers.ONE,
            OptionalDateTime=datetime.now(),
            OptionalDuration=None,
            OptionalBinary=b"example binary data",
        )

    @server.handle_call_optional_struct
    def call_optional_struct(input1: stinger_types.AllTypes) -> stinger_types.AllTypes:
        """This is an example handler for the 'callOptionalStruct' method."""
        print(f"Running call_optional_struct'({input1})'")
        return stinger_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=stinger_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            OptionalInteger=42,
            OptionalString="apples",
            OptionalEnum=stinger_types.Numbers.ONE,
            OptionalDateTime=datetime.now(),
            OptionalDuration=None,
            OptionalBinary=b"example binary data",
        )

    @server.handle_call_three_structs
    def call_three_structs(input1: stinger_types.AllTypes, input2: stinger_types.AllTypes, input3: stinger_types.AllTypes) -> stinger_types.CallThreeStructsReturnValues:
        """This is an example handler for the 'callThreeStructs' method."""
        print(f"Running call_three_structs'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeStructsReturnValues(
            output1=stinger_types.AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=stinger_types.Numbers.ONE,
                date_and_time=datetime.now(),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                OptionalInteger=42,
                OptionalString="apples",
                OptionalEnum=stinger_types.Numbers.ONE,
                OptionalDateTime=datetime.now(),
                OptionalDuration=None,
                OptionalBinary=b"example binary data",
            ),
            output2=stinger_types.AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=stinger_types.Numbers.ONE,
                date_and_time=datetime.now(),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                OptionalInteger=42,
                OptionalString="apples",
                OptionalEnum=stinger_types.Numbers.ONE,
                OptionalDateTime=datetime.now(),
                OptionalDuration=None,
                OptionalBinary=b"example binary data",
            ),
            output3=stinger_types.AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=stinger_types.Numbers.ONE,
                date_and_time=datetime.now(),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                OptionalInteger=42,
                OptionalString="apples",
                OptionalEnum=stinger_types.Numbers.ONE,
                OptionalDateTime=datetime.now(),
                OptionalDuration=None,
                OptionalBinary=b"example binary data",
            ),
        )

    @server.handle_call_one_date_time
    def call_one_date_time(input1: datetime) -> datetime:
        """This is an example handler for the 'callOneDateTime' method."""
        print(f"Running call_one_date_time'({input1})'")
        return datetime.now()

    @server.handle_call_optional_date_time
    def call_optional_date_time(input1: Optional[datetime]) -> Optional[datetime]:
        """This is an example handler for the 'callOptionalDateTime' method."""
        print(f"Running call_optional_date_time'({input1})'")
        return datetime.now()

    @server.handle_call_three_date_times
    def call_three_date_times(input1: datetime, input2: datetime, input3: Optional[datetime]) -> stinger_types.CallThreeDateTimesReturnValues:
        """This is an example handler for the 'callThreeDateTimes' method."""
        print(f"Running call_three_date_times'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeDateTimesReturnValues(output1=datetime.now(), output2=datetime.now(), output3=datetime.now())

    @server.handle_call_one_duration
    def call_one_duration(input1: timedelta) -> timedelta:
        """This is an example handler for the 'callOneDuration' method."""
        print(f"Running call_one_duration'({input1})'")
        return timedelta(seconds=3536)

    @server.handle_call_optional_duration
    def call_optional_duration(input1: Optional[timedelta]) -> Optional[timedelta]:
        """This is an example handler for the 'callOptionalDuration' method."""
        print(f"Running call_optional_duration'({input1})'")
        return None

    @server.handle_call_three_durations
    def call_three_durations(input1: timedelta, input2: timedelta, input3: Optional[timedelta]) -> stinger_types.CallThreeDurationsReturnValues:
        """This is an example handler for the 'callThreeDurations' method."""
        print(f"Running call_three_durations'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeDurationsReturnValues(output1=timedelta(seconds=3536), output2=timedelta(seconds=3536), output3=None)

    @server.handle_call_one_binary
    def call_one_binary(input1: bytes) -> bytes:
        """This is an example handler for the 'callOneBinary' method."""
        print(f"Running call_one_binary'({input1})'")
        return b"example binary data"

    @server.handle_call_optional_binary
    def call_optional_binary(input1: bytes) -> bytes:
        """This is an example handler for the 'callOptionalBinary' method."""
        print(f"Running call_optional_binary'({input1})'")
        return b"example binary data"

    @server.handle_call_three_binaries
    def call_three_binaries(input1: bytes, input2: bytes, input3: bytes) -> stinger_types.CallThreeBinariesReturnValues:
        """This is an example handler for the 'callThreeBinaries' method."""
        print(f"Running call_three_binaries'({input1}, {input2}, {input3})'")
        return stinger_types.CallThreeBinariesReturnValues(output1=b"example binary data", output2=b"example binary data", output3=b"example binary data")

    @server.on_read_write_integer_updates
    def on_read_write_integer_update(value: int):
        print(f"Received update for 'read_write_integer' property: { value= }")

    @server.on_read_only_integer_updates
    def on_read_only_integer_update(value: int):
        print(f"Received update for 'read_only_integer' property: { value= }")

    @server.on_read_write_optional_integer_updates
    def on_read_write_optional_integer_update(value: Optional[int]):
        print(f"Received update for 'read_write_optional_integer' property: { value= }")

    @server.on_read_write_two_integers_updates
    def on_read_write_two_integers_update(first: int, second: Optional[int]):
        print(f"Received update for 'read_write_two_integers' property: { first= }, { second= }")

    @server.on_read_only_string_updates
    def on_read_only_string_update(value: str):
        print(f"Received update for 'read_only_string' property: { value= }")

    @server.on_read_write_string_updates
    def on_read_write_string_update(value: str):
        print(f"Received update for 'read_write_string' property: { value= }")

    @server.on_read_write_optional_string_updates
    def on_read_write_optional_string_update(value: Optional[str]):
        print(f"Received update for 'read_write_optional_string' property: { value= }")

    @server.on_read_write_two_strings_updates
    def on_read_write_two_strings_update(first: str, second: Optional[str]):
        print(f"Received update for 'read_write_two_strings' property: { first= }, { second= }")

    @server.on_read_write_struct_updates
    def on_read_write_struct_update(value: stinger_types.AllTypes):
        print(f"Received update for 'read_write_struct' property: { value= }")

    @server.on_read_write_optional_struct_updates
    def on_read_write_optional_struct_update(value: stinger_types.AllTypes):
        print(f"Received update for 'read_write_optional_struct' property: { value= }")

    @server.on_read_write_two_structs_updates
    def on_read_write_two_structs_update(first: stinger_types.AllTypes, second: stinger_types.AllTypes):
        print(f"Received update for 'read_write_two_structs' property: { first= }, { second= }")

    @server.on_read_only_enum_updates
    def on_read_only_enum_update(value: stinger_types.Numbers):
        print(f"Received update for 'read_only_enum' property: { value= }")

    @server.on_read_write_enum_updates
    def on_read_write_enum_update(value: stinger_types.Numbers):
        print(f"Received update for 'read_write_enum' property: { value= }")

    @server.on_read_write_optional_enum_updates
    def on_read_write_optional_enum_update(value: Optional[stinger_types.Numbers]):
        print(f"Received update for 'read_write_optional_enum' property: { value= }")

    @server.on_read_write_two_enums_updates
    def on_read_write_two_enums_update(first: stinger_types.Numbers, second: Optional[stinger_types.Numbers]):
        print(f"Received update for 'read_write_two_enums' property: { first= }, { second= }")

    @server.on_read_write_datetime_updates
    def on_read_write_datetime_update(value: datetime):
        print(f"Received update for 'read_write_datetime' property: { value= }")

    @server.on_read_write_optional_datetime_updates
    def on_read_write_optional_datetime_update(value: Optional[datetime]):
        print(f"Received update for 'read_write_optional_datetime' property: { value= }")

    @server.on_read_write_two_datetimes_updates
    def on_read_write_two_datetimes_update(first: datetime, second: Optional[datetime]):
        print(f"Received update for 'read_write_two_datetimes' property: { first= }, { second= }")

    @server.on_read_write_duration_updates
    def on_read_write_duration_update(value: timedelta):
        print(f"Received update for 'read_write_duration' property: { value= }")

    @server.on_read_write_optional_duration_updates
    def on_read_write_optional_duration_update(value: Optional[timedelta]):
        print(f"Received update for 'read_write_optional_duration' property: { value= }")

    @server.on_read_write_two_durations_updates
    def on_read_write_two_durations_update(first: timedelta, second: Optional[timedelta]):
        print(f"Received update for 'read_write_two_durations' property: { first= }, { second= }")

    @server.on_read_write_binary_updates
    def on_read_write_binary_update(value: bytes):
        print(f"Received update for 'read_write_binary' property: { value= }")

    @server.on_read_write_optional_binary_updates
    def on_read_write_optional_binary_update(value: bytes):
        print(f"Received update for 'read_write_optional_binary' property: { value= }")

    @server.on_read_write_two_binaries_updates
    def on_read_write_two_binaries_update(first: bytes, second: bytes):
        print(f"Received update for 'read_write_two_binaries' property: { first= }, { second= }")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_empty()
            server.emit_single_int(42)
            server.emit_single_optional_int(42)
            server.emit_three_integers(42, 42, 42)
            server.emit_single_string("apples")
            server.emit_single_optional_string("apples")
            server.emit_three_strings("apples", "apples", "apples")
            server.emit_single_enum(stinger_types.Numbers.ONE)
            server.emit_single_optional_enum(stinger_types.Numbers.ONE)
            server.emit_three_enums(stinger_types.Numbers.ONE, stinger_types.Numbers.ONE, stinger_types.Numbers.ONE)
            server.emit_single_struct(
                stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                )
            )
            server.emit_single_optional_struct(
                stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                )
            )
            server.emit_three_structs(
                stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                ),
                stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                ),
                stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                ),
            )
            server.emit_single_date_time(datetime.now())
            server.emit_single_optional_datetime(datetime.now())
            server.emit_three_date_times(datetime.now(), datetime.now(), datetime.now())
            server.emit_single_duration(timedelta(seconds=3536))
            server.emit_single_optional_duration(None)
            server.emit_three_durations(timedelta(seconds=3536), timedelta(seconds=3536), None)
            server.emit_single_binary(b"example binary data")
            server.emit_single_optional_binary(b"example binary data")
            server.emit_three_binaries(b"example binary data", b"example binary data", b"example binary data")

            sleep(4)
            server.emit_empty()
            server.emit_single_int(value=42)
            server.emit_single_optional_int(value=42)
            server.emit_three_integers(first=42, second=42, third=42)
            server.emit_single_string(value="apples")
            server.emit_single_optional_string(value="apples")
            server.emit_three_strings(first="apples", second="apples", third="apples")
            server.emit_single_enum(value=stinger_types.Numbers.ONE)
            server.emit_single_optional_enum(value=stinger_types.Numbers.ONE)
            server.emit_three_enums(first=stinger_types.Numbers.ONE, second=stinger_types.Numbers.ONE, third=stinger_types.Numbers.ONE)
            server.emit_single_struct(
                value=stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                )
            )
            server.emit_single_optional_struct(
                value=stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                )
            )
            server.emit_three_structs(
                first=stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                ),
                second=stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=None,
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                ),
                third=stinger_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=stinger_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    OptionalInteger=42,
                    OptionalString="apples",
                    OptionalEnum=stinger_types.Numbers.ONE,
                    OptionalDateTime=datetime.now(),
                    OptionalDuration=None,
                    OptionalBinary=b"example binary data",
                ),
            )
            server.emit_single_date_time(value=datetime.now())
            server.emit_single_optional_datetime(value=datetime.now())
            server.emit_three_date_times(first=datetime.now(), second=datetime.now(), third=None)
            server.emit_single_duration(value=timedelta(seconds=3536))
            server.emit_single_optional_duration(value=None)
            server.emit_three_durations(first=timedelta(seconds=3536), second=timedelta(seconds=3536), third=None)
            server.emit_single_binary(value=b"example binary data")
            server.emit_single_optional_binary(value=b"example binary data")
            server.emit_three_binaries(first=b"example binary data", second=b"example binary data", third=b"example binary data")

            sleep(6)
        except KeyboardInterrupt:
            break

    signal.pause()
