"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the testable interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from pydantic import BaseModel, Field, PlainValidator, PlainSerializer, ConfigDict
from datetime import datetime, timedelta, UTC

from typing import Optional, Annotated, Union, List
import base64
from enum import IntEnum


def base64_decode_if_str(value: Union[str, bytes, None]) -> Optional[bytes]:
    """If the value is a string, decode it from base64 to bytes.  Otherwise return the bytes as-is."""
    if isinstance(value, str):
        return base64.b64decode(value)
    return value


class InterfaceInfo(BaseModel):
    interface_name: str = Field(default="testable")
    title: str = Field(default="Interface for testing")
    version: str = Field(default="0.0.1")
    instance: str
    connection_topic: str
    timestamp: str


class Numbers(IntEnum):
    """Interface enum `Numbers`."""

    ONE = 1
    TWO = 2
    THREE = 3


class Entry(BaseModel):
    """Interface struct `entry`."""

    model_config = ConfigDict(populate_by_name=True)
    key: Annotated[
        int,
        Field(
            description="An identifier.",
        ),
    ]
    value: Annotated[
        str,
        Field(
            description="A name.",
        ),
    ]


class AllTypes(BaseModel):
    """Interface struct `AllTypes`."""

    model_config = ConfigDict(populate_by_name=True)
    the_bool: Annotated[bool, Field()]
    the_int: Annotated[int, Field()]
    the_number: Annotated[
        float,
        Field(
            description="A floating point number.  Bool and int do not have descriptions.",
        ),
    ]
    the_str: Annotated[
        str,
        Field(
            description="A string type.",
        ),
    ]
    the_enum: Annotated[
        Numbers,
        Field(
            description="An enum type",
        ),
    ]
    an_entry_object: Annotated[
        Entry,
        Field(
            description="A struct type.",
        ),
    ]
    date_and_time: Annotated[
        datetime,
        Field(
            description="A date and time type.",
        ),
    ]
    time_duration: Annotated[
        timedelta,
        Field(
            description="A duration type.",
        ),
    ]
    data: Annotated[
        bytes,
        Field(
            description="A binary type.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]
    optional_integer: Annotated[Optional[int], Field(description="An optional integer type.", alias="OptionalInteger")]
    optional_string: Annotated[Optional[str], Field(description="An optional string type.", alias="OptionalString")]
    optional_enum: Annotated[Optional[Numbers], Field(description="An optional enum type, one of the numbers.", alias="OptionalEnum")]
    optional_entry_object: Annotated[Optional[Entry], Field(description="An optional struct type.", alias="optionalEntryObject")]
    optional_date_time: Annotated[Optional[datetime], Field(description="An optional date and time type.", alias="OptionalDateTime")]
    optional_duration: Annotated[Optional[timedelta], Field(description="An optional duration type.", alias="OptionalDuration")]
    optional_binary: Annotated[
        Optional[bytes],
        Field(description="An optional binary type.", alias="OptionalBinary"),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None),
    ]

    array_of_integers: Annotated[
        List[int],
        Field(
            description="An array of integers.",
        ),
    ]

    optional_array_of_integers: Annotated[
        Optional[List[int]],
        Field(
            description="An optional array of integers.",
        ),
    ]

    array_of_strings: Annotated[
        List[str],
        Field(
            description="An array of strings.",
        ),
    ]

    optional_array_of_strings: Annotated[
        Optional[List[str]],
        Field(
            description="An optional array of strings.",
        ),
    ]

    array_of_enums: Annotated[
        List[Numbers],
        Field(
            description="An array of enums.",
        ),
    ]

    optional_array_of_enums: Annotated[
        Optional[List[Numbers]],
        Field(
            description="An optional array of enums.",
        ),
    ]

    array_of_datetimes: Annotated[
        List[datetime],
        Field(
            description="An array of date and time values.",
        ),
    ]

    optional_array_of_datetimes: Annotated[
        Optional[List[datetime]],
        Field(
            description="An optional array of date and time values.",
        ),
    ]

    array_of_durations: Annotated[
        List[timedelta],
        Field(
            description="An array of duration values.",
        ),
    ]

    optional_array_of_durations: Annotated[
        Optional[List[timedelta]],
        Field(
            description="An optional array of duration values.",
        ),
    ]

    array_of_binaries: Annotated[
        List[bytes],
        Field(
            description="An array of binary values.",
        ),
        PlainValidator(lambda arr: [base64_decode_if_str(v) for v in arr]),
        PlainSerializer(lambda arr: [base64.b64encode(v).decode("utf-8") for v in arr]),
    ]

    optional_array_of_binaries: Annotated[
        Optional[List[bytes]],
        Field(
            description="An optional array of binary values.",
        ),
        PlainValidator(lambda arr: [base64_decode_if_str(v) for v in arr]),
        PlainSerializer(lambda arr: [base64.b64encode(v).decode("utf-8") for v in arr]),
    ]

    array_of_entry_objects: Annotated[
        List[Entry],
        Field(
            description="An array of struct values.",
        ),
    ]

    optional_array_of_entry_objects: Annotated[
        Optional[List[Entry]],
        Field(
            description="An optional array of struct values.",
        ),
    ]


class EmptySignalPayload(BaseModel):
    """Interface signal `empty`.

    A signal with no parameters.
    """

    model_config = ConfigDict(populate_by_name=True)


class SingleIntSignalPayload(BaseModel):
    """Interface signal `singleInt`.

    A signal with a single integer parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        int,
        Field(
            description="The integer value.",
        ),
    ]


class SingleOptionalIntSignalPayload(BaseModel):
    """Interface signal `singleOptionalInt`.

    A signal with a single optional integer parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[int],
        Field(
            description="The integer value.",
        ),
    ]


