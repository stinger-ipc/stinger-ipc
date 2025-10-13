"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
"""

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
from enum import IntEnum


class InterfaceInfo(BaseModel):
    interfaceName: str = Field(default="Full")
    title: str = Field(default="Fully Featured Example Interface")
    version: str = Field(default="0.0.1")
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

    drink: bool
    sandwich: str
    crackers: float
    day: DayOfTheWeek
    order_number: Optional[int]
    time_of_lunch: datetime
    duration_of_lunch: timedelta


class TodayIsSignalPayload(BaseModel):
    """Interface signal `todayIs`."""

    dayOfMonth: int
    dayOfWeek: Optional[DayOfTheWeek]
    timestamp: datetime
    process_time: timedelta
    memory_segment: bytes


class FavoriteNumberProperty(BaseModel):
    """Interface property `favorite_number` (multi-value struct).

    My favorite number

    """

    number: int


class FavoriteFoodsProperty(BaseModel):
    """Interface property `favorite_foods` (multi-value struct)."""

    drink: str
    slices_of_pizza: int
    breakfast: Optional[str]


class LunchMenuProperty(BaseModel):
    """Interface property `lunch_menu` (multi-value struct)."""

    monday: Lunch
    tuesday: Lunch = Field(description="Tuesday's lunch menu.")


class FamilyNameProperty(BaseModel):
    """Interface property `family_name` (multi-value struct).

    This is to test a property with a single string value.
    """

    family_name: str


class LastBreakfastTimeProperty(BaseModel):
    """Interface property `last_breakfast_time` (multi-value struct).

    This is to test a property with a single datetime value.
    """

    timestamp: datetime


class BreakfastLengthProperty(BaseModel):
    """Interface property `breakfast_length` (multi-value struct).

    This is to test a property with a single duration value.
    """

    length: timedelta


class LastBirthdaysProperty(BaseModel):
    """Interface property `last_birthdays` (multi-value struct).

    This is to test a property with multiple datetime values.
    """

    mom: datetime
    dad: datetime
    sister: Optional[datetime]
    brothers_age: Optional[int]


class AddNumbersMethodRequest(BaseModel):
    """Interface method `addNumbers` request object."""

    first: int
    second: int
    third: Optional[int]


class AddNumbersMethodResponse(BaseModel):
    """Interface method `addNumbers` response object."""

    sum: int


class DoSomethingMethodRequest(BaseModel):
    """Interface method `doSomething` request object."""

    aString: str


class DoSomethingMethodResponse(BaseModel):
    """Interface method `doSomething` response object."""

    label: str
    identifier: int
    day: DayOfTheWeek


class EchoMethodRequest(BaseModel):
    """Interface method `echo` request object.

    Echo back the received message.
    """

    message: str


class EchoMethodResponse(BaseModel):
    """Interface method `echo` response object.

    Echo back the received message.
    """

    message: str


class WhatTimeIsItMethodRequest(BaseModel):
    """Interface method `what_time_is_it` request object.

    Get the current date and time.
    """

    the_first_time: datetime


class WhatTimeIsItMethodResponse(BaseModel):
    """Interface method `what_time_is_it` response object.

    Get the current date and time.
    """

    timestamp: datetime


class SetTheTimeMethodRequest(BaseModel):
    """Interface method `set_the_time` request object."""

    the_first_time: datetime
    the_second_time: datetime


class SetTheTimeMethodResponse(BaseModel):
    """Interface method `set_the_time` response object."""

    timestamp: datetime
    confirmation_message: str


class ForwardTimeMethodRequest(BaseModel):
    """Interface method `forward_time` request object.

    This method takes a time and a duration, and returns the time plus the duration.
    """

    adjustment: timedelta


class ForwardTimeMethodResponse(BaseModel):
    """Interface method `forward_time` response object.

    This method takes a time and a duration, and returns the time plus the duration.
    """

    new_time: datetime


class HowOffIsTheClockMethodRequest(BaseModel):
    """Interface method `how_off_is_the_clock` request object.

    Returns how far off the clock is from the actual time.
    """

    actual_time: datetime


class HowOffIsTheClockMethodResponse(BaseModel):
    """Interface method `how_off_is_the_clock` response object.

    Returns how far off the clock is from the actual time.
    """

    difference: timedelta
