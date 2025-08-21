"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
"""
from pydantic import BaseModel
from enum import IntEnum


class DayOfTheWeek(IntEnum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7



class Lunch(BaseModel):
    drink: bool
    sandwich: str
    crackers: float
    day: DayOfTheWeek
    order_number: int | None



class (BaseModel):
    label: str
    identifier: int
    day: DayOfTheWeek



class FavoriteFoodsProperty(BaseModel):
    drink: str
    slices_of_pizza: int
    breakfast: str | None

class LunchMenuProperty(BaseModel):
    monday: Monday
    tuesday: Tuesday