class ThreeIntegersSignalPayload(BaseModel):
    """Interface signal `threeIntegers`.

    A signal with three integer parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        int,
        Field(
            description="The first integer value.",
        ),
    ]
    second: Annotated[
        int,
        Field(
            description="The second integer value.",
        ),
    ]
    third: Annotated[
        Optional[int],
        Field(
            description="The third integer value.",
        ),
    ]


class SingleStringSignalPayload(BaseModel):
    """Interface signal `singleString`.

    A signal with a single string parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        str,
        Field(
            description="The string value.",
        ),
    ]


class SingleOptionalStringSignalPayload(BaseModel):
    """Interface signal `singleOptionalString`.

    A signal with a single optional string parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[str],
        Field(
            description="The string value.",
        ),
    ]


class ThreeStringsSignalPayload(BaseModel):
    """Interface signal `threeStrings`.

    A signal with three string parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        str,
        Field(
            description="The first string value.",
        ),
    ]
    second: Annotated[
        str,
        Field(
            description="The second string value.",
        ),
    ]
    third: Annotated[
        Optional[str],
        Field(
            description="The third string value.",
        ),
    ]


class SingleEnumSignalPayload(BaseModel):
    """Interface signal `singleEnum`.

    A signal with a single enum parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Numbers,
        Field(
            description="The enum value.",
        ),
    ]


class SingleOptionalEnumSignalPayload(BaseModel):
    """Interface signal `singleOptionalEnum`.

    A signal with a single optional enum parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[Numbers],
        Field(
            description="The enum value.",
        ),
    ]


class ThreeEnumsSignalPayload(BaseModel):
    """Interface signal `threeEnums`.

    A signal with three enum parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        Numbers,
        Field(
            description="The first enum value.",
        ),
    ]
    second: Annotated[
        Numbers,
        Field(
            description="The second enum value.",
        ),
    ]
    third: Annotated[
        Optional[Numbers],
        Field(
            description="The third enum value.",
        ),
    ]


class SingleStructSignalPayload(BaseModel):
    """Interface signal `singleStruct`.

    A signal with a single struct parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        AllTypes,
        Field(
            description="The struct value.",
        ),
    ]


