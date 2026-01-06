from typing import Callable, Optional

from pydantic import BaseModel
from .interface_types import *


class WeatherInitialPropertyValues(BaseModel):

    location: LocationProperty
    location_version: int = 0

    current_temperature: float
    current_temperature_version: int = 0

    current_condition: CurrentConditionProperty
    current_condition_version: int = 0

    daily_forecast: DailyForecastProperty
    daily_forecast_version: int = 0

    hourly_forecast: HourlyForecastProperty
    hourly_forecast_version: int = 0

    current_condition_refresh_interval: int
    current_condition_refresh_interval_version: int = 0

    hourly_forecast_refresh_interval: int
    hourly_forecast_refresh_interval_version: int = 0

    daily_forecast_refresh_interval: int
    daily_forecast_refresh_interval_version: int = 0


class WeatherPropertyAccess(BaseModel):

    location_getter: Callable[[], LocationProperty]

    location_setter: Callable[[LocationProperty], None]

    current_temperature_getter: Callable[[], float]

    current_condition_getter: Callable[[], CurrentConditionProperty]

    daily_forecast_getter: Callable[[], DailyForecastProperty]

    hourly_forecast_getter: Callable[[], HourlyForecastProperty]

    current_condition_refresh_interval_getter: Callable[[], int]

    current_condition_refresh_interval_setter: Callable[[int], None]

    hourly_forecast_refresh_interval_getter: Callable[[], int]

    hourly_forecast_refresh_interval_setter: Callable[[int], None]

    daily_forecast_refresh_interval_getter: Callable[[], int]

    daily_forecast_refresh_interval_setter: Callable[[int], None]
