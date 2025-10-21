"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
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
    interface_name: str = Field(default="weather")
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

    model_config = ConfigDict(populate_by_name=True)
    temperature: Annotated[
        float,
        Field(
            description="Forecasted temperature in degrees fahrenheit.",
        ),
    ]
    starttime: Annotated[
        datetime,
        Field(
            description="Forecast is valid for the hour starting at this time.",
        ),
    ]
    condition: Annotated[WeatherCondition, Field()]


class ForecastForDay(BaseModel):
    """Interface struct `forecast_for_day`."""

    model_config = ConfigDict(populate_by_name=True)
    high_temperature: Annotated[
        float,
        Field(
            description="High temperature for the day in degrees fahrenheit.",
        ),
    ]
    low_temperature: Annotated[
        float,
        Field(
            description="Low temperature for the day in degrees fahrenheit.",
        ),
    ]
    condition: Annotated[WeatherCondition, Field()]
    start_time: Annotated[str, Field()]
    end_time: Annotated[str, Field()]


class CurrentTimeSignalPayload(BaseModel):
    """Interface signal `current_time`.

        Once in a while (at intervals decided by the provider) the current date
    and time will be published.  (Mostly for example purposes).

    """

    model_config = ConfigDict(populate_by_name=True)
    current_time: Annotated[str, Field()]


class LocationProperty(BaseModel):
    """Interface property `location` (multi-value struct).

    Weather will be retrieved for the provided location.

    """

    model_config = ConfigDict(populate_by_name=True)
    latitude: Annotated[float, Field()]
    longitude: Annotated[float, Field()]


class CurrentTemperatureProperty(BaseModel):
    """Interface property `current_temperature` (multi-value struct).

        This is the current (estimated) temperature in degrees fahrenheit.  This values
    is regularly updated.  The value is extrapolated from the hourly forecast, but
    adjusted based on the latest conditions at the nearest weather station.

    """

    model_config = ConfigDict(populate_by_name=True)
    temperature_f: Annotated[float, Field()]


class CurrentConditionProperty(BaseModel):
    """Interface property `current_condition` (multi-value struct).

        This is the current weather outside.  This comes from the hourly forecast and is
    updated about once per hour.

    """

    model_config = ConfigDict(populate_by_name=True)
    condition: Annotated[WeatherCondition, Field()]
    description: Annotated[str, Field()]


class DailyForecastProperty(BaseModel):
    """Interface property `daily_forecast` (multi-value struct).

        This contains the weather forecast for each day of the next few days.  It is updated
    a couple of times a day.  The current day may not have the high or low temperature
    provided.  This is an example which shows only a few days.  The actual implementation
    will have a value for each day of the week.

    """

    model_config = ConfigDict(populate_by_name=True)
    monday: Annotated[
        ForecastForDay,
        Field(
            description="This is the forecast for Monday.",
        ),
    ]
    tuesday: Annotated[ForecastForDay, Field()]
    wednesday: Annotated[ForecastForDay, Field()]


class HourlyForecastProperty(BaseModel):
    """Interface property `hourly_forecast` (multi-value struct).

        This contains the weather forecast for each hour of the next 24 hours.  The data source
    us updated a couple of times per day, but this API property is updated every hour on the
    hour.

    """

    model_config = ConfigDict(populate_by_name=True)
    hour_0: Annotated[
        ForecastForHour,
        Field(
            description="This is the forecast for the current hour.",
        ),
    ]
    hour_1: Annotated[
        ForecastForHour,
        Field(
            description="This is the forecast for the next hour.",
        ),
    ]
    hour_2: Annotated[ForecastForHour, Field()]
    hour_3: Annotated[ForecastForHour, Field()]


class CurrentConditionRefreshIntervalProperty(BaseModel):
    """Interface property `current_condition_refresh_interval` (multi-value struct).

        This is the maximum interval, in seconds, that the latest weather conditions at the nearest weather
    station are retrieved.

    """

    model_config = ConfigDict(populate_by_name=True)
    seconds: Annotated[int, Field()]


class HourlyForecastRefreshIntervalProperty(BaseModel):
    """Interface property `hourly_forecast_refresh_interval` (multi-value struct).

    This is the maximum interval, in seconds, that the hourly forecast data is retrieved.

    """

    model_config = ConfigDict(populate_by_name=True)
    seconds: Annotated[
        int,
        Field(
            description="Interval duration in seconds.",
        ),
    ]


class DailyForecastRefreshIntervalProperty(BaseModel):
    """Interface property `daily_forecast_refresh_interval` (multi-value struct).

    This is the maximum interval, in seconds, that the daily forecast data is retrieved.

    """

    model_config = ConfigDict(populate_by_name=True)
    seconds: Annotated[int, Field()]


class RefreshDailyForecastMethodRequest(BaseModel):
    """Interface method `refresh_daily_forecast` request object.

        When called, this method will force the retrieval of the daily weather forecast from
    the NWS weather API.

    When called, the `daily_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    model_config = ConfigDict(populate_by_name=True)


class RefreshDailyForecastMethodResponse(BaseModel):
    """Interface method `refresh_daily_forecast` response object.

        When called, this method will force the retrieval of the daily weather forecast from
    the NWS weather API.

    When called, the `daily_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    model_config = ConfigDict(populate_by_name=True)


class RefreshHourlyForecastMethodRequest(BaseModel):
    """Interface method `refresh_hourly_forecast` request object.

        When called, this method will force the retrieval of the hourly weather forecast from
    the NWS weather API.

    When called, the `hourly_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    model_config = ConfigDict(populate_by_name=True)


class RefreshHourlyForecastMethodResponse(BaseModel):
    """Interface method `refresh_hourly_forecast` response object.

        When called, this method will force the retrieval of the hourly weather forecast from
    the NWS weather API.

    When called, the `hourly_forecast` API property will be republished with the latest data.

    This method has no arguments and provides no return values.

    """

    model_config = ConfigDict(populate_by_name=True)


class RefreshCurrentConditionsMethodRequest(BaseModel):
    """Interface method `refresh_current_conditions` request object.

        When called, this method will force the retrieval of the latest weather conditions
    from the nearest weather station.  It also forces a re-calculation of the current
    temperature.

    When called, the `current_temperature` and `current_condition` API properties are
    republished with the latest value.

    This method has no arguments and provides no return values.

    """

    model_config = ConfigDict(populate_by_name=True)


class RefreshCurrentConditionsMethodResponse(BaseModel):
    """Interface method `refresh_current_conditions` response object.

        When called, this method will force the retrieval of the latest weather conditions
    from the nearest weather station.  It also forces a re-calculation of the current
    temperature.

    When called, the `current_temperature` and `current_condition` API properties are
    republished with the latest value.

    This method has no arguments and provides no return values.

    """

    model_config = ConfigDict(populate_by_name=True)