class SingleOptionalStructSignalPayload(BaseModel):
    """Interface signal `singleOptionalStruct`.

    A signal with a single optional struct parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[AllTypes],
        Field(
            description="The struct value.",
        ),
    ]


class ThreeStructsSignalPayload(BaseModel):
    """Interface signal `threeStructs`.

    A signal with three struct parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        AllTypes,
        Field(
            description="The first struct value.",
        ),
    ]
    second: Annotated[
        AllTypes,
        Field(
            description="The second struct value.",
        ),
    ]
    third: Annotated[
        Optional[AllTypes],
        Field(
            description="The third struct value.",
        ),
    ]


class SingleDateTimeSignalPayload(BaseModel):
    """Interface signal `singleDateTime`.

    A signal with a single date and time parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        datetime,
        Field(
            description="The date and time value.",
        ),
    ]


class SingleOptionalDatetimeSignalPayload(BaseModel):
    """Interface signal `singleOptionalDatetime`.

    A signal with a single optional date and time parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[datetime],
        Field(
            description="The date and time value.",
        ),
    ]


class ThreeDateTimesSignalPayload(BaseModel):
    """Interface signal `threeDateTimes`.

    A signal with three date and time parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        datetime,
        Field(
            description="The first date and time value.",
        ),
    ]
    second: Annotated[
        datetime,
        Field(
            description="The second date and time value.",
        ),
    ]
    third: Annotated[
        Optional[datetime],
        Field(
            description="The third date and time value.",
        ),
    ]


class SingleDurationSignalPayload(BaseModel):
    """Interface signal `singleDuration`.

    A signal with a single duration parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        timedelta,
        Field(
            description="The duration value.",
        ),
    ]


class SingleOptionalDurationSignalPayload(BaseModel):
    """Interface signal `singleOptionalDuration`.

    A signal with a single optional duration parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[timedelta],
        Field(
            description="The duration value.",
        ),
    ]


class ThreeDurationsSignalPayload(BaseModel):
    """Interface signal `threeDurations`.

    A signal with three duration parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        timedelta,
        Field(
            description="The first duration value.",
        ),
    ]
    second: Annotated[
        timedelta,
        Field(
            description="The second duration value.",
        ),
    ]
    third: Annotated[
        Optional[timedelta],
        Field(
            description="The third duration value.",
        ),
    ]


class SingleBinarySignalPayload(BaseModel):
    """Interface signal `singleBinary`.

    A signal with a single binary parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        bytes,
        Field(
            description="The binary value.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]


class SingleOptionalBinarySignalPayload(BaseModel):
    """Interface signal `singleOptionalBinary`.

    A signal with a single optional binary parameter.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[
        Optional[bytes],
        Field(
            description="The binary value.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None),
    ]


class ThreeBinariesSignalPayload(BaseModel):
    """Interface signal `threeBinaries`.

    A signal with three binary parameters, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        bytes,
        Field(
            description="The first binary value.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]
    second: Annotated[
        bytes,
        Field(
            description="The second binary value.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]
    third: Annotated[
        Optional[bytes],
        Field(
            description="The third binary value.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None),
    ]


class SingleArrayOfIntegersSignalPayload(BaseModel):
    """Interface signal `singleArrayOfIntegers`.

    A signal with an array of integers.
    """

    model_config = ConfigDict(populate_by_name=True)

    values: Annotated[
        List[int],
        Field(
            description="The array of integers.",
        ),
    ]


class SingleOptionalArrayOfStringsSignalPayload(BaseModel):
    """Interface signal `singleOptionalArrayOfStrings`.

    A signal with an optional array of strings.
    """

    model_config = ConfigDict(populate_by_name=True)

    values: Annotated[
        Optional[List[str]],
        Field(
            description="The array of strings.",
        ),
    ]


class ArrayOfEveryTypeSignalPayload(BaseModel):
    """Interface signal `arrayOfEveryType`."""

    model_config = ConfigDict(populate_by_name=True)

    first_of_integers: Annotated[
        List[int],
        Field(
            description="The first array of integers.",
        ),
    ]

    second_of_floats: Annotated[
        List[float],
        Field(
            description="The second array of floats.",
        ),
    ]

    third_of_strings: Annotated[
        List[str],
        Field(
            description="The third array of strings.",
        ),
    ]

    fourth_of_enums: Annotated[
        List[Numbers],
        Field(
            description="The fourth array of enums.",
        ),
    ]

    fifth_of_structs: Annotated[
        List[Entry],
        Field(
            description="The fifth array of structs.",
        ),
    ]

    sixth_of_datetimes: Annotated[
        List[datetime],
        Field(
            description="The sixth array of date and time values.",
        ),
    ]

    seventh_of_durations: Annotated[
        List[timedelta],
        Field(
            description="The seventh array of duration values.",
        ),
    ]

    eighth_of_binaries: Annotated[
        List[bytes],
        Field(
            description="The eighth array of binary values.",
        ),
        PlainValidator(lambda arr: [base64_decode_if_str(v) for v in arr]),
        PlainSerializer(lambda arr: [base64.b64encode(v).decode("utf-8") for v in arr]),
    ]


class ReadWriteIntegerProperty(BaseModel):
    """Interface property `read_write_integer` (multi-value struct).

    A read-write integer property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[int, Field()]


class ReadOnlyIntegerProperty(BaseModel):
    """Interface property `read_only_integer` (multi-value struct).

    A read-only integer property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[int, Field()]


class ReadWriteOptionalIntegerProperty(BaseModel):
    """Interface property `read_write_optional_integer` (multi-value struct).

    A read-write optional integer property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[int], Field()]


