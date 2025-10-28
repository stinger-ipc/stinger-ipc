from time import sleep
import signal
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from testableipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from testableipc.server import TestAbleServer
from testableipc.interface_types import *

if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = TestAbleServer(conn, "py-server-demo:1")

    server.read_write_integer = 42

    server.read_only_integer = 42

    server.read_write_optional_integer = 42

    server.read_write_two_integers = ReadWriteTwoIntegersProperty(
        first=42,
        second=42,
    )

    server.read_only_string = "apples"

    server.read_write_string = "apples"

    server.read_write_optional_string = "apples"

    server.read_write_two_strings = ReadWriteTwoStringsProperty(
        first="apples",
        second="apples",
    )

    server.read_write_struct = AllTypes(
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

    server.read_write_optional_struct = AllTypes(
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

    server.read_write_two_structs = ReadWriteTwoStructsProperty(
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
    )

    server.read_only_enum = Numbers.ONE

    server.read_write_enum = Numbers.ONE

    server.read_write_optional_enum = Numbers.ONE

    server.read_write_two_enums = ReadWriteTwoEnumsProperty(
        first=Numbers.ONE,
        second=Numbers.ONE,
    )

    server.read_write_datetime = datetime.now(UTC)

    server.read_write_optional_datetime = datetime.now(UTC)

    server.read_write_two_datetimes = ReadWriteTwoDatetimesProperty(
        first=datetime.now(UTC),
        second=datetime.now(UTC),
    )

    server.read_write_duration = timedelta(seconds=3536)

    server.read_write_optional_duration = None

    server.read_write_two_durations = ReadWriteTwoDurationsProperty(
        first=timedelta(seconds=3536),
        second=None,
    )

    server.read_write_binary = b"example binary data"

    server.read_write_optional_binary = b"example binary data"

    server.read_write_two_binaries = ReadWriteTwoBinariesProperty(
        first=b"example binary data",
        second=b"example binary data",
    )

    server.read_write_list_of_strings = ["apples", "foo"]

    server.read_write_lists = ReadWriteListsProperty(
        the_list=[Numbers.ONE, Numbers.ONE],
        optionalList=[datetime.now(UTC), datetime.now(UTC)],
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
    def call_three_integers(input1: int, input2: int, input3: Optional[int]) -> CallThreeIntegersMethodResponse:
        """This is an example handler for the 'callThreeIntegers' method."""
        print(f"Running call_three_integers'({input1}, {input2}, {input3})'")
        return CallThreeIntegersMethodResponse(output1=42, output2=42, output3=42)

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
    def call_three_strings(input1: str, input2: Optional[str], input3: str) -> CallThreeStringsMethodResponse:
        """This is an example handler for the 'callThreeStrings' method."""
        print(f"Running call_three_strings'({input1}, {input2}, {input3})'")
        return CallThreeStringsMethodResponse(output1="apples", output2="apples", output3="apples")

    @server.handle_call_one_enum
    def call_one_enum(input1: Numbers) -> Numbers:
        """This is an example handler for the 'callOneEnum' method."""
        print(f"Running call_one_enum'({input1})'")
        return Numbers.ONE

    @server.handle_call_optional_enum
    def call_optional_enum(input1: Optional[Numbers]) -> Optional[Numbers]:
        """This is an example handler for the 'callOptionalEnum' method."""
        print(f"Running call_optional_enum'({input1})'")
        return Numbers.ONE

    @server.handle_call_three_enums
    def call_three_enums(input1: Numbers, input2: Numbers, input3: Optional[Numbers]) -> CallThreeEnumsMethodResponse:
        """This is an example handler for the 'callThreeEnums' method."""
        print(f"Running call_three_enums'({input1}, {input2}, {input3})'")
        return CallThreeEnumsMethodResponse(output1=Numbers.ONE, output2=Numbers.ONE, output3=Numbers.ONE)

    @server.handle_call_one_struct
    def call_one_struct(input1: AllTypes) -> AllTypes:
        """This is an example handler for the 'callOneStruct' method."""
        print(f"Running call_one_struct'({input1})'")
        return AllTypes(
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

    @server.handle_call_optional_struct
    def call_optional_struct(input1: AllTypes) -> AllTypes:
        """This is an example handler for the 'callOptionalStruct' method."""
        print(f"Running call_optional_struct'({input1})'")
        return AllTypes(
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

    @server.handle_call_three_structs
    def call_three_structs(input1: AllTypes, input2: AllTypes, input3: AllTypes) -> CallThreeStructsMethodResponse:
        """This is an example handler for the 'callThreeStructs' method."""
        print(f"Running call_three_structs'({input1}, {input2}, {input3})'")
        return CallThreeStructsMethodResponse(
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

    @server.handle_call_one_date_time
    def call_one_date_time(input1: datetime) -> datetime:
        """This is an example handler for the 'callOneDateTime' method."""
        print(f"Running call_one_date_time'({input1})'")
        return datetime.now(UTC)

    @server.handle_call_optional_date_time
    def call_optional_date_time(input1: Optional[datetime]) -> Optional[datetime]:
        """This is an example handler for the 'callOptionalDateTime' method."""
        print(f"Running call_optional_date_time'({input1})'")
        return datetime.now(UTC)

    @server.handle_call_three_date_times
    def call_three_date_times(input1: datetime, input2: datetime, input3: Optional[datetime]) -> CallThreeDateTimesMethodResponse:
        """This is an example handler for the 'callThreeDateTimes' method."""
        print(f"Running call_three_date_times'({input1}, {input2}, {input3})'")
        return CallThreeDateTimesMethodResponse(output1=datetime.now(UTC), output2=datetime.now(UTC), output3=datetime.now(UTC))

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
    def call_three_durations(input1: timedelta, input2: timedelta, input3: Optional[timedelta]) -> CallThreeDurationsMethodResponse:
        """This is an example handler for the 'callThreeDurations' method."""
        print(f"Running call_three_durations'({input1}, {input2}, {input3})'")
        return CallThreeDurationsMethodResponse(output1=timedelta(seconds=3536), output2=timedelta(seconds=3536), output3=None)

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
    def call_three_binaries(input1: bytes, input2: bytes, input3: bytes) -> CallThreeBinariesMethodResponse:
        """This is an example handler for the 'callThreeBinaries' method."""
        print(f"Running call_three_binaries'({input1}, {input2}, {input3})'")
        return CallThreeBinariesMethodResponse(output1=b"example binary data", output2=b"example binary data", output3=b"example binary data")

    @server.handle_call_one_list_of_integers
    def call_one_list_of_integers(input1: List[int]) -> List[int]:
        """This is an example handler for the 'callOneListOfIntegers' method."""
        print(f"Running call_one_list_of_integers'({input1})'")
        return [42, 2022]

    @server.handle_call_optional_list_of_floats
    def call_optional_list_of_floats(input1: List[float]) -> List[float]:
        """This is an example handler for the 'callOptionalListOfFloats' method."""
        print(f"Running call_optional_list_of_floats'({input1})'")
        return [3.14, 1.0]

    @server.handle_call_two_lists
    def call_two_lists(input1: List[Numbers], input2: List[str]) -> CallTwoListsMethodResponse:
        """This is an example handler for the 'callTwoLists' method."""
        print(f"Running call_two_lists'({input1}, {input2})'")
        return CallTwoListsMethodResponse(output1=[Numbers.ONE, Numbers.ONE], output2=["apples", "foo"])

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
    def on_read_write_struct_update(value: AllTypes):
        print(f"Received update for 'read_write_struct' property: { value= }")

    @server.on_read_write_optional_struct_updates
    def on_read_write_optional_struct_update(value: AllTypes):
        print(f"Received update for 'read_write_optional_struct' property: { value= }")

    @server.on_read_write_two_structs_updates
    def on_read_write_two_structs_update(first: AllTypes, second: AllTypes):
        print(f"Received update for 'read_write_two_structs' property: { first= }, { second= }")

    @server.on_read_only_enum_updates
    def on_read_only_enum_update(value: Numbers):
        print(f"Received update for 'read_only_enum' property: { value= }")

    @server.on_read_write_enum_updates
    def on_read_write_enum_update(value: Numbers):
        print(f"Received update for 'read_write_enum' property: { value= }")

    @server.on_read_write_optional_enum_updates
    def on_read_write_optional_enum_update(value: Optional[Numbers]):
        print(f"Received update for 'read_write_optional_enum' property: { value= }")

    @server.on_read_write_two_enums_updates
    def on_read_write_two_enums_update(first: Numbers, second: Optional[Numbers]):
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

    @server.on_read_write_list_of_strings_updates
    def on_read_write_list_of_strings_update(value: List[str]):
        print(f"Received update for 'read_write_list_of_strings' property: { value= }")

    @server.on_read_write_lists_updates
    def on_read_write_lists_update(the_list: List[Numbers], optionalList: List[datetime]):
        print(f"Received update for 'read_write_lists' property: { the_list= }, { optionalList= }")

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
            server.emit_single_enum(Numbers.ONE)
            server.emit_single_optional_enum(Numbers.ONE)
            server.emit_three_enums(Numbers.ONE, Numbers.ONE, Numbers.ONE)
            server.emit_single_struct(
                AllTypes(
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
            server.emit_single_optional_struct(
                AllTypes(
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
            )
            server.emit_three_structs(
                AllTypes(
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
                AllTypes(
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
                AllTypes(
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
            server.emit_single_date_time(datetime.now(UTC))
            server.emit_single_optional_datetime(datetime.now(UTC))
            server.emit_three_date_times(datetime.now(UTC), datetime.now(UTC), datetime.now(UTC))
            server.emit_single_duration(timedelta(seconds=3536))
            server.emit_single_optional_duration(None)
            server.emit_three_durations(timedelta(seconds=3536), timedelta(seconds=3536), None)
            server.emit_single_binary(b"example binary data")
            server.emit_single_optional_binary(b"example binary data")
            server.emit_three_binaries(b"example binary data", b"example binary data", b"example binary data")
            server.emit_single_array_of_integers([42, 2022])
            server.emit_single_optional_array_of_strings(["apples", "foo"])
            server.emit_array_of_every_type(
                [42, 2022],
                [3.14, 1.0],
                ["apples", "foo"],
                [Numbers.ONE, Numbers.ONE],
                [Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                [datetime.now(UTC), datetime.now(UTC)],
                [timedelta(seconds=3536), timedelta(seconds=975)],
                [b"example binary data", b"example binary data"],
            )

            sleep(4)
            server.emit_empty()
            server.emit_single_int(value=42)
            server.emit_single_optional_int(value=42)
            server.emit_three_integers(first=42, second=42, third=42)
            server.emit_single_string(value="apples")
            server.emit_single_optional_string(value="apples")
            server.emit_three_strings(first="apples", second="apples", third="apples")
            server.emit_single_enum(value=Numbers.ONE)
            server.emit_single_optional_enum(value=Numbers.ONE)
            server.emit_three_enums(first=Numbers.ONE, second=Numbers.ONE, third=Numbers.ONE)
            server.emit_single_struct(
                value=AllTypes(
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
            server.emit_single_optional_struct(
                value=AllTypes(
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
            )
            server.emit_three_structs(
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
                third=AllTypes(
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
            server.emit_single_date_time(value=datetime.now(UTC))
            server.emit_single_optional_datetime(value=datetime.now(UTC))
            server.emit_three_date_times(first=datetime.now(UTC), second=datetime.now(UTC), third=datetime.now(UTC))
            server.emit_single_duration(value=timedelta(seconds=3536))
            server.emit_single_optional_duration(value=None)
            server.emit_three_durations(first=timedelta(seconds=3536), second=timedelta(seconds=3536), third=None)
            server.emit_single_binary(value=b"example binary data")
            server.emit_single_optional_binary(value=b"example binary data")
            server.emit_three_binaries(first=b"example binary data", second=b"example binary data", third=b"example binary data")
            server.emit_single_array_of_integers(values=[42, 2022])
            server.emit_single_optional_array_of_strings(values=["apples", "foo"])
            server.emit_array_of_every_type(
                first_of_integers=[42, 2022],
                second_of_floats=[3.14, 1.0],
                third_of_strings=["apples", "foo"],
                fourth_of_enums=[Numbers.ONE, Numbers.ONE],
                fifth_of_structs=[Entry(key=42, value="apples"), Entry(key=2022, value="foo")],
                sixth_of_datetimes=[datetime.now(UTC), datetime.now(UTC)],
                seventh_of_durations=[timedelta(seconds=3536), timedelta(seconds=975)],
                eighth_of_binaries=[b"example binary data", b"example binary data"],
            )

            sleep(16)
        except KeyboardInterrupt:
            break

    signal.pause()
