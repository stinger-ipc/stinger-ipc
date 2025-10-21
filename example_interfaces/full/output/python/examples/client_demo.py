import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from fullipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from fullipc.client import FullClient, FullClientBuilder, FullClientDiscoverer
from fullipc.interface_types import *

if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)

    client_builder = FullClientBuilder()

    @client_builder.receive_today_is
    def print_todayIs_receipt(dayOfMonth: int, dayOfWeek: Optional[DayOfTheWeek], timestamp: datetime, process_time: timedelta, memory_segment: bytes):
        """
        @param dayOfMonth int
        @param dayOfWeek Optional[DayOfTheWeek]
        @param timestamp datetime
        @param process_time timedelta
        @param memory_segment bytes
        """
        print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } timestamp={ timestamp } process_time={ process_time } memory_segment={ memory_segment } ")

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

    @client_builder.breakfast_length_updated
    def print_new_breakfast_length_value(value: timedelta):
        """ """
        print(f"Property 'breakfast_length' has been updated to: {value}")

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

    print("Making call to 'add_numbers'")
    future_resp = client.add_numbers(first=42, second=42, third=42)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'add_numbers' call")

    print("Making call to 'do_something'")
    future_resp = client.do_something(a_string="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'do_something' call")

    print("Making call to 'echo'")
    future_resp = client.echo(message="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'echo' call")

    print("Making call to 'what_time_is_it'")
    future_resp = client.what_time_is_it(the_first_time=datetime.now(UTC))
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'what_time_is_it' call")

    print("Making call to 'set_the_time'")
    future_resp = client.set_the_time(the_first_time=datetime.now(UTC), the_second_time=datetime.now(UTC))
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'set_the_time' call")

    print("Making call to 'forward_time'")
    future_resp = client.forward_time(adjustment=timedelta(seconds=3536))
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'forward_time' call")

    print("Making call to 'how_off_is_the_clock'")
    future_resp = client.how_off_is_the_clock(actual_time=datetime.now(UTC))
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'how_off_is_the_clock' call")

    print("Ctrl-C will stop the program.")
    signal.pause()