class ReadWriteTwoIntegersProperty(BaseModel):
    """Interface property `read_write_two_integers` (multi-value struct).

    A read-write property with two integer values. The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        int,
        Field(
            description="An integer value.",
        ),
    ]
    second: Annotated[Optional[int], Field()]


class ReadOnlyStringProperty(BaseModel):
    """Interface property `read_only_string` (multi-value struct).

    A read-only string property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[str, Field()]


class ReadWriteStringProperty(BaseModel):
    """Interface property `read_write_string` (multi-value struct).

    A read-write string property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[str, Field()]


class ReadWriteOptionalStringProperty(BaseModel):
    """Interface property `read_write_optional_string` (multi-value struct).

    A read-write optional string property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[str], Field()]


class ReadWriteTwoStringsProperty(BaseModel):
    """Interface property `read_write_two_strings` (multi-value struct).

    A read-write property with two string values. The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        str,
        Field(
            description="A string value.",
        ),
    ]
    second: Annotated[Optional[str], Field()]


class ReadWriteStructProperty(BaseModel):
    """Interface property `read_write_struct` (multi-value struct).

    A read-write struct property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[AllTypes, Field()]


class ReadWriteOptionalStructProperty(BaseModel):
    """Interface property `read_write_optional_struct` (multi-value struct).

    A read-write optional struct property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[AllTypes], Field()]


class ReadWriteTwoStructsProperty(BaseModel):
    """Interface property `read_write_two_structs` (multi-value struct).

    A read-write property with two struct values. The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        AllTypes,
        Field(
            description="A struct value.",
        ),
    ]
    second: Annotated[Optional[AllTypes], Field()]


class ReadOnlyEnumProperty(BaseModel):
    """Interface property `read_only_enum` (multi-value struct).

    A read-only enum property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Numbers, Field()]


class ReadWriteEnumProperty(BaseModel):
    """Interface property `read_write_enum` (multi-value struct).

    A read-write enum property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Numbers, Field()]


class ReadWriteOptionalEnumProperty(BaseModel):
    """Interface property `read_write_optional_enum` (multi-value struct).

    A read-write optional enum property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[Numbers], Field()]


class ReadWriteTwoEnumsProperty(BaseModel):
    """Interface property `read_write_two_enums` (multi-value struct).

    A read-write property with two enum values. The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        Numbers,
        Field(
            description="An enum value.",
        ),
    ]
    second: Annotated[Optional[Numbers], Field()]


