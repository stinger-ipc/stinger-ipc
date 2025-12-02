"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""



from pydantic import BaseModel, Field, PlainValidator, PlainSerializer, ConfigDict
from datetime import datetime, timedelta, UTC
from typing import Optional, Annotated, Union, List
import base64
from enum import IntEnum

def base64_decode_if_str(value: Union[str, bytes, None]) -> Optional[bytes]:
    """ If the value is a string, decode it from base64 to bytes.  Otherwise return the bytes as-is."""
    if isinstance(value, str):
        return base64.b64decode(value)
    return value

class InterfaceInfo(BaseModel):
    interface_name: str = Field(default="Full")
    title: str = Field(default="Fully Featured Example Interface")
    version: str = Field(default="0.0.1")
    instance: str
    connection_topic: str
    timestamp: str


class DayOfTheWeek(IntEnum):
    """ Interface enum `dayOfTheWeek`."""
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7

class Lunch(BaseModel):
    """ Interface struct `lunch`. """
    
    model_config = ConfigDict(populate_by_name=True)
    drink: Annotated[bool, Field()]
    sandwich: Annotated[str, Field()]
    crackers: Annotated[float, Field()]
    day: Annotated[DayOfTheWeek, Field()]
    order_number: Annotated[Optional[int], Field()]
    time_of_lunch: Annotated[datetime, Field()]
    duration_of_lunch: Annotated[timedelta, Field()]



class TodayIsSignalPayload(BaseModel):
    """ Interface signal `todayIs`. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    day_of_month: Annotated[int, Field(alias="dayOfMonth")]
    day_of_week: Annotated[Optional[DayOfTheWeek], Field(alias="dayOfWeek")]
    timestamp: Annotated[datetime, Field()]
    process_time: Annotated[timedelta, Field()]
    memory_segment: Annotated[bytes, Field(), PlainValidator(base64_decode_if_str), PlainSerializer(lambda v: base64.b64encode(v).decode('utf-8'))]



class FavoriteNumberProperty(BaseModel):
    """ Interface property `favorite_number` (multi-value struct).
    
    My favorite number

    """
    
    model_config = ConfigDict(populate_by_name=True)
    number: Annotated[int, Field()]



class FavoriteFoodsProperty(BaseModel):
    """ Interface property `favorite_foods` (multi-value struct).
    """
    
    model_config = ConfigDict(populate_by_name=True)
    drink: Annotated[str, Field()]
    slices_of_pizza: Annotated[int, Field()]
    breakfast: Annotated[Optional[str], Field()]



class LunchMenuProperty(BaseModel):
    """ Interface property `lunch_menu` (multi-value struct).
    """
    
    model_config = ConfigDict(populate_by_name=True)
    monday: Annotated[Lunch, Field()]
    tuesday: Annotated[Lunch, Field(description="Tuesday's lunch menu.", )]



class FamilyNameProperty(BaseModel):
    """ Interface property `family_name` (multi-value struct).
    
    This is to test a property with a single string value.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    family_name: Annotated[str, Field()]



class LastBreakfastTimeProperty(BaseModel):
    """ Interface property `last_breakfast_time` (multi-value struct).
    
    This is to test a property with a single datetime value.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    timestamp: Annotated[datetime, Field()]



class BreakfastLengthProperty(BaseModel):
    """ Interface property `breakfast_length` (multi-value struct).
    
    This is to test a property with a single duration value.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    length: Annotated[timedelta, Field()]



class LastBirthdaysProperty(BaseModel):
    """ Interface property `last_birthdays` (multi-value struct).
    
    This is to test a property with multiple datetime values.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    mom: Annotated[datetime, Field()]
    dad: Annotated[datetime, Field()]
    sister: Annotated[Optional[datetime], Field()]
    brothers_age: Annotated[Optional[int], Field()]



class AddNumbersMethodRequest(BaseModel):
    """ Interface method `addNumbers` request object. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    first: Annotated[int, Field()]
    second: Annotated[int, Field()]
    third: Annotated[Optional[int], Field()]




class AddNumbersMethodResponse(BaseModel):
    """ Interface method `addNumbers` response object. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    sum: Annotated[int, Field()]



class DoSomethingMethodRequest(BaseModel):
    """ Interface method `doSomething` request object. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    a_string: Annotated[str, Field(alias="aString")]




class DoSomethingMethodResponse(BaseModel):
    """ Interface method `doSomething` response object. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    label: Annotated[str, Field()]
    identifier: Annotated[int, Field()]
    day: Annotated[DayOfTheWeek, Field()]



class EchoMethodRequest(BaseModel):
    """ Interface method `echo` request object. 

    Echo back the received message.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    message: Annotated[str, Field()]




class EchoMethodResponse(BaseModel):
    """ Interface method `echo` response object. 

    Echo back the received message.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    message: Annotated[str, Field()]



class WhatTimeIsItMethodRequest(BaseModel):
    """ Interface method `what_time_is_it` request object. 

    Get the current date and time.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    the_first_time: Annotated[datetime, Field()]




class WhatTimeIsItMethodResponse(BaseModel):
    """ Interface method `what_time_is_it` response object. 

    Get the current date and time.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    timestamp: Annotated[datetime, Field()]



class SetTheTimeMethodRequest(BaseModel):
    """ Interface method `set_the_time` request object. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    the_first_time: Annotated[datetime, Field()]
    the_second_time: Annotated[datetime, Field()]




class SetTheTimeMethodResponse(BaseModel):
    """ Interface method `set_the_time` response object. 
    """
    
    model_config = ConfigDict(populate_by_name=True)
    timestamp: Annotated[datetime, Field()]
    confirmation_message: Annotated[str, Field()]



class ForwardTimeMethodRequest(BaseModel):
    """ Interface method `forward_time` request object. 

    This method takes a time and a duration, and returns the time plus the duration.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    adjustment: Annotated[timedelta, Field()]




class ForwardTimeMethodResponse(BaseModel):
    """ Interface method `forward_time` response object. 

    This method takes a time and a duration, and returns the time plus the duration.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    new_time: Annotated[datetime, Field()]



class HowOffIsTheClockMethodRequest(BaseModel):
    """ Interface method `how_off_is_the_clock` request object. 

    Returns how far off the clock is from the actual time.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    actual_time: Annotated[datetime, Field()]




class HowOffIsTheClockMethodResponse(BaseModel):
    """ Interface method `how_off_is_the_clock` response object. 

    Returns how far off the clock is from the actual time.
    """
    
    model_config = ConfigDict(populate_by_name=True)
    difference: Annotated[timedelta, Field()]


