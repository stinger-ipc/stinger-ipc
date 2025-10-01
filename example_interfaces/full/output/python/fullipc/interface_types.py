"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
"""

from pydantic import BaseModel, Field
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
    order_number: int | None


class DoSomethingReturnValue(BaseModel):
    """Interface method `doSomething` return value struct."""

    label: str
    identifier: int
    day: DayOfTheWeek


class FavoriteFoodsProperty(BaseModel):
    """Interface property `favorite_foods` (multi-value struct)."""

    drink: str
    slices_of_pizza: int
    breakfast: str | None


class LunchMenuProperty(BaseModel):
    """Interface property `lunch_menu` (multi-value struct)."""

    monday: Lunch
    tuesday: Lunch