class ReadWriteDatetimeProperty(BaseModel):
    """Interface property `read_write_datetime` (multi-value struct).

    A read-write datetime property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[datetime, Field()]


class ReadWriteOptionalDatetimeProperty(BaseModel):
    """Interface property `read_write_optional_datetime` (multi-value struct).

    A read-write optional datetime property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[datetime], Field()]


class ReadWriteTwoDatetimesProperty(BaseModel):
    """Interface property `read_write_two_datetimes` (multi-value struct).

    A read-write property with two datetime values. The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        datetime,
        Field(
            description="A date and time value.",
        ),
    ]
    second: Annotated[Optional[datetime], Field()]


class ReadWriteDurationProperty(BaseModel):
    """Interface property `read_write_duration` (multi-value struct).

    A read-write duration property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[timedelta, Field()]


class ReadWriteOptionalDurationProperty(BaseModel):
    """Interface property `read_write_optional_duration` (multi-value struct).

    A read-write optional duration property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[timedelta], Field()]


class ReadWriteTwoDurationsProperty(BaseModel):
    """Interface property `read_write_two_durations` (multi-value struct).

    A read-write property with two duration values. The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        timedelta,
        Field(
            description="A duration of time.",
        ),
    ]
    second: Annotated[Optional[timedelta], Field()]


class ReadWriteBinaryProperty(BaseModel):
    """Interface property `read_write_binary` (multi-value struct).

    A read-write binary property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[bytes, Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8"))]


class ReadWriteOptionalBinaryProperty(BaseModel):
    """Interface property `read_write_optional_binary` (multi-value struct).

    A read-write optional binary property.
    """

    model_config = ConfigDict(populate_by_name=True)
    value: Annotated[Optional[bytes], Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None)]


class ReadWriteTwoBinariesProperty(BaseModel):
    """Interface property `read_write_two_binaries` (multi-value struct).

    A read-write property with two binary values.  The second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[
        bytes,
        Field(
            description="A binary blob of data.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]
    second: Annotated[Optional[bytes], Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None)]


class ReadWriteListOfStringsProperty(BaseModel):
    """Interface property `read_write_list_of_strings` (multi-value struct).

    A read-write property that is a list of strings.
    """

    model_config = ConfigDict(populate_by_name=True)

    value: Annotated[List[str], Field()]


class ReadWriteListsProperty(BaseModel):
    """Interface property `read_write_lists` (multi-value struct).

    A read-write property containing two lists.  The second list is optional.
    """

    model_config = ConfigDict(populate_by_name=True)

    the_list: Annotated[List[Numbers], Field()]

    optional_list: Annotated[Optional[List[datetime]], Field(alias="optionalList")]


class CallWithNothingMethodRequest(BaseModel):
    """Interface method `callWithNothing` request object.

    Method that takes no arguments and returns nothing.
    """

    model_config = ConfigDict(populate_by_name=True)


class CallWithNothingMethodResponse(BaseModel):
    """Interface method `callWithNothing` response object.

    Method that takes no arguments and returns nothing.
    """

    model_config = ConfigDict(populate_by_name=True)


class CallOneIntegerMethodRequest(BaseModel):
    """Interface method `callOneInteger` request object.

    Method that takes one integer argument and returns one integer value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[int, Field()]


class CallOneIntegerMethodResponse(BaseModel):
    """Interface method `callOneInteger` response object.

    Method that takes one integer argument and returns one integer value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[int, Field()]


class CallOptionalIntegerMethodRequest(BaseModel):
    """Interface method `callOptionalInteger` request object.

    Method that takes one optional integer argument and returns one optional integer value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[int], Field()]


class CallOptionalIntegerMethodResponse(BaseModel):
    """Interface method `callOptionalInteger` response object.

    Method that takes one optional integer argument and returns one optional integer value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[int], Field()]


