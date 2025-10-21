from time import sleep
import signal
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from weatheripc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from weatheripc.server import WeatherServer
from weatheripc.interface_types import *

if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = WeatherServer(conn, "py-server-demo:1")

    server.location = LocationProperty(
        latitude=3.14,
        longitude=3.14,
    )

    server.current_temperature = 3.14

    server.current_condition = CurrentConditionProperty(
        condition=WeatherCondition.SNOWY,
        description="apples",
    )

    server.daily_forecast = DailyForecastProperty(
        monday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
        tuesday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
        wednesday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
    )

    server.hourly_forecast = HourlyForecastProperty(
        hour_0=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
        hour_1=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
        hour_2=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
        hour_3=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
    )

    server.current_condition_refresh_interval = 42

    server.hourly_forecast_refresh_interval = 42

    server.daily_forecast_refresh_interval = 42

    @server.handle_refresh_daily_forecast
    def refresh_daily_forecast() -> None:
        """This is an example handler for the 'refresh_daily_forecast' method."""
        print(f"Running refresh_daily_forecast'()'")
        return None

    @server.handle_refresh_hourly_forecast
    def refresh_hourly_forecast() -> None:
        """This is an example handler for the 'refresh_hourly_forecast' method."""
        print(f"Running refresh_hourly_forecast'()'")
        return None

    @server.handle_refresh_current_conditions
    def refresh_current_conditions() -> None:
        """This is an example handler for the 'refresh_current_conditions' method."""
        print(f"Running refresh_current_conditions'()'")
        return None

    @server.on_location_updates
    def on_location_update(latitude: float, longitude: float):
        print(f"Received update for 'location' property: { latitude= }, { longitude= }")

    @server.on_current_temperature_updates
    def on_current_temperature_update(temperature_f: float):
        print(f"Received update for 'current_temperature' property: { temperature_f= }")

    @server.on_current_condition_updates
    def on_current_condition_update(condition: WeatherCondition, description: str):
        print(f"Received update for 'current_condition' property: { condition= }, { description= }")

    @server.on_daily_forecast_updates
    def on_daily_forecast_update(monday: ForecastForDay, tuesday: ForecastForDay, wednesday: ForecastForDay):
        print(f"Received update for 'daily_forecast' property: { monday= }, { tuesday= }, { wednesday= }")

    @server.on_hourly_forecast_updates
    def on_hourly_forecast_update(hour_0: ForecastForHour, hour_1: ForecastForHour, hour_2: ForecastForHour, hour_3: ForecastForHour):
        print(f"Received update for 'hourly_forecast' property: { hour_0= }, { hour_1= }, { hour_2= }, { hour_3= }")

    @server.on_current_condition_refresh_interval_updates
    def on_current_condition_refresh_interval_update(seconds: int):
        print(f"Received update for 'current_condition_refresh_interval' property: { seconds= }")

    @server.on_hourly_forecast_refresh_interval_updates
    def on_hourly_forecast_refresh_interval_update(seconds: int):
        print(f"Received update for 'hourly_forecast_refresh_interval' property: { seconds= }")

    @server.on_daily_forecast_refresh_interval_updates
    def on_daily_forecast_refresh_interval_update(seconds: int):
        print(f"Received update for 'daily_forecast_refresh_interval' property: { seconds= }")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_current_time("apples")

            sleep(4)
            server.emit_current_time(current_time="apples")

            sleep(16)
        except KeyboardInterrupt:
            break

    signal.pause()
