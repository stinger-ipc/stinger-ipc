"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.
"""

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
from enum import IntEnum


class InterfaceInfo(BaseModel):
    interfaceName: str = Field(default="Test Able")
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


class AllTypes(BaseModel):
    """Interface struct `AllTypes`."""

    the_bool: bool
    the_int: int
    the_number: float
    the_str: str
    the_enum: Numbers
    date_and_time: datetime
    time_duration: timedelta
    data: bytes
    OptionalInteger: Optional[int]
    OptionalString: Optional[str]
    OptionalEnum: Optional[Numbers]
    OptionalDateTime: Optional[datetime]
    OptionalDuration: Optional[timedelta]
    OptionalBinary: Optional[bytes]


class EmptySignalPayload(BaseModel):
    """Interface signal `empty`.

    A signal with no parameters.
    """


class SingleIntSignalPayload(BaseModel):
    """Interface signal `singleInt`.

    A signal with a single integer parameter.
    """

    value: int = Field(description="The integer value.")


class SingleOptionalIntSignalPayload(BaseModel):
    """Interface signal `singleOptionalInt`.

    A signal with a single optional integer parameter.
    """

    value: Optional[int] = Field(description="The integer value.")


class ThreeIntegersSignalPayload(BaseModel):
    """Interface signal `threeIntegers`.

    A signal with three integer parameters, the third is optional.
    """

    first: int = Field(description="The first integer value.")
    second: int = Field(description="The second integer value.")
    third: Optional[int] = Field(description="The third integer value.")


class SingleStringSignalPayload(BaseModel):
    """Interface signal `singleString`.

    A signal with a single string parameter.
    """

    value: str = Field(description="The string value.")


class SingleOptionalStringSignalPayload(BaseModel):
    """Interface signal `singleOptionalString`.

    A signal with a single optional string parameter.
    """

    value: Optional[str] = Field(description="The string value.")


class ThreeStringsSignalPayload(BaseModel):
    """Interface signal `threeStrings`.

    A signal with three string parameters, the third is optional.
    """

    first: str = Field(description="The first string value.")
    second: str = Field(description="The second string value.")
    third: Optional[str] = Field(description="The third string value.")


class SingleEnumSignalPayload(BaseModel):
    """Interface signal `singleEnum`.

    A signal with a single enum parameter.
    """

    value: Numbers = Field(description="The enum value.")


class SingleOptionalEnumSignalPayload(BaseModel):
    """Interface signal `singleOptionalEnum`.

    A signal with a single optional enum parameter.
    """

    value: Optional[Numbers] = Field(description="The enum value.")


class ThreeEnumsSignalPayload(BaseModel):
    """Interface signal `threeEnums`.

    A signal with three enum parameters, the third is optional.
    """

    first: Numbers = Field(description="The first enum value.")
    second: Numbers = Field(description="The second enum value.")
    third: Optional[Numbers] = Field(description="The third enum value.")


class SingleStructSignalPayload(BaseModel):
    """Interface signal `singleStruct`.

    A signal with a single struct parameter.
    """

    value: AllTypes = Field(description="The struct value.")


class SingleOptionalStructSignalPayload(BaseModel):
    """Interface signal `singleOptionalStruct`.

    A signal with a single optional struct parameter.
    """

    value: Optional[AllTypes] = Field(description="The struct value.")


class ThreeStructsSignalPayload(BaseModel):
    """Interface signal `threeStructs`.

    A signal with three struct parameters, the third is optional.
    """

    first: AllTypes = Field(description="The first struct value.")
    second: AllTypes = Field(description="The second struct value.")
    third: Optional[AllTypes] = Field(description="The third struct value.")


class SingleDateTimeSignalPayload(BaseModel):
    """Interface signal `singleDateTime`.

    A signal with a single date and time parameter.
    """

    value: datetime = Field(description="The date and time value.")


class SingleOptionalDatetimeSignalPayload(BaseModel):
    """Interface signal `singleOptionalDatetime`.

    A signal with a single optional date and time parameter.
    """

    value: Optional[datetime] = Field(description="The date and time value.")


class ThreeDateTimesSignalPayload(BaseModel):
    """Interface signal `threeDateTimes`.

    A signal with three date and time parameters, the third is optional.
    """

    first: datetime = Field(description="The first date and time value.")
    second: datetime = Field(description="The second date and time value.")
    third: Optional[datetime] = Field(description="The third date and time value.")


class SingleDurationSignalPayload(BaseModel):
    """Interface signal `singleDuration`.

    A signal with a single duration parameter.
    """

    value: timedelta = Field(description="The duration value.")


class SingleOptionalDurationSignalPayload(BaseModel):
    """Interface signal `singleOptionalDuration`.

    A signal with a single optional duration parameter.
    """

    value: Optional[timedelta] = Field(description="The duration value.")


class ThreeDurationsSignalPayload(BaseModel):
    """Interface signal `threeDurations`.

    A signal with three duration parameters, the third is optional.
    """

    first: timedelta = Field(description="The first duration value.")
    second: timedelta = Field(description="The second duration value.")
    third: Optional[timedelta] = Field(description="The third duration value.")


class SingleBinarySignalPayload(BaseModel):
    """Interface signal `singleBinary`.

    A signal with a single binary parameter.
    """

    value: bytes = Field(description="The binary value.")


class SingleOptionalBinarySignalPayload(BaseModel):
    """Interface signal `singleOptionalBinary`.

    A signal with a single optional binary parameter.
    """

    value: Optional[bytes] = Field(description="The binary value.")


class ThreeBinariesSignalPayload(BaseModel):
    """Interface signal `threeBinaries`.

    A signal with three binary parameters, the third is optional.
    """

    first: bytes = Field(description="The first binary value.")
    second: bytes = Field(description="The second binary value.")
    third: Optional[bytes] = Field(description="The third binary value.")


class AllTypes(BaseModel):
    """Interface method `callOneStruct` return value struct."""

    the_bool: bool
    the_int: int
    the_number: float = Field(description="A floating point number.  Bool and int do not have descriptions.")
    the_str: str = Field(description="A string type.")
    the_enum: Numbers = Field(description="An enum type")
    date_and_time: datetime = Field(description="A date and time type.")
    time_duration: timedelta = Field(description="A duration type.")
    data: bytes = Field(description="A binary type.")
    OptionalInteger: Optional[int] = Field(description="An optional integer type.")
    OptionalString: Optional[str] = Field(description="An optional string type.")
    OptionalEnum: Optional[Numbers] = Field(description="An optional enum type, one of the numbers.")
    OptionalDateTime: Optional[datetime] = Field(description="An optional date and time type.")
    OptionalDuration: Optional[timedelta] = Field(description="An optional duration type.")
    OptionalBinary: Optional[bytes] = Field(description="An optional binary type.")


class AllTypes(BaseModel):
    """Interface method `callOptionalStruct` return value struct."""

    the_bool: bool
    the_int: int
    the_number: float = Field(description="A floating point number.  Bool and int do not have descriptions.")
    the_str: str = Field(description="A string type.")
    the_enum: Numbers = Field(description="An enum type")
    date_and_time: datetime = Field(description="A date and time type.")
    time_duration: timedelta = Field(description="A duration type.")
    data: bytes = Field(description="A binary type.")
    OptionalInteger: Optional[int] = Field(description="An optional integer type.")
    OptionalString: Optional[str] = Field(description="An optional string type.")
    OptionalEnum: Optional[Numbers] = Field(description="An optional enum type, one of the numbers.")
    OptionalDateTime: Optional[datetime] = Field(description="An optional date and time type.")
    OptionalDuration: Optional[timedelta] = Field(description="An optional duration type.")
    OptionalBinary: Optional[bytes] = Field(description="An optional binary type.")


class ReadWriteTwoIntegersProperty(BaseModel):
    """Interface property `read_write_two_integers` (multi-value struct).

    A read-write property with two integer values. The second is optional.
    """

    first: int = Field(description="An integer value.")
    second: Optional[int]


class ReadWriteTwoStringsProperty(BaseModel):
    """Interface property `read_write_two_strings` (multi-value struct).

    A read-write property with two string values. The second is optional.
    """

    first: str = Field(description="A string value.")
    second: Optional[str]


class ReadWriteTwoStructsProperty(BaseModel):
    """Interface property `read_write_two_structs` (multi-value struct).

    A read-write property with two struct values. The second is optional.
    """

    first: AllTypes = Field(description="A struct value.")
    second: Optional[AllTypes]


class ReadWriteTwoEnumsProperty(BaseModel):
    """Interface property `read_write_two_enums` (multi-value struct).

    A read-write property with two enum values. The second is optional.
    """

    first: Numbers = Field(description="An enum value.")
    second: Optional[Numbers]


class ReadWriteTwoDatetimesProperty(BaseModel):
    """Interface property `read_write_two_datetimes` (multi-value struct).

    A read-write property with two datetime values. The second is optional.
    """

    first: datetime = Field(description="A date and time value.")
    second: Optional[datetime]


class ReadWriteTwoDurationsProperty(BaseModel):
    """Interface property `read_write_two_durations` (multi-value struct).

    A read-write property with two duration values. The second is optional.
    """

    first: timedelta = Field(description="A duration of time.")
    second: Optional[timedelta]


class ReadWriteTwoBinariesProperty(BaseModel):
    """Interface property `read_write_two_binaries` (multi-value struct).

    A read-write property with two binary values.  The second is optional.
    """

    first: bytes = Field(description="A binary blob of data.")
    second: Optional[bytes]


class CallWithNothingMethodRequest(BaseModel):
    """Interface method `callWithNothing` request object.

    Method that takes no arguments and returns nothing.
    """

    pass


class CallWithNothingMethodResponse(BaseModel):
    """Interface method `callWithNothing` response object.

    Method that takes no arguments and returns nothing.
    """

    pass


class CallOneIntegerMethodRequest(BaseModel):
    """Interface method `callOneInteger` request object.

    Method that takes one integer argument and returns one integer value.
    """

    input1: int


class CallOneIntegerMethodResponse(BaseModel):
    """Interface method `callOneInteger` response object.

    Method that takes one integer argument and returns one integer value.
    """

    output1: int


class CallOptionalIntegerMethodRequest(BaseModel):
    """Interface method `callOptionalInteger` request object.

    Method that takes one optional integer argument and returns one optional integer value.
    """

    input1: Optional[int]


class CallOptionalIntegerMethodResponse(BaseModel):
    """Interface method `callOptionalInteger` response object.

    Method that takes one optional integer argument and returns one optional integer value.
    """

    output1: Optional[Optional[int]]


class CallThreeIntegersMethodRequest(BaseModel):
    """Interface method `callThreeIntegers` request object.

    Method that takes three integer arguments, the third is optional, and returns three integer values, the third is optional.
    """

    input1: int = Field(description="The first integer input.  The other two don't have descriptions.")
    input2: int
    input3: Optional[int]


class CallThreeIntegersMethodResponse(BaseModel):
    """Interface method `callThreeIntegers` response object.

    Method that takes three integer arguments, the third is optional, and returns three integer values, the third is optional.
    """

    output1: int = Field(description="The first integer output.  The other two don't have descriptions.")
    output2: int
    output3: Optional[int]


class CallOneStringMethodRequest(BaseModel):
    """Interface method `callOneString` request object.

    Method that takes one string argument and returns one string value.
    """

    input1: str


class CallOneStringMethodResponse(BaseModel):
    """Interface method `callOneString` response object.

    Method that takes one string argument and returns one string value.
    """

    output1: str


class CallOptionalStringMethodRequest(BaseModel):
    """Interface method `callOptionalString` request object.

    Method that takes one optional string argument and returns one optional string value.
    """

    input1: Optional[str]


class CallOptionalStringMethodResponse(BaseModel):
    """Interface method `callOptionalString` response object.

    Method that takes one optional string argument and returns one optional string value.
    """

    output1: Optional[Optional[str]]


class CallThreeStringsMethodRequest(BaseModel):
    """Interface method `callThreeStrings` request object.

    Method that takes three string arguments, the 2nd is optional, and returns three string values, the 2nd is optional.
    """

    input1: str = Field(description="The first string input.  The other two don't have descriptions.")
    input2: Optional[str]
    input3: str


class CallThreeStringsMethodResponse(BaseModel):
    """Interface method `callThreeStrings` response object.

    Method that takes three string arguments, the 2nd is optional, and returns three string values, the 2nd is optional.
    """

    output1: str = Field(description="The first string output.  The other two don't have descriptions.")
    output2: Optional[str]
    output3: str


class CallOneEnumMethodRequest(BaseModel):
    """Interface method `callOneEnum` request object.

    Method that takes one enum argument and returns one enum value.
    """

    input1: Numbers


class CallOneEnumMethodResponse(BaseModel):
    """Interface method `callOneEnum` response object.

    Method that takes one enum argument and returns one enum value.
    """

    output1: stinger_types.Numbers


class CallOptionalEnumMethodRequest(BaseModel):
    """Interface method `callOptionalEnum` request object.

    Method that takes one optional enum argument and returns one optional enum value.
    """

    input1: Optional[Numbers]


class CallOptionalEnumMethodResponse(BaseModel):
    """Interface method `callOptionalEnum` response object.

    Method that takes one optional enum argument and returns one optional enum value.
    """

    output1: Optional[Optional[stinger_types.Numbers]]


class CallThreeEnumsMethodRequest(BaseModel):
    """Interface method `callThreeEnums` request object.

    Method that takes three enum arguments, the third is optional, and returns three enum values, the third is optional.
    """

    input1: Numbers = Field(description="The first enum input.  The other two don't have descriptions.")
    input2: Numbers
    input3: Optional[Numbers]


class CallThreeEnumsMethodResponse(BaseModel):
    """Interface method `callThreeEnums` response object.

    Method that takes three enum arguments, the third is optional, and returns three enum values, the third is optional.
    """

    output1: Numbers = Field(description="The first enum output.  The other two don't have descriptions.")
    output2: Numbers
    output3: Optional[Numbers]


class CallOneStructMethodRequest(BaseModel):
    """Interface method `callOneStruct` request object.

    Method that takes one struct argument and returns one struct value.
    """

    input1: AllTypes


class CallOneStructMethodResponse(BaseModel):
    """Interface method `callOneStruct` response object.

    Method that takes one struct argument and returns one struct value.
    """

    the_bool: bool
    the_int: int
    the_number: float = Field(description="A floating point number.  Bool and int do not have descriptions.")
    the_str: str = Field(description="A string type.")
    the_enum: Numbers = Field(description="An enum type")
    date_and_time: datetime = Field(description="A date and time type.")
    time_duration: timedelta = Field(description="A duration type.")
    data: bytes = Field(description="A binary type.")
    OptionalInteger: Optional[int] = Field(description="An optional integer type.")
    OptionalString: Optional[str] = Field(description="An optional string type.")
    OptionalEnum: Optional[Numbers] = Field(description="An optional enum type, one of the numbers.")
    OptionalDateTime: Optional[datetime] = Field(description="An optional date and time type.")
    OptionalDuration: Optional[timedelta] = Field(description="An optional duration type.")
    OptionalBinary: Optional[bytes] = Field(description="An optional binary type.")


class CallOptionalStructMethodRequest(BaseModel):
    """Interface method `callOptionalStruct` request object.

    Method that takes one optional struct argument and returns one optional struct value.
    """

    input1: Optional[AllTypes]


class CallOptionalStructMethodResponse(BaseModel):
    """Interface method `callOptionalStruct` response object.

    Method that takes one optional struct argument and returns one optional struct value.
    """

    the_bool: bool
    the_int: int
    the_number: float = Field(description="A floating point number.  Bool and int do not have descriptions.")
    the_str: str = Field(description="A string type.")
    the_enum: Numbers = Field(description="An enum type")
    date_and_time: datetime = Field(description="A date and time type.")
    time_duration: timedelta = Field(description="A duration type.")
    data: bytes = Field(description="A binary type.")
    OptionalInteger: Optional[int] = Field(description="An optional integer type.")
    OptionalString: Optional[str] = Field(description="An optional string type.")
    OptionalEnum: Optional[Numbers] = Field(description="An optional enum type, one of the numbers.")
    OptionalDateTime: Optional[datetime] = Field(description="An optional date and time type.")
    OptionalDuration: Optional[timedelta] = Field(description="An optional duration type.")
    OptionalBinary: Optional[bytes] = Field(description="An optional binary type.")


class CallThreeStructsMethodRequest(BaseModel):
    """Interface method `callThreeStructs` request object.

    Method that takes three struct arguments, the first is optional, and returns three struct values, the first is optional.
    """

    input1: Optional[AllTypes] = Field(description="The first struct input.  The other two don't have descriptions.")
    input2: AllTypes
    input3: AllTypes


class CallThreeStructsMethodResponse(BaseModel):
    """Interface method `callThreeStructs` response object.

    Method that takes three struct arguments, the first is optional, and returns three struct values, the first is optional.
    """

    output1: Optional[AllTypes] = Field(description="The first struct output.  The other two don't have descriptions.")
    output2: AllTypes
    output3: AllTypes


class CallOneDateTimeMethodRequest(BaseModel):
    """Interface method `callOneDateTime` request object.

    Method that takes one date and time argument and returns one date and time value.
    """

    input1: datetime


class CallOneDateTimeMethodResponse(BaseModel):
    """Interface method `callOneDateTime` response object.

    Method that takes one date and time argument and returns one date and time value.
    """

    output1: datetime


class CallOptionalDateTimeMethodRequest(BaseModel):
    """Interface method `callOptionalDateTime` request object.

    Method that takes one optional date and time argument and returns one optional date and time value.
    """

    input1: Optional[datetime]


class CallOptionalDateTimeMethodResponse(BaseModel):
    """Interface method `callOptionalDateTime` response object.

    Method that takes one optional date and time argument and returns one optional date and time value.
    """

    output1: Optional[Optional[datetime]]


class CallThreeDateTimesMethodRequest(BaseModel):
    """Interface method `callThreeDateTimes` request object.

    Method that takes three date and time arguments, the third is optional, and returns three date and time values, the third is optional.
    """

    input1: datetime = Field(description="The first date and time input.  The other two don't have descriptions.")
    input2: datetime
    input3: Optional[datetime]


class CallThreeDateTimesMethodResponse(BaseModel):
    """Interface method `callThreeDateTimes` response object.

    Method that takes three date and time arguments, the third is optional, and returns three date and time values, the third is optional.
    """

    output1: datetime = Field(description="The first date and time output.  The other two don't have descriptions.")
    output2: datetime
    output3: Optional[datetime]


class CallOneDurationMethodRequest(BaseModel):
    """Interface method `callOneDuration` request object.

    Method that takes one duration argument and returns one duration value.
    """

    input1: timedelta


class CallOneDurationMethodResponse(BaseModel):
    """Interface method `callOneDuration` response object.

    Method that takes one duration argument and returns one duration value.
    """

    output1: timedelta


class CallOptionalDurationMethodRequest(BaseModel):
    """Interface method `callOptionalDuration` request object.

    Method that takes one optional duration argument and returns one optional duration value.
    """

    input1: Optional[timedelta]


class CallOptionalDurationMethodResponse(BaseModel):
    """Interface method `callOptionalDuration` response object.

    Method that takes one optional duration argument and returns one optional duration value.
    """

    output1: Optional[Optional[timedelta]]


class CallThreeDurationsMethodRequest(BaseModel):
    """Interface method `callThreeDurations` request object.

    Method that takes three duration arguments, the third is optional, and returns three duration values, the third is optional.
    """

    input1: timedelta = Field(description="The first duration input.  The other two don't have descriptions.")
    input2: timedelta
    input3: Optional[timedelta]


class CallThreeDurationsMethodResponse(BaseModel):
    """Interface method `callThreeDurations` response object.

    Method that takes three duration arguments, the third is optional, and returns three duration values, the third is optional.
    """

    output1: timedelta = Field(description="The first duration output.  The other two don't have descriptions.")
    output2: timedelta
    output3: Optional[timedelta]


class CallOneBinaryMethodRequest(BaseModel):
    """Interface method `callOneBinary` request object.

    Method that takes one binary argument and returns one binary value.
    """

    input1: bytes


class CallOneBinaryMethodResponse(BaseModel):
    """Interface method `callOneBinary` response object.

    Method that takes one binary argument and returns one binary value.
    """

    output1: bytes


class CallOptionalBinaryMethodRequest(BaseModel):
    """Interface method `callOptionalBinary` request object.

    Method that takes one optional binary argument and returns one optional binary value.
    """

    input1: Optional[bytes]


class CallOptionalBinaryMethodResponse(BaseModel):
    """Interface method `callOptionalBinary` response object.

    Method that takes one optional binary argument and returns one optional binary value.
    """

    output1: Optional[bytes]


class CallThreeBinariesMethodRequest(BaseModel):
    """Interface method `callThreeBinaries` request object.

    Method that takes three binary arguments, the third is optional, and returns three binary values, the third is optional.
    """

    input1: bytes = Field(description="The first binary input.  The other two don't have descriptions.")
    input2: bytes
    input3: Optional[bytes]


class CallThreeBinariesMethodResponse(BaseModel):
    """Interface method `callThreeBinaries` response object.

    Method that takes three binary arguments, the third is optional, and returns three binary values, the third is optional.
    """

    output1: bytes = Field(description="The first binary output.  The other two don't have descriptions.")
    output2: bytes
    output3: Optional[bytes]