class CallThreeIntegersMethodRequest(BaseModel):
    """Interface method `callThreeIntegers` request object.

    Method that takes three integer arguments, the third is optional, and returns three integer values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        int,
        Field(
            description="The first integer input.  The other two don't have descriptions.",
        ),
    ]
    input2: Annotated[int, Field()]
    input3: Annotated[Optional[int], Field()]


class CallThreeIntegersMethodResponse(BaseModel):
    """Interface method `callThreeIntegers` response object.

    Method that takes three integer arguments, the third is optional, and returns three integer values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        int,
        Field(
            description="The first integer output.  The other two don't have descriptions.",
        ),
    ]
    output2: Annotated[int, Field()]
    output3: Annotated[Optional[int], Field()]


class CallOneStringMethodRequest(BaseModel):
    """Interface method `callOneString` request object.

    Method that takes one string argument and returns one string value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[str, Field()]


class CallOneStringMethodResponse(BaseModel):
    """Interface method `callOneString` response object.

    Method that takes one string argument and returns one string value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[str, Field()]


class CallOptionalStringMethodRequest(BaseModel):
    """Interface method `callOptionalString` request object.

    Method that takes one optional string argument and returns one optional string value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[str], Field()]


class CallOptionalStringMethodResponse(BaseModel):
    """Interface method `callOptionalString` response object.

    Method that takes one optional string argument and returns one optional string value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[str], Field()]


class CallThreeStringsMethodRequest(BaseModel):
    """Interface method `callThreeStrings` request object.

    Method that takes three string arguments, the 2nd is optional, and returns three string values, the 2nd is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        str,
        Field(
            description="The first string input.  The other two don't have descriptions.",
        ),
    ]
    input2: Annotated[Optional[str], Field()]
    input3: Annotated[str, Field()]


class CallThreeStringsMethodResponse(BaseModel):
    """Interface method `callThreeStrings` response object.

    Method that takes three string arguments, the 2nd is optional, and returns three string values, the 2nd is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        str,
        Field(
            description="The first string output.  The other two don't have descriptions.",
        ),
    ]
    output2: Annotated[Optional[str], Field()]
    output3: Annotated[str, Field()]


class CallOneEnumMethodRequest(BaseModel):
    """Interface method `callOneEnum` request object.

    Method that takes one enum argument and returns one enum value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Numbers, Field()]


class CallOneEnumMethodResponse(BaseModel):
    """Interface method `callOneEnum` response object.

    Method that takes one enum argument and returns one enum value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Numbers, Field()]


class CallOptionalEnumMethodRequest(BaseModel):
    """Interface method `callOptionalEnum` request object.

    Method that takes one optional enum argument and returns one optional enum value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[Numbers], Field()]


class CallOptionalEnumMethodResponse(BaseModel):
    """Interface method `callOptionalEnum` response object.

    Method that takes one optional enum argument and returns one optional enum value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[Numbers], Field()]


class CallThreeEnumsMethodRequest(BaseModel):
    """Interface method `callThreeEnums` request object.

    Method that takes three enum arguments, the third is optional, and returns three enum values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        Numbers,
        Field(
            description="The first enum input.  The other two don't have descriptions.",
        ),
    ]
    input2: Annotated[Numbers, Field()]
    input3: Annotated[Optional[Numbers], Field()]


class CallThreeEnumsMethodResponse(BaseModel):
    """Interface method `callThreeEnums` response object.

    Method that takes three enum arguments, the third is optional, and returns three enum values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        Numbers,
        Field(
            description="The first enum output.  The other two don't have descriptions.",
        ),
    ]
    output2: Annotated[Numbers, Field()]
    output3: Annotated[Optional[Numbers], Field()]


class CallOneStructMethodRequest(BaseModel):
    """Interface method `callOneStruct` request object.

    Method that takes one struct argument and returns one struct value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[AllTypes, Field()]


class CallOneStructMethodResponse(BaseModel):
    """Interface method `callOneStruct` response object.

    Method that takes one struct argument and returns one struct value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[AllTypes, Field()]


