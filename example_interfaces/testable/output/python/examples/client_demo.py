import signal
from time import sleep
from typing import Optional, Union
from datetime import datetime, timedelta
from testableipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from testableipc.client import TestAbleClient, TestAbleClientBuilder, TestAbleClientDiscoverer
from testableipc import interface_types

if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)

    client_builder = TestAbleClientBuilder()

    @client_builder.receive_empty
    def print_empty_receipt():
        """ """
        print(f"Got a 'empty' signal: ")

    @client_builder.receive_single_int
    def print_singleInt_receipt(value: int):
        """
        @param value int The integer value.
        """
        print(f"Got a 'singleInt' signal: value={ value } ")

    @client_builder.receive_single_optional_int
    def print_singleOptionalInt_receipt(value: Optional[int]):
        """
        @param value Optional[int] The integer value.
        """
        print(f"Got a 'singleOptionalInt' signal: value={ value } ")

    @client_builder.receive_three_integers
    def print_threeIntegers_receipt(first: int, second: int, third: Optional[int]):
        """
        @param first int The first integer value.
        @param second int The second integer value.
        @param third Optional[int] The third integer value.
        """
        print(f"Got a 'threeIntegers' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_string
    def print_singleString_receipt(value: str):
        """
        @param value str The string value.
        """
        print(f"Got a 'singleString' signal: value={ value } ")

    @client_builder.receive_single_optional_string
    def print_singleOptionalString_receipt(value: Optional[str]):
        """
        @param value Optional[str] The string value.
        """
        print(f"Got a 'singleOptionalString' signal: value={ value } ")

    @client_builder.receive_three_strings
    def print_threeStrings_receipt(first: str, second: str, third: Optional[str]):
        """
        @param first str The first string value.
        @param second str The second string value.
        @param third Optional[str] The third string value.
        """
        print(f"Got a 'threeStrings' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_enum
    def print_singleEnum_receipt(value: interface_types.Numbers):
        """
        @param value interface_types.Numbers The enum value.
        """
        print(f"Got a 'singleEnum' signal: value={ value } ")

    @client_builder.receive_single_optional_enum
    def print_singleOptionalEnum_receipt(value: Optional[interface_types.Numbers]):
        """
        @param value Optional[interface_types.Numbers] The enum value.
        """
        print(f"Got a 'singleOptionalEnum' signal: value={ value } ")

    @client_builder.receive_three_enums
    def print_threeEnums_receipt(first: interface_types.Numbers, second: interface_types.Numbers, third: Optional[interface_types.Numbers]):
        """
        @param first interface_types.Numbers The first enum value.
        @param second interface_types.Numbers The second enum value.
        @param third Optional[interface_types.Numbers] The third enum value.
        """
        print(f"Got a 'threeEnums' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_struct
    def print_singleStruct_receipt(value: interface_types.AllTypes):
        """
        @param value interface_types.AllTypes The struct value.
        """
        print(f"Got a 'singleStruct' signal: value={ value } ")

    @client_builder.receive_single_optional_struct
    def print_singleOptionalStruct_receipt(value: interface_types.AllTypes):
        """
        @param value interface_types.AllTypes The struct value.
        """
        print(f"Got a 'singleOptionalStruct' signal: value={ value } ")

    @client_builder.receive_three_structs
    def print_threeStructs_receipt(first: interface_types.AllTypes, second: interface_types.AllTypes, third: interface_types.AllTypes):
        """
        @param first interface_types.AllTypes The first struct value.
        @param second interface_types.AllTypes The second struct value.
        @param third interface_types.AllTypes The third struct value.
        """
        print(f"Got a 'threeStructs' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_date_time
    def print_singleDateTime_receipt(value: datetime):
        """
        @param value datetime The date and time value.
        """
        print(f"Got a 'singleDateTime' signal: value={ value } ")

    @client_builder.receive_single_optional_datetime
    def print_singleOptionalDatetime_receipt(value: Optional[datetime]):
        """
        @param value Optional[datetime] The date and time value.
        """
        print(f"Got a 'singleOptionalDatetime' signal: value={ value } ")

    @client_builder.receive_three_date_times
    def print_threeDateTimes_receipt(first: datetime, second: datetime, third: Optional[datetime]):
        """
        @param first datetime The first date and time value.
        @param second datetime The second date and time value.
        @param third Optional[datetime] The third date and time value.
        """
        print(f"Got a 'threeDateTimes' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_duration
    def print_singleDuration_receipt(value: timedelta):
        """
        @param value timedelta The duration value.
        """
        print(f"Got a 'singleDuration' signal: value={ value } ")

    @client_builder.receive_single_optional_duration
    def print_singleOptionalDuration_receipt(value: Optional[timedelta]):
        """
        @param value Optional[timedelta] The duration value.
        """
        print(f"Got a 'singleOptionalDuration' signal: value={ value } ")

    @client_builder.receive_three_durations
    def print_threeDurations_receipt(first: timedelta, second: timedelta, third: Optional[timedelta]):
        """
        @param first timedelta The first duration value.
        @param second timedelta The second duration value.
        @param third Optional[timedelta] The third duration value.
        """
        print(f"Got a 'threeDurations' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_binary
    def print_singleBinary_receipt(value: bytes):
        """
        @param value bytes The binary value.
        """
        print(f"Got a 'singleBinary' signal: value={ value } ")

    @client_builder.receive_single_optional_binary
    def print_singleOptionalBinary_receipt(value: bytes):
        """
        @param value bytes The binary value.
        """
        print(f"Got a 'singleOptionalBinary' signal: value={ value } ")

    @client_builder.receive_three_binaries
    def print_threeBinaries_receipt(first: bytes, second: bytes, third: bytes):
        """
        @param first bytes The first binary value.
        @param second bytes The second binary value.
        @param third bytes The third binary value.
        """
        print(f"Got a 'threeBinaries' signal: first={ first } second={ second } third={ third } ")

    @client_builder.receive_single_array_of_integers
    def print_singleArrayOfIntegers_receipt(values: list[int]):
        """
        @param values list[int] The array of integers.
        """
        print(f"Got a 'singleArrayOfIntegers' signal: values={ values } ")

    @client_builder.receive_single_optional_array_of_strings
    def print_singleOptionalArrayOfStrings_receipt(values: list[str]):
        """
        @param values list[str] The array of strings.
        """
        print(f"Got a 'singleOptionalArrayOfStrings' signal: values={ values } ")

    @client_builder.receive_array_of_every_type
    def print_arrayOfEveryType_receipt(
        first_of_integers: list[int],
        second_of_floats: list[float],
        third_of_strings: list[str],
        fourth_of_enums: list[interface_types.Numbers],
        fifth_of_structs: list[interface_types.Entry],
        sixth_of_datetimes: list[datetime.datetime],
        seventh_of_durations: list[datetime.timedelta],
        eighth_of_binaries: list[bytes],
    ):
        """
        @param first_of_integers list[int] The first array of integers.
        @param second_of_floats list[float] The second array of floats.
        @param third_of_strings list[str] The third array of strings.
        @param fourth_of_enums list[interface_types.Numbers] The fourth array of enums.
        @param fifth_of_structs list[interface_types.Entry] The fifth array of structs.
        @param sixth_of_datetimes list[datetime.datetime] The sixth array of date and time values.
        @param seventh_of_durations list[datetime.timedelta] The seventh array of duration values.
        @param eighth_of_binaries list[bytes] The eighth array of binary values.
        """
        print(
            f"Got a 'arrayOfEveryType' signal: first_of_integers={ first_of_integers } second_of_floats={ second_of_floats } third_of_strings={ third_of_strings } fourth_of_enums={ fourth_of_enums } fifth_of_structs={ fifth_of_structs } sixth_of_datetimes={ sixth_of_datetimes } seventh_of_durations={ seventh_of_durations } eighth_of_binaries={ eighth_of_binaries } "
        )

    @client_builder.read_write_integer_updated
    def print_new_read_write_integer_value(value: int):
        """ """
        print(f"Property 'read_write_integer' has been updated to: {value}")

    @client_builder.read_only_integer_updated
    def print_new_read_only_integer_value(value: int):
        """ """
        print(f"Property 'read_only_integer' has been updated to: {value}")

    @client_builder.read_write_optional_integer_updated
    def print_new_read_write_optional_integer_value(value: Optional[int]):
        """ """
        print(f"Property 'read_write_optional_integer' has been updated to: {value}")

    @client_builder.read_write_two_integers_updated
    def print_new_read_write_two_integers_value(value: interface_types.ReadWriteTwoIntegersProperty):
        """ """
        print(f"Property 'read_write_two_integers' has been updated to: {value}")

    @client_builder.read_only_string_updated
    def print_new_read_only_string_value(value: str):
        """ """
        print(f"Property 'read_only_string' has been updated to: {value}")

    @client_builder.read_write_string_updated
    def print_new_read_write_string_value(value: str):
        """ """
        print(f"Property 'read_write_string' has been updated to: {value}")

    @client_builder.read_write_optional_string_updated
    def print_new_read_write_optional_string_value(value: Optional[str]):
        """ """
        print(f"Property 'read_write_optional_string' has been updated to: {value}")

    @client_builder.read_write_two_strings_updated
    def print_new_read_write_two_strings_value(value: interface_types.ReadWriteTwoStringsProperty):
        """ """
        print(f"Property 'read_write_two_strings' has been updated to: {value}")

    @client_builder.read_write_struct_updated
    def print_new_read_write_struct_value(value: interface_types.AllTypes):
        """ """
        print(f"Property 'read_write_struct' has been updated to: {value}")

    @client_builder.read_write_optional_struct_updated
    def print_new_read_write_optional_struct_value(value: interface_types.AllTypes):
        """ """
        print(f"Property 'read_write_optional_struct' has been updated to: {value}")

    @client_builder.read_write_two_structs_updated
    def print_new_read_write_two_structs_value(value: interface_types.ReadWriteTwoStructsProperty):
        """ """
        print(f"Property 'read_write_two_structs' has been updated to: {value}")

    @client_builder.read_only_enum_updated
    def print_new_read_only_enum_value(value: interface_types.Numbers):
        """ """
        print(f"Property 'read_only_enum' has been updated to: {value}")

    @client_builder.read_write_enum_updated
    def print_new_read_write_enum_value(value: interface_types.Numbers):
        """ """
        print(f"Property 'read_write_enum' has been updated to: {value}")

    @client_builder.read_write_optional_enum_updated
    def print_new_read_write_optional_enum_value(value: Optional[interface_types.Numbers]):
        """ """
        print(f"Property 'read_write_optional_enum' has been updated to: {value}")

    @client_builder.read_write_two_enums_updated
    def print_new_read_write_two_enums_value(value: interface_types.ReadWriteTwoEnumsProperty):
        """ """
        print(f"Property 'read_write_two_enums' has been updated to: {value}")

    @client_builder.read_write_datetime_updated
    def print_new_read_write_datetime_value(value: datetime):
        """ """
        print(f"Property 'read_write_datetime' has been updated to: {value}")

    @client_builder.read_write_optional_datetime_updated
    def print_new_read_write_optional_datetime_value(value: Optional[datetime]):
        """ """
        print(f"Property 'read_write_optional_datetime' has been updated to: {value}")

    @client_builder.read_write_two_datetimes_updated
    def print_new_read_write_two_datetimes_value(value: interface_types.ReadWriteTwoDatetimesProperty):
        """ """
        print(f"Property 'read_write_two_datetimes' has been updated to: {value}")

    @client_builder.read_write_duration_updated
    def print_new_read_write_duration_value(value: timedelta):
        """ """
        print(f"Property 'read_write_duration' has been updated to: {value}")

    @client_builder.read_write_optional_duration_updated
    def print_new_read_write_optional_duration_value(value: Optional[timedelta]):
        """ """
        print(f"Property 'read_write_optional_duration' has been updated to: {value}")

    @client_builder.read_write_two_durations_updated
    def print_new_read_write_two_durations_value(value: interface_types.ReadWriteTwoDurationsProperty):
        """ """
        print(f"Property 'read_write_two_durations' has been updated to: {value}")

    @client_builder.read_write_binary_updated
    def print_new_read_write_binary_value(value: bytes):
        """ """
        print(f"Property 'read_write_binary' has been updated to: {value}")

    @client_builder.read_write_optional_binary_updated
    def print_new_read_write_optional_binary_value(value: bytes):
        """ """
        print(f"Property 'read_write_optional_binary' has been updated to: {value}")

    @client_builder.read_write_two_binaries_updated
    def print_new_read_write_two_binaries_value(value: interface_types.ReadWriteTwoBinariesProperty):
        """ """
        print(f"Property 'read_write_two_binaries' has been updated to: {value}")

    @client_builder.read_write_list_of_strings_updated
    def print_new_read_write_list_of_strings_value(value: list[str]):
        """ """
        print(f"Property 'read_write_list_of_strings' has been updated to: {value}")

    @client_builder.read_write_lists_updated
    def print_new_read_write_lists_value(value: interface_types.ReadWriteListsProperty):
        """ """
        print(f"Property 'read_write_lists' has been updated to: {value}")

    discovery = TestAbleClientDiscoverer(conn, client_builder)
    fut_client = discovery.get_singleton_client()
    try:
        client = fut_client.result(10)
    except futures.TimeoutError:
        print("Timed out waiting for a service to appear")
        exit(1)

    sleep(2)

    print("Making call to 'call_with_nothing'")
    future_resp = client.call_with_nothing()
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_with_nothing' call")

    print("Making call to 'call_one_integer'")
    future_resp = client.call_one_integer(input1=42)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_integer' call")

    print("Making call to 'call_optional_integer'")
    future_resp = client.call_optional_integer(input1=42)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_integer' call")

    print("Making call to 'call_three_integers'")
    future_resp = client.call_three_integers(input1=42, input2=42, input3=42)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_integers' call")

    print("Making call to 'call_one_string'")
    future_resp = client.call_one_string(input1="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_string' call")

    print("Making call to 'call_optional_string'")
    future_resp = client.call_optional_string(input1="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_string' call")

    print("Making call to 'call_three_strings'")
    future_resp = client.call_three_strings(input1="apples", input2="apples", input3="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_strings' call")

    print("Making call to 'call_one_enum'")
    future_resp = client.call_one_enum(input1=interface_types.Numbers.ONE)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_enum' call")

    print("Making call to 'call_optional_enum'")
    future_resp = client.call_optional_enum(input1=interface_types.Numbers.ONE)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_enum' call")

    print("Making call to 'call_three_enums'")
    future_resp = client.call_three_enums(input1=interface_types.Numbers.ONE, input2=interface_types.Numbers.ONE, input3=interface_types.Numbers.ONE)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_enums' call")

    print("Making call to 'call_one_struct'")
    future_resp = client.call_one_struct(
        input1=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            an_entry_object=interface_types.Entry(key=42, value="apples"),
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_entry_object=interface_types.Entry(key=42, value="apples"),
            optional_date_time=datetime.now(),
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            optional_array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            array_of_datetimes=[datetime.now(), datetime.now()],
            optional_array_of_datetimes=[datetime.now(), datetime.now()],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
        )
    )
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_struct' call")

    print("Making call to 'call_optional_struct'")
    future_resp = client.call_optional_struct(
        input1=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            an_entry_object=interface_types.Entry(key=42, value="apples"),
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_entry_object=interface_types.Entry(key=42, value="apples"),
            optional_date_time=datetime.now(),
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            optional_array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            array_of_datetimes=[datetime.now(), datetime.now()],
            optional_array_of_datetimes=[datetime.now(), datetime.now()],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
        )
    )
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_struct' call")

    print("Making call to 'call_three_structs'")
    future_resp = client.call_three_structs(
        input1=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            an_entry_object=interface_types.Entry(key=42, value="apples"),
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_entry_object=interface_types.Entry(key=42, value="apples"),
            optional_date_time=None,
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            optional_array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            array_of_datetimes=[datetime.now(), datetime.now()],
            optional_array_of_datetimes=[datetime.now(), datetime.now()],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
        ),
        input2=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            an_entry_object=interface_types.Entry(key=42, value="apples"),
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_entry_object=interface_types.Entry(key=42, value="apples"),
            optional_date_time=None,
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            optional_array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            array_of_datetimes=[datetime.now(), datetime.now()],
            optional_array_of_datetimes=[datetime.now(), datetime.now()],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
        ),
        input3=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            an_entry_object=interface_types.Entry(key=42, value="apples"),
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_entry_object=interface_types.Entry(key=42, value="apples"),
            optional_date_time=datetime.now(),
            optional_duration=None,
            optional_binary=b"example binary data",
            array_of_integers=[42, 2022],
            optional_array_of_integers=[42, 2022],
            array_of_strings=["apples", "foo"],
            optional_array_of_strings=["apples", "foo"],
            array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            optional_array_of_enums=[interface_types.Numbers.ONE, interface_types.Numbers.ONE],
            array_of_datetimes=[datetime.now(), datetime.now()],
            optional_array_of_datetimes=[datetime.now(), datetime.now()],
            array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            optional_array_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
            array_of_binaries=[b"example binary data", b"example binary data"],
            optional_array_of_binaries=[b"example binary data", b"example binary data"],
            array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
            optional_array_of_entry_objects=[interface_types.Entry(key=42, value="apples"), interface_types.Entry(key=2022, value="foo")],
        ),
    )
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_structs' call")

    print("Making call to 'call_one_date_time'")
    future_resp = client.call_one_date_time(input1=datetime.now())
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_date_time' call")

    print("Making call to 'call_optional_date_time'")
    future_resp = client.call_optional_date_time(input1=datetime.now())
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_date_time' call")

    print("Making call to 'call_three_date_times'")
    future_resp = client.call_three_date_times(input1=datetime.now(), input2=datetime.now(), input3=datetime.now())
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_date_times' call")

    print("Making call to 'call_one_duration'")
    future_resp = client.call_one_duration(input1=timedelta(seconds=3536))
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_duration' call")

    print("Making call to 'call_optional_duration'")
    future_resp = client.call_optional_duration(input1=None)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_duration' call")

    print("Making call to 'call_three_durations'")
    future_resp = client.call_three_durations(input1=timedelta(seconds=3536), input2=timedelta(seconds=3536), input3=None)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_durations' call")

    print("Making call to 'call_one_binary'")
    future_resp = client.call_one_binary(input1=b"example binary data")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_binary' call")

    print("Making call to 'call_optional_binary'")
    future_resp = client.call_optional_binary(input1=b"example binary data")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_binary' call")

    print("Making call to 'call_three_binaries'")
    future_resp = client.call_three_binaries(input1=b"example binary data", input2=b"example binary data", input3=b"example binary data")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_three_binaries' call")

    print("Making call to 'call_one_list_of_integers'")
    future_resp = client.call_one_list_of_integers(input1=[42, 2022])
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_one_list_of_integers' call")

    print("Making call to 'call_optional_list_of_floats'")
    future_resp = client.call_optional_list_of_floats(input1=[3.14, 1.0])
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_optional_list_of_floats' call")

    print("Making call to 'call_two_lists'")
    future_resp = client.call_two_lists(input1=[interface_types.Numbers.ONE, interface_types.Numbers.ONE], input2=["apples", "foo"])
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'call_two_lists' call")

    print("Ctrl-C will stop the program.")
    signal.pause()
