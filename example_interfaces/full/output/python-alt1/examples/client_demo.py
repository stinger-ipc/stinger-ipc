import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from fullipc.client import FullClient, FullClientBuilder, FullClientDiscoverer
from fullipc.interface_types import *
import threading


def request_loop(client: FullClient):
    """Example request loop that runs in a separate thread."""
    sleep(30)
    while True:
        print("Making call to 'add_numbers'")
        future_resp = client.add_numbers(first=42, second=42, third=42)
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'add_numbers' call")
        sleep(5)

        print("Making call to 'do_something'")
        future_resp = client.do_something(task_to_do="apples")
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'do_something' call")
        sleep(5)

        print("Making call to 'what_time_is_it'")
        future_resp = client.what_time_is_it()
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'what_time_is_it' call")
        sleep(5)

        print("Making call to 'hold_temperature'")
        future_resp = client.hold_temperature(temperature_celsius=3.14)
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'hold_temperature' call")
        sleep(5)

        client.favorite_number = 42

        client.favorite_foods = FavoriteFoodsProperty(
            drink="apples",
            slices_of_pizza=42,
            breakfast="apples",
        )

        client.family_name = "apples"

        client.last_breakfast_time = datetime.now(UTC)

        client.last_birthdays = LastBirthdaysProperty(
            mom=datetime.now(UTC),
            dad=datetime.now(UTC),
            sister=datetime.now(UTC),
            brothers_age=42,
        )

        sleep(10)


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    client_builder = FullClientBuilder()

    @client_builder.receive_today_is
    def print_todayIs_receipt(dayOfMonth: int, dayOfWeek: DayOfTheWeek):
        """
        @param dayOfMonth int The calendar day of the month.
        @param dayOfWeek DayOfTheWeek
        """
        print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth} dayOfWeek={ dayOfWeek} ")

    @client_builder.receive_random_word
    def print_randomWord_receipt(word: str, time: datetime):
        """
        @param word str
        @param time datetime
        """
        print(f"Got a 'randomWord' signal: word={ word} time={ time} ")

    @client_builder.favorite_number_updated
    def print_new_favorite_number_value(value: int):
        """ """
        print(f"Property 'favorite_number' has been updated to: {value}")

    @client_builder.favorite_foods_updated
    def print_new_favorite_foods_value(value: FavoriteFoodsProperty):
        """ """
        print(f"Property 'favorite_foods' has been updated to: {value}")

    @client_builder.lunch_menu_updated
    def print_new_lunch_menu_value(value: LunchMenuProperty):
        """ """
        print(f"Property 'lunch_menu' has been updated to: {value}")

    @client_builder.family_name_updated
    def print_new_family_name_value(value: str):
        """ """
        print(f"Property 'family_name' has been updated to: {value}")

    @client_builder.last_breakfast_time_updated
    def print_new_last_breakfast_time_value(value: datetime):
        """ """
        print(f"Property 'last_breakfast_time' has been updated to: {value}")

    @client_builder.last_birthdays_updated
    def print_new_last_birthdays_value(value: LastBirthdaysProperty):
        """ """
        print(f"Property 'last_birthdays' has been updated to: {value}")

    discovery = FullClientDiscoverer(conn, client_builder)
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