class CallOptionalStructMethodRequest(BaseModel):
    """Interface method `callOptionalStruct` request object.

    Method that takes one optional struct argument and returns one optional struct value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[AllTypes], Field()]


class CallOptionalStructMethodResponse(BaseModel):
    """Interface method `callOptionalStruct` response object.

    Method that takes one optional struct argument and returns one optional struct value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[AllTypes], Field()]


class CallThreeStructsMethodRequest(BaseModel):
    """Interface method `callThreeStructs` request object.

    Method that takes three struct arguments, the first is optional, and returns three struct values, the first is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        Optional[AllTypes],
        Field(
            description="The first struct input.  The other two don't have descriptions.",
        ),
    ]
    input2: Annotated[AllTypes, Field()]
    input3: Annotated[AllTypes, Field()]


class CallThreeStructsMethodResponse(BaseModel):
    """Interface method `callThreeStructs` response object.

    Method that takes three struct arguments, the first is optional, and returns three struct values, the first is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        Optional[AllTypes],
        Field(
            description="The first struct output.  The other two don't have descriptions.",
        ),
    ]
    output2: Annotated[AllTypes, Field()]
    output3: Annotated[AllTypes, Field()]


class CallOneDateTimeMethodRequest(BaseModel):
    """Interface method `callOneDateTime` request object.

    Method that takes one date and time argument and returns one date and time value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[datetime, Field()]


class CallOneDateTimeMethodResponse(BaseModel):
    """Interface method `callOneDateTime` response object.

    Method that takes one date and time argument and returns one date and time value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[datetime, Field()]


class CallOptionalDateTimeMethodRequest(BaseModel):
    """Interface method `callOptionalDateTime` request object.

    Method that takes one optional date and time argument and returns one optional date and time value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[datetime], Field()]


class CallOptionalDateTimeMethodResponse(BaseModel):
    """Interface method `callOptionalDateTime` response object.

    Method that takes one optional date and time argument and returns one optional date and time value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[datetime], Field()]


class CallThreeDateTimesMethodRequest(BaseModel):
    """Interface method `callThreeDateTimes` request object.

    Method that takes three date and time arguments, the third is optional, and returns three date and time values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        datetime,
        Field(
            description="The first date and time input.  The other two don't have descriptions.",
        ),
    ]
    input2: Annotated[datetime, Field()]
    input3: Annotated[Optional[datetime], Field()]


class CallThreeDateTimesMethodResponse(BaseModel):
    """Interface method `callThreeDateTimes` response object.

    Method that takes three date and time arguments, the third is optional, and returns three date and time values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        datetime,
        Field(
            description="The first date and time output.  The other two don't have descriptions.",
        ),
    ]
    output2: Annotated[datetime, Field()]
    output3: Annotated[Optional[datetime], Field()]


class CallOneDurationMethodRequest(BaseModel):
    """Interface method `callOneDuration` request object.

    Method that takes one duration argument and returns one duration value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[timedelta, Field()]


class CallOneDurationMethodResponse(BaseModel):
    """Interface method `callOneDuration` response object.

    Method that takes one duration argument and returns one duration value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[timedelta, Field()]


class CallOptionalDurationMethodRequest(BaseModel):
    """Interface method `callOptionalDuration` request object.

    Method that takes one optional duration argument and returns one optional duration value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[timedelta], Field()]


class CallOptionalDurationMethodResponse(BaseModel):
    """Interface method `callOptionalDuration` response object.

    Method that takes one optional duration argument and returns one optional duration value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[timedelta], Field()]


class CallThreeDurationsMethodRequest(BaseModel):
    """Interface method `callThreeDurations` request object.

    Method that takes three duration arguments, the third is optional, and returns three duration values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        timedelta,
        Field(
            description="The first duration input.  The other two don't have descriptions.",
        ),
    ]
    input2: Annotated[timedelta, Field()]
    input3: Annotated[Optional[timedelta], Field()]


class CallThreeDurationsMethodResponse(BaseModel):
    """Interface method `callThreeDurations` response object.

    Method that takes three duration arguments, the third is optional, and returns three duration values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        timedelta,
        Field(
            description="The first duration output.  The other two don't have descriptions.",
        ),
    ]
    output2: Annotated[timedelta, Field()]
    output3: Annotated[Optional[timedelta], Field()]


