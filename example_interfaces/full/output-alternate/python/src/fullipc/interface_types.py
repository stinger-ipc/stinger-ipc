"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from pydantic import BaseModel, Field, PlainValidator, PlainSerializer, ConfigDict
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

from typing import Optional, Union, List
import base64
from enum import IntEnum
import sys

# Use typing_extensions for Python < 3.9 compatibility
if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated


def base64_decode_if_str(value: Union[str, bytes, None]) -> Optional[bytes]:
    """If the value is a string, decode it from base64 to bytes.  Otherwise return the bytes as-is."""
    if isinstance(value, str):
        return base64.b64decode(value)
    return value


class InterfaceInfo(BaseModel):
    interface_name: str = Field(default="Full")
    title: str = Field(default="Example Interface")
    version: str = Field(default="0.0.2")
    instance: str
    connection_topic: str
    timestamp: str


class DayOfTheWeek(IntEnum):
    """Interface enum `dayOfTheWeek`."""

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


class Lunch(BaseModel):
    """Interface struct `lunch`."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    drink: Annotated[bool, Field()]
    sandwich: Annotated[str, Field()]
    crackers: Annotated[float, Field()]
    day: Annotated[DayOfTheWeek, Field()]
    order_number: Annotated[Optional[int], Field()]
    time_of_lunch: Annotated[datetime, Field()]
    duration_of_lunch: Annotated[timedelta, Field()]


class TodayIsSignalPayload(BaseModel):
    """Interface signal `todayIs`."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    day_of_month: Annotated[int, Field(alias="dayOfMonth")]
    day_of_week: Annotated[DayOfTheWeek, Field(alias="dayOfWeek")]


class RandomWordSignalPayload(BaseModel):
    """Interface signal `randomWord`."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    word: Annotated[str, Field()]
    time: Annotated[datetime, Field()]


class FavoriteNumberProperty(BaseModel):
    """Interface property `favorite_number` (multi-value struct).

    My favorite number

    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    number: Annotated[int, Field()]


class FavoriteFoodsProperty(BaseModel):
    """Interface property `favorite_foods` (multi-value struct)."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    drink: Annotated[str, Field()]
    slices_of_pizza: Annotated[int, Field()]
    breakfast: Annotated[Optional[str], Field()]


class LunchMenuProperty(BaseModel):
    """Interface property `lunch_menu` (multi-value struct)."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    monday: Annotated[Lunch, Field()]
    tuesday: Annotated[
        Lunch,
        Field(
            description="Tuesday's lunch menu.",
        ),
    ]


class FamilyNameProperty(BaseModel):
    """Interface property `family_name` (multi-value struct).

    This is to test a property with a single string value.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    family_name: Annotated[str, Field()]


class LastBreakfastTimeProperty(BaseModel):
    """Interface property `last_breakfast_time` (multi-value struct).

    This is to test a property with a single datetime value.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    timestamp: Annotated[datetime, Field()]


class LastBirthdaysProperty(BaseModel):
    """Interface property `last_birthdays` (multi-value struct).

    This is to test a property with multiple datetime values.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    mom: Annotated[datetime, Field()]
    dad: Annotated[datetime, Field()]
    sister: Annotated[Optional[datetime], Field()]
    brothers_age: Annotated[Optional[int], Field()]


class AddNumbersMethodRequest(BaseModel):
    """Interface method `addNumbers` request object."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    first: Annotated[int, Field()]
    second: Annotated[int, Field()]
    third: Annotated[Optional[int], Field()]


class AddNumbersMethodResponse(BaseModel):
    """Interface method `addNumbers` response object."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    sum: Annotated[int, Field()]


class DoSomethingMethodRequest(BaseModel):
    """Interface method `doSomething` request object."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    task_to_do: Annotated[str, Field()]


class DoSomethingMethodResponse(BaseModel):
    """Interface method `doSomething` response object."""

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    label: Annotated[str, Field()]
    identifier: Annotated[int, Field()]


class WhatTimeIsItMethodRequest(BaseModel):
    """Interface method `what_time_is_it` request object.

    Get the current date and time.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")


class WhatTimeIsItMethodResponse(BaseModel):
    """Interface method `what_time_is_it` response object.

    Get the current date and time.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    timestamp: Annotated[datetime, Field()]


class HoldTemperatureMethodRequest(BaseModel):
    """Interface method `hold_temperature` request object.

    Hold a temperature for a specified duration.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    temperature_celsius: Annotated[float, Field()]


class HoldTemperatureMethodResponse(BaseModel):
    """Interface method `hold_temperature` response object.

    Hold a temperature for a specified duration.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True, extra="forbid")
    success: Annotated[bool, Field()]
