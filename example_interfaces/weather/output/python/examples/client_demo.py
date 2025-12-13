import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from weatheripc.client import WeatherClient, WeatherClientBuilder, WeatherClientDiscoverer
from weatheripc.interface_types import *
import threading


def request_loop(client: WeatherClient):
    """Example request loop that runs in a separate thread."""
    sleep(30)
    while True:
        print("Making call to 'refresh_daily_forecast'")
        future_resp = client.refresh_daily_forecast()
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'refresh_daily_forecast' call")
        sleep(5)

        print("Making call to 'refresh_hourly_forecast'")
        future_resp = client.refresh_hourly_forecast()
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'refresh_hourly_forecast' call")
        sleep(5)

        print("Making call to 'refresh_current_conditions'")
        future_resp = client.refresh_current_conditions()
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'refresh_current_conditions' call")
        sleep(5)

        client.location = LocationProperty(
            latitude=3.14,
            longitude=3.14,
        )

        client.current_condition_refresh_interval = 42

        client.hourly_forecast_refresh_interval = 42

        client.daily_forecast_refresh_interval = 42

        sleep(10)


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    client_builder = WeatherClientBuilder()

    @client_builder.receive_current_time
    def print_current_time_receipt(current_time: str):
        """
        @param current_time str
        """
        print(f"Got a 'current_time' signal: current_time={ current_time } ")

    @client_builder.location_updated
    def print_new_location_value(value: LocationProperty):
        """ """
        print(f"Property 'location' has been updated to: {value}")

    @client_builder.current_temperature_updated
    def print_new_current_temperature_value(value: float):
        """ """
        print(f"Property 'current_temperature' has been updated to: {value}")

    @client_builder.current_condition_updated
    def print_new_current_condition_value(value: CurrentConditionProperty):
        """ """
        print(f"Property 'current_condition' has been updated to: {value}")

    @client_builder.daily_forecast_updated
    def print_new_daily_forecast_value(value: DailyForecastProperty):
        """ """
        print(f"Property 'daily_forecast' has been updated to: {value}")

    @client_builder.hourly_forecast_updated
    def print_new_hourly_forecast_value(value: HourlyForecastProperty):
        """ """
        print(f"Property 'hourly_forecast' has been updated to: {value}")

    @client_builder.current_condition_refresh_interval_updated
    def print_new_current_condition_refresh_interval_value(value: int):
        """ """
        print(f"Property 'current_condition_refresh_interval' has been updated to: {value}")

    @client_builder.hourly_forecast_refresh_interval_updated
    def print_new_hourly_forecast_refresh_interval_value(value: int):
        """ """
        print(f"Property 'hourly_forecast_refresh_interval' has been updated to: {value}")

    @client_builder.daily_forecast_refresh_interval_updated
    def print_new_daily_forecast_refresh_interval_value(value: int):
        """ """
        print(f"Property 'daily_forecast_refresh_interval' has been updated to: {value}")

    discovery = WeatherClientDiscoverer(conn, client_builder)
    fut_client = discovery.get_singleton_client()
    try:
        client = fut_client.result(10)
    except futures.TimeoutError:
        print("Timed out waiting for a service to appear")
        exit(1)

    sleep(2)

    threading.Thread(target=request_loop, args=(client,), daemon=True).start()

    print("Ctrl-C will stop the program.")
    signal.pause()
