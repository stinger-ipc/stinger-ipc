"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather-forecast interface.
"""
from pydantic import BaseModel
from enum import IntEnum


class WeatherCondition(IntEnum):
    """ Interface enum `weather_condition`."""
    RAINY = 1
    SUNNY = 2
    PARTLY_CLOUDY = 3
    MOSTLY_CLOUDY = 4
    OVERCAST = 5
    WINDY = 6
    SNOWY = 7

class ForecastForHour(BaseModel):
    """ Interface struct `forecast_for_hour`. """
    temperature: float
    starttime: str
    condition: WeatherCondition

class ForecastForDay(BaseModel):
    """ Interface struct `forecast_for_day`. """
    high_temperature: float
    low_temperature: float
    condition: WeatherCondition
    start_time: str
    end_time: str

class LocationProperty(BaseModel):
    """ Interface property `location` (multi-value struct)."""
    latitude: float
    longitude: float
    

class CurrentConditionProperty(BaseModel):
    """ Interface property `current_condition` (multi-value struct)."""
    condition: WeatherCondition
    description: str
    

class DailyForecastProperty(BaseModel):
    """ Interface property `daily_forecast` (multi-value struct)."""
    monday: ForecastForDay
    tuesday: ForecastForDay
    wednesday: ForecastForDay
    

class HourlyForecastProperty(BaseModel):
    """ Interface property `hourly_forecast` (multi-value struct)."""
    hour_0: ForecastForHour
    hour_1: ForecastForHour
    hour_2: ForecastForHour
    hour_3: ForecastForHour
    
