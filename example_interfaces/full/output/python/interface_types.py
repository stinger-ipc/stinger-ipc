"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
"""
from dataclasses import dataclass
from enum import Enum


class DayOfTheWeek(Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7






@dataclass
class DoSomethingReturnValue:
    label: str
    
    identifier: int
    
    day: DayOfTheWeek
    
