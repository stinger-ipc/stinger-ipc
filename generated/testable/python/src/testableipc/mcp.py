from stinger_python_utils.mcp import (
    MethodDefinition,
    PropertyDefinition,
    SignalDefinition,
    StingerMCPPlugin,
)

from testableipc.client import TestableClient, TestableClientDiscoverer
from testableipc.interface_types import *


class TestableMCPPlugin(StingerMCPPlugin):
    """MCP plugin for the testable interface."""

    def get_plugin_name(self) -> str:
        return "testable"

    def get_discovery_class(self) -> type:
        return TestableClientDiscoverer

    def get_client_class(self) -> type:
        return TestableClient

    def get_signals(self) -> list[SignalDefinition]:
        return [
            SignalDefinition(
                name="empty",
                description="A signal with no parameters.",
            ),
            SignalDefinition(
                name="single_int",
                description="A signal with a single integer parameter.",
            ),
            SignalDefinition(
                name="single_optional_int",
                description="A signal with a single optional integer parameter.",
            ),
            SignalDefinition(
                name="three_integers",
                description="A signal with three integer parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_string",
                description="A signal with a single string parameter.",
            ),
            SignalDefinition(
                name="single_optional_string",
                description="A signal with a single optional string parameter.",
            ),
            SignalDefinition(
                name="three_strings",
                description="A signal with three string parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_enum",
                description="A signal with a single enum parameter.",
            ),
            SignalDefinition(
                name="single_optional_enum",
                description="A signal with a single optional enum parameter.",
            ),
            SignalDefinition(
                name="three_enums",
                description="A signal with three enum parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_struct",
                description="A signal with a single struct parameter.",
            ),
            SignalDefinition(
                name="single_optional_struct",
                description="A signal with a single optional struct parameter.",
            ),
            SignalDefinition(
                name="three_structs",
                description="A signal with three struct parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_date_time",
                description="A signal with a single date and time parameter.",
            ),
            SignalDefinition(
                name="single_optional_datetime",
                description="A signal with a single optional date and time parameter.",
            ),
            SignalDefinition(
                name="three_date_times",
                description="A signal with three date and time parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_duration",
                description="A signal with a single duration parameter.",
            ),
            SignalDefinition(
                name="single_optional_duration",
                description="A signal with a single optional duration parameter.",
            ),
            SignalDefinition(
                name="three_durations",
                description="A signal with three duration parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_binary",
                description="A signal with a single binary parameter.",
            ),
            SignalDefinition(
                name="single_optional_binary",
                description="A signal with a single optional binary parameter.",
            ),
            SignalDefinition(
                name="three_binaries",
                description="A signal with three binary parameters, the third is optional.",
            ),
            SignalDefinition(
                name="single_array_of_integers",
                description="A signal with an array of integers.",
            ),
            SignalDefinition(
                name="single_optional_array_of_strings",
                description="A signal with an optional array of strings.",
            ),
            SignalDefinition(
                name="array_of_every_type",
                description="",
            ),
        ]

    def get_methods(self) -> list[MethodDefinition]:
        return [
            MethodDefinition(
                name="call_with_nothing",
                description="Method that takes no arguments and returns nothing.",
                arguments_model=CallWithNothingMethodRequest,
            ),
            MethodDefinition(
                name="call_one_integer",
                description="Method that takes one integer argument and returns one integer value.",
                arguments_model=CallOneIntegerMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_integer",
                description="Method that takes one optional integer argument and returns one optional integer value.",
                arguments_model=CallOptionalIntegerMethodRequest,
            ),
            MethodDefinition(
                name="call_three_integers",
                description="Method that takes three integer arguments, the third is optional, and returns three integer values, the third is optional.",
                arguments_model=CallThreeIntegersMethodRequest,
            ),
            MethodDefinition(
                name="call_one_string",
                description="Method that takes one string argument and returns one string value.",
                arguments_model=CallOneStringMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_string",
                description="Method that takes one optional string argument and returns one optional string value.",
                arguments_model=CallOptionalStringMethodRequest,
            ),
            MethodDefinition(
                name="call_three_strings",
                description="Method that takes three string arguments, the 2nd is optional, and returns three string values, the 2nd is optional.",
                arguments_model=CallThreeStringsMethodRequest,
            ),
            MethodDefinition(
                name="call_one_enum",
                description="Method that takes one enum argument and returns one enum value.",
                arguments_model=CallOneEnumMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_enum",
                description="Method that takes one optional enum argument and returns one optional enum value.",
                arguments_model=CallOptionalEnumMethodRequest,
            ),
            MethodDefinition(
                name="call_three_enums",
                description="Method that takes three enum arguments, the third is optional, and returns three enum values, the third is optional.",
                arguments_model=CallThreeEnumsMethodRequest,
            ),
            MethodDefinition(
                name="call_one_struct",
                description="Method that takes one struct argument and returns one struct value.",
                arguments_model=CallOneStructMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_struct",
                description="Method that takes one optional struct argument and returns one optional struct value.",
                arguments_model=CallOptionalStructMethodRequest,
            ),
            MethodDefinition(
                name="call_three_structs",
                description="Method that takes three struct arguments, the first is optional, and returns three struct values, the first is optional.",
                arguments_model=CallThreeStructsMethodRequest,
            ),
            MethodDefinition(
                name="call_one_date_time",
                description="Method that takes one date and time argument and returns one date and time value.",
                arguments_model=CallOneDateTimeMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_date_time",
                description="Method that takes one optional date and time argument and returns one optional date and time value.",
                arguments_model=CallOptionalDateTimeMethodRequest,
            ),
            MethodDefinition(
                name="call_three_date_times",
                description="Method that takes three date and time arguments, the third is optional, and returns three date and time values, the third is optional.",
                arguments_model=CallThreeDateTimesMethodRequest,
            ),
            MethodDefinition(
                name="call_one_duration",
                description="Method that takes one duration argument and returns one duration value.",
                arguments_model=CallOneDurationMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_duration",
                description="Method that takes one optional duration argument and returns one optional duration value.",
                arguments_model=CallOptionalDurationMethodRequest,
            ),
            MethodDefinition(
                name="call_three_durations",
                description="Method that takes three duration arguments, the third is optional, and returns three duration values, the third is optional.",
                arguments_model=CallThreeDurationsMethodRequest,
            ),
            MethodDefinition(
                name="call_one_binary",
                description="Method that takes one binary argument and returns one binary value.",
                arguments_model=CallOneBinaryMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_binary",
                description="Method that takes one optional binary argument and returns one optional binary value.",
                arguments_model=CallOptionalBinaryMethodRequest,
            ),
            MethodDefinition(
                name="call_three_binaries",
                description="Method that takes three binary arguments, the third is optional, and returns three binary values, the third is optional.",
                arguments_model=CallThreeBinariesMethodRequest,
            ),
            MethodDefinition(
                name="call_one_list_of_integers",
                description="Method that takes one list of integers argument and returns one list of integers value.",
                arguments_model=CallOneListOfIntegersMethodRequest,
            ),
            MethodDefinition(
                name="call_optional_list_of_floats",
                description="Method that takes one optional list of floats argument and returns one optional list of floats value.",
                arguments_model=CallOptionalListOfFloatsMethodRequest,
            ),
            MethodDefinition(
                name="call_two_lists",
                description="Method that takes two list arguments, the second is optional, and returns two list values, the second is optional.",
                arguments_model=CallTwoListsMethodRequest,
            ),
        ]

    def get_properties(self) -> list[PropertyDefinition]:
        return [
            PropertyDefinition(
                name="read_write_integer",
                description="A read-write integer property.",
                readonly=False,
                schema=ReadWriteIntegerProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_only_integer",
                description="A read-only integer property.",
                readonly=True,
                schema=ReadOnlyIntegerProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_integer",
                description="A read-write optional integer property.",
                readonly=False,
                schema=ReadWriteOptionalIntegerProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_integers",
                description="A read-write property with two integer values. The second is optional.",
                readonly=False,
                schema=ReadWriteTwoIntegersProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_only_string",
                description="A read-only string property.",
                readonly=True,
                schema=ReadOnlyStringProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_string",
                description="A read-write string property.",
                readonly=False,
                schema=ReadWriteStringProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_string",
                description="A read-write optional string property.",
                readonly=False,
                schema=ReadWriteOptionalStringProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_strings",
                description="A read-write property with two string values. The second is optional.",
                readonly=False,
                schema=ReadWriteTwoStringsProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_struct",
                description="A read-write struct property.",
                readonly=False,
                schema=ReadWriteStructProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_struct",
                description="A read-write optional struct property.",
                readonly=False,
                schema=ReadWriteOptionalStructProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_structs",
                description="A read-write property with two struct values. The second is optional.",
                readonly=False,
                schema=ReadWriteTwoStructsProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_only_enum",
                description="A read-only enum property.",
                readonly=True,
                schema=ReadOnlyEnumProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_enum",
                description="A read-write enum property.",
                readonly=False,
                schema=ReadWriteEnumProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_enum",
                description="A read-write optional enum property.",
                readonly=False,
                schema=ReadWriteOptionalEnumProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_enums",
                description="A read-write property with two enum values. The second is optional.",
                readonly=False,
                schema=ReadWriteTwoEnumsProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_datetime",
                description="A read-write datetime property.",
                readonly=False,
                schema=ReadWriteDatetimeProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_datetime",
                description="A read-write optional datetime property.",
                readonly=False,
                schema=ReadWriteOptionalDatetimeProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_datetimes",
                description="A read-write property with two datetime values. The second is optional.",
                readonly=False,
                schema=ReadWriteTwoDatetimesProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_duration",
                description="A read-write duration property.",
                readonly=False,
                schema=ReadWriteDurationProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_duration",
                description="A read-write optional duration property.",
                readonly=False,
                schema=ReadWriteOptionalDurationProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_durations",
                description="A read-write property with two duration values. The second is optional.",
                readonly=False,
                schema=ReadWriteTwoDurationsProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_binary",
                description="A read-write binary property.",
                readonly=False,
                schema=ReadWriteBinaryProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_optional_binary",
                description="A read-write optional binary property.",
                readonly=False,
                schema=ReadWriteOptionalBinaryProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_two_binaries",
                description="A read-write property with two binary values.  The second is optional.",
                readonly=False,
                schema=ReadWriteTwoBinariesProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_list_of_strings",
                description="A read-write property that is a list of strings.",
                readonly=False,
                schema=ReadWriteListOfStringsProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="read_write_lists",
                description="A read-write property containing two lists.  The second list is optional.",
                readonly=False,
                schema=ReadWriteListsProperty.model_json_schema(),
            ),
        ]
