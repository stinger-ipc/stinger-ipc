import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from testableipc.client import TestableClient, TestableClientBuilder, TestableClientDiscoverer
from testableipc.interface_types import *
import threading

client_builder = TestableClientBuilder()


class SuperAwesomeDoerOfThings:

    def __init__(self, label: str, connection: Mqtt5Connection):
        self.counter = 0
        self.label = label
        discovery = TestableClientDiscoverer(connection, client_builder, build_binding=self)  # The build binding will bind all @client_builder decorated methods to this instance.
        self.client = discovery.get_singleton_client().result()
        threading.Thread(target=self.request_loop, daemon=True).start()

    @client_builder.receive_empty
    def print_empty_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'empty' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_int
    def print_singleInt_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleInt' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_int
    def print_singleOptionalInt_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalInt' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_integers
    def print_threeIntegers_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeIntegers' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_string
    def print_singleString_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleString' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_string
    def print_singleOptionalString_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalString' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_strings
    def print_threeStrings_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeStrings' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_enum
    def print_singleEnum_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleEnum' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_enum
    def print_singleOptionalEnum_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalEnum' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_enums
    def print_threeEnums_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeEnums' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_struct
    def print_singleStruct_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleStruct' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_struct
    def print_singleOptionalStruct_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalStruct' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_structs
    def print_threeStructs_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeStructs' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_date_time
    def print_singleDateTime_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleDateTime' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_datetime
    def print_singleOptionalDatetime_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalDatetime' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_date_times
    def print_threeDateTimes_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeDateTimes' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_duration
    def print_singleDuration_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleDuration' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_duration
    def print_singleOptionalDuration_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalDuration' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_durations
    def print_threeDurations_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeDurations' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_binary
    def print_singleBinary_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleBinary' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_binary
    def print_singleOptionalBinary_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalBinary' : args={args}, kwargs={kwargs}")

    @client_builder.receive_three_binaries
    def print_threeBinaries_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'threeBinaries' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_array_of_integers
    def print_singleArrayOfIntegers_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleArrayOfIntegers' : args={args}, kwargs={kwargs}")

    @client_builder.receive_single_optional_array_of_strings
    def print_singleOptionalArrayOfStrings_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'singleOptionalArrayOfStrings' : args={args}, kwargs={kwargs}")

    @client_builder.receive_array_of_every_type
    def print_arrayOfEveryType_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'arrayOfEveryType' : args={args}, kwargs={kwargs}")

    @client_builder.read_write_integer_updated
    def print_new_read_write_integer_value(self, value: int):
        print(f"{self.label}-{self.counter} printing signal 'read_write_integer' : value={value}")

    @client_builder.read_only_integer_updated
    def print_new_read_only_integer_value(self, value: int):
        print(f"{self.label}-{self.counter} printing signal 'read_only_integer' : value={value}")

    @client_builder.read_write_optional_integer_updated
    def print_new_read_write_optional_integer_value(self, value: Optional[int]):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_integer' : value={value}")

    @client_builder.read_write_two_integers_updated
    def print_new_read_write_two_integers_value(self, value: ReadWriteTwoIntegersProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_integers' : value={value}")

    @client_builder.read_only_string_updated
    def print_new_read_only_string_value(self, value: str):
        print(f"{self.label}-{self.counter} printing signal 'read_only_string' : value={value}")

    @client_builder.read_write_string_updated
    def print_new_read_write_string_value(self, value: str):
        print(f"{self.label}-{self.counter} printing signal 'read_write_string' : value={value}")

    @client_builder.read_write_optional_string_updated
    def print_new_read_write_optional_string_value(self, value: Optional[str]):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_string' : value={value}")

    @client_builder.read_write_two_strings_updated
    def print_new_read_write_two_strings_value(self, value: ReadWriteTwoStringsProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_strings' : value={value}")

    @client_builder.read_write_struct_updated
    def print_new_read_write_struct_value(self, value: AllTypes):
        print(f"{self.label}-{self.counter} printing signal 'read_write_struct' : value={value}")

    @client_builder.read_write_optional_struct_updated
    def print_new_read_write_optional_struct_value(self, value: AllTypes):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_struct' : value={value}")

    @client_builder.read_write_two_structs_updated
    def print_new_read_write_two_structs_value(self, value: ReadWriteTwoStructsProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_structs' : value={value}")

    @client_builder.read_only_enum_updated
    def print_new_read_only_enum_value(self, value: Numbers):
        print(f"{self.label}-{self.counter} printing signal 'read_only_enum' : value={value}")

    @client_builder.read_write_enum_updated
    def print_new_read_write_enum_value(self, value: Numbers):
        print(f"{self.label}-{self.counter} printing signal 'read_write_enum' : value={value}")

    @client_builder.read_write_optional_enum_updated
    def print_new_read_write_optional_enum_value(self, value: Optional[Numbers]):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_enum' : value={value}")

    @client_builder.read_write_two_enums_updated
    def print_new_read_write_two_enums_value(self, value: ReadWriteTwoEnumsProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_enums' : value={value}")

    @client_builder.read_write_datetime_updated
    def print_new_read_write_datetime_value(self, value: datetime):
        print(f"{self.label}-{self.counter} printing signal 'read_write_datetime' : value={value}")

    @client_builder.read_write_optional_datetime_updated
    def print_new_read_write_optional_datetime_value(self, value: Optional[datetime]):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_datetime' : value={value}")

    @client_builder.read_write_two_datetimes_updated
    def print_new_read_write_two_datetimes_value(self, value: ReadWriteTwoDatetimesProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_datetimes' : value={value}")

    @client_builder.read_write_duration_updated
    def print_new_read_write_duration_value(self, value: timedelta):
        print(f"{self.label}-{self.counter} printing signal 'read_write_duration' : value={value}")

    @client_builder.read_write_optional_duration_updated
    def print_new_read_write_optional_duration_value(self, value: Optional[timedelta]):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_duration' : value={value}")

    @client_builder.read_write_two_durations_updated
    def print_new_read_write_two_durations_value(self, value: ReadWriteTwoDurationsProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_durations' : value={value}")

    @client_builder.read_write_binary_updated
    def print_new_read_write_binary_value(self, value: bytes):
        print(f"{self.label}-{self.counter} printing signal 'read_write_binary' : value={value!r}")

    @client_builder.read_write_optional_binary_updated
    def print_new_read_write_optional_binary_value(self, value: bytes):
        print(f"{self.label}-{self.counter} printing signal 'read_write_optional_binary' : value={value!r}")

    @client_builder.read_write_two_binaries_updated
    def print_new_read_write_two_binaries_value(self, value: ReadWriteTwoBinariesProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_two_binaries' : value={value}")

    @client_builder.read_write_list_of_strings_updated
    def print_new_read_write_list_of_strings_value(self, value: List[str]):
        print(f"{self.label}-{self.counter} printing signal 'read_write_list_of_strings' : value={value}")

    @client_builder.read_write_lists_updated
    def print_new_read_write_lists_value(self, value: ReadWriteListsProperty):
        print(f"{self.label}-{self.counter} printing signal 'read_write_lists' : value={value}")

    def request_loop(self):
        """Example request loop that runs in a separate thread."""
        sleep(30)
        while True:
            print("Making call to 'call_with_nothing'")
            future_resp = self.client.call_with_nothing()
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_with_nothing' call")
            sleep(5)

            print("Making call to 'call_one_integer'")
            future_resp = self.client.call_one_integer(input1=42)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_integer' call")
            sleep(5)

            print("Making call to 'call_optional_integer'")
            future_resp = self.client.call_optional_integer(input1=42)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_integer' call")
            sleep(5)

            print("Making call to 'call_three_integers'")
            future_resp = self.client.call_three_integers(input1=42, input2=42, input3=42)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_integers' call")
            sleep(5)

            print("Making call to 'call_one_string'")
            future_resp = self.client.call_one_string(input1="apples")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_string' call")
            sleep(5)

            print("Making call to 'call_optional_string'")
            future_resp = self.client.call_optional_string(input1="apples")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_string' call")
            sleep(5)

            print("Making call to 'call_three_strings'")
            future_resp = self.client.call_three_strings(input1="apples", input2="apples", input3="apples")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_strings' call")
            sleep(5)

            print("Making call to 'call_one_enum'")
            future_resp = self.client.call_one_enum(input1=Numbers.ONE)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_enum' call")
            sleep(5)

            print("Making call to 'call_optional_enum'")
            future_resp = self.client.call_optional_enum(input1=Numbers.ONE)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_enum' call")
            sleep(5)

            print("Making call to 'call_three_enums'")
            future_resp = self.client.call_three_enums(input1=Numbers.ONE, input2=Numbers.ONE, input3=Numbers.ONE)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_enums' call")
            sleep(5)

            print("Making call to 'call_one_struct'")
            future_resp = self.client.call_one_struct(
                input1=AllTypes(
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
            )
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_struct' call")
            sleep(5)

            print("Making call to 'call_optional_struct'")
            future_resp = self.client.call_optional_struct(
                input1=AllTypes(
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
            )
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_struct' call")
            sleep(5)

            print("Making call to 'call_three_structs'")
            future_resp = self.client.call_three_structs(
                input1=AllTypes(
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
                input2=AllTypes(
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
                input3=AllTypes(
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
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_structs' call")
            sleep(5)

            print("Making call to 'call_one_date_time'")
            future_resp = self.client.call_one_date_time(input1=datetime.now(UTC))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_date_time' call")
            sleep(5)

            print("Making call to 'call_optional_date_time'")
            future_resp = self.client.call_optional_date_time(input1=datetime.now(UTC))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_date_time' call")
            sleep(5)

            print("Making call to 'call_three_date_times'")
            future_resp = self.client.call_three_date_times(input1=datetime.now(UTC), input2=datetime.now(UTC), input3=datetime.now(UTC))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_date_times' call")
            sleep(5)

            print("Making call to 'call_one_duration'")
            future_resp = self.client.call_one_duration(input1=timedelta(seconds=3536))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_duration' call")
            sleep(5)

            print("Making call to 'call_optional_duration'")
            future_resp = self.client.call_optional_duration(input1=None)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_duration' call")
            sleep(5)

            print("Making call to 'call_three_durations'")
            future_resp = self.client.call_three_durations(input1=timedelta(seconds=3536), input2=timedelta(seconds=3536), input3=None)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_durations' call")
            sleep(5)

            print("Making call to 'call_one_binary'")
            future_resp = self.client.call_one_binary(input1=b"example binary data")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_binary' call")
            sleep(5)

            print("Making call to 'call_optional_binary'")
            future_resp = self.client.call_optional_binary(input1=b"example binary data")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_binary' call")
            sleep(5)

            print("Making call to 'call_three_binaries'")
            future_resp = self.client.call_three_binaries(input1=b"example binary data", input2=b"example binary data", input3=b"example binary data")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_three_binaries' call")
            sleep(5)

            print("Making call to 'call_one_list_of_integers'")
            future_resp = self.client.call_one_list_of_integers(input1=[42, 2022])
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_one_list_of_integers' call")
            sleep(5)

            print("Making call to 'call_optional_list_of_floats'")
            future_resp = self.client.call_optional_list_of_floats(input1=[3.14, 1.0])
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_optional_list_of_floats' call")
            sleep(5)

            print("Making call to 'call_two_lists'")
            future_resp = self.client.call_two_lists(input1=[Numbers.ONE, Numbers.ONE], input2=["apples", "foo"])
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'call_two_lists' call")
            sleep(5)

            self.client.read_write_integer = 42

            self.client.read_write_optional_integer = 42

            self.client.read_write_two_integers = ReadWriteTwoIntegersProperty(
                first=42,
                second=42,
            )

            self.client.read_write_string = "apples"

            self.client.read_write_optional_string = "apples"

            self.client.read_write_two_strings = ReadWriteTwoStringsProperty(
                first="apples",
                second="apples",
            )

            self.client.read_write_struct = AllTypes(
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

            self.client.read_write_optional_struct = AllTypes(
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

            self.client.read_write_two_structs = ReadWriteTwoStructsProperty(
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
            )

            self.client.read_write_enum = Numbers.ONE

            self.client.read_write_optional_enum = Numbers.ONE

            self.client.read_write_two_enums = ReadWriteTwoEnumsProperty(
                first=Numbers.ONE,
                second=Numbers.ONE,
            )

            self.client.read_write_datetime = datetime.now(UTC)

            self.client.read_write_optional_datetime = datetime.now(UTC)

            self.client.read_write_two_datetimes = ReadWriteTwoDatetimesProperty(
                first=datetime.now(UTC),
                second=None,
            )

            self.client.read_write_duration = timedelta(seconds=3536)

            self.client.read_write_optional_duration = None

            self.client.read_write_two_durations = ReadWriteTwoDurationsProperty(
                first=timedelta(seconds=3536),
                second=None,
            )

            self.client.read_write_binary = b"example binary data"

            self.client.read_write_optional_binary = b"example binary data"

            self.client.read_write_two_binaries = ReadWriteTwoBinariesProperty(
                first=b"example binary data",
                second=b"example binary data",
            )

            self.client.read_write_list_of_strings = ["apples", "foo"]

            self.client.read_write_lists = ReadWriteListsProperty(
                the_list=[Numbers.ONE, Numbers.ONE],
                optional_list=[datetime.now(UTC), datetime.now(UTC)],
            )

            sleep(10)


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    doer1 = SuperAwesomeDoerOfThings("Doer1", conn)

    print("Ctrl-C will stop the program.")
    signal.pause()
