import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from weatheripc.client import WeatherClient, WeatherClientBuilder, WeatherClientDiscoverer
from weatheripc.interface_types import *
import threading

client_builder = WeatherClientBuilder()


class SuperAwesomeDoerOfThings:

    def __init__(self, label: str, connection: MqttBrokerConnection):
        self.counter = 0
        self.label = label
        discovery = WeatherClientDiscoverer(connection, client_builder, build_binding=self)  # The build binding will bind all @client_builder decorated methods to this instance.
        self.client = discovery.get_singleton_client().result()
        threading.Thread(target=self.request_loop, daemon=True).start()

    @client_builder.receive_current_time
    def print_current_time_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'current_time' : args={args}, kwargs={kwargs}")

    @client_builder.location_updated
    def print_new_location_value(self, value: LocationProperty):
        print(f"{self.label}-{self.counter} printing signal 'location' : value={value}")

    @client_builder.current_temperature_updated
    def print_new_current_temperature_value(self, value: float):
        print(f"{self.label}-{self.counter} printing signal 'current_temperature' : value={value}")

    @client_builder.current_condition_updated
    def print_new_current_condition_value(self, value: CurrentConditionProperty):
        print(f"{self.label}-{self.counter} printing signal 'current_condition' : value={value}")

    @client_builder.daily_forecast_updated
    def print_new_daily_forecast_value(self, value: DailyForecastProperty):
        print(f"{self.label}-{self.counter} printing signal 'daily_forecast' : value={value}")

    @client_builder.hourly_forecast_updated
    def print_new_hourly_forecast_value(self, value: HourlyForecastProperty):
        print(f"{self.label}-{self.counter} printing signal 'hourly_forecast' : value={value}")

    @client_builder.current_condition_refresh_interval_updated
    def print_new_current_condition_refresh_interval_value(self, value: int):
        print(f"{self.label}-{self.counter} printing signal 'current_condition_refresh_interval' : value={value}")

    @client_builder.hourly_forecast_refresh_interval_updated
    def print_new_hourly_forecast_refresh_interval_value(self, value: int):
        print(f"{self.label}-{self.counter} printing signal 'hourly_forecast_refresh_interval' : value={value}")

    @client_builder.daily_forecast_refresh_interval_updated
    def print_new_daily_forecast_refresh_interval_value(self, value: int):
        print(f"{self.label}-{self.counter} printing signal 'daily_forecast_refresh_interval' : value={value}")

    def request_loop(self):
        """Example request loop that runs in a separate thread."""
        sleep(30)
        while True:
            print("Making call to 'refresh_daily_forecast'")
            future_resp = self.client.refresh_daily_forecast()
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'refresh_daily_forecast' call")
            sleep(5)

            print("Making call to 'refresh_hourly_forecast'")
            future_resp = self.client.refresh_hourly_forecast()
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'refresh_hourly_forecast' call")
            sleep(5)

            print("Making call to 'refresh_current_conditions'")
            future_resp = self.client.refresh_current_conditions()
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'refresh_current_conditions' call")
            sleep(5)

            self.client.location = LocationProperty(
                latitude=3.14,
                longitude=3.14,
            )

            self.client.current_condition_refresh_interval = 42

            self.client.hourly_forecast_refresh_interval = 42

            self.client.daily_forecast_refresh_interval = 42

            sleep(10)


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    doer1 = SuperAwesomeDoerOfThings("Doer1", conn)

    print("Ctrl-C will stop the program.")
    signal.pause()
