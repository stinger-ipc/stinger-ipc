from time import sleep
import signal
from typing import Optional, Union
from datetime import datetime, timedelta
from testableipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from testableipc.server import TestAbleServer
from testableipc import interface_types

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

    server.read_write_two_integers = interface_types.ReadWriteTwoIntegersProperty(
        first=42,
        second=42,
    )

    server.read_only_string = "apples"

    server.read_write_string = "apples"

    server.read_write_optional_string = "apples"

    server.read_write_two_strings = interface_types.ReadWriteTwoStringsProperty(
        first="apples",
        second="apples",
    )

    server.read_write_struct = interface_types.AllTypes(
        the_bool=True,
        the_int=42,
        the_number=3.14,
        the_str="apples",
        the_enum=interface_types.Numbers.ONE,
        date_and_time=datetime.now(),
        time_duration=timedelta(seconds=3536),
        data=b"example binary data",
        optional_integer=42,
        optional_string="apples",
        optional_enum=interface_types.Numbers.ONE,
        optional_date_time=datetime.now(),
        optional_duration=None,
        optional_binary=b"example binary data",
    )

    server.read_write_optional_struct = interface_types.AllTypes(
        the_bool=True,
        the_int=42,
        the_number=3.14,
        the_str="apples",
        the_enum=interface_types.Numbers.ONE,
        date_and_time=datetime.now(),
        time_duration=timedelta(seconds=3536),
        data=b"example binary data",
        optional_integer=42,
        optional_string="apples",
        optional_enum=interface_types.Numbers.ONE,
        optional_date_time=datetime.now(),
        optional_duration=None,
        optional_binary=b"example binary data",
    )

    server.read_write_two_structs = interface_types.ReadWriteTwoStructsProperty(
        first=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_date_time=datetime.now(),
            optional_duration=None,
            optional_binary=b"example binary data",
        ),
        second=interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_date_time=None,
            optional_duration=None,
            optional_binary=b"example binary data",
        ),
    )

    server.read_only_enum = interface_types.Numbers.ONE

    server.read_write_enum = interface_types.Numbers.ONE

    server.read_write_optional_enum = interface_types.Numbers.ONE

    server.read_write_two_enums = interface_types.ReadWriteTwoEnumsProperty(
        first=interface_types.Numbers.ONE,
        second=interface_types.Numbers.ONE,
    )

    server.read_write_datetime = datetime.now()

    server.read_write_optional_datetime = datetime.now()

    server.read_write_two_datetimes = interface_types.ReadWriteTwoDatetimesProperty(
        first=datetime.now(),
        second=datetime.now(),
    )

    server.read_write_duration = timedelta(seconds=3536)

    server.read_write_optional_duration = None

    server.read_write_two_durations = interface_types.ReadWriteTwoDurationsProperty(
        first=timedelta(seconds=3536),
        second=None,
    )

    server.read_write_binary = b"example binary data"

    server.read_write_optional_binary = b"example binary data"

    server.read_write_two_binaries = interface_types.ReadWriteTwoBinariesProperty(
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
    def call_three_integers(input1: int, input2: int, input3: Optional[int]) -> interface_types.CallThreeIntegersMethodResponse:
        """This is an example handler for the 'callThreeIntegers' method."""
        print(f"Running call_three_integers'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeIntegersMethodResponse(output1=42, output2=42, output3=42)

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
    def call_three_strings(input1: str, input2: Optional[str], input3: str) -> interface_types.CallThreeStringsMethodResponse:
        """This is an example handler for the 'callThreeStrings' method."""
        print(f"Running call_three_strings'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeStringsMethodResponse(output1="apples", output2="apples", output3="apples")

    @server.handle_call_one_enum
    def call_one_enum(input1: interface_types.Numbers) -> interface_types.Numbers:
        """This is an example handler for the 'callOneEnum' method."""
        print(f"Running call_one_enum'({input1})'")
        return interface_types.Numbers.ONE

    @server.handle_call_optional_enum
    def call_optional_enum(input1: Optional[interface_types.Numbers]) -> Optional[interface_types.Numbers]:
        """This is an example handler for the 'callOptionalEnum' method."""
        print(f"Running call_optional_enum'({input1})'")
        return interface_types.Numbers.ONE

    @server.handle_call_three_enums
    def call_three_enums(input1: interface_types.Numbers, input2: interface_types.Numbers, input3: Optional[interface_types.Numbers]) -> interface_types.CallThreeEnumsMethodResponse:
        """This is an example handler for the 'callThreeEnums' method."""
        print(f"Running call_three_enums'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeEnumsMethodResponse(output1=interface_types.Numbers.ONE, output2=interface_types.Numbers.ONE, output3=interface_types.Numbers.ONE)

    @server.handle_call_one_struct
    def call_one_struct(input1: interface_types.AllTypes) -> interface_types.AllTypes:
        """This is an example handler for the 'callOneStruct' method."""
        print(f"Running call_one_struct'({input1})'")
        return interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_date_time=datetime.now(),
            optional_duration=None,
            optional_binary=b"example binary data",
        )

    @server.handle_call_optional_struct
    def call_optional_struct(input1: interface_types.AllTypes) -> interface_types.AllTypes:
        """This is an example handler for the 'callOptionalStruct' method."""
        print(f"Running call_optional_struct'({input1})'")
        return interface_types.AllTypes(
            the_bool=True,
            the_int=42,
            the_number=3.14,
            the_str="apples",
            the_enum=interface_types.Numbers.ONE,
            date_and_time=datetime.now(),
            time_duration=timedelta(seconds=3536),
            data=b"example binary data",
            optional_integer=42,
            optional_string="apples",
            optional_enum=interface_types.Numbers.ONE,
            optional_date_time=datetime.now(),
            optional_duration=None,
            optional_binary=b"example binary data",
        )

    @server.handle_call_three_structs
    def call_three_structs(input1: interface_types.AllTypes, input2: interface_types.AllTypes, input3: interface_types.AllTypes) -> interface_types.CallThreeStructsMethodResponse:
        """This is an example handler for the 'callThreeStructs' method."""
        print(f"Running call_three_structs'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeStructsMethodResponse(
            output1=interface_types.AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=interface_types.Numbers.ONE,
                date_and_time=datetime.now(),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=interface_types.Numbers.ONE,
                optional_date_time=datetime.now(),
                optional_duration=None,
                optional_binary=b"example binary data",
            ),
            output2=interface_types.AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=interface_types.Numbers.ONE,
                date_and_time=datetime.now(),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=interface_types.Numbers.ONE,
                optional_date_time=datetime.now(),
                optional_duration=None,
                optional_binary=b"example binary data",
            ),
            output3=interface_types.AllTypes(
                the_bool=True,
                the_int=42,
                the_number=3.14,
                the_str="apples",
                the_enum=interface_types.Numbers.ONE,
                date_and_time=datetime.now(),
                time_duration=timedelta(seconds=3536),
                data=b"example binary data",
                optional_integer=42,
                optional_string="apples",
                optional_enum=interface_types.Numbers.ONE,
                optional_date_time=None,
                optional_duration=None,
                optional_binary=b"example binary data",
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
    def call_three_date_times(input1: datetime, input2: datetime, input3: Optional[datetime]) -> interface_types.CallThreeDateTimesMethodResponse:
        """This is an example handler for the 'callThreeDateTimes' method."""
        print(f"Running call_three_date_times'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeDateTimesMethodResponse(output1=datetime.now(), output2=datetime.now(), output3=datetime.now())

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
    def call_three_durations(input1: timedelta, input2: timedelta, input3: Optional[timedelta]) -> interface_types.CallThreeDurationsMethodResponse:
        """This is an example handler for the 'callThreeDurations' method."""
        print(f"Running call_three_durations'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeDurationsMethodResponse(output1=timedelta(seconds=3536), output2=timedelta(seconds=3536), output3=None)

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
    def call_three_binaries(input1: bytes, input2: bytes, input3: bytes) -> interface_types.CallThreeBinariesMethodResponse:
        """This is an example handler for the 'callThreeBinaries' method."""
        print(f"Running call_three_binaries'({input1}, {input2}, {input3})'")
        return interface_types.CallThreeBinariesMethodResponse(output1=b"example binary data", output2=b"example binary data", output3=b"example binary data")

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
    def on_read_write_struct_update(value: interface_types.AllTypes):
        print(f"Received update for 'read_write_struct' property: { value= }")

    @server.on_read_write_optional_struct_updates
    def on_read_write_optional_struct_update(value: interface_types.AllTypes):
        print(f"Received update for 'read_write_optional_struct' property: { value= }")

    @server.on_read_write_two_structs_updates
    def on_read_write_two_structs_update(first: interface_types.AllTypes, second: interface_types.AllTypes):
        print(f"Received update for 'read_write_two_structs' property: { first= }, { second= }")

    @server.on_read_only_enum_updates
    def on_read_only_enum_update(value: interface_types.Numbers):
        print(f"Received update for 'read_only_enum' property: { value= }")

    @server.on_read_write_enum_updates
    def on_read_write_enum_update(value: interface_types.Numbers):
        print(f"Received update for 'read_write_enum' property: { value= }")

    @server.on_read_write_optional_enum_updates
    def on_read_write_optional_enum_update(value: Optional[interface_types.Numbers]):
        print(f"Received update for 'read_write_optional_enum' property: { value= }")

    @server.on_read_write_two_enums_updates
    def on_read_write_two_enums_update(first: interface_types.Numbers, second: Optional[interface_types.Numbers]):
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
            server.emit_single_enum(interface_types.Numbers.ONE)
            server.emit_single_optional_enum(interface_types.Numbers.ONE)
            server.emit_three_enums(interface_types.Numbers.ONE, interface_types.Numbers.ONE, interface_types.Numbers.ONE)
            server.emit_single_struct(
                interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=None,
                    optional_duration=None,
                    optional_binary=b"example binary data",
                )
            )
            server.emit_single_optional_struct(
                interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                )
            )
            server.emit_three_structs(
                interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                ),
                interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                ),
                interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                ),
            )
            server.emit_single_date_time(datetime.now())
            server.emit_single_optional_datetime(None)
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
            server.emit_single_enum(value=interface_types.Numbers.ONE)
            server.emit_single_optional_enum(value=interface_types.Numbers.ONE)
            server.emit_three_enums(first=interface_types.Numbers.ONE, second=interface_types.Numbers.ONE, third=interface_types.Numbers.ONE)
            server.emit_single_struct(
                value=interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                )
            )
            server.emit_single_optional_struct(
                value=interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                )
            )
            server.emit_three_structs(
                first=interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                ),
                second=interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                ),
                third=interface_types.AllTypes(
                    the_bool=True,
                    the_int=42,
                    the_number=3.14,
                    the_str="apples",
                    the_enum=interface_types.Numbers.ONE,
                    date_and_time=datetime.now(),
                    time_duration=timedelta(seconds=3536),
                    data=b"example binary data",
                    optional_integer=42,
                    optional_string="apples",
                    optional_enum=interface_types.Numbers.ONE,
                    optional_date_time=datetime.now(),
                    optional_duration=None,
                    optional_binary=b"example binary data",
                ),
            )
            server.emit_single_date_time(value=datetime.now())
            server.emit_single_optional_datetime(value=datetime.now())
            server.emit_three_date_times(first=datetime.now(), second=datetime.now(), third=datetime.now())
            server.emit_single_duration(value=timedelta(seconds=3536))
            server.emit_single_optional_duration(value=None)
            server.emit_three_durations(first=timedelta(seconds=3536), second=timedelta(seconds=3536), third=None)
            server.emit_single_binary(value=b"example binary data")
            server.emit_single_optional_binary(value=b"example binary data")
            server.emit_three_binaries(first=b"example binary data", second=b"example binary data", third=b"example binary data")

            sleep(16)
        except KeyboardInterrupt:
            break

    signal.pause()
