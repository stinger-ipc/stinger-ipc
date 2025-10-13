"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
"""

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
from enum import IntEnum


class InterfaceInfo(BaseModel):
    interfaceName: str = Field(default="weather")
    title: str = Field(default="NWS weather forecast")
    version: str = Field(default="0.1.2")
    instance: str
    connection_topic: str
    timestamp: str


class WeatherCondition(IntEnum):
    """Interface enum `weather_condition`."""

    RAINY = 1
    SUNNY = 2
    PARTLY_CLOUDY = 3
    MOSTLY_CLOUDY = 4
    OVERCAST = 5
    WINDY = 6
    SNOWY = 7


class ForecastForHour(BaseModel):
    """Interface struct `forecast_for_hour`."""

    temperature: float
    starttime: datetime
    condition: WeatherCondition


class ForecastForDay(BaseModel):
    """Interface struct `forecast_for_day`."""

    high_temperature: float
    low_temperature: float
    condition: WeatherCondition
    start_time: str
    end_time: str


class CurrentTimeSignalPayload(BaseModel):
    """Interface signal `current_time`.

        Once in a while (at intervals decided by the provider) the current date
    and time will be published.  (Mostly for example purposes).

    """

    current_time: str


class LocationProperty(BaseModel):
    """Interface property `location` (multi-value struct).

    Weather will be retrieved for the provided location.

    """

    latitude: float
    longitude: float


class CurrentTemperatureProperty(BaseModel):
    """Interface property `current_temperature` (multi-value struct).

        This is the current (estimated) temperature in degrees fahrenheit.  This values
    is regularly updated.  The value is extrapolated from the hourly forecast, but
    adjusted based on the latest conditions at the nearest weather station.

    """

    temperature_f: float


class CurrentConditionProperty(BaseModel):
    """Interface property `current_condition` (multi-value struct).

        This is the current weather outside.  This comes from the hourly forecast and is
    updated about once per hour.

    """

    condition: WeatherCondition
    description: str


class DailyForecastProperty(BaseModel):
    """Interface property `daily_forecast` (multi-value struct).

        This contains the weather forecast for each day of the next few days.  It is updated
    a couple of times a day.  The current day may not have the high or low temperature
    provided.  This is an example which shows only a few days.  The actual implementation
    will have a value for each day of the week.

    """

    monday: ForecastForDay = Field(description="This is the forecast for Monday.")
    tuesday: ForecastForDay
    wednesday: ForecastForDay


class HourlyForecastProperty(BaseModel):
    """Interface property `hourly_forecast` (multi-value struct).

        This contains the weather forecast for each hour of the next 24 hours.  The data source
    us updated a couple of times per day, but this API property is updated every hour on the
    hour.

    """

    hour_0: ForecastForHour = Field(description="This is the forecast for the current hour.")
    hour_1: ForecastForHour = Field(description="This is the forecast for the next hour.")
    hour_2: ForecastForHour
    hour_3: ForecastForHour


class CurrentConditionRefreshIntervalProperty(BaseModel):
    """Interface property `current_condition_refresh_interval` (multi-value struct).

        This is the maximum interval, in seconds, that the latest weather conditions at the nearest weather
    station are retrieved.

    """

    seconds: int


class HourlyForecastRefreshIntervalProperty(BaseModel):
    """Interface property `hourly_forecast_refresh_interval` (multi-value struct).

    This is the maximum interval, in seconds, that the hourly forecast data is retrieved.

    """

    seconds: int = Field(description="Interval duration in seconds.")


class DailyForecastRefreshIntervalProperty(BaseModel):
    """Interface property `daily_forecast_refresh_interval` (multi-value struct).

    This is the maximum interval, in seconds, that the daily forecast data is retrieved.

    """

    seconds: int


class RefreshDailyForecastMethodRequest(BaseModel):
    """Interface method `refresh_daily_forecast` request object.

        When called, this method will force the retrieval of the daily weather forecast from
    the NWS weather API.

    When called, the `daily_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    pass


class RefreshDailyForecastMethodResponse(BaseModel):
    """Interface method `refresh_daily_forecast` response object.

        When called, this method will force the retrieval of the daily weather forecast from
    the NWS weather API.

    When called, the `daily_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    pass


class RefreshHourlyForecastMethodRequest(BaseModel):
    """Interface method `refresh_hourly_forecast` request object.

        When called, this method will force the retrieval of the hourly weather forecast from
    the NWS weather API.

    When called, the `hourly_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    pass


class RefreshHourlyForecastMethodResponse(BaseModel):
    """Interface method `refresh_hourly_forecast` response object.

        When called, this method will force the retrieval of the hourly weather forecast from
    the NWS weather API.

    When called, the `hourly_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    pass


class RefreshCurrentConditionsMethodRequest(BaseModel):
    """Interface method `refresh_current_conditions` request object.

        When called, this method will force the retrieval of the latest weather conditions
    from the nearest weather station.  It also forces a re-calculation of the current
    temperature.

    When called, the `current_temperature` and `current_condition` API properties are
    republished with the latest value.

    This method has no arguments and provides no return values.

    """

    pass


class RefreshCurrentConditionsMethodResponse(BaseModel):
    """Interface method `refresh_current_conditions` response object.

        When called, this method will force the retrieval of the latest weather conditions
    from the nearest weather station.  It also forces a re-calculation of the current
    temperature.

    When called, the `current_temperature` and `current_condition` API properties are
    republished with the latest value.

    This method has no arguments and provides no return values.

    """

    pass
