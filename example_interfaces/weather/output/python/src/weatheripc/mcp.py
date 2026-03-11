from stinger_python_utils.mcp import (
    MethodDefinition,
    PropertyDefinition,
    SignalDefinition,
    StingerMCPPlugin,
)

from weatheripc.client import WeatherClient, WeatherClientDiscoverer
from weatheripc.interface_types import *

class WeatherMCPPlugin(StingerMCPPlugin):
    """MCP plugin for the weather interface."""

    def get_plugin_name(self) -> str:
        return "weather"
    
    def get_discovery_class(self) -> type:
        return WeatherClientDiscoverer

    def get_client_class(self) -> type:
        return WeatherClient
    
    def get_signals(self) -> list[SignalDefinition]:
        return [
            
            SignalDefinition(
                name="current_time",
                description="Once in a while (at intervals decided by the provider) the current date and time will be published.  (Mostly for example purposes). ",
            ),
            
        ]

    def get_methods(self) -> list[MethodDefinition]:
        return [
            
            MethodDefinition(
                name="refresh_daily_forecast",
                description="When called, this method will force the retrieval of the daily weather forecast from the NWS weather API.    When called, the `daily_forecast` API property will be republished with the latest data.  This method has no arguments and provides no return values. ",
                arguments_model=RefreshDailyForecastMethodRequest,
            ),
            
            MethodDefinition(
                name="refresh_hourly_forecast",
                description="When called, this method will force the retrieval of the hourly weather forecast from the NWS weather API.    When called, the `hourly_forecast` API property will be republished with the latest data.  This method has no arguments and provides no return values. ",
                arguments_model=RefreshHourlyForecastMethodRequest,
            ),
            
            MethodDefinition(
                name="refresh_current_conditions",
                description="When called, this method will force the retrieval of the latest weather conditions from the nearest weather station.  It also forces a re-calculation of the current temperature.  When called, the `current_temperature` and `current_condition` API properties are republished with the latest value.  This method has no arguments and provides no return values. ",
                arguments_model=RefreshCurrentConditionsMethodRequest,
            ),
            
        ]

    def get_properties(self) -> list[PropertyDefinition]:
        return [
            
            PropertyDefinition(
                name="location",
                description="Weather will be retrieved for the provided location. ",
                readonly=False,
                schema=LocationProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="current_temperature",
                description="This is the current (estimated) temperature in degrees fahrenheit.  This values is regularly updated.  The value is extrapolated from the hourly forecast, but adjusted based on the latest conditions at the nearest weather station. ",
                readonly=True,
                schema=CurrentTemperatureProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="current_condition",
                description="This is the current weather outside.  This comes from the hourly forecast and is updated about once per hour. ",
                readonly=True,
                schema=CurrentConditionProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="daily_forecast",
                description="This contains the weather forecast for each day of the next few days.  It is updated a couple of times a day.  The current day may not have the high or low temperature provided.  This is an example which shows only a few days.  The actual implementation will have a value for each day of the week. ",
                readonly=True,
                schema=DailyForecastProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="hourly_forecast",
                description="This contains the weather forecast for each hour of the next 24 hours.  The data source us updated a couple of times per day, but this API property is updated every hour on the hour. ",
                readonly=True,
                schema=HourlyForecastProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="current_condition_refresh_interval",
                description="This is the maximum interval, in seconds, that the latest weather conditions at the nearest weather station are retrieved. ",
                readonly=False,
                schema=CurrentConditionRefreshIntervalProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="hourly_forecast_refresh_interval",
                description="This is the maximum interval, in seconds, that the hourly forecast data is retrieved. ",
                readonly=False,
                schema=HourlyForecastRefreshIntervalProperty.model_json_schema(),
            ),
            
            PropertyDefinition(
                name="daily_forecast_refresh_interval",
                description="This is the maximum interval, in seconds, that the daily forecast data is retrieved. ",
                readonly=False,
                schema=DailyForecastRefreshIntervalProperty.model_json_schema(),
            ),
            
        ]