class CallOneBinaryMethodRequest(BaseModel):
    """Interface method `callOneBinary` request object.

    Method that takes one binary argument and returns one binary value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[bytes, Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8"))]


class CallOneBinaryMethodResponse(BaseModel):
    """Interface method `callOneBinary` response object.

    Method that takes one binary argument and returns one binary value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[bytes, Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8"))]


class CallOptionalBinaryMethodRequest(BaseModel):
    """Interface method `callOptionalBinary` request object.

    Method that takes one optional binary argument and returns one optional binary value.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[Optional[bytes], Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None)]


class CallOptionalBinaryMethodResponse(BaseModel):
    """Interface method `callOptionalBinary` response object.

    Method that takes one optional binary argument and returns one optional binary value.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[Optional[bytes], Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None)]


class CallThreeBinariesMethodRequest(BaseModel):
    """Interface method `callThreeBinaries` request object.

    Method that takes three binary arguments, the third is optional, and returns three binary values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    input1: Annotated[
        bytes,
        Field(
            description="The first binary input.  The other two don't have descriptions.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]
    input2: Annotated[bytes, Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8"))]
    input3: Annotated[Optional[bytes], Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None)]


class CallThreeBinariesMethodResponse(BaseModel):
    """Interface method `callThreeBinaries` response object.

    Method that takes three binary arguments, the third is optional, and returns three binary values, the third is optional.
    """

    model_config = ConfigDict(populate_by_name=True)
    output1: Annotated[
        bytes,
        Field(
            description="The first binary output.  The other two don't have descriptions.",
        ),
        PlainValidator(base64_decode_if_str),
        PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8")),
    ]
    output2: Annotated[bytes, Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8"))]
    output3: Annotated[Optional[bytes], Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode("utf-8") if v is not None else None)]


class CallOneListOfIntegersMethodRequest(BaseModel):
    """Interface method `callOneListOfIntegers` request object.

    Method that takes one list of integers argument and returns one list of integers value.
    """

    model_config = ConfigDict(populate_by_name=True)

    input1: Annotated[List[int], Field()]


class CallOneListOfIntegersMethodResponse(BaseModel):
    """Interface method `callOneListOfIntegers` response object.

    Method that takes one list of integers argument and returns one list of integers value.
    """

    model_config = ConfigDict(populate_by_name=True)

    output1: Annotated[List[int], Field()]


class CallOptionalListOfFloatsMethodRequest(BaseModel):
    """Interface method `callOptionalListOfFloats` request object.

    Method that takes one optional list of floats argument and returns one optional list of floats value.
    """

    model_config = ConfigDict(populate_by_name=True)

    input1: Annotated[Optional[List[float]], Field()]


class CallOptionalListOfFloatsMethodResponse(BaseModel):
    """Interface method `callOptionalListOfFloats` response object.

    Method that takes one optional list of floats argument and returns one optional list of floats value.
    """

    model_config = ConfigDict(populate_by_name=True)

    output1: Annotated[Optional[List[float]], Field()]


class CallTwoListsMethodRequest(BaseModel):
    """Interface method `callTwoLists` request object.

    Method that takes two list arguments, the second is optional, and returns two list values, the second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)

    input1: Annotated[
        List[Numbers],
        Field(
            description="The first list of enums.",
        ),
    ]

    input2: Annotated[Optional[List[str]], Field()]


class CallTwoListsMethodResponse(BaseModel):
    """Interface method `callTwoLists` response object.

    Method that takes two list arguments, the second is optional, and returns two list values, the second is optional.
    """

    model_config = ConfigDict(populate_by_name=True)

    output1: Annotated[
        List[Numbers],
        Field(
            description="The first list of enums.",
        ),
    ]

    output2: Annotated[Optional[List[str]], Field()]